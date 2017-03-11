'''This module implements a class for retrieving individual signals
from DIII-D magnetics.

'''


import numpy as np
from data import Data


class Signal(object):
    '''An object corresponding to the retrieved DIII-D magnetics signal.

    This is essentially a convenience wrapper around DIII-D's
    :py:class: `Data <data.Data>`.

    Attributes:
    -----------
    shot - int
        DIII-D shot number of the retrieved signal.

    point_name - string
        Point name of the retrieved signal.

    x - array-like, (`N`,)
        The retrieved signal.
        [x] = see the relevant documentation on the internal DIII-D website:

            https://diii-d.gat.com/DIII-D/diag/magnetics/magnetics.html

    Fs - float
        The signal sampling rate.
        [Fs] = samples / second

    t0 - float
        The time corresponding to the first retrieved point in the signal;
        that is, if x(t) corresponds to the continuous signal being sampled,
        then `Signal.x[0]` = x(t0)
        [t0] = s

    Methods:
    --------
    t - returns retrieved signal time-base, array-like, (`N`,)
        The time-base is generated on the fly as needed and is not stored
        as an object property; this helps save memory and processing time,
        as we do not typically look at the raw signal vs. time.
        [t] = s

    '''
    def __init__(self, shot, point_name, tlim=None):
        '''Create an instance of the `Signal` class.

        Input parameters:
        -----------------
        shot - int
            DIII-D shot number.

        point_name - string
            Point name of the desired magnetic signal. Valid point
            names are listed on the internal DIII-D website here:

            https://diii-d.gat.com/DIII-D/diag/magnetics/magnetics.html

        tlim - array_like, (2,)
            The lower and upper limits in time for which the signal
            will be retrieved.

            If `tlim` is not `None` and it is *not* a length-two array,
            a ValueError is raised.

            [tlim] = s

        '''
        self.shot = shot
        self.point_name = point_name
        self.t0, self.Fs, self.x = self._getSignal(tlim)

    def _getSignal(self, tlim):
        'For window `tlim`, get initial time, sampling rate, and signal.'
        if tlim is not None:
            # Ensure limits in time are correctly sized and sorted
            if len(tlim) != 2:
                raise ValueError('`tlim` must be an iterable of length 2.')
            else:
                tlim = np.sort(tlim)

                # DIII-D times are ms by convention, so
                # convert `tlim` from seconds to ms
                tlim *= 1e3

        # Timing
        # [t0] = [t1] = seconds, [Fs] = samples / s
        t0, t1 = 1e-3 * Data(self.point_name, self.shot,
                             tmin=tlim[0], tmax=tlim[1]).x[0][0:2]
        Fs = 1. / (t1 - t0)

        # Signal
        x = Data(self.point_name, self.shot, tmin=tlim[0], tmax=tlim[1]).y

        return t0, Fs, x

    def t(self):
        'Get times for points in `self.x`.'
        return self.t0 + (np.arange(len(self.x)) / self.Fs)
