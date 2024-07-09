'''
Utility functions for math and function fitting.

@author: Andrew Wetzel <arwetzel@gmail.com>
'''

import numpy as np
from scipy import integrate, interpolate, ndimage, special, stats

from . import array, binning, constant, io


# --------------------------------------------------------------------------------------------------
# math utility
# --------------------------------------------------------------------------------------------------
def get_log(values):
    '''
    Safely get log of values.
    Values = 0 is ok, but print warning if values < 0.

    Parameters
    ----------
    values : array

    Returns
    -------
    values : array
    '''
    if np.isscalar(values):
        if values <= 0:
            values = -np.Inf
        else:
            values = np.log10(values)
    else:
        if not isinstance(values, np.ndarray):
            values = np.array(values, np.float32)
        else:
            values = 1.0 * np.array(values)

        if np.min(values) < 0:
            print(
                '! input value minimum = {:.3f} < 0, cannot take log, setting to -Inf!'.format(
                    np.min(values)
                )
            )

        masks_negative = values <= 0

        if np.sum(masks_negative):
            values[masks_negative] = -np.Inf

        masks_positive = values > 0

        values[masks_positive] = np.log10(values[masks_positive])

    return values


def percentile_weighted(values, percentiles, weights=None, axis=None):
    '''
    Compute weighted percentiles.
    If weights are equal, this is the same as normal percentiles.
    Elements of the C{data} and C{weights} arrays correspond to each other and must have
    equal length (unless C{weights} is C{None}).

    Parameters
    ----------
    values : array (1-D)
    percentiles : float or array
        percentiles to get corresponding values of [0, 100]
    weights : array
        weight to give to each value. if none, weight all equally
    axis : bool
        which axis to compute statistics along

    Returns
    -------
    values_at_percents : array
        value[s] at each input percentile[s]
    '''
    if weights is None:
        return np.percentile(values, percentiles, axis)

    values = np.array(values, dtype=np.float64)
    assert len(values.shape) == 1

    value_number = values.shape[0]
    assert value_number > 0

    if value_number == 1:
        return values[0]

    assert np.min(percentiles) >= 0, 'input percentiles < 0'
    assert np.max(percentiles) <= 100, 'input percentiles > 100'
    if np.isscalar(percentiles):
        percentiles = [percentiles]
    percentiles = np.asarray(percentiles)
    fractions = 0.01 * percentiles

    weights = np.asarray(weights, dtype=np.float64)

    assert np.min(weights) >= 0, 'input weights < 0'
    assert weights.shape == values.shape

    indices = np.argsort(values)
    values_sorted = np.take(values, indices, axis=0)
    weights_sorted = np.take(weights, indices, axis=0)
    weights_cumsum = np.cumsum(weights_sorted)
    if not weights_cumsum[-1] > 0:
        raise ValueError('nonpositive weight sum')

    # normalize like np.percentile
    weight_fractions = (weights_cumsum - weights_sorted) / (weights_cumsum[-1] - weights_cumsum[0])
    indices = np.digitize(fractions, weight_fractions) - 1

    values_at_percents = []
    for ii, frac in zip(indices, fractions):
        if ii == value_number - 1:
            values_at_percents.append(values_sorted[-1])
        else:
            weight_dif = weight_fractions[ii + 1] - weight_fractions[ii]
            f1 = (frac - weight_fractions[ii]) / weight_dif
            f2 = (weight_fractions[ii + 1] - frac) / weight_dif
            assert f1 >= 0 and f2 >= 0 and f1 <= 1 and f2 <= 1
            assert abs(f1 + f2 - 1.0) < 1e-6
            values_at_percents.append(values_sorted[ii + 1] * f1 + values_sorted[ii] * f2)

    if len(values_at_percents) == 1:
        values_at_percents = values_at_percents[0]

    return values_at_percents


def sample_random_reject(func, params, x_limits, y_max, size):
    '''
    Use rejection method to sample distribution and return as array, assuming minimum of func is 0.

    Parameters
    ----------
    func : function
    params : list
        function's parameters
    x_limits : list
        min and max limits for function's x-range
    y_max : list
        min and max limits for function's y-range
    size : int
        number of values to sample

    Returns
    -------
    xs_rand : array
        sampled distribution
    '''
    xs_rand = np.random.uniform(x_limits[0], x_limits[1], size)
    ys_rand = np.random.uniform(0, y_max, size)
    ys = func(xs_rand, params)
    xs_rand = xs_rand[ys_rand < ys]
    x_number = xs_rand.size
    if x_number < size:
        xs_rand = np.append(
            xs_rand, sample_random_reject(func, params, x_limits, y_max, size - x_number)
        )

    return xs_rand


