Project 4

This project is in Python!
The packages you will need are:
numpy, matplotlib, scipy.sparse, and skimage, including
skimage.exposure, skimage.transform, and skimage.draw


Main.py will run all three sections. Set appropriate truth values to run one section at a time. Most of the code in main.py is for splitting and recombining color channels.

Part 0:
* image_io *
These two functions load and save images by normalizing them and converting them to B&W if necessary.

* compute_lsqr *
construct A2
    This creates a sparse 2-neighbor constraint matrix for s, and sets the top left corner pixel to be the same as the source image.
compute_lsqr
    This creates b by multiplying A by s, then solves for v.

Part 1:
* align_images * and * get_mask *
All these functions work basically the same as the starter code that was provided.

* masking operations *
shift and inside combine to get the border of mask s.

construct_A4 creates a 4-neigbor mask and zeroes out the border.

set_b sets the values of b as requested.

poisson_blend actually does the blending. (See website for full description of method.)

Part 2:
This part is exactly the same as part 1, except we also compare the s and t gradients and take whichever is larger.