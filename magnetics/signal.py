'''This module implements a class for retrieving individual signals
from DIII-D magnetics.

'''


import numpy as np
from data import Data


class Signal(object):
    '''An object corresponding to the retrieved DIII-D magnetics signal.

    This is essentially a convenience wrapper around DIII-D's
    :py:class:`Data <pyDatautils.data.Data>`.

    Attributes:
    -----------
    shot - int
        DIII-D shot number of the retrieved signal.

    pointname - string
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
    def __init__(self, shot, pointname, tlim=None):
        '''Create an instance of the `Signal` class.

        Input parameters:
        -----------------
        shot - int
            DIII-D shot number.

        pointname - string
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
        self.pointname = pointname
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
                tlim = 1e3 * tlim

        # Load data
        if tlim is not None:
            d = Data([self.pointname, '.MAG'], self.shot,
                     tmin=tlim[0], tmax=tlim[1])
        else:
            d = Data([self.pointname, '.MAG'], self.shot)

        # Extract relevant values
        t0, t1 = d.x[0][0:2]
        sig = d.y

        # Convert timing to SI units
        # [t0] = [t1] = seconds, [Fs] = samples / s
        t0 *= 1e-3
        t1 *= 1e-3
        Fs = 1. / (t1 - t0)

        return t0, Fs, sig

    def t(self):
        'Get times for points in `self.x`.'
        return self.t0 + (np.arange(len(self.x)) / self.Fs)


class ToroidalSignals(object):
    '''An object corresponding to DIII-D toroidal magnetics signals.

    This is essentially a convenience wrapper around
    :py:class:`Signal <magnetics.signal.Signal>`.

    Attributes:
    -----------
    shot - int
        DIII-D shot number.

    pointnames - array_like (`M`,)
        Point names of the retrieved signals, where `M` is
        the number of signals.

    locations - array_like, (`M`,)
        The toroidal locations of the retrieved signals, where `M` is
        the number of signals.
        [locations] = radian

    x - array_like, (`M`, `N`)
        The retrieved signals, where `M` is the number of signals and
        `N` is the number of points in each digital record.
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
    def __init__(self, shot, tlim=None):
        '''Create an instance of the `ToroidalSignals` class.

        Input parameters:
        -----------------
        shot - int
            DIII-D shot number.

        tlim - array_like, (2,)
            The lower and upper limits in time for which the signal
            will be retrieved.

            If `tlim` is not `None` and it is *not* a length-two array,
            a ValueError is raised.

            [tlim] = s

        '''

        self.shot = shot
        self.t0, self.Fs, self.x = self._getSignals(tlim)

    def _getSignals(self, tlim):
        'For window `tlim`, get initial time, sampling rate, and signals.'
        # Toroidal location of sensor, as obtained from
        # Bill Heidbrink in
        #
        #       ~heidbrin/idl/FFT/d3d_array_tor.pro
        #
        # on GA's Venus cluster.
        #
        # [self.locations] = radian
        self.locations = (np.pi / 180) * np.array(
            [67.5, 97.4, 127.8, 137.4, 157.6, 246.4,
             277.5, 307, 312.4, 317.4, 339.8])

        # Construct the corresponding point names
        nominal_locations = ['067', '097', '127', '137', '157', '247',
                             '277', '307', '312', '322', '340']

        self.pointnames = [('MPI66M%sD' % s) for s in nominal_locations]

        # Load the first signal to determine initial time `t0`
        # sampling rate `Fs`
        sig = Signal(self.shot, self.pointnames[0], tlim=tlim)
        t0 = sig.t0
        Fs = sig.Fs

        # Initialize `signals` array and store first waveform
        signals = np.zeros((len(self.pointnames), len(sig.x)))
        signals[0, :] = sig.x

        # Loop through *remainder* of sensors
        for i, pointname in enumerate(self.pointnames[1:]):
            sig = Signal(self.shot, pointname, tlim=tlim)
            signals[i + 1, :] = sig.x

        return t0, Fs, signals

    def t(self):
        'Get times for points in `self.x`.'
        return self.t0 + (np.arange(self.x.shape[1]) / self.Fs)
