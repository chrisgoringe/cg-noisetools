# Noise Tools

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
