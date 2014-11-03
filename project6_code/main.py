import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d
from glob import glob


fpath = '/Users/rachel/Desktop/tarot_cards/*.png'
flist = glob(fpath)

print('loading images...')
images = []
for fname in flist:
    images.append(plt.imread(fname))


def shift_image(im, shift):
    delta_y = shift[0]
    delta_x = shift[1]
    imOut = np.zeros(im.shape)
    for i, c in enumerate(np.dsplit(im, 3)):
        c = c[:, :, 0]
        Y = np.arange(c.shape[0])
        X = np.arange(c.shape[1])
        f = interp2d(X + delta_x, Y + delta_y, c)
        imOut[:, :, i] = f(X, Y)
    return imOut


def shifted_images():
    for fnum, f in enumerate(np.arange(-9, 13)):
    #for fnum, f in enumerate(np.arange(-2, 2)):
        print(f)
        total = 0.
        for i, curr_img in enumerate(images):
            # get x and y coords for each image
            yval = np.floor(i/17.)
            xval = i % 17.
            total += shift_image(curr_img, (f*(9.-yval), f*(9.-xval)))
        out_name = './output/frame_{0}.jpg'.format(fnum)
        plt.imsave(out_name, total/len(images))


def get_aperture(ay, ax):
    a2 = (int(np.round(ay/2.)), int(np.round(ax/2.)))
    coords = np.arange(289).reshape((17, 17))
    return np.array(coords[8 - a2[0]: 9 + a2[0],
                           8 - a2[1]: 9 + a2[1]].flatten())


def aperture_images():
    print('computing aperture images...')
    ays = [ 1, 17,  5, 17]
    axs = [17,  1, 17,  5]
    #ays = np.arange(1, 17)
    #axs = ays.copy()
    for anum, (ay, ax) in enumerate(zip(ays, axs)):
        print('aperture {0} of {1}'.format(anum, len(ays)-1))
        coords = get_aperture(ay, ax)

        if len(coords) == 1:
            out_im = images[coords]
        else:
            out_im = np.mean([images[i] for i in coords], axis=0)
        out_name = './output/apertures/asymmetric/aperture_{0}_{1}.jpg'.format(ay, ax)
        plt.imsave(out_name, out_im)

shifted_images()
aperture_images()