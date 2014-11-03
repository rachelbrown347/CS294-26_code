import numpy as np 
import matplotlib.pyplot as plt
from skimage.exposure import rescale_intensity

from unsharp import *

# Load file and normalize to 0-1
fname = 'iguana.jpg'
im = plt.imread(fname)
if im.mean() >= 1:
    im = im/255.

sigma = 5
amplitude = 1.5
imsharp = unsharp_mask(im, sigma, amplitude)
imsharp = rescale_intensity(imsharp, in_range=(0, 1), out_range=(0,1))

new_fname = fname[:-4]+'_sharp.jpg'
plt.imsave(new_fname, imsharp)