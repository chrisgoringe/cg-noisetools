from abc import ABC, abstractmethod
import torch

class Noise(ABC):
    @abstractmethod
    def generate_noise(self, input_latent:torch.Tensor) -> torch.Tensor: pass

    @property
    def seed(self): return None

class NormalisableNoise(Noise):
    def __init__(self, renormalise:bool):
        self.renormalise = renormalise

    def generate_noise(self, input_latent:torch.Tensor) -> torch.Tensor:
        def normalise(noise:torch.Tensor, eps=1e-8):
            std, mean = torch.std_mean(noise)
            return (noise-mean)/(std+eps)
        noise = self._generate_noise(input_latent)
        return normalise(noise) if self.renormalise else noise
    
    @abstractmethod
    def _generate_noise(self, input_latent:torch.Tensor) -> torch.Tensor: pass