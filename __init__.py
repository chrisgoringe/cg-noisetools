from .noise_nodes import MixNoise, ShapeNoise
from .noise_batch_nodes import SeperableBatchNoise, BatchNoiseSimulate

VERSION = "1.1"

NODE_CLASS_MAPPINGS = {
    "Mix Noise"             : MixNoise,
    "Shape Noise"           : ShapeNoise,
    "Seperable Batch Noise" : SeperableBatchNoise,
    "Batch Noise Simulate"  : BatchNoiseSimulate,
}
__all__ = ['NODE_CLASS_MAPPINGS',]