def deconvolve(ys_conv, scatter, x_width, iter_number=10):
    '''
    Get Gaussian-deconvolved values via Lucy routine.

    Parameters
    ----------
    ys_conv : array
        y-values that already are convolved with gaussian
    scatter : float
        gaussian scatter
    x_width : float
        bin width
    iter_number : int
        number of iterations to do

    Returns
    -------
    y_it : array
        deconvolved y values
    '''
    y_it = ys_conv
    for _ in range(iter_number):
        ratio = ys_conv / ndimage.filters.gaussian_filter1d(y_it, scatter / x_width)
        y_it = y_it * ndimage.filters.gaussian_filter1d(ratio, scatter / x_width)
        # this is part of lucy's routine, but seems less stable
        # y_it = y_it * ratio

    return y_it


def convert_luminosity(kind, luminosities):
    '''
    Convert luminosity to magnitude, or vice-versa.

    Parameters
    ----------
    kind : str
        luminosity kind: 'luminosity', 'mag.r'
    luminosities : array
        value[s] (if luminosity, in Solar luminosity)

    Returns
    -------
    values : array
        luminosity[s] or magnitude[s]
    '''
    assert kind in ['luminosity', 'mag.r']

    if kind == 'luminosity':
        values = constant.sun_magnitude - 2.5 * np.log10(luminosities)
    elif kind == 'mag.r':
        if np.min(luminosities) > 0:
            luminosities = -luminosities
        values = 10 ** ((constant.sun_magnitude - luminosities) / 2.5)

    return values


# --------------------------------------------------------------------------------------------------
# fraction
# --------------------------------------------------------------------------------------------------
class FractionClass(dict, io.SayClass):
    '''
    Compute fraction safely, convert from fraction to ratio, store fractions in self dictionary.
    '''

    def __init__(self, array_shape=None, uncertainty_kind=None):
        '''
        Initialize dictionary to store fraction values and uncertainties.

        Parameters
        ----------
        array_shape : int or list
            shape of array to store fractions
        uncertainty_kind : str
            uncertainty kind for fraction: None, 'normal', 'beta'
        '''
        self.uncertainty_kind = uncertainty_kind

        if array_shape is not None:
            array_shape = array.arrayize(array_shape)
            if uncertainty_kind:
                if uncertainty_kind == 'normal':
                    self['error'] = np.zeros(array_shape)
                elif uncertainty_kind == 'beta':
                    self['error'] = np.zeros(np.append(array_shape, 2))
                else:
                    raise ValueError(f'not recognize uncertainty kind: {uncertainty_kind}')
            else:
                self.say('! not calculating uncertainty for fraction')

            self['value'] = np.zeros(array_shape)
            self['numer'] = np.zeros(array_shape)
            self['denom'] = np.zeros(array_shape)

    def get_fraction(self, numers, denoms, uncertainty_kind=None):
        '''
        Get numers/denoms [and uncertainty if uncertainty kind defined].
        Assume numers < denoms, and that numers = 0 if denoms = 0.

        Parameters
        ----------
        numers : float or array
            subset count[s]
        denoms : float or array
            total count[s]
        uncertainty_kind : str
            uncertainty kind: None, 'normal', 'beta'

        Returns
        -------
        frac_values : float or array
        [frac_errors : float or array]
        '''
        if not uncertainty_kind:
            uncertainty_kind = self.uncertainty_kind

        if np.isscalar(numers):
            if numers == 0 and denoms == 0:
                # avoid dividing by 0
                if not uncertainty_kind:
                    return 0.0
                elif uncertainty_kind == 'normal':
                    return 0.0, 0.0
                elif uncertainty_kind == 'beta':
                    return 0.0, np.array([0.0, 0.0])
                else:
                    raise ValueError(f'not recognize uncertainty kind = {uncertainty_kind}')
            elif denoms == 0:
                raise ValueError('numers != 0, but denoms = 0')
        else:
            numers = np.array(numers)
            denoms = np.array(denoms).clip(1e-20)

        frac_values = numers / denoms

        if uncertainty_kind:
            if uncertainty_kind == 'normal':
                frac_errors = ((numers / denoms * (1 - numers / denoms)) / denoms) ** 0.5
            elif uncertainty_kind == 'beta':
                # Cameron 2011
                conf_inter = 0.683  # 1 - sigma
                p_lo = numers / denoms - stats.distributions.beta.ppf(
                    0.5 * (1 - conf_inter), numers + 1, denoms - numers + 1
                )
                p_hi = (
                    stats.distributions.beta.ppf(
                        1 - 0.5 * (1 - conf_inter), numers + 1, denoms - numers + 1
                    )
                    - numers / denoms
                )
                frac_errors = np.array([p_lo, p_hi]).clip(0)
            else:
                raise ValueError(f'not recognize uncertainty kind = {uncertainty_kind}')

            return frac_values, frac_errors
        else:
            return frac_values

    def get_fraction_from_ratio(self, ratio):
        '''
        Get fraction relative to total: x / (x + y).

        Parameters
        ----------
        ratio : float or array
            x / y

        Returns
        -------
        float or array
            fraction
        '''
        return 1 / (1 + 1 / ratio)

    def get_ratio_from_fraction(self, frac):
        '''
        Get ratio: x / y.

        Parameters
        ----------
        frac : float or array
            fraction of total x / (x + y)

        Returns
        -------
        float or array
            ratio
        '''
        return frac / (1 - frac)

    def assign_to_dict(self, indices, numer, denom):
        '''
        Assign fraction to self dictionary.

        Parameters
        ----------
        indices : array
            index[s] to assign to in self dictionary
        numer : int
            subset count[s]
        denom : int
            total count[s]
        '''
        if np.ndim(indices):
            indices = tuple(indices)
        self['value'][indices], self['error'][indices] = self.get_fraction(
            numer, denom, self.uncertainty_kind
        )
        self['numer'][indices] = numer
        self['denom'][indices] = denom


