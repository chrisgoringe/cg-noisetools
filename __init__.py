from .noise_nodes import MixNoise, ShapeNoise
from .noise_batch_nodes import SeperableBatchNoise, BatchNoiseSimulate
from .renoise_calculation import SplitSigmasWithRewind

VERSION = "1.1"

NODE_CLASS_MAPPINGS = {
    "Mix Noise"             : MixNoise,
    "Shape Noise"           : ShapeNoise,
    "Seperable Batch Noise" : SeperableBatchNoise,
    "Batch Noise Simulate"  : BatchNoiseSimulate,
    "Split Sigmas with Rewind" : SplitSigmasWithRewind,
}
__all__ = ['NODE_CLASS_MAPPINGS',]