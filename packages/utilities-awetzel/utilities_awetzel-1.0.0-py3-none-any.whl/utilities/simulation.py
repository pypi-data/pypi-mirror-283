'''
Utilities for setting up and running simulations with Gizmo or CART.

@author: Andrew Wetzel <arwetzel@gmail.com>

----------
Units

Unless otherwise noted, this package stores all quantities in (combinations of) these base units
    mass [M_sun]
    position [kpc comoving]
    distance, radius [kpc physical]
    time [Gyr]
    temperature [K]
    magnetic field [Gauss]
    elemental abundance [linear mass fraction]

These are the common exceptions to those standards
    velocity [km/s]
    acceleration [km/s / Gyr]
    gravitational potential [km^2 / s^2]
    rates (star formation, cooling, accretion) [M_sun / yr]
    metallicity (if converted from stored massfraction)
        [log10(mass_fraction / mass_fraction_solar)], using Asplund et al 2009 for Solar
'''

import numpy as np

from . import array, binning, constant, io, particle, plot


# --------------------------------------------------------------------------------------------------
# snapshots
# --------------------------------------------------------------------------------------------------
class SnapshotClass(dict, io.SayClass):
    '''
    Dictionary class to store/print redshifts, scale-factors, times, to use for simulation.
    '''

    def __init__(self, verbose=True):
        self['scalefactor.spacing'] = None
        self['cosmology'] = None
        self['verbose'] = verbose

    def get_snapshot_indices(self, time_name='redshift', time_values=None, round_kind='near'):
        '''
        Get index[s] in snapshot list where values are closest to, using input round_kind.

        Parameters
        ----------
        time_name : str
            time kind for values: 'redshift', 'scalefactor', 'time'
        time_values : float or array or str
            redshift[s] / scale-factor[s] / time[s] to get index of
        round_kind : str
            method to identify nearest snapshot: 'up', 'down', 'near'

        Returns
        -------
        snapshot_indices : int or array
            index number[s] of snapshot file
        '''
        snapshot_values = np.sort(self[time_name])  # sort redshifts because are in reverse order

        scalarize = False
        if np.isscalar(time_values):
            time_values = [time_values]
            scalarize = True  # if input scalar value, return scalar value (instead of array)

        assert np.min(time_values) >= np.min(snapshot_values) and np.max(time_values) <= np.max(
            snapshot_values
        )

        snapshot_indices = binning.get_bin_indices(
            time_values, snapshot_values, round_kind=round_kind
        )

        if time_name == 'redshift':
            # because had to sort redshifts in increasing order, have to reverse indices
            snapshot_indices = (snapshot_values.size - 1) - snapshot_indices

        if scalarize:
            snapshot_indices = snapshot_indices[0]

        return snapshot_indices

    def parse_snapshot_values(self, snapshot_value_name, snapshot_values, verbose=True):
        '''
        Convert input snapshot value[s] to snapshot index[s].

        Parameters
        ----------
        snapshot_value_name : str
            kind of value supplying: 'redshift', 'scalefactor', 'time', 'index'
        snapshot_values : int or float or array thereof, or str
            corresponding value[s]
            if 'all' or None, return all snapshot indices
        verbose : bool
            whether to print conversions

        Returns
        -------
        snapshot_indices : int or array
            index[s] of snapshots
        '''
        if isinstance(snapshot_values, str) or snapshot_values is None:
            # return all snapshot indices
            return self['index']

        if not np.isscalar(snapshot_values):
            snapshot_values = np.asarray(snapshot_values)

        if snapshot_value_name in ['redshift', 'scalefactor', 'time']:
            snapshot_indices = self.get_snapshot_indices(snapshot_value_name, snapshot_values)
            snapshot_time_name = snapshot_value_name
            snapshot_time_values = self[snapshot_value_name][snapshot_indices]
            self.say(
                '* input {} = {}:'.format(
                    array.scalarize(snapshot_value_name), array.scalarize(snapshot_values)
                ),
                verbose,
                end='',
            )
        else:
            # assume that input snapshot indices
            assert snapshot_value_name == 'index'
            snapshot_indices = snapshot_values
            snapshot_time_name = 'redshift'
            snapshot_time_values = self['redshift'][snapshot_indices]

        if np.isscalar(snapshot_indices) or len(snapshot_indices) == 1:
            self.say(
                'using snapshot index = {}, {} = {:.3f}\n'.format(
                    array.scalarize(snapshot_indices),
                    snapshot_time_name,
                    array.scalarize(snapshot_time_values),
                ),
                verbose,
            )
        else:
            self.say(
                f'* using snapshot indices = {array.scalarize(snapshot_indices)}',
                verbose,
            )
            self.say(f'{snapshot_time_name}s = {snapshot_time_values}\n', verbose)

        return snapshot_indices

    def get_redshifts_sampled(self, redshift_limts, number, scalefactor_log_scale=False):
        '''
        Get array of redshifts spaced linearly or logarithmically in scale-factor.

        Parameters
        ----------
        redshift_limits: list
            min and max limits on redshifts
        number : int
            number of snapshots
        scalefactor_log_scale : bool
            whether to use logarithmic spacing for scale-factor.
            ompute spacings in terms of *scale-factor*, not redshift, for stability

        Returns
        -------
        redshifts : array
        '''
        redshift_limits = np.array([np.max(redshift_limts), np.min(redshift_limts)])
        scale_limits = np.sort(1 / (1 + redshift_limits))

        if scalefactor_log_scale:
            scalefactors = np.logspace(
                np.log10(scale_limits.min()), np.log10(scale_limits.max()), number
            )
        else:
            scalefactors = np.linspace(scale_limits.min(), scale_limits.max(), number)

        return 1 / scalefactors - 1

    def generate_snapshots(
        self,
        regular_redshift_limits=[9, 0.0072],
        regular_snapshot_number=401,
        exact_redshifts=[
            99,
            20,
            19,
            18,
            17,
            16,
            15,
            14,
            13,
            12,
            11,
            10,
            9,
            8,
            7,
            6,
            5,
            4,
            3,
            2,
            1,
        ],
        hires_redshift_limits=[0.0072, 0],
        hires_snapshot_number=100,
        snapshot_log_scale=False,
        Cosmology=None,
    ):
        '''
        Assign scale-factors, redshifts, [ages, look-back times, time spacings] to self.
        Use to determine snapshots for simulation.

        Parameters
        ----------
        regular_redshift_limits : list
            min and max redshifts to sample snapshots at 'regular' spacing in scale-factor
        regular_snapshot_number : int
            number of snapshots at 'regular' spacing
            (including any additional redshifts beyond the limits in exact_redshifts)
        exact_redshifts : array-like
            exact redshifts to include in snapshot list
            if inside redshift_limits, adjust snapshot spacing to ensure inclusion of these values
            if outside redshift_limits, append these values but do not use for sampling
        hires_redshift_limits : list
            min and max redshifts to sample snapshots at 'high-resolution' spacing in scale-factor
        hires_snapshot_number : int
            number of snapshots at 'high-resolution' spacing
        snapshot_log_scale: bool
            whether to use logarithmic spacing for scale-factors
        Cosmology : cosmology class
            if want to generate times corresponding to scale-factors
        '''
        # sort from early to late time (high to low redshift)
        regular_redshift_limits = np.sort(regular_redshift_limits)[::-1]
        exact_redshifts = np.sort(exact_redshifts)[::-1]
        if hires_redshift_limits is not None and len(hires_redshift_limits) > 0:
            assert hires_snapshot_number > 0
            hires_redshift_limits = np.sort(hires_redshift_limits)[::-1]

        # only append redshifts earlier than regular_redshift_limits
        assert exact_redshifts.min() >= regular_redshift_limits.min()
        if hires_redshift_limits is not None and len(hires_redshift_limits) > 0:
            # require that high-res snapshot spacing comes after regular spacing
            assert hires_redshift_limits.max() <= regular_redshift_limits.min()

        # get redshift to include beyond (before) sampling limits
        redshifts_append = exact_redshifts[exact_redshifts > regular_redshift_limits.max()]
        # get redshifts to include within sampling limits
        redshifts_ensure = exact_redshifts[exact_redshifts < regular_redshift_limits.max()]

        if snapshot_log_scale:
            self['scalefactor.spacing'] = 'log'
        else:
            self['scalefactor.spacing'] = 'linear'

        # generate snapshots sampled at regular spacing
        # subtract exact snapshots before max redshift of regular spacing
        self['redshift'] = self.get_redshifts_sampled(
            regular_redshift_limits,
            regular_snapshot_number - redshifts_append.size,
            snapshot_log_scale,
        )

        if len(redshifts_ensure) > 0:
            # ensure that ensure_reshifts are in array
            for z in redshifts_ensure:
                if z not in self['redshift']:
                    # get snapshot index closest to this redshift
                    z_i = self.get_snapshot_indices('redshift', z)
                    self['redshift'][z_i] = z

            # adjust sampling between these redshifts
            for ensure_i, z_hi in enumerate(redshifts_ensure[:-1]):
                z_lo = redshifts_ensure[ensure_i + 1]
                zi_hi = self.get_snapshot_indices('redshift', z_hi)
                zi_lo = self.get_snapshot_indices('redshift', z_lo)
                self['redshift'][zi_hi : zi_lo + 1] = self.get_redshifts_sampled(
                    [z_hi, z_lo], zi_lo - zi_hi + 1, snapshot_log_scale
                )

        # append include_redshifts that are before sampled redshifts
        if redshifts_append.size:
            self['redshift'] = np.append(redshifts_append, self['redshift'])

        # append high-resolution snapshot spacing at low redshift
        if hires_redshift_limits is not None and len(hires_redshift_limits) > 0:
            if regular_redshift_limits.min() == hires_redshift_limits.max():
                hires_snapshot_number += 1  # ensure non-overlapping snapshot
            hires_redshifts = self.get_redshifts_sampled(
                hires_redshift_limits,
                hires_snapshot_number,
                snapshot_log_scale,
            )
            if regular_redshift_limits.min() == hires_redshift_limits.max():
                hires_redshifts = hires_redshifts[1:]
            self['redshift'] = np.append(self['redshift'], hires_redshifts)

        self['scalefactor'] = 1 / (1 + self['redshift'])
        self['index'] = np.arange(self['redshift'].size)
        if Cosmology is not None:
            self.assign_cosmology(Cosmology)

    def _generate_snapshots_v1(
        self,
        snapshot_number=601,
        snapshot_log_scale=False,
        sample_redshift_limits=[12, 0],
        include_redshifts=[
            99,
            30,
            25,
            20,
            19,
            18,
            17,
            16,
            15,
            14,
            13,
            12,
            11,
            10,
            9,
            8,
            7,
            6,
            5,
            4,
            3,
            2,
            1,
            0,
        ],
        hires_redshifts=[0],
        hires_sample_factor=10,
        Cosmology=None,
    ):
        '''
        Assign scale-factors, redshifts, [ages, time spacings] to self.
        Use to determine snapshots for simulation.

        Parameters
        ----------
        snapshot_number : int
            total number of snapshots (including redshifts_include and hi-res sampling)
        snapshot_log_scale: bool
            whether to use logarithmic spacing for scale-factors
        sample_redshift_limits : array-like
            min and max limits for redshifts for regularly sampled snapshots
        redshifts_include : array-like
            exact redshifts to include in snapshot list
            if inside redshift_limits, adjust snapshot spacing to ensure inclusion of these values
            if outside redshift_limits, append these values but do not use for sampling
        hires_redshifts : array-like
            redshifts to sub-sample (prior to each redshift) at higher resolution
        hires_sample_factor : int
            factor by which to sub-sample each hires_redshift at higher resolution
        Cosmology : cosmology class
            if want to generate times corresponding to scale-factors
        '''
        # sort from early to late time (high to low redshift)
        sample_redshift_limits = np.sort(sample_redshift_limits)[::-1]
        include_redshifts = np.sort(include_redshifts)[::-1]
        hires_redshifts = np.sort(hires_redshifts)[::-1]

        # only append earlier redshifts
        assert include_redshifts.min() >= sample_redshift_limits.min()

        # get redshift to include beyond (before) sampling limits
        append_redshifts = include_redshifts[include_redshifts > sample_redshift_limits.max()]
        # get redshifts to include within sampling limits
        ensure_redshifts = include_redshifts[include_redshifts < sample_redshift_limits.max()]

        # subtract extra snapshots to get the number to sample evenly in scale-factor
        snapshot_sample_number = (
            snapshot_number
            - append_redshifts.size
            - hires_redshifts.size * (hires_sample_factor - 1)
        )

        # generate sampled redshifts
        self['redshift'] = self.get_redshifts_sampled(
            sample_redshift_limits, snapshot_sample_number, snapshot_log_scale
        )

        if len(ensure_redshifts) > 0:
            # ensure that ensure_reshifts are in array
            for ensure_redshift in ensure_redshifts:
                if ensure_redshift not in self['redshift']:
                    # get index closest to this redshift
                    z_i = self.get_snapshot_indices('redshift', ensure_redshift)
                    self['redshift'][z_i] = ensure_redshift

            # adjust sampling between these redshifts
            for ensure_i, z_hi in enumerate(ensure_redshifts[:-1]):
                z_lo = ensure_redshifts[ensure_i + 1]
                zi_hi = self.get_snapshot_indices('redshift', z_hi)
                zi_lo = self.get_snapshot_indices('redshift', z_lo)
                self['redshift'][zi_hi : zi_lo + 1] = self.get_redshifts_sampled(
                    [z_hi, z_lo], zi_lo - zi_hi + 1, snapshot_log_scale
                )

        if snapshot_log_scale:
            self['scalefactor.spacing'] = 'log'
        else:
            self['scalefactor.spacing'] = 'linear'

        # append include_redshifts that are before sampled redshifts
        if append_redshifts.size:
            self['redshift'] = np.append(append_redshifts, self['redshift'])

        # sample redshifts at higher resolution
        if hires_redshifts.size:
            for hires_redshift in hires_redshifts:
                # get index closest to this redshift
                z_i = self.get_snapshot_indices('redshift', hires_redshift)
                redshifts_subsampled = self.get_redshifts_sampled(
                    [self['redshift'][z_i - 1], self['redshift'][z_i]],
                    hires_sample_factor + 1,
                    snapshot_log_scale,
                )
                redshifts_all = np.zeros(self['redshift'].size + hires_sample_factor - 1)
                redshifts_all[: z_i - 1] = self['redshift'][: z_i - 1]
                redshifts_all[z_i - 1 : z_i - 1 + hires_sample_factor] = redshifts_subsampled[:-1]
                redshifts_all[z_i - 1 + hires_sample_factor :] = self['redshift'][z_i:]
                self['redshift'] = redshifts_all

        self['scalefactor'] = 1 / (1 + self['redshift'])
        self['index'] = np.arange(self['redshift'].size)
        if Cosmology is not None:
            self.assign_cosmology(Cosmology)

    def read_snapshots(self, file_name='snapshot_times.txt', directory='.'):
        '''
        Read scale-factors, [redshifts, times, look-back times, time spacings] from file.
        Assign to self dictionary.

        Parameters
        ----------
        file_name : str
            name of file that contains list of snapshots
        directory : str
            directory of snapshot file
        regenerate : bool
            whether to regenerate redshifts and times from input scale-factors
        '''
        path_file_name = io.get_path(directory) + file_name

        self.say('* reading:  {}\n'.format(path_file_name.lstrip('./')), verbose=self['verbose'])

        if 'times' in file_name:
            try:
                # newest file format
                snap = np.loadtxt(
                    path_file_name,
                    encoding='utf-8',
                    comments='#',
                    dtype=[
                        ('index', np.int32),
                        ('scalefactor', np.float64),
                        ('redshift', np.float64),
                        ('time', np.float64),  # [Gyr]
                        ('time.lookback', np.float64),  # [Gyr]
                        ('time.width', np.float64),  # [Myr]
                    ],
                )
            except (ValueError, OSError, IOError, IndexError):
                # older file format
                snap = np.loadtxt(
                    path_file_name,
                    encoding='utf-8',
                    comments='#',
                    dtype=[
                        ('index', np.int32),
                        ('scalefactor', np.float64),
                        ('redshift', np.float64),
                        ('time', np.float64),  # [Gyr]
                        ('time.width', np.float64),  # [Myr]
                    ],
                )
            for k in snap.dtype.names:
                self[k] = snap[k]

        elif 'scalefactors' in file_name or 'scale-factors' in file_name:
            scalefactors = np.loadtxt(path_file_name, encoding='utf-8', dtype=np.float32)
            self['index'] = np.arange(scalefactors.size, dtype=np.int32)
            self['scalefactor'] = scalefactors
            self['redshift'] = 1 / self['scalefactor'] - 1

    def assign_cosmology(self, Cosmology=None):
        '''
        Generate and assign to self times from scale-factors, given input Cosmology.

        Parameters
        ----------
        Cosmology : cosmology class
            to generate times corresponding to scale-factors
        '''
        self['cosmology'] = Cosmology.source
        self['time'] = Cosmology.get_time(self['scalefactor'], 'scalefactor')  # [Gyr]
        self['time.lookback'] = np.max(self['time']) - self['time']
        self['time.width'] = np.zeros(self['time'].size)
        self['time.width'][1:] = (self['time'][1:] - self['time'][:-1]) * 1000  # [Myr]

    def print_snapshots(
        self,
        write_file=False,
        print_times=False,
        file_name='snapshot_times.txt',
        directory='.',
        subsample_factor=0,
        redshift_max=None,
    ):
        '''
        Print snapshot time information from self to screen or file.

        Parameters
        ----------
        write_file : bool
            whether to write to file
        print_times : bool
            whether to print scale-factor + redshfit + time + time width
        file_name : str
            name for snapshot file
        directory : str
            directory for snapshot file
        subsample_factor : int
            factor by which to subsample snapshot times
        '''
        file_out = None
        if write_file:
            path_file_name = io.get_path(directory) + file_name
            file_out = open(path_file_name, 'w', encoding='utf-8')

        Write = io.WriteClass(file_out)

        snapshot_indices = np.array(self['index'])

        if subsample_factor > 1:
            # sort backwards in time to ensure get snapshot at z = 0
            snapshot_indices = snapshot_indices[::-1]
            snapshot_indices = snapshot_indices[::subsample_factor]
            snapshot_indices = snapshot_indices[::-1]

        if redshift_max:
            snapshot_indices = snapshot_indices[self['redshift'][snapshot_indices] <= redshift_max]

        if print_times:
            Write.write('# {} snapshots'.format(self['scalefactor'].size))
            if self['scalefactor.spacing'] is not None:
                Write.write('# {} spacing in scale-factor'.format(self['scalefactor.spacing']))
            if subsample_factor > 1:
                Write.write('# subsampling every {} snapshots'.format(subsample_factor))
            Write.write('# times assume cosmology from {}'.format(self['cosmology']))
            Write.write('# i scale-factor redshift time[Gyr] lookback-time[Gyr] time-width[Myr]')

            for snap_i in snapshot_indices:
                if 'time' in self:
                    Write.write(
                        '{:3d} {:11.9f} {:12.9f} {:12.9f} {:12.9f} {:8.4f}'.format(
                            snap_i,
                            self['scalefactor'][snap_i],
                            self['redshift'][snap_i],
                            self['time'][snap_i],
                            self['time.lookback'][snap_i],
                            self['time.width'][snap_i],
                        )
                    )
                else:
                    Write.write(
                        '{:3d} {:11.9f} {:12.9f}'.format(
                            snap_i, self['scalefactor'][snap_i], self['redshift'][snap_i]
                        )
                    )
        else:
            for snap_i in snapshot_indices:
                Write.write('{:11.9f}'.format(self['scalefactor'][snap_i]))

        if file_out is not None:
            file_out.close()