Fraction = FractionClass()


# --------------------------------------------------------------------------------------------------
# statistics
# --------------------------------------------------------------------------------------------------
class StatisticClass(io.SayClass):
    '''
    Store statistics and probability distribution of input array.
    '''

    def __init__(
        self,
        values=None,
        limits=None,
        bin_width=None,
        bin_number=10,
        log_scale=False,
        weights=None,
        values_possible=None,
    ):
        '''
        Parameters
        ----------
        values : array
        limits : list
            min and max limits to impose
        bin_width : float
            width of each bin
        bin_number : int
            number of bins
        log_scale : bool
            whether to use logarithmic scaling
        weights : array
            weight for each value
        values_possible : array
            all possible input values
            use to map input values to int value, to then bin by intrinsic scaling in values
            if defined, this overrides bin_number
            for example, if values correspond to redshifts of simulation snapshots,
            input every possible snapshot redshift to bin according to that width
        '''
        self.stat = {}
        self.distr = {}

        if values is not None and len(values) > 0:
            self.stat = self.get_statistic_dict(values, limits, weights)
            self.distr = self.get_distribution_dict(
                values,
                limits,
                bin_width,
                bin_number,
                log_scale,
                weights,
                values_possible,
            )

    def parse_limits(self, values, limits=None):
        '''
        Get limits, either as input or from input values.
        Impose sanity checks.

        Parameters
        ----------
        values : array
            value[s]
        limits : list
            *linear* min and max limits to impose
        '''
        limit_buffer = 1e-6

        if limits is None or len(limits) == 0 or limits[0] is None or limits[1] is None:
            limits_values = array.get_limits(values)
            if limits is None or len(limits) == 0:
                limits = [None, None]
            if limits[0] is None:
                limits[0] = limits_values[0]
            if limits[1] is None:
                limits[1] = limits_values[1]
                limits[1] *= 1 + limit_buffer  # make sure single value remains valid
                limits[1] += limit_buffer

        if limits[0] == limits[1] or isinstance(limits[1], int):
            limits[1] *= 1 + limit_buffer  # make sure single value remains valid
            limits[1] += limit_buffer

        return limits

    def get_statistic_dict(self, values, limits=[-np.Inf, np.Inf], weights=None):
        '''
        Get dicionary of statistics within limits.

        Parameters
        ----------
        values : array
            values to get statistics of
        limits : list
            min and max limits to impose
        weights : array
            weight for each value
        '''
        stat = {
            'limits': [np.nan, np.nan],  # impose limits or limits of input values
            'number': 0,  # number of values
            # values at confidence
            'median': np.nan,
            'percent.16': np.nan,
            'percent.84': np.nan,
            'percent.2': np.nan,
            'percent.98': np.nan,
            'percent.0.1': np.nan,
            'percent.99.9': np.nan,
            'percent.25': np.nan,
            'percent.75': np.nan,
            'percents.68': [np.nan, np.nan],
            'percents.95': [np.nan, np.nan],
            'median.dif.2': np.nan,
            'median.dif.16': np.nan,
            'median.dif.84': np.nan,
            'median.dif.98': np.nan,
            'median.difs.68': [np.nan, np.nan],
            'median.difs.95': [np.nan, np.nan],
            'average': np.nan,
            'std': np.nan,
            'sem': np.nan,  # average, std dev, std dev of mean
            'std.lo': np.nan,
            'std.hi': np.nan,  # values of std limits
            'min': np.nan,
            'max': np.nan,  # minimum and maximum
        }

        if values is None or len(values) == 0:
            return stat

        values = np.array(values)

        limits = self.parse_limits(values, limits)

        masks = array.get_indices(values, limits)
        if masks.size < values.size:
            values = values[masks]
            if weights is not None:
                weights = weights[masks]

        if not values.size:
            self.say(
                '! no values are within bin limit: [{:.3f}, {:.3f}]'.format(
                    min(limits), max(limits)
                )
            )
            return stat

        # scalar statistics
        stat['limits'] = limits
        stat['number'] = values.size
        if weights is None or len(weights) == 0:
            stat['median'] = np.median(values)
            stat['percent.50'] = np.median(values)
            stat['percent.16'] = np.percentile(values, 16)
            stat['percent.84'] = np.percentile(values, 84)
            stat['percent.2'] = np.percentile(values, 2.275)
            stat['percent.98'] = np.percentile(values, 97.725)
            stat['percent.0.1'] = np.percentile(values, 0.135)
            stat['percent.99.9'] = np.percentile(values, 99.865)
            stat['percent.25'] = np.percentile(values, 25)
            stat['percent.75'] = np.percentile(values, 75)
        else:
            stat['median'] = percentile_weighted(values, 50, weights)
            stat['percent.50'] = percentile_weighted(values, 50, weights)
            stat['percent.16'] = percentile_weighted(values, 16, weights)
            stat['percent.84'] = percentile_weighted(values, 84, weights)
            stat['percent.2'] = percentile_weighted(values, 2.275, weights)
            stat['percent.98'] = percentile_weighted(values, 97.725, weights)
            stat['percent.0.1'] = percentile_weighted(values, 0.135, weights)
            stat['percent.99.9'] = percentile_weighted(values, 99.865, weights)
            stat['percent.25'] = percentile_weighted(values, 25, weights)
            stat['percent.75'] = percentile_weighted(values, 75, weights)

        stat['percents.68'] = [stat['percent.16'], stat['percent.84']]
        stat['percents.95'] = [stat['percent.2'], stat['percent.98']]

        stat['median.dif.2'] = stat['median'] - stat['percent.2']
        stat['median.dif.16'] = stat['median'] - stat['percent.16']
        stat['median.dif.84'] = stat['percent.84'] - stat['median']
        stat['median.dif.98'] = stat['percent.98'] - stat['median']
        stat['median.difs.68'] = [stat['median.dif.16'], stat['median.dif.84']]
        stat['median.difs.95'] = [stat['median.dif.2'], stat['median.dif.98']]
        stat['width.68'] = (stat['median.dif.16'] + stat['median.dif.84']) / 2
        stat['width.95'] = (stat['median.dif.2'] + stat['median.dif.98']) / 2

        if weights is None or len(weights) == 0:
            stat['average'] = np.mean(values)
            stat['average.50'] = np.mean(
                values[(values > stat['percent.25']) * (values < stat['percent.75'])]
            )
            stat['std'] = np.std(values, ddof=1)
            stat['sem'] = stats.sem(values)
        else:
            stat['average'] = np.sum(values * weights) / np.sum(weights)
            masks = (values > stat['percent.25']) * (values < stat['percent.75'])
            stat['average.50'] = np.sum(values[masks] * weights[masks]) / np.sum(weights[masks])
            stat['std'] = np.sqrt(
                np.sum(weights / np.sum(weights) * (values - stat['average']) ** 2)
            )
            stat['sem'] = stat['std'] / np.sqrt(values.size)
        stat['std.lo'] = stat['average'] - stat['std']
        stat['std.hi'] = stat['average'] + stat['std']
        stat['sem.lo'] = stat['average'] - stat['sem']
        stat['sem.hi'] = stat['average'] + stat['sem']
        stat['min'] = values.min()
        stat['max'] = values.max()

        # make sure array has more than one value
        # if stat['max'] != stat['min']:
        #    vals_sort = np.unique(values)
        #    if vals_sort.size > 2:
        #        stat['min.2'] = vals_sort[1]
        #        stat['max.2'] = vals_sort[-2]
        #    if vals_sort.size > 4:
        #        stat['min.3'] = vals_sort[2]
        #        stat['max.3'] = vals_sort[-3]

        return stat

    def get_distribution_dict(
        self,
        values,
        limits=None,
        bin_width=None,
        bin_number=0,
        log_scale=False,
        weights=None,
        values_possible=None,
    ):
        '''
        Get dicionary for histogram/probability distribution.

        Parameters
        ----------
        values : array
            value[s]
        limits : list
            *linear* max and min limits to impose
        bin_width : float
            width of each bin
        bin_number : int
            number of bins
        log_scale : bool
            whether to use logarithmic scaling
        weights : array
            weight for each value
        values_possible : array
            all possible input values
            use to map input values to int value, to then bin by intrinsic scaling in values
            if defined, this overrides bin_number
            for example, if values correspond to redshifts of simulation snapshots,
            input every possible snapshot redshift to bin according to that width
        '''
        distr = {
            'limits': np.array([]),
            'bin.min': np.array([]),
            'bin.mid': np.array([]),
            'bin.max': np.array([]),
            'bin.width': np.array([]),
            'probability': np.array([]),
            'probability.err': np.array([]),
            'probability.cum': np.array([]),
            'probability.norm': np.array([]),
            'probability.norm.err': np.array([]),
            'histogram': np.array([]),
            'histogram.cum': np.array([]),
            'histogram.err': np.array([]),
        }

        if values is None or len(values) == 0:
            return distr

        assert (
            values_possible is not None
            or (bin_number is not None and bin_number > 0)
            or (bin_width is not None and bin_width > 0)
        )

        values = np.array(values, dtype=np.float64)
        limits = self.parse_limits(values, limits)

        val_indices = array.get_indices(values, limits)
        if not val_indices.size:
            self.say('! no values within bin limits = {}'.format(distr['limits']))
            return distr
        values_in_limits = values[val_indices]

        if weights is not None:
            weights_in_limits = weights[val_indices]
            # divide by mean not median because median can be 0
            weights_in_limits /= np.mean(weights_in_limits)
        else:
            weights_in_limits = None

        if values_possible is None:
            # fixed bin width
            Bin = binning.BinClass(limits, bin_width, bin_number, False, log_scale, values=values)

            distr['histogram'] = Bin.get_histogram(
                values_in_limits, weights_in_limits, density=False
            )
            distr['probability'] = Bin.get_histogram(
                values_in_limits, weights_in_limits, density=True
            )

            distr['bin.min'] = Bin.mins
            distr['bin.mid'] = Bin.mids
            distr['bin.max'] = Bin.maxs
        else:
            # variable bin width
            self.say('using spacing of input values_possible to set bin widths')

            values_possible = np.unique(values_possible)

            if log_scale:
                values_in_limits = get_log(values_in_limits)
                if values_possible is not None:
                    values_possible = get_log(values_possible)

            vals_possible_width = np.abs(values_possible[:-1] - values_possible[1:])
            value_bin_indices = binning.get_bin_indices(
                values_in_limits, values_possible, values_possible.max(), 'down'
            )
            val_bin_limits = [0, value_bin_indices.max() + 2]
            val_bin_range = np.arange(val_bin_limits[0], val_bin_limits[1], dtype=np.int64)
            values_possible = values_possible[val_bin_range]
            vals_possible_width = vals_possible_width[val_bin_range]

            if log_scale:
                distr['bin.min'] = 10**values_possible
                distr['bin.mid'] = 10 ** (values_possible + 0.5 * vals_possible_width)
                distr['bin.max'] = 10 ** (values_possible + vals_possible_width)
            else:
                distr['bin.min'] = values_possible
                distr['bin.mid'] = values_possible + 0.5 * vals_possible_width
                distr['bin.max'] = values_possible + vals_possible_width

            distr['histogram'] = np.histogram(
                value_bin_indices,
                values_possible.size,
                val_bin_limits,
                weights=weights_in_limits,
                density=False,
            )[0]

            if weights is not None:
                distr['probability'] = (
                    distr['histogram'] / np.sum(weights_in_limits) / vals_possible_width
                )
            else:
                distr['probability'] = (
                    distr['histogram'] / values_in_limits.size / vals_possible_width
                )

        distr['limits'] = limits
        distr['bin.width'] = distr['bin.max'] - distr['bin.min']

        below_limit_number = np.sum(values < limits[0])

        # for cumulative stats, include all values, including those below and above input limits
        distr['histogram.cum'] = np.cumsum(distr['histogram']) + below_limit_number
        distr['histogram.err'] = distr['histogram'] ** 0.5
        if weights is not None:
            distr['probability.cum'] = distr['histogram.cum'] / np.sum(weights)
        else:
            distr['probability.cum'] = distr['histogram.cum'] / values.size
        distr['probability.err'] = Fraction.get_fraction(
            distr['probability'], distr['histogram.err']
        )

        # get 'normalized' probability, so max prob = 1
        distr['probability.norm'] = distr['probability'] / distr['probability'].max()
        distr['probability.norm.err'] = distr['probability.err'] / distr['probability'].max()

        for prop_name in list(distr):
            if '.err' not in prop_name and np.min(distr[prop_name]) > 0:
                distr['log ' + prop_name] = get_log(distr[prop_name])

        return distr

    def append_to_dictionary(
        self,
        values,
        limits=None,
        bin_width=None,
        bin_number=0,
        log_scale=False,
        weights=None,
        values_possible=None,
    ):
        '''
        Make dictionaries for statistics and histogram/probability distribution, append to self.

        Parameters
        ----------
        values : array
            value[s]
        limits : list
            *linear* min and max limits to impose
        bin_width : float
            width of each bin
        bin_number : int
            number of bins
        log_scale : bool
            whether to use logarithmic scaling
        weights : array
            weight for each value
        values_possible : array
            all possible input values
            use to map input values to int value, to then bin by intrinsic scaling in values
            if defined, this overrides bin_number
            for example, if values correspond to redshifts of simulation snapshots,
            input every possible snapshot redshift to bin according to that width
        '''
        # check if need to array-ize dictionaries
        if (
            self.distr
            and self.distr['probability']
            and len(self.distr['probability']) > 0
            and np.isscalar(self.distr['probability'][0])
        ):
            for k in self.stat:
                self.stat[k] = [self.stat[k]]
            for k in self.distr:
                self.distr[k] = [self.distr[k]]

        stat_new = self.get_statistic_dict(values, limits, weights)
        array.append_dictionary(self.stat, stat_new)

        if limits is not None and len(limits) and (bin_width > 0 or bin_number > 0):
            distr_new = self.get_distribution_dict(
                values,
                limits,
                bin_width,
                bin_number,
                log_scale,
                weights,
                values_possible,
            )
            array.append_dictionary(self.distr, distr_new)

    def append_class_to_dictionary(self, StatIn):
        '''
        Append statistics class dictionaries to self.

        Parameters
        ----------
        StatIn : class
            another statistic/distribution class
        '''
        array.append_dictionary(self.stat, StatIn.stat)
        array.append_dictionary(self.distr, StatIn.distr)

    def arrayize(self):
        '''
        Convert dicionary lists to arrays.
        '''
        self.stat = array.arrayize(self.stat)
        self.distr = array.arrayize(self.distr)

    def print_statistics(self, bin_index=None):
        '''
        Print statistics in self.

        Parameters
        ----------
        bin_index : int
            bin index to print statistic of
        '''
        stat_list = [
            'min',
            'max',
            'median',
            'average',
            'std',
            'width.68',
            'width.95',
            'percent.0.1',
            'percent.2',
            'percent.16',
            'percent.50',
            'percent.84',
            'percent.98',
            'percent.99.9',
        ]
        # , 'min.2', 'min.3', 'max.2', 'max.3']

        if bin_index is None and not np.isscalar(self.stat['median']):
            raise ValueError('no input index, but stat is multi-dimensional')

        if bin_index is not None:
            value = self.stat['number'][bin_index]
        else:
            value = self.stat['number']

        self.say(f'number = {value}\n')

        for k in stat_list:
            if bin_index is not None:
                value = self.stat[k][bin_index]
            else:
                value = self.stat[k]
            self.say('{} = {}'.format(k, io.get_string_from_numbers(value, 3)))
            if k in ['max', 'average', 'width.95']:
                self.say('')


