import numpy as np
import matplotlib.pyplot as plt
from skimage.exposure import rescale_intensity


def image_open(fpath, fname, in_color=True):

    im = plt.imread(fpath + fname)

    if np.max(im) > 1:
        im = im/255.

    if in_color == False:
        im = np.mean(im, 2)
    
    return im

def image_save(new_fpath, new_fname, im, in_color):
    if in_color:
        im = rescale_intensity(im, in_range=(0, 1), out_range=(0, 1))
        plt.imsave(new_fpath + new_fname, im, vmin=0, vmax=1)
    else:
        plt.imsave(new_fpath + new_fname, im, cmap='gray', vmin=0, vmax=1)
