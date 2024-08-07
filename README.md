# Noise Tools

Two nodes for playing with noise.

`Mix Noise` is designed for generating small variations in order to create sets of similar images.

`Shape Noise` is designed to push noise towards (or away from) the center of the image.

All the images below were generated using [LEOSAM](https://civitai.com/user/LEOSAM)'s HelloWorld XL 7, and
the prompt was stolen from the [example image](https://civitai.com/images/15652252).

Drag and drop any of these images into Comfy to get the workflow.

## Mix Noise

This node takes two noise inputs and produces a weighted mix, optionally with a weight mask. The effect is to allow you to interpolate the noise between two extremes, or generate small variations:

|Seed 1|0.1|0.3|0.5|Seed 2|
|-|-|-|-|-|
|![1](media/weight0.00.png)|![1](media/weight0.10.png)|![1](media/weight0.30.png)|![1](media/weight0.50.png)|![1](media/weight1.00.png)


### Inputs 

- *Required* - `noise1` - the original noise source.
- *Optional* - `noise2` - the secondary noise source. If not connected, it is zero noise.
- *Required* - `weight2` - the weight given to the second noise source. The first noise source has weight `1-weight2`.
- *Optional* - `mask` - multiply `weight2` by the mask values. The mask will be rescaled to fit the latent. Note that this is not the sort of noise masking you want for inpainting - the sampler will try to remove noise globally. 
- *Required* - `renormalise` - should the noise be renormalised (`mean=0, stdev=1`) after mixing. Normally `yes`.

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

This node takes a noise input and applies some simple shaping options to it. The effect is to push detail into the middle, or out of it.

||0.1|0.2|0.3|0.4|0.5|
|-|-|-|-|-|-|
|+|![1](media/shape0.10.png)|![1](media/shape0.20.png)|![1](media/shape0.30.png)|![1](media/shape0.40.png)|![1](media/shape0.50.png)|
|-|![1](media/negshape0.10.png)|![1](media/negshape0.20.png)|![1](media/negshape0.30.png)|![1](media/negshape0.40.png)|![1](media/negshape0.50.png)|

The negative push breaks down when the detail is pushed out to the corners, and the sampler can't make any sense of it. The more realistic an image, generally the sooner it breaks down.

A small negative value can help detail spread across the whole image (as there is a tendency for many models to focus on the main feature in the center)

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