def print_statistics(values, weights=None, plot=False):
    '''
    For input array, print statistics (and plot histogram).

    Parameters
    ----------
    values : array
        value[s]
    weights : array
        weight for each value
    plot : bool
        whether to plot histogram
    '''
    values = np.array(values)
    if np.ndim(values) > 1:
        values = np.concatenate(values)

    Stat = StatisticClass(values, weights=weights)
    Stat.print_statistics()

    if 0 in values:
        print('  contains 0')
        masks = values > 0
        if max(masks):
            print('  minimum value > 0 = {:.4f}'.format(np.min(values[masks])))

    if -np.Inf in values:
        print('  contains -Inf')
        print('  minimum value > -Inf = {:.4f}'.format(np.min(values[values > -np.Inf])))

    if np.Inf in values:
        print('  contains Inf')
        print('  maximum value < Inf = {:.4f}'.format(np.min(values[values < np.Inf])))

    if plot:
        from matplotlib import pyplot as plt

        bin_number = np.int(np.clip(values.size / 10, 0, 1000))
        plt.hist(values, bins=bin_number)


# --------------------------------------------------------------------------------------------------
# spline fitting
# --------------------------------------------------------------------------------------------------
class SplineFunctionClass(io.SayClass):
    '''
    Fit spline [and its inverse] to input function.
    '''

    def __init__(
        self, func, x_limits=[0, 1], number=100, dtype=np.float64, make_inverse=True, **kwargs
    ):
        '''
        Fit f(x) to spline, and fit x(f) if f is monotonic.

        Parameters
        ----------
        func
            function f(x)
        x_limits : list
            min and max limits on x
        number : int
            number of spline points
        dtype
            data type to store
        make_inverse : bool
            whether to make inverse spline, x(f)
        kwargs
            keyword arguments for func
        '''
        self.dtype = dtype
        self.xs = np.linspace(min(x_limits), max(x_limits), number).astype(dtype)

        self.fs = np.zeros(number, dtype)
        for x_i, x in enumerate(self.xs):
            self.fs[x_i] = func(x, **kwargs)

        self.spline_f_from_x = interpolate.splrep(self.xs, self.fs)

        if make_inverse:
            self.make_spline_inverse()

    def make_spline_inverse(self):
        '''
        Make inverse spline, x(f).
        '''
        xs_temp = self.xs
        fs_temp = self.fs
        if fs_temp[1] < fs_temp[0]:
            fs_temp = fs_temp[::-1]
            xs_temp = xs_temp[::-1]
        fis = array.get_arange(fs_temp.size - 1)

        if (fs_temp[fis] < fs_temp[fis + 1]).min():
            self.spline_x_from_f = interpolate.splrep(fs_temp, xs_temp)
        else:
            self.say('! unable to make inverse spline: function values not monotonic')

    # wrappers for spline evaluation, ext=2 raises ValueError if input x in outside of limits
    def value(self, x, ext=2):
        '''
        .
        '''
        return interpolate.splev(x, self.spline_f_from_x, ext=ext).astype(self.dtype)

    def derivative(self, x, ext=2):
        '''
        .
        '''
        return interpolate.splev(x, self.spline_f_from_x, der=1, ext=ext).astype(self.dtype)

    def value_inverse(self, f, ext=2):
        '''
        .
        '''
        return interpolate.splev(f, self.spline_x_from_f, ext=ext).astype(self.dtype)

    def derivative_inverse(self, f, ext=2):
        '''
        .
        '''
        return interpolate.splev(f, self.spline_x_from_f, der=1, ext=ext).astype(self.dtype)


