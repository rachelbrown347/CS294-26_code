from skimage.exposure import rescale_intensity

from align_images import *
from unsharp import *

fname1 = 'mjagger_old.jpg'
fname2 = 'mjagger_young.jpg'

# high sf
im1 = plt.imread(fname1)
oh1, ow1, _ = im1.shape
if im1.mean() >= 1:
    im1 = im1/255.

# low sf
im2 = plt.imread(fname2)
oh2, ow2, _ = im2.shape
if im2.mean() >= 1:
    im2 = im2/255.

pts = get_points(im1, im2)
im1, im2 = align_images(im1, im2, pts)
im1, im2 = rescale_images(im1, im2, pts)
im1, angle = rotate_im1(im1, im2, pts)
im1, im2 = match_img_size(im1, im2, (oh1, ow1), (oh2, ow2))

sigma1 = 4
sigma2 = 4
both = combine_freq(im1, im2, sigma1, sigma2)
both = rescale_intensity(both, in_range=(0, 1), out_range=(0, 1))

new_fname = fname1[:-4]+'_composite.jpg' 
plt.imsave(new_fname, both, cmap='gray')