def read_snapshot_times(directory='.', verbose=True, error_if_no_file=True):
    '''
    Within imput directory, search for and read snapshot file,
    that contains scale-factors[, redshifts, times, look-back times, time spacings].
    Return as dictionary.

    Parameters
    ----------
    directory : str
        directory that contains file that contains list of snapshots
    verbose : bool
        verbosity flat to store in Snapshot dictionary class
    error_if_no_file : bool
        raise error if can not find snapshot file, else return None

    Returns
    -------
    Snapshot : dictionary class
        snapshot information
    '''
    Snapshot = SnapshotClass(verbose=verbose)

    try:
        try:
            Snapshot.read_snapshots('snapshot_times.txt', directory)
        except OSError:
            try:
                Snapshot.read_snapshots('snapshot_scalefactors.txt', directory)
            except OSError:
                Snapshot.read_snapshots('snapshot_scale-factors.txt', directory)
    except OSError as exc:
        message = f'cannot find file of snapshot times in {directory}'
        if error_if_no_file:
            raise OSError(message) from exc
        else:
            print(message)
            Snapshot = None

    return Snapshot


# --------------------------------------------------------------------------------------------------
# particle/cell properties
# --------------------------------------------------------------------------------------------------
def plot_kernel(
    kernel_name='cubic',
    function_names=['density', 'mass', 'acceleration', 'potential/newtonian'],
    distance_limits=[0, 1],
    distance_bin_width=0.001,
    file_name=None,
    directory='.',
    figure_index=1,
):
    '''
    .
    '''
    from matplotlib import pyplot as plt

    distances = np.arange(
        distance_bin_width, max(distance_limits) + distance_bin_width, distance_bin_width
    )

    kernel_values = np.zeros((len(function_names), distances.size))
    for f_i, function_name in enumerate(function_names):
        if '/newtonian' in function_name:
            function_name = function_name.replace('/newtonian', '')
            ratio_newtonian = True
        else:
            ratio_newtonian = False

        for d_i, distance in enumerate(distances):
            kernel_values[f_i, d_i] = particle.get_kernel(
                kernel_name, function_name, distance, ratio_newtonian=ratio_newtonian
            )

        if function_name == 'potential':
            kernel_values[f_i] -= kernel_values[f_i].min()
        kernel_values[f_i] /= kernel_values[f_i].max()

    # plot ----------
    _fig, subplot = plot.make_figure(figure_index)

    plot.set_axes_scaling_limits(subplot, False, distance_limits, None, False, [0, 1])

    subplot.set_ylabel('kernel')
    subplot.set_xlabel('$r/H_{\\rm kernel}$')

    for f_i, function_name in enumerate(function_names):
        label = function_name
        if label == 'mass':
            label += ' ($= a / a_{{\\rm newt}}$)'
        subplot.plot(distances, kernel_values[f_i], alpha=0.8, label=label)

    plot.make_legends(subplot, 'best')

    plt.arrow(1 / 2.8, 0, 0, 0.1, alpha=0.5)

    plt.arrow(1 / 2, 0, 0, 0.05, alpha=0.5)

    if file_name is True or file_name == '':
        file_name = f'kernel.{kernel_name}_v_distance'
    plot.parse_output(file_name, directory)


