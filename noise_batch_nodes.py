from .noise import Noise
import torch
from comfy_extras.nodes_custom_sampler import Noise_RandomNoise

class Noise_SeperableBatchNoise:
    def __init__(self, seed:int, seed_delta:int):
        self.seed       = seed
        self.seed_delta = seed_delta

    def generate_noise(self, input_latent:torch.Tensor) -> torch.Tensor:
        return torch.cat( [ Noise_RandomNoise(self.seed+i*self.seed_delta).generate_noise({'samples':latent.unsqueeze_(0)}) \
                                                                           for i,latent in enumerate(input_latent['samples']) ] )
    
class SeperableBatchNoise:
    @classmethod    
    def INPUT_TYPES(s):
        return { 
            "required":  { 
                "seed":       ("INT", {"default":0, "min": 0,    "max": 0xffffffffffffffff}), 
                "seed_delta": ("INT", {"default":1, "min": -1e9, "max": 1e9}),
            }
        }

    RETURN_TYPES = ("NOISE",)
    FUNCTION = "func"
    CATEGORY = "noise"

    def func(self, seed, seed_delta):
        return (Noise_SeperableBatchNoise(seed, seed_delta), )

class Noise_BatchNoiseSimulate:
    def __init__(self, noise:Noise, batch_entry:int):
        self.noise = noise
        self.batch_entry = batch_entry

    @property
    def seed(self): return self.noise.seed

    def generate_noise(self, input_latent:torch.Tensor) -> torch.Tensor:
        assert input_latent['samples'].shape[0] == 1, "Batch Noise Simulate works with a batch size of 1, and simulates the nth entry from a larger batch"
        return self.noise.generate_noise( {'samples':input_latent['samples'].expand( (self.batch_entry,-1,-1,-1) )} )[-1].unsqueeze_(0)

class BatchNoiseSimulate:
    @classmethod    
    def INPUT_TYPES(s):
        return { 
            "required":  { 
                "noise":       ("NOISE", {}), 
                "batch_entry": ("INT", {"default":1, "min": 1, "max": 64}),
            }
        }

    RETURN_TYPES = ("NOISE",)
    FUNCTION = "func"
    CATEGORY = "noise"

    def func(self, noise, batch_entry):
        return (Noise_BatchNoiseSimulate(noise, batch_entry), )