# Noise Tools

Two nodes for playing with noise.

`Mix Noise` is designed for generating small variations in order to create sets of similar images.

`Shape Noise` is designed to push noise towards (or away from) the center of the image.

## Mix Noise

This node takes two noise inputs and produces a weighted mix, optionally with a weight mask.

Note that this is not the sort of noise masking you want for inpainting - the sampler will try to remove noise globally. 

### Inputs 

- *Required* - `noise1` - the original noise source.
- *Optional* - `noise2` - the secondary noise source. If not connected, it is zero noise.
- *Required* - `weight2` - the weight given to the second noise source. The first noise source has weight `1-weight2`.
- *Optional* - `mask` - multiply `weight2` by the mask values. The mask will be rescaled to fit the latent.
- *Required* - `renormalise` - should the noise be renormalised to mean of zero and stdev of one after mixing. Normally `yes`.

### Outputs

- `noise` A noise generator

### Usage

#### Generating small variations

- Connect two noise sources to the node, and set `weight2` to `0`. Set the noise sources to have (different) fixed seeds.
- Try different seeds on the first source until you get an image you like.
- Increase `weight2` slowly (a weight of 0.2 is pretty big) to get variations on the image.
- Try different second seeds as well

#### Masked noise

This is a bit more experimental!

- Follow the first two steps above. 
- Once you get an image you like, copy it into a `Load Image` node and edit a mask to pick the parts of the image you'd like to vary the noise for.
- Connect the mask to the mask input, and then follow the third and fourth steps above.

If you leave `noise2` unconnected, the effect of the mask is to reduce the noise (mixing it with zero) in the areas masked. This is similar in concept to the `Shape Noise` node below.


## Shape Noise

This node takes a noise input and applies some simple shaping options to it.

### Inputs

- *Required* - `noise` - the original noise source.
- *Required* - `weight` - the weight of the shaping. Positive values increase noise in the center of the image and reduce it at the periphery, negative values do the opposite.
- *Required* - `renormalise` - should the noise be renormalised to mean of zero and stdev of one after mixing. Normally `yes`.
- *Required* - `mode` - Apply just in the `x` direction, just in the `y` direction, or `xy` both.
- *Required* - `shape` - the shape of the weighting. `sin` looks like `sin(x) for 0<x<pi`, `point` goes linearly up then down (so it's harsher)

### Outputs

- `noise` A noise generator

### Concept

The sampling process works by trying to remove noise to reveal an image. It is trained with noise evenly distributed over the latent, so that is
what it tries to remove. If There is more noise in one part of the image than another, it tries to make sense of that by making that part of the image 'noisier' - that is, more busy, or detailed.

So *to a slight extent* you can make part of the image more detailed (or more bland) by shifting the magnitude of noise around.

### Usage

- Plug your noise source in. Set the weight to `0` (which does nothing). Leave `renormnalise` at `yes`, `mode` at `xy` and `shape` at `sin`.
- Put the seed of your noise to `fixed` so you can compare images
- Generate an image
- Increase the weight a little, and try again
- Above a weight of about 0.3 you'll probably find things go crazy (you can go higher if the mode is `x` or `y` instead of `xy`)