class ParticlePropertyClass(io.SayClass):
    '''
    Calculate properties (such as mass, size) of particles and cells in a simulation of given size,
    number of particles, and cosmology.
    '''

    def __init__(self, Cosmology):
        '''
        Store variables from cosmology class and spline for converting between virial density
        definitions.

        Parameters
        ----------
        Cosmology : class
            cosmology information
        '''
        self.Cosmology = Cosmology

    def get_particle_mass(self, simulation_length, number_per_dimension, particle_name='combined'):
        '''
        Get particle mass [M_sun] for given cosmology.

        Parameters
        ----------
        simulation_length : float
            box length [kpc comoving]
        number_per_dimension : int
            number of particles per dimension
        particle_name : str
            'combined' = dark + gas (for n-body only), 'dark', 'gas'

        Returns
        -------
        mass : float
            [M_sun]
        '''
        mass = (
            constant.density_critical_0
            * self.Cosmology['hubble'] ** 2
            * self.Cosmology['omega_matter']
            * (simulation_length / number_per_dimension) ** 3
        )

        if particle_name == 'combined':
            pass
        elif particle_name == 'dark':
            mass *= 1 - self.Cosmology['omega_baryon'] / self.Cosmology['omega_matter']
        elif particle_name == 'gas':
            mass *= self.Cosmology['omega_baryon'] / self.Cosmology['omega_matter']
        else:
            raise ValueError(f'not recognize particle_name = {particle_name}')

        return mass

    def get_cell_length(
        self,
        simulation_length=25000 / 0.7,
        grid_root_number=7,
        grid_refine_number=8,
        redshift=None,
        units='kpc comoving',
    ):
        '''
        Get length of grid cell at refinement level,
        in units [comoving or physical] corresponding to simulation_length.

        Parameters
        ----------
        simulation_length : float
            box length [kpc comoving]
        grid_root_number : int
            number of root grid refinement levels
        grid_refine_number : int
            number of adaptive refinement levels
        redshift : float
        units : str
            'kpc[/h]', 'pc/h', 'cm' + 'comoving' or 'physical'

        Returns
        -------
        length : float
            size of cell
        '''
        length = simulation_length / 2 ** (grid_root_number + grid_refine_number)
        if units[:3] == 'kpc':
            pass
        elif units[:2] == 'pc':
            length *= constant.kilo
        elif units[:2] == 'cm':
            length *= constant.cm_per_kpc
        else:
            raise ValueError(f'not recognize units = {units}')

        if '/h' in units:
            length *= self.Cosmology['hubble']

        if 'physical' in units:
            if redshift is None:
                raise ValueError('need to input redshift to scale to physical length')
            else:
                length /= 1 + redshift
        elif 'comoving' in units:
            pass
        else:
            raise ValueError(f'need to specify comoving or physical in units = {units}')

        return length

    def get_gas_mass_per_cell(
        self,
        number_density,
        simulation_length=25000 / 0.7,
        grid_root_number=7,
        grid_refine_number=8,
        redshift=0,
        units='M_sun',
    ):
        '''
        Get mass in cell of given size at given number density.

        Parameters
        ----------
        number_density : float
            hydrogen number density [cm^-3 physical]
        simulation_length : float
            box length [kpc comoving]
        grid_root_number : int
            number of root grid refinement levels
        grid_refine_number : int
            number of adaptive refinement levels
        redshift : float
        units : str
            mass units: g, M_sun, M_sun/h

        Returns
        -------
        mass : float
            mass of cell
        '''
        cell_length = self.get_cell_length(
            simulation_length, grid_root_number, grid_refine_number, redshift, 'cm physical'
        )
        mass = constant.proton_mass * number_density * cell_length**3

        if 'g' in units:
            pass
        elif 'M_sun' in units:
            mass /= constant.sun_mass
        else:
            raise ValueError(f'not recognize units = {units}')

        if '/h' in units[-2:]:
            mass *= self.Cosmology['hubble']

        return mass
