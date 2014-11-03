import numpy as np
import matplotlib.pyplot as plt

from unsharp import *
from stack_functions import *

im1_fname = 'orange.jpg'
im2_fname = 'apple.jpg'

im1 = plt.imread(im1_fname)
if im1.mean() >= 1.0:
    im1 = im1/255.

im2 = plt.imread(im2_fname)
if im2.mean() >= 1.0:
    im2 = im2/255.

#if np.max(mask) > 1.0:
#    mask = mask/255.

levels = 7
mask = np.hstack([np.zeros([im1.shape[0],  np.ceil(im1.shape[1]/2.)]), 
                   np.ones([im1.shape[0], np.floor(im1.shape[1]/2.)])])

mask_stack = create_fstack(mask, Gaussian, levels)
im1_stack  = create_stack(im1, levels)
im2_stack  = create_stack(im2, levels)

im1_m_stack = apply_mask_stack(im1_stack, mask_stack, 1)
im2_m_stack = apply_mask_stack(im2_stack, mask_stack, 0)
combined_stack = [a+b for a,b in zip(im1_m_stack, im2_m_stack)]

combined_fname = im1_fname[:-4] + '_' + im2_fname[:-4]
stack_list = [im1_m_stack, im2_m_stack, combined_stack]
stack_shape = (len(stack_list), levels)

save_stacks(combined_fname, np.concatenate(stack_list), stack_shape)

composite = composite((im1, im2), combined_stack, mask, levels)
composite = rescale_intensity(composite, in_range = (0, 1), out_range=(0, 1))
plt.imsave(combined_fname+'_composite.jpg', composite)


