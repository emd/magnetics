Python tools for retrieving and analyzing DIII-D magnetics signals.


Installation:
=============


... on GA's Iris cluster:
-------------------------
Package management is cleanly handled on Iris via
[modules](https://diii-d.gat.com/diii-d/Iris#Environment_modules).
The `magnetics` package has a corresponding modulefile
[here](https://github.com/emd/modulefiles).

To use the `magnetics` package, change to the directory
you'd like to download the source files to and
retrieve the source files from github by typing

    $ git clone https://github.com/emd/magnetics.git

The created `magnetics` directory defines the
package's top-level directory.
The modulefiles should be similarly cloned.

Now, at the top of the corresponding
[modulefile](https://github.com/emd/modulefiles/blob/master/magnetics),
there is a TCL variable named `magnetics_root`;
this must be altered to point at the
top-level directory of the cloned `magnetics` package.
That's it! You shouldn't need to change anything else in
the modulefile. The `magnetics` module can
then be loaded, unloaded, etc., as is discussed in the
above-linked Iris documentation.

The modulefile also defines a series of automated tests
for the `magnetics` package. Run these tests at the command line
by typing

    $ test_magnetics

If the tests return "OK", the installation should be working.
(Currently, no automated tests are implemented).


... elsewhere:
--------------
Define an environmental variable `$pci_path` specifying
the appropriate MDSplus server's tree-path definitions
(`hermit.gat.com::/trees/pci`)
by, for example, adding the following to your `.bashrc`

    $ export pci_path='hermit.gat.com::/trees/pci'

(While data is digitized on `magnetics`, it should (ideally)
always be transferred to `hermit` prior to analysis;
digitization and writing is very resource intensive, and
an untimely request for data retrieval from `magnetics` could cause
sufficient loading to result in data loss or a system crash).

Now, change to the directory you'd like to download the source files to
and retrieve the source files from github by typing

    $ git clone https://github.com/emd/magnetics.git

Change into the `magnetics` top-level directory by typing

    $ cd magnetics

For accounts with root access, install by running

    $ python setup.py install

For accounts without root access (e.g. a standard account on GA's Venus
cluster), install locally by running

    $ python setup.py install --user

To test your installation, run

    $ nosetests tests/

If the tests return "OK", the installation should be working.
(Currently, no automated tests are implemented).


Use:
====
Single magnetics signals are readily retrieved via
the `magnetics.signal.Signal` class. For example, use:

```python
import magnetics

shot = 167342
pointname = 'MPI66M307D'
tlim = [1.0, 2.5]        # [tlim] = s

sig = magnetics.signal.Signal(shot, pointname, tlim=tlim)

```

to retrieve the magnetics signal from the 307-degree midplane probe
(which measures *poloidal* magnetic-field fluctuations)
for the specified time window and shot.

Retrieval and analysis of *all* of the magnetic signals
from the midplane toroidal array is facilitated by
the `magnetics.signal.ToroidalSignals` class.
For example, having executed the above code, use

```python
torsigs = magnetics.signal.ToroidalSignals(shot, tlim=tlim)

```

to retrieve all of the magnetics signals from the midplane toroidal array
for the specified time window and shot. The toroidal mode number
as a function of frequency and time can then be computed and
visualized using the
[random_data package](https://github.com/emd/random_data).
Specifically,

```python
import random_data as rd

# Spectral-estimation parameters
Tens = 5e-3         # Ensemble time length, [Tens] = s
Nreal_per_ens = 4   # Number of realizations per ensemeble

# Determine mode numbers
A = rd.array.Array(
    torsigs.x, torsigs.locations, Fs=torsigs.Fs, t0=torsigs.t0,
    Tens=Tens, Nreal_per_ens=Nreal_per_ens)

A.plotModeNumber()

```

![mode_number_spectrum](https://raw.githubusercontent.com/emd/magnetics/master/figs/mode_number_spectrum.png)
