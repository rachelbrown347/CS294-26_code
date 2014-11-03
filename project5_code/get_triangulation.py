import numpy as np
import matplotlib.pyplot as plt


def get_corr(im, example):
    fig, axes = plt.subplots(nrows=1, ncols=2)
    plt.suptitle('Please select points according to the example. Double-click on the last point to exit.')
    axes[0].imshow(example)
    axes[1].imshow(im)

    ax = axes[1].axis()
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
        axes[1].plot(xs, ys, 'bs')
        plt.draw()
    plt.close('all')
    return (np.array(xs), np.array(ys))

def get_shape(im, example, fnamepath):
    tshape = np.array(get_corr(im, example)).T

    # add four corners
    x, y, c = im.shape
    corners = np.array([[0, 0], [0, x], [y, 0], [y, x]])
    tshape = np.vstack([tshape, corners])

    np.savetxt(fnamepath, tshape, fmt='%.0f')
    return tshape