class SplinePointClass(SplineFunctionClass):
    '''
    Fit spline [and its inverse] to input points.
    '''

    def __init__(self, x_values, f_values, dtype=np.float64, make_inverse=True):
        '''
        Fit f(x) to spline, and fit x(f) if f is monotonic.
        Store to self.

        Parameters
        ----------
        x_values : array
            x values
        f_values : array
            f(x) values
        dtype
            data type to store
        make_inverse : bool
            whether to make inverse spline
        '''
        self.Say = io.SayClass(SplineFunctionClass)
        self.dtype = dtype
        self.xs = np.array(x_values)
        self.fs = np.array(f_values)
        self.spline_f_from_x = interpolate.splrep(self.xs, self.fs)
        if make_inverse:
            self.make_spline_inverse()


# --------------------------------------------------------------------------------------------------
# general functions
# --------------------------------------------------------------------------------------------------
class FunctionClass:
    '''
    Collection of functions, for fitting.
    '''

    def get_ave(self, func, params, x_limits=[0, 1]):
        '''
        .
        '''

        def integrand_func_ave(x, func, params):
            return x * func(x, params)

        return integrate.quad(integrand_func_ave, x_limits[0], x_limits[1], (func, params))[0]

    def gaussian(self, x, params):
        '''
        .
        '''
        return (
            1 / ((2 * np.pi) ** 0.5 * params[1]) * np.exp(-0.5 * ((x - params[0]) / params[1]) ** 2)
        )

    def gaussian_normalized(self, x):
        '''
        .
        '''
        return 1 / (2 * np.pi) ** 0.5 * np.exp(-0.5 * x**2)

    def gaussian_double(self, x, params):
        '''
        .
        '''
        return params[2] * np.exp(-0.5 * ((x - params[0]) / params[1]) ** 2) + (
            1 - params[2]
        ) * np.exp(-0.5 * ((x - params[3]) / params[4]) ** 2)

    def gaussian_double_skew(self, x, params):
        '''
        .
        '''
        return params[3] * self.skew(x, params[0], params[1], params[2]) + (
            1 - params[3]
        ) * self.skew(x, params[4], params[5], params[6])

    def skew(self, x, e=0, width=1, skew=0):
        '''
        .
        '''
        t = (x - e) / width
        return 2 * stats.norm.pdf(t) * stats.norm.cdf(skew * t) / width

    def erf_0to1(self, x, params):
        '''
        Varies from 0 to 1.
        '''
        # pylint: disable=no-member
        return 0.5 * (1 + special.erf((x - params[0]) / (np.sqrt(2) * params[1])))

    def erf_AtoB(self, x, params):
        '''
        Varies from params[2] to params[3].
        '''
        # pylint: disable=no-member
        return (
            params[2] * 0.5 * (1 + special.erf((x - params[0]) / ((np.sqrt(2) * params[1]))))
            + params[3]
        )

    def line(self, x, params):
        '''
        .
        '''
        return params[0] + x * params[1]

    def power_law(self, x, params):
        '''
        .
        '''
        return params[0] + params[1] * x ** params[2]

    def line_exp(self, x, params):
        '''
        .
        '''
        return params[0] + params[1] * x * np.exp(-(x ** params[2]))

    def m_function_schechter(self, m, params):
        '''
        Compute d(num-den) / d(log m) = ln(10) * amplitude * (10 ^ (m - m_char)) ^ slope *
        exp(-10**(m - m_char)).

        Parameters
        ----------
        m : float
            (stellar) mass
        params : list
            parameters (0 = amplitude, 1 = m_char, 2 = slope)
        '''
        m_ratios = 10 ** (m - params[1])

        return np.log(10) * params[0] * m_ratios ** params[2] * np.exp(-m_ratios)

    def numden_schechter(self, m, params, m_max=20):
        '''
        Get cumulative number density above m.

        Parameters
        ----------
        m : float
            (stellar) mass
        params : list
            parameters (0 = amplitude, 1 = m_char, 2 = slope)
        m_max : float
            maximum mass for integration
        '''
        return integrate.quad(self.m_function_schechter, m, m_max, (params))[0]


