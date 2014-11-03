
import numpy as np
import matplotlib.pyplot as plt
from skimage.draw import polygon

def get_outline(im, instructions):
    fig = plt.figure()
    plt.imshow(im, cmap='gray', vmin=0, vmax=1)
    plt.title(instructions)
    ax = plt.axis()
    plt.xlim(ax[0], ax[1])
    plt.ylim(ax[2], ax[3])

    pts = []

    while True:
        x, y = plt.ginput(n=1, timeout=0)[0]
        x = int(x)
        y = int(y)
        if pts and (x, y) == pts[-1]:
            break
        pts.append((x, y))
        xs, ys = zip(*pts)
        plt.plot(xs, ys, 'ko-')
        plt.draw()
    plt.close('all')
    return np.array(xs), np.array(ys)

def get_mask(im, ys, xs):
    rr, cc = polygon(ys, xs)
    mask = np.zeros(im.shape)
    mask[rr, cc] = 1.0
    return mask