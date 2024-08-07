from noise_nodes import MixNoise, ShapeNoise

VERSION = "1.0"

NODE_CLASS_MAPPINGS = {
    "Mix Noise"   : MixNoise,
    "Shape Noise" : ShapeNoise,
}
__all__ = ['NODE_CLASS_MAPPINGS',]


