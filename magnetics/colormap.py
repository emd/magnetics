import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


try:
    from distinct_colours import get_distinct
except ImportError:
    print '\n`distinct_colours` module not found.'

    import os as _os
    _dir = _os.path.dirname(__file__)
    _url = 'https://personal.sron.nl/~pault/python/distinct_colours.py'

    print '\nAttempting to download local copy of `distinct_colours`...\n'
    _err = _os.system('wget -P %s %s' % (_dir, _url))

    if not _err:
        print 'Success!'
        from .distinct_colours import get_distinct
    else:
        print '\nFailed...'
        print ''
        print ('`distinct_colours` defines color-blind-proof,'
               ' distinct color schemes.')
        print ('If you wish to use this module, please download from:')
        print ('\n    %s' % _url)
        print ('\nand place in your Python path.')


def mixed_sign_mode_numbers(angular_separation=(np.pi / 4)):
    '''Get discrete colormap for -6 <= mode number <= 5.

    The `distinct_colours` module defines up to twelve,
    distinct, color-blind-proof colors. The primary colormap
    returned by this function (for use with the magnetics)
    utilizes all twelve of these colors. The secondary
    colormap, for use with a two-point-correlation measurement
    separated by `angular_separation`, will consist of
    the appropriate subset.

    Parameters:
    -----------
    angular_separation - float
        The angular separation of the measurements used
        in the two-point-correlation.
        [angular_separation] = radian

    Returns:
    --------
    (cmap, cmap2) - tuple, where

    cmap - :py:class:`ListedColormap <matplotlib.colors.ListedColormap>`
        A discrete colormap of distinct, color-blind-proof colors
        for use with magnetics.

    cmap2 - :py:class:`ListedColormap <matplotlib.colors.ListedColormap>`
        An appropriate subset of `cmap` for use with a
        two-point-correlation measurement.

    '''
    # Construct primary (magnetics) colormap
    Ncols = 12
    cool_to_warm = False
    cmap = _distinct_colormap(
        Ncols, cool_to_warm=cool_to_warm)

    # Construct secondary colormap for two-point-correlation
    mode_numbers = np.arange(-6, 6)
    lbound = np.int(np.floor(-np.pi / angular_separation)) + 1
    ubound = np.int(np.floor(np.pi / angular_separation))

    if lbound > mode_numbers[0]:
        start = np.where(mode_numbers >= lbound)[0][0]
    else:
        start = None

    if ubound < mode_numbers[-1]:
        stop = np.where(mode_numbers <= ubound)[0][-1] + 1
    else:
        stop = None

    cmap2 = _distinct_colormap(
        Ncols, start=start, stop=stop, cool_to_warm=cool_to_warm)

    return cmap, cmap2


def positive_mode_numbers(angular_separation=(np.pi / 4)):
    # Construct primary (magnetics) colormap
    Ncols = 12
    cool_to_warm = True
    cmap = _distinct_colormap(
        Ncols, cool_to_warm=cool_to_warm)

    # Construct secondary colormap for two-point-correlation
    mode_numbers = np.arange(0, Ncols)
    lbound = np.int(np.floor(-np.pi / angular_separation)) + 1
    ubound = np.int(np.floor(np.pi / angular_separation))

    ubound = ubound - lbound

    if ubound < mode_numbers[-1]:
        stop = np.where(mode_numbers <= ubound)[0][-1] + 1
    else:
        stop = None

    cmap2 = _distinct_colormap(
        Ncols, start=None, stop=stop, cool_to_warm=cool_to_warm)

    return cmap, cmap2


# def negative_mode_numbers(dtheta=None):
#     cool_to_warm = False
#     return


def _distinct_colormap(Ncols, start=None, stop=None, cool_to_warm=False):
    '''Get a color-blind-proof, discrete colormap of *distinct* colors.

    Parameters:
    -----------
    Ncols - int
        The total number of colors to be included in the colormap.
        Note that 1 <= `Ncols` <= 12; this constraint is imposed
        by :py:function:`get_distinct <distinct_colours.get_distinct>`.

    start (stop) - int (or None, if not slicing)
        To only use a subset of the `Ncols` in the colormap,
        specify a start and a stop index. To use the full colormap,
        start can be specified as `0` or `None` and stop can
        be specified as `None`.

        Note: if reversal of the colormap is requested (i.e. if
        `cool_to_warm` is False), the reversal is performed
        *before* the slicing.

    cool_to_warm - bool
        The `distinct_colours` submodule returns colors that
        progress from "cool" to "warm". If `cool_to_warm` is
        False, reverse the color scheme such that colors progress
        from "warm" to "cool".

    Returns:
    --------
    cmap - :py:class:`ListedColormap <matplotlib.colors.ListedColormap>`
        A discrete colormap of distinct, color-blind-proof colors.

    '''
    # Determine the identity of *all* of the distinct colors in colormap
    cols = get_distinct(Ncols)
    cmap_name = 'distinct_%i' % Ncols

    # Reverse colormap, if requested
    if not cool_to_warm:
        cols.reverse()
        cmap_name += '_warm_to_cool'
    else:
        cmap_name += '_cool_to_warm'

    # Slice colormap, if requested
    sl = slice(start, stop)

    if start is not None:
        cmap_name += '_%i' % start
    else:
        cmap_name += '_None'

    if stop is not None:
        cmap_name += '_%i' % stop
    else:
        cmap_name += '_None'

    # Create the colormap
    cmap = ListedColormap(cols[sl], name=cmap_name)

    return cmap
