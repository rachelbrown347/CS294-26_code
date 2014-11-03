
from image_io import *
from compute_lsqr import *
from get_mask import *
from align_images import *
from masking_operations import *


runToy = True
runPoisson = True
runMixed = True


def toy_problem(fpath, fname):
    s = image_open(fpath, fname, in_color=True)

    r = s[:, :, 0]
    g = s[:, :, 1]
    b = s[:, :, 2]

    # for each color channel, compute lsqr
    c_out = []
    for i, c in enumerate([r, g, b]):
        print('Solving for color channel {0}...'.format(i))
        c_out.append(compute_lsqr(c))
    im_out = np.dstack(c_out)

    # save the image to view output
    new_fpath = './output/'
    new_fname = fname[:-4] + '_2.jpg'
    image_save(new_fpath, new_fname, im_out, in_color=True)

    # check to make sure images are the same
    assert np.allclose(s, im_out, atol=1.e-4)


def poisson_blending(s_fpath, t_fpath, s_fname, t_fname, maximum):
    s = image_open(s_fpath, s_fname, in_color=1)
    t = image_open(t_fpath, t_fname, in_color=1)

    # get alignment and mask
    s, s_mask, tinyt, tinyt_topleft = align_images(s, t)

    sr = s[:, :, 0]
    sg = s[:, :, 1]
    sb = s[:, :, 2]

    tr = tinyt[:, :, 0]
    tg = tinyt[:, :, 1]
    tb = tinyt[:, :, 2]

    fr = t[:, :, 0]
    fg = t[:, :, 1]
    fb = t[:, :, 2]

    s_mask = np.mean(s_mask, 2).astype(bool)

    # blend each channel
    c_out = []
    for cnum, (sc, tc, fc) in enumerate(zip([sr, sg, sb], [tr, tg, tb], [fr, fg, fb])):
        print('Blending channel {0}'.format(cnum))
        c_out.append(poisson_blend(sc, s_mask, tc, fc, tinyt_topleft, maximum=maximum))
    im_out = np.dstack(c_out)

    # save output image
    new_fpath = './output/'
    new_fname = s_fname[:-4] + '_blended.jpg'
    image_save(new_fpath, new_fname, im_out, in_color=True)


if runToy:
    print('Running toy problem...')
    fpath = './images/source/'
    fname = 'lego_small.jpg'
    toy_problem(fpath, fname)
    print('Toy problem complete.')

if runPoisson:
    print('Running Poisson blending...')
    s_fpath = './images/source/'
    t_fpath = './images/target/'
    s_fname = 'lego_small.jpg'
    t_fname = 'landscape.jpg'
    maximum = False
    poisson_blending(s_fpath, t_fpath, s_fname, t_fname, maximum)
    print('Poisson blending complete.')

if runMixed:
    print('Running mixed gradient Poisson blending...')
    s_fpath = './images/source/'
    t_fpath = './images/target/'
    s_fname = 'logo.jpg'
    t_fname = 'landscape.jpg'
    maximum = True
    poisson_blending(s_fpath, t_fpath, s_fname, t_fname, maximum)
    print('Mixed gradient Poisson blending complete.')