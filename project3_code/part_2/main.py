import numpy as np
import matplotlib.pyplot as plt

from unsharp import *
from stack_functions import *

flist = ['mjagger_old_composite.jpg']
#flist = ['lenna.jpg']

for fname in flist:
    im = plt.imread(fname)
    if im.mean() >= 1:
        im = im/255.

    levels = 5
    gstack = create_fstack(im, Gaussian, levels)
    lstack = create_stack(im, levels)
    stack_list = [gstack, lstack]
    stack_shape = (len(stack_list), levels)
    save_stacks(fname[:-4], np.concatenate(stack_list), stack_shape)