Function = FunctionClass()


# --------------------------------------------------------------------------------------------------
# function fitting
# --------------------------------------------------------------------------------------------------
def get_chisq_reduced(values_test, values_ref, values_ref_err, param_number=1):
    '''
    Get reduced chi ^ 2, excising reference values with 0 uncertainty.

    Parameters
    ----------
    values_test : array
        value[s] to test
    values_ref : array
        reference value[s]
    values_ref_err : array
        reference uncertainties (can be asymmetric)
    param_number : int
        number of free parameters in getting test values

    Returns
    -------
    array
        chi^2 / dof
    '''
    Say = io.SayClass(get_chisq_reduced)

    values_test = array.arrayize(values_test)
    values_ref = array.arrayize(values_ref)
    values_ref_err = array.arrayize(values_ref_err)

    if np.ndim(values_ref_err) > 1:
        # get uncertainty on correct side of reference values
        if values_ref_err.shape[0] != values_ref.size:
            values_ref_err = values_ref_err.transpose()
        values_ref_err_sided = np.zeros(values_ref_err.shape[0])
        values_ref_err_sided[values_test <= values_ref] = values_ref_err[:, 0][
            values_test <= values_ref
        ]
        values_ref_err_sided[values_test > values_ref] = values_ref_err[:, 1][
            values_test > values_ref
        ]
    else:
        values_ref_err_sided = values_ref_err

    val_indices = array.get_arange(values_ref)[values_ref_err_sided > 0]
    if val_indices.size != values_ref.size:
        Say.say(
            f'excise {values_ref.size - val_indices.size} reference values with uncertainty = 0'
        )

    chi2 = np.sum(
        ((values_test[val_indices] - values_ref[val_indices]) / values_ref_err_sided[val_indices])
        ** 2
    )
    dof = val_indices.size - 1 - param_number

    return chi2 / dof
