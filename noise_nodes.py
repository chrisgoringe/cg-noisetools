import torch
from typing import Optional
from math import sin, pi
from .noise import Noise, NormalisableNoise

class Noise_MixedNoise(NormalisableNoise):
    def __init__(self, noise1:Noise, noise2:Optional[Noise], weight2:float, renormalise:bool, mask:Optional[torch.Tensor]):
        super().__init__(renormalise)
        self.noise1      = noise1
        self.noise2      = noise2
        self.weight2     = weight2
        self.mask        = mask
        
    @property
    def seed(self): return self.noise1.seed

    def _generate_noise(self, input_latent:torch.Tensor) -> torch.Tensor:
        noise1 = self.noise1.generate_noise(input_latent)
        noise2 = self.noise2.generate_noise(input_latent) if self.noise2 is not None else torch.zeros_like(noise1)
        mixed_noise = noise1 * (1.0-self.weight2) + noise2 * (self.weight2)
        
        if self.mask is not None:
            while len(self.mask.shape)<4: self.mask.unsqueeze_(0)
            mask:torch.Tensor = torch.nn.functional.interpolate(self.mask, size=input_latent['samples'].shape[-2:], mode='bilinear')
            mask = mask.expand(-1,noise1.shape[1],-1,-1)
            mixed_noise = mixed_noise * (mask) + noise1 * (1.0-mask)

        return mixed_noise
    
class MixNoise:
    CATEGORY = "noise"
    @classmethod    
    def INPUT_TYPES(s):
        return { 
            "required":  { 
                "noise1":      ("NOISE",), 
                "weight2":     ("FLOAT", {"default":0.01, "step":0.001, "min":-1.0, "max":1.0}),
                "renormalise": (["yes","no"],),
                }, 
            "optional" : {
                "noise2": ("NOISE",), 
                "mask":   ("MASK",),
            }
        }

    RETURN_TYPES = ("NOISE",)
    FUNCTION = "func"

    def func(self, noise1, weight2, renormalise, noise2=None, mask=None):
        return (Noise_MixedNoise(noise1, noise2, weight2, renormalise=='yes', mask),)
    
class Noise_ShapedNoise(NormalisableNoise):
    def __init__(self, noise:NormalisableNoise, weight:float, renormalise:bool, x:bool, y:bool, function:str):
        super().__init__(renormalise)
        self.noise  = noise
        self.weight = weight
        self.x      = x
        self.y      = y
        
        self.function = function

    def shape(self, l:int) -> list[float]:
        if self.function=='sin':   return [ 2*sin(pi*x/l)-1  for x in range(l) ]
        if self.function=='point': return [ 1-abs((4*x/l)-2) for x in range(l) ]
        raise NotImplementedError()

    @property
    def seed(self): return self.noise.seed

    def _generate_noise(self, input_latent:torch.Tensor) -> torch.Tensor:
        noise = self.noise.generate_noise(input_latent)
        b,c,h,w = noise.shape
        xscale = torch.ones((w,1)) + (self.weight * torch.Tensor([self.shape(w),]) if self.x else 0)
        yscale = torch.ones((h,1)) + (self.weight * torch.Tensor([self.shape(h),]) if self.y else 0)
        noise = noise * (torch.matmul(yscale.T,xscale))
        return noise

class ShapeNoise:
    CATEGORY = "noise"
    @classmethod    
    def INPUT_TYPES(s):
        return { 
            "required":  { 
                "noise":       ("NOISE",), 
                "weight":      ("FLOAT", {"default":0.01, "step":0.001, "min":-1.0, "max":1.0}),
                "renormalise": (["yes","no"],),
                "mode":        (["xy","x","y"],),
                "function":    (["sin","point",],)
            }, 
        }
    RETURN_TYPES = ("NOISE",)
    FUNCTION = "func"   

    def func(self, noise:NormalisableNoise, weight:float, renormalise:str, mode:str, function:str):
        return (Noise_ShapedNoise(noise, weight, renormalise=="yes", 'x' in mode, 'y' in mode, function),)


