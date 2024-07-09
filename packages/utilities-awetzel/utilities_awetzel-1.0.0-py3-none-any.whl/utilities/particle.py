'''
Tools to analyze particle data.

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
from scipy import spatial

from . import array, binning, constant, coordinate, io, math, halo_property, orbit, catalog


# --------------------------------------------------------------------------------------------------
# utilities - parsing input arguments
# --------------------------------------------------------------------------------------------------
def parse_species(part, species):
    '''
    Parse input list of species to ensure that all are in catalog.

    Parameters
    ----------
    part : dict
        catalog of particles
    species : str or list
        name[s] of particle species to analyze

    Returns
    -------
    species_in_part : list
        name[s] of particle species in particle catalog
    '''
    Say = io.SayClass(parse_species)

    if np.isscalar(species):
        species = [species]
    if species == ['all'] or species == ['total']:
        species = list(part.keys())
    elif species == ['baryon']:
        species = ['gas', 'star']

    species_in_part = []
    for spec_name in list(species):
        if spec_name in part:
            species_in_part.append(spec_name)
        else:
            Say.say(f'! {spec_name} not in particle catalog')

    return species_in_part


def parse_indices(part_spec, part_indicess, center_index=None):
    '''
    Parse input list of particle indices.
    If none, generate via arange.

    Parameters
    ----------
    part_spec : dict
        catalog of particles of given species
    part_indices : array or list of arrays
        indices of particles
    center_index : int
        index of center/host position, to select from part_indicess (if list)

    Returns
    -------
    part_indices : array
        indices of particles (for single center/host)
    '''
    if part_indicess is None or len(part_indicess) == 0:
        # input null, so get indices of all particles via catalog
        if 'position' in part_spec:
            part_indices = array.get_arange(part_spec['position'].shape[0])
        elif 'id' in part_spec:
            part_indices = array.get_arange(part_spec['id'].size)
        elif 'mass' in part_spec:
            part_indices = array.get_arange(part_spec['mass'].size)
        else:
            raise ValueError('cannot determine particle indices array')
    else:
        assert len(part_indicess) > 0
        if not np.isscalar(part_indicess[0]):
            # input array of particle indices for each center/host
            part_indices = part_indicess[center_index]
        else:
            part_indices = part_indicess

    return part_indices


def parse_property(parts_or_species, property_name, property_values=None, host_index=None):
    '''
    Get property values, either input or stored in particle catalog.
    List-ify as necessary to match input particle catalog.

    Parameters
    ----------
    parts_or_species : dict or string or list thereof
        catalog[s] of particles or string[s] of species
    property_name : str
        options: 'position', 'velocity', 'rotation', 'indices'
    property_values : float/array or list thereof
        property values to assign
    host_index : int
        which stored host to get position or velocity from.
        if None, return *all* stored host positions or velocities

    Returns
    -------
    property_values : float or list
    '''

    def _parse_property_single(part_or_spec, property_name, property_values, host_index):
        if property_name in ['position', 'velocity', 'rotation']:
            if property_values is None or len(property_values) == 0:
                if property_name == 'position':
                    property_values = part_or_spec.host['position']
                elif property_name == 'velocity':
                    property_values = part_or_spec.host['velocity']
                elif property_name == 'rotation':
                    property_values = part_or_spec.host['rotation']

                if property_values is None or len(property_values) == 0:
                    raise ValueError(
                        f'no input {property_name} and no {property_name} in input catalog'
                    )

                if host_index is not None:
                    # get position or velocity of given host (instead of all of them)
                    property_values = property_values[host_index]

        if isinstance(property_values, list):
            raise ValueError(f'input list of {property_name}s but input single catalog')

        return property_values

    assert property_name in ['position', 'velocity', 'rotation', 'indices']

    if isinstance(parts_or_species, list):
        # input list of particle catalogs
        if (
            property_values is None
            or len(property_values) == 0
            or not isinstance(property_values, list)
        ):
            property_values = [property_values for _ in parts_or_species]

        if len(property_values) != len(parts_or_species):
            raise ValueError(f'number of input {property_name}s not match number of input catalogs')

        for i, part_or_spec in enumerate(parts_or_species):
            property_values[i] = _parse_property_single(
                part_or_spec, property_name, property_values[i], host_index
            )
    else:
        # input single particle catalog
        property_values = _parse_property_single(
            parts_or_species, property_name, property_values, host_index
        )

    return property_values


def parse_coordinate_names(host_index=0, coordinate_modifier=''):
    '''
    Get names to call for particle positions (distances) and velocities, relative to the host.

    Parameters
    ----------
    host_index : int
        index of host galaxy/halo
    coordinate_modifier : str
        modifier name for coordinates
            options: 'principal', 'principal.cylindrical', 'principal.spherical'
    '''
    host_name = 'host'
    if host_index > 0:
        host_name += f'{host_index}'

    if coordinate_modifier is not None and len(coordinate_modifier) > 0:
        if coordinate_modifier[0] != '.':
            coordinate_modifier = '.' + coordinate_modifier

    # get coordinates relative to host galaxy/halo [kpc, km/s physical]
    position_name = f'{host_name}.distance{coordinate_modifier}'
    velocity_name = f'{host_name}.velocity{coordinate_modifier}'

    return position_name, velocity_name


# --------------------------------------------------------------------------------------------------
# kernel smoothing / gravitational softening
# --------------------------------------------------------------------------------------------------
def get_kernel(
    kernel_name='cubic',
    property_name='acceleration',
    radiuss=1,
    kernel_radiuss=1,
    ratio_newtonian=False,
):
    '''
    Get function_kind (potential, acceleration, density, or mass) at input radius[s],
    using input kernel_kind and kernel_radiuss.
    To compute a physical quantity, multiply by G * M (for acceleration or potential) or M
    (for density or mass).
    Note: 'plummer equivalent' scale radius := cubic_kernel_radius / 2.8

    Parameters
    ----------
    kernel_name : str
        kernel/function to use: 'newtonian', 'plummer', 'cubic'
    property_name : str
        property to compute: 'potential', 'acceleration', 'density', 'mass'
    radiuss : float or array
        distances from center
    kernel_radiuss : float or array
        radius of kernel
            for cubic kernel, this is the radius of compact support (full extent of the kernel)
            for plummer sphere, this is the plummer scale radius
    ratio_newtonian : bool
        whether to return the ratio wrt newtonian (for a point mass)

    Returns
    -------
    values : float or array
    '''
    assert property_name in ['acceleration', 'potential', 'density', 'mass']

    if kernel_name == 'newtonian':
        if property_name == 'acceleration':
            # a := G M /r^2
            values = 1 / radiuss**2

        elif property_name == 'potential':
            # phi := G M / r
            values = -1 / radiuss

        elif property_name == 'density':
            # rho := 3 M / (4 pi)/ r^3
            values = 3 / (4 * np.pi) / radiuss**3

        elif property_name == 'mass':
            values = 1

    elif kernel_name == 'plummer':
        if property_name == 'acceleration':
            # a := G M r / (r^2 + e^2)^{3/2)
            values = radiuss / (radiuss**2 + kernel_radiuss**2) ** (3 / 2)

        elif property_name == 'potential':
            # phi := -G M / (r^2 + e^2)^(1/2)
            values = -1 / np.sqrt(radiuss**2 + kernel_radiuss**2)

        elif property_name == 'density':
            # rho := 3 M / (4 pi) * e^2 / (r^2 + e^2)^(3/2)
            values = (
                3 / (4 * np.pi) * kernel_radiuss**2 / (radiuss**2 + kernel_radiuss**2) ** (3 / 2)
            )

        elif property_name == 'mass':
            # M(< r) := M r^3 / (r^2 + e^2)^(3/2)
            values = radiuss**3 / (radiuss**2 + kernel_radiuss**2) ** (3 / 2)

    elif kernel_name == 'cubic':
        q = radiuss / kernel_radiuss

        if property_name == 'potential':
            if q < 0.5:
                values = 14 / 5 * q - 16 / 3 * q**3 + 48 / 5 * q**5 - 32 / 5 * q**6
            elif q < 1:
                values = (
                    -1 / 15
                    + 16 / 5 * q
                    - 32 / 3 * q**3
                    + 16 * q**4
                    - 48 / 5 * q**5
                    + 32 / 15 * q**6
                )
            else:
                values = 1
            values *= -1 / (q * kernel_radiuss)

        elif property_name == 'acceleration':
            if q < 0.5:
                values = 32 / 3 * q - 192 / 5 * q**3 + 32 * q**4
            elif q < 1:
                values = -1 / 15 / q**2 + 64 / 3 * q - 48 * q**2 + 192 / 5 * q**3 - 32 / 3 * q**4
            else:
                values = 1 / q**2

        elif property_name == 'density':
            # equivalent to kernel weight
            if q < 0.5:
                values = 1 + 6 * q**2 * (q - 1)
            elif q < 1:
                values = 2 * (1 - q) ** 3
            else:
                values = 0
            # if comment out, normalize so density(r = 0) = 1
            values *= 8 / np.pi * kernel_radiuss**3

        elif property_name == 'mass':
            # equivalent to integrated (enclosed) kernel weight
            if q < 0.5:
                values = 1 / 3 * q**3 - 6 / 5 * q**5 + q**6
            elif q < 1:
                values = (1 / 3 * 1 / 2**3 - 6 / 5 * 1 / 2**5 + 1 / 2**6) + 2 * (
                    1 / 3 * (q**3 - 1 / 2**3)
                    - 3 / 4 * (q**4 - 1 / 2**4)
                    + 3 / 5 * (q**5 - 1 / 2**5)
                    - 1 / 6 * (q**6 - 1 / 2**6)
                )
            else:
                values = 1 / 32
            values *= 32

    if ratio_newtonian:
        values /= get_kernel('newtonian', property_name, radiuss)

    return values


# --------------------------------------------------------------------------------------------------
# position, velocity
# --------------------------------------------------------------------------------------------------
def get_center_positions(
    part,
    species_name='star',
    part_indicess=None,
    weight_property='mass',
    center_number=1,
    exclusion_distance=400,
    center_positions=None,
    distance_max=np.Inf,
    return_single_array=True,
    verbose=True,
):
    '''
    Get host/center position[s] [kpc comoving] via iterative zoom-in on input particle species,
    weighting particle positions by input weight_property.

    Parameters
    ----------
    part : dict
        dictionary of particles
    species : str
        typically 'star' or 'dark'
    part_indicess : array or list of arrays
        indices of particles to use to compute center position[s]
        if a list, use different particles indices for different centers
    weight_property : str
        property to weight particles by: 'mass', 'potential', 'massfraction.metals'
    center_number : int
        number of centers (hosts) to compute
    exclusion_distance : float
        radius around previous center to cut out particles for finding next center [kpc comoving]
    center_positions : array or list of arrays
        initial position[s] to center on
    distance_max : float
        maximum distance around center_positions to use to select particles
    return_single_array : bool
        whether to return single array instead of array of arrays, if center_number = 1
    verbose : bool
        flag for verbosity in print diagnostics

    Returns
    -------
    center_positions : array or array of arrays
        position[s] of center[s] [kpc comoving]
    '''
    Say = io.SayClass(get_center_positions)

    assert weight_property in ['mass', 'potential', 'massfraction.metals']

    part_spec = part[species_name]

    if verbose:
        center_string = 'center/host'
        if center_number > 1:
            center_string += 's'
        Say.say(
            f'* assigning position for {center_number} {center_string},'
            + f' via iterative zoom-in on {species_name} particle {weight_property}'
        )

    if weight_property == 'potential' and center_number > 1:
        Say.say(
            f'! warning: using {weight_property} to compute {center_number} center positions'
            + ' likely will produce weird results for centers beyond the first!'
        )

    if weight_property not in part_spec:
        Say.say(
            f'! {species_name} particles do not have {weight_property}, weighting by mass instead'
        )
        weight_property = 'mass'

    if center_positions is None or np.ndim(center_positions) == 1:
        # list-ify center_positions
        center_positions = [center_positions for _ in range(center_number)]
    if np.shape(center_positions)[0] != center_number:
        raise ValueError(
            f'! input center_positions = {center_positions}'
            + f' but also center_number = {center_number}'
        )

    for center_i, center_position in enumerate(center_positions):
        part_indices = parse_indices(part_spec, part_indicess, center_i)

        if center_i > 0 and exclusion_distance is not None and exclusion_distance > 0:
            # cull out particles near previous center
            distances = get_distances_wrt_center(
                part,
                species_name,
                parse_indices(part_spec, part_indicess, center_i - 1),
                center_positions[center_i - 1],
                total_distance=True,
                return_single_array=True,
            )
            # exclusion distance in [kpc comoving]
            masks = distances > (exclusion_distance * part.info['scalefactor'])
            part_indices = part_indices[masks]

        if center_position is not None and distance_max > 0 and distance_max < np.Inf:
            # impose distance cut around input center
            part_indices = get_indices_within_coordinates(
                part,
                species_name,
                part_indices,
                [0, distance_max],
                center_position,
                return_single_array=True,
            )

        # if weight_property == 'potential':
        #    part_index = np.nanargmin(part_spec['potential'][part_indices])
        #    center_positions[center_i] = part_spec['position'][part_index]

        center_positions[center_i] = coordinate.get_center_position(
            part_spec['position'][part_indices],
            part_spec.prop(weight_property, part_indices),
            part.info['box.length'],
            center_position=center_position,
            distance_max=distance_max,
        )

    center_positions = np.array(center_positions)

    if verbose:
        for center_i, center_position in enumerate(center_positions):
            Say.say(f'host{center_i + 1} position = (', end='')
            io.print_array(center_position, '{:.2f}', end='')
            print(') [kpc comoving]')
        # print()

    if return_single_array and center_number == 1:
        center_positions = center_positions[0]

    return center_positions


def get_center_velocities_or_accelerations(
    part,
    property_kind='velocity',
    species_name='star',
    part_indicess=None,
    weight_property='mass',
    distance_max=10,
    center_positions=None,
    return_single_array=True,
    verbose=True,
):
    '''
    Get host/center velocity[s] [km/s] or acceleration[s] [km/s / Gyr] of input particle species
    that are within distance_max of center_positions,
    weighting particle velocities by input weight_property.
    If input multiple center_positions, compute a center velocity for each one.

    Parameters
    ----------
    part : dict
        dictionary of particles
    property_kind : str
        velocity or acceleration
    species_name : str
        name of particle species to use
    part_indicess : array or list of arrays
        indices of particles to use to define center
        use this to exclude particles that you know are not relevant
        if list, use host_index to determine which list element to use
    weight_property : str
        property to weight particles by: 'mass', 'potential', 'massfraction.metals'
    distance_max : float
        maximum radius to consider [kpc physical]
    center_positions : array or list of arrays
        center position[s] [kpc comoving]
        if None, will use default center position[s] in catalog
        if list, compute a center velocity for each center position
    return_single_array : bool
        whether to return single array instead of array of arrays, if input single center position
    verbose : bool
        flag for verbosity in print diagnostics

    Returns
    -------
    center_values : array or array of arrays
        velocity[s] [km/s] or acceleration[s] [km/s / Gyr] of center[s]
    '''
    Say = io.SayClass(get_center_velocities_or_accelerations)

    assert property_kind in ['velocity', 'acceleration']
    assert weight_property in ['mass', 'potential', 'massfraction.metals']

    part_spec = part[species_name]

    center_positions = parse_property(part_spec, 'position', center_positions)

    distance_max /= part.snapshot['scalefactor']  # convert to [kpc comoving] to match positions

    center_values = np.zeros(center_positions.shape, part_spec[property_kind].dtype)

    if verbose:
        center_string = 'center/host'
        if center_positions.shape[0] > 1:
            center_string += 's'
        Say.say(
            f'* assigning {property_kind} for {center_positions.shape[0]} {center_string},'
            + f' weighting {species_name} particles by {weight_property}'
        )

    for center_i, center_position in enumerate(center_positions):
        part_indices = parse_indices(part_spec, part_indicess, center_i)

        center_values[center_i] = coordinate.get_center_velocity(
            part_spec[property_kind][part_indices],
            part_spec.prop(weight_property, part_indices),
            part_spec['position'][part_indices],
            center_position,
            distance_max,
            part.info['box.length'],
        )

    if verbose:
        for center_i, center_value in enumerate(center_values):
            Say.say(f'host{center_i + 1} {property_kind} = (', end='')
            io.print_array(center_value, '{:.1f}', end='')
            if property_kind == 'velocity':
                print(') [km/s]')
            elif property_kind == 'acceleration':
                print(') [km/s / Gyr]')
        # print()

    if return_single_array and len(center_values) == 1:
        center_values = center_values[0]

    return center_values


def get_distances_wrt_center(
    part,
    species=['star'],
    part_indicess=None,
    center_position=None,
    rotation=None,
    host_index=0,
    coordinate_system='cartesian',
    total_distance=False,
    return_single_array=True,
):
    '''
    Get distances (scalar or vector) between input particle species positions and center_position
    (input or stored in particle catalog).

    Parameters
    ----------
    part : dict
        catalog of particles at snapshot
    species : str or list
        name[s] of particle species to compute
    part_indicess : array or list
        indices[s] of particles to compute, one array per input species
    center_position : array
        position of center [kpc comoving]
        if None, will use default center position in particle catalog
    rotation : bool or array
        whether to rotate particles. two options:
        (a) if input array of eigen-vectors, will define rotation axes for all species
        (b) if true, will rotate to align with principal axes defined by input species
    host_index : int
        index of host to get stored position of (if not input center_position)
    coordinate_system : str
        which coordinates to get distances in: 'cartesian' (default), 'cylindrical', 'spherical'
    total_distance : bool
        whether to compute total/scalar distance
    return_single_array : bool
        whether to return single array (instead of dict) if input single species

    Returns
    -------
    dist : array (object number x dimension number) or dict thereof
        [kpc physical]
        3-D distance vectors aligned with default x,y,z axes OR
        3-D distance vectors aligned with major, medium, minor axis OR
        2-D distance vectors along major axes and along minor axis OR
        1-D scalar distances
    OR
    dictionary of above for each species
    '''
    assert coordinate_system in ('cartesian', 'cylindrical', 'spherical')

    species = parse_species(part, species)

    center_position = parse_property(part, 'position', center_position, host_index)
    part_indicess = parse_property(species, 'indices', part_indicess)

    dist = {}

    for spec_i, spec_name in enumerate(species):
        part_indices = parse_indices(part[spec_name], part_indicess[spec_i])

        dist[spec_name] = coordinate.get_distances(
            part[spec_name]['position'][part_indices],
            center_position,
            part.info['box.length'],
            part.snapshot['scalefactor'],
            total_distance,
        )  # [kpc physical]

        if not total_distance:
            if rotation is not None:
                if rotation is True:
                    rotation_tensor = parse_property(part, 'rotation', None, host_index)
                elif len(rotation) > 0:
                    assert len(rotation) > 0
                    rotation_tensor = rotation

                dist[spec_name] = coordinate.get_coordinates_rotated(
                    dist[spec_name], rotation_tensor
                )

            if coordinate_system in ['cylindrical', 'spherical']:
                dist[spec_name] = coordinate.get_positions_in_coordinate_system(
                    dist[spec_name], 'cartesian', coordinate_system
                )

    if return_single_array and len(species) == 1:
        dist = dist[species[0]]

    return dist


def get_velocities_wrt_center(
    part,
    species=['star'],
    part_indicess=None,
    center_velocity=None,
    center_position=None,
    rotation=False,
    host_index=0,
    coordinate_system='cartesian',
    total_velocity=False,
    return_single_array=True,
):
    '''
    Get velocities (either scalar or vector) between input particle species velocities and
    center_velocity (input or stored in particle catalog).

    Parameters
    ----------
    part : dict
        catalog of particles at snapshot
    species : str or list
        name[s] of particle species to get
    part_indicess : array or list
        indices[s] of particles to select, one array per input species
    center_velocity : array
        center velocity [km/s]. if None, will use default center velocity in catalog
    center_position : array
        center position [kpc comoving], to use in computing Hubble flow.
        if None, will use default center position in catalog
    rotation : bool or array
        whether to rotate particles. two options:
        (a) if input array of eigen-vectors, will define rotation axes for all species
        (b) if True, will rotate to align with principal axes defined by input species
    host_index : int
        index of host to get stored position and velocity of (if not input center_position or
        center_velocity)
    coordinate_system : str
        which coordinates to get positions in: 'cartesian' (default), 'cylindrical', 'spherical'
    total_velocity : bool
        whether to compute total/scalar velocity
    return_single_array : bool
        whether to return array (instead of dict) if input single species

    Returns
    -------
    vel : array or dict thereof
        velocities (object number x dimension number, or object number) [km/s]
    '''
    assert coordinate_system in ('cartesian', 'cylindrical', 'spherical')

    species = parse_species(part, species)

    center_velocity = parse_property(part, 'velocity', center_velocity, host_index)
    center_position = parse_property(part, 'position', center_position, host_index)
    part_indicess = parse_property(species, 'indices', part_indicess)

    vel = {}
    for spec_i, spec_name in enumerate(species):
        part_indices = parse_indices(part[spec_name], part_indicess[spec_i])

        vel[spec_name] = coordinate.get_velocity_differences(
            part[spec_name]['velocity'][part_indices],
            center_velocity,
            part[spec_name]['position'][part_indices],
            center_position,
            part.info['box.length'],
            part.snapshot['scalefactor'],
            part.snapshot['time.hubble'],
            total_velocity,
        )

        if not total_velocity:
            if rotation is not None:
                if rotation is True:
                    rotation_tensor = parse_property(part, 'rotation', None, host_index)
                else:
                    assert len(rotation) > 0
                    rotation_tensor = rotation

                vel[spec_name] = coordinate.get_coordinates_rotated(vel[spec_name], rotation_tensor)

            if coordinate_system in ('cylindrical', 'spherical'):
                # need to compute distance vectors
                distances = coordinate.get_distances(
                    part[spec_name]['position'][part_indices],
                    center_position,
                    part.info['box.length'],
                    part.snapshot['scalefactor'],
                )  # [kpc physical]

                if rotation is not None:
                    # need to rotate distances too
                    distances = coordinate.get_coordinates_rotated(distances, rotation_tensor)

                vel[spec_name] = coordinate.get_velocities_in_coordinate_system(
                    vel[spec_name], distances, 'cartesian', coordinate_system
                )

    if return_single_array and len(species) == 1:
        vel = vel[species[0]]

    return vel


def get_orbit_dictionary(
    part,
    species=['star'],
    part_indicess=None,
    center_position=None,
    center_velocity=None,
    host_index=0,
    return_single_dict=True,
):
    '''
    Get dictionary of orbital parameters with respect to center_position and center_velocity
    (input or stored in particle catalog).

    Parameters
    ----------
    part : dict
        catalog of particles at snapshot
    species : str or list
        name[s] of particle species to compute
    part_indicess : array or list
        indices[s] of particles to select, one array per input species
    center_position : array
        center (reference) position
    center_position : array
        center (reference) velociy
    host_index : int
        index of host to get stored position and velocity of (if not input center_position or
        center_velocity)
    return_single_dict : bool
        whether to return single dict (instead of dict of dicts), if single species

    Returns
    -------
    orb : dict
        dictionary of orbital properties, one for each species (unless scalarize is True)
    '''
    species = parse_species(part, species)

    center_position = parse_property(part, 'position', center_position, host_index)
    center_velocity = parse_property(part, 'velocity', center_velocity, host_index)
    part_indicess = parse_property(species, 'indices', part_indicess)

    orb = {}
    for spec_i, spec_name in enumerate(species):
        part_indices = parse_indices(part[spec_name], part_indicess[spec_i])

        distance_vectors = coordinate.get_distances(
            part[spec_name]['position'][part_indices],
            center_position,
            part.info['box.length'],
            part.snapshot['scalefactor'],
        )

        velocity_vectors = coordinate.get_velocity_differences(
            part[spec_name]['velocity'][part_indices],
            center_velocity,
            part[spec_name]['position'][part_indices],
            center_position,
            part.info['box.length'],
            part.snapshot['scalefactor'],
            part.snapshot['time.hubble'],
        )

        orb[spec_name] = orbit.get_orbit_dictionary(distance_vectors, velocity_vectors)

    if return_single_dict and len(species) == 1:
        orb = orb[species[0]]

    return orb


# --------------------------------------------------------------------------------------------------
# neighbors
# --------------------------------------------------------------------------------------------------
def get_neighbors(
    part,
    species_name='star',
    property_select={},
    part_indices=None,
    center_positions=None,
    neig_distance_max=1,
    neig_number_max=3000,
    dimension_number=3,
    host_index=0,
    periodic=False,
):
    '''
    Get distances [and indices] of neighbor particles near input particles.
    If input center_positions (relative to host galaxy), use them to find neighboring particles.
    Else, by default, use each particle as a center to find neighboring particles around.

    Parameters
    ----------
    part : dict
        catalog of particles at snapshot
    species_name : str
        name of particle species to use
    property_select : dict
        (other) properties to select particles on: names as keys and limits as values
    part_indices : array
        prior indices[s] of particles to select
    center_positions : array
        positions of centers to find neighbors around, in the coordinates of the host galaxy
        if input, use these instead of using position of each input particle
    neig_distance_max : float
        maximum distance to find neighbors [kpc physical]
    neig_number_max : int
        maximum neighbors to get for each particle
    dimension_number : int
        how many spatial dimensions to use to compute distances
    host_index : int
        index of host galaxy/halo to use
    periodic : bool
        whether to impose periodic boundaries, based on stored box.length in particle catalog
    '''
    part_spec = part[species_name]

    part_indices = parse_indices(part_spec, part_indices)

    if property_select:
        part_indices = catalog.get_indices_catalog(part_spec, property_select, part_indices)

    position_name, _velocity_name = parse_coordinate_names(host_index)

    if periodic:
        periodic_length = part_spec.info['box.length']
    else:
        periodic_length = None

    # get positions relative to center of host galaxy [kpc physical]
    if dimension_number is None or dimension_number == 3:
        positions = part_spec.prop(position_name, part_indices)
    elif dimension_number == 2:
        # if finding neighbors in 2-D, ensure alignment with host galaxy
        positions = part_spec.prop(f'{position_name}.principal', part_indices)
        positions = positions[:, [0, 1]]
    elif dimension_number == 1:
        # if finding neighbors in 1-D, ensure alignment with host galaxy
        positions = part_spec.prop(f'{position_name}.principal', part_indices)
        positions = positions[:, [2]]

    if center_positions is None or len(center_positions) == 0:
        # not input any center positions - use all particle indices as centers
        center_positions = positions
    else:
        if np.ndim(center_positions) == 1:
            # ensure correct shape, if input single center
            center_positions = np.array([center_positions])
        assert center_positions.shape[1] == positions.shape[1]

    neig_distancess, neig_indicess = coordinate.get_neighbors(
        center_positions,
        positions,
        neig_distance_max,
        neig_number_max,
        periodic_length,
        neig_ids=part_indices,
    )

    return neig_distancess, neig_indicess


def get_indices_within_coordinates(
    part,
    species=['star'],
    part_indicess=None,
    distance_limitss=None,
    center_position=None,
    velocity_limitss=None,
    center_velocity=None,
    host_index=0,
    rotation=None,
    coordinate_system='cartesian',
    return_single_array=True,
):
    '''
    Get indices of particles that are within distance and/or velocity limits from center_position
    and center_velocity (input or stored in particle catalog).

    Parameters
    ----------
    part : dict
        catalog of particles at snapshot
    species : str or list
        name[s] of particle species to use
    part_indicess : array
        prior indices[s] of particles to select, one array per input species
    distance_limitss : list or list of lists
        min and max distance[s], relative to center, to get particles [kpc physical]
        default is 1-D list, but can be 2-D or 3-D list to select separately along dimensions
        if 2-D or 3-D, need to input *signed* limits
    center_position : array
        center position [kpc comoving]. if None, use default center position in particle catalog
    velocity_limitss : list or list of lists
        min and max velocities, relative to center, to get particles [km/s]
        default is 1-D list, but can be 2-D or 3-D list to select separately along dimensions
        if 2-D or 3-D, need to input *signed* limits
    center_velocity : array
        center velocity [km/s]. if None, use default center velocity in particle catalog
    host_index : int
        index of host galaxy/halo to get position or velocity of (if not input center_position or
        center_velocity)
    rotation : bool or array
        whether to rotate particle coordinates. two options:
        (a) if input array of eigen-vectors, will use to define rotation axes for all species
        (b) if True, will rotate to align with principal axes defined by each input species
    coordinate_system : str
        which coordinates to get positions in: 'cartesian' (default), 'cylindrical', 'spherical'
    return_single_array : bool
        whether to return single array (instead of dict), if input single species

    Returns
    -------
    part_index : dict or array
        indices of particles in region
    '''
    assert coordinate_system in ['cartesian', 'cylindrical', 'spherical']

    species = parse_species(part, species)
    center_position = parse_property(part, 'position', center_position, host_index)
    if velocity_limitss is not None and len(velocity_limitss) > 0:
        center_velocity = parse_property(part, 'velocity', center_velocity, host_index)
    part_indicess = parse_property(species, 'indices', part_indicess)

    part_index = {}
    for spec_i, spec_name in enumerate(species):
        part_indices = parse_indices(part[spec_name], part_indicess[spec_i])

        if len(part_indices) > 0 and distance_limitss is not None and len(distance_limitss) > 0:
            distance_limits_dimen = np.ndim(distance_limitss)

            if distance_limits_dimen == 1:
                total_distance = True
            elif distance_limits_dimen == 2:
                total_distance = False
                assert len(distance_limitss) in [2, 3]
            else:
                raise ValueError(f'! cannot parse distance_limitss = {distance_limitss}')

            if (
                distance_limits_dimen == 1
                and distance_limitss[0] <= 0
                and distance_limitss[1] >= np.Inf
            ):
                pass  # null case, no actual limits imposed, so skip rest
            else:
                # an attempt to be clever, but gains seem modest
                # distances = np.abs(coordinate.get_position_difference(
                #    part[spec_name]['position'] - center_position,
                #    part.info['box.length'])) * part.snapshot['scalefactor']  # [kpc physical]

                # for dimension_i in range(part[spec_name]['position'].shape[1]):
                #    masks *= ((distances[:, dimension_i] < np.max(distance_limits)) *
                #              (distances[:, dimension_i] >= np.min(distance_limits)))
                #    part_indices[spec_name] = part_indices[spec_name][masks]
                #    distances = distances[masks]

                # distances = np.sum(distances ** 2, 1)  # assume 3-d position

                distancess = get_distances_wrt_center(
                    part,
                    spec_name,
                    part_indices,
                    center_position,
                    rotation,
                    host_index,
                    coordinate_system,
                    total_distance,
                )

                if distance_limits_dimen == 1:
                    # distances are absolute
                    masks = (distancess >= np.min(distance_limitss)) * (
                        distancess < np.max(distance_limitss)
                    )
                elif distance_limits_dimen == 2:
                    if len(distance_limitss) == 2:
                        # distances are signed
                        masks = (
                            (distancess[0] >= np.min(distance_limitss[0]))
                            * (distancess[0] < np.max(distance_limitss[0]))
                            * (distancess[1] >= np.min(distance_limitss[1]))
                            * (distancess[1] < np.max(distance_limitss[1]))
                        )
                    elif distance_limits_dimen == 3:
                        # distances are signed
                        masks = (
                            (distancess[0] >= np.min(distance_limitss[0]))
                            * (distancess[0] < np.max(distance_limitss[0]))
                            * (distancess[1] >= np.min(distance_limitss[1]))
                            * (distancess[1] < np.max(distance_limitss[1]))
                            * (distancess[2] >= np.min(distance_limitss[2]))
                            * (distancess[2] < np.max(distance_limitss[2]))
                        )

                part_indices = part_indices[masks]

        if len(part_indices) > 0 and velocity_limitss is not None and len(velocity_limitss) > 0:
            velocity_limits_dimen = np.ndim(velocity_limitss)

            if velocity_limits_dimen == 1:
                return_total_velocity = True
            elif velocity_limits_dimen == 2:
                return_total_velocity = False
                assert len(velocity_limitss) in [2, 3]
            else:
                raise ValueError(f'! cannot parse velocity_limitss = {velocity_limitss}')

            if (
                velocity_limits_dimen == 1
                and velocity_limitss[0] <= 0
                and velocity_limitss[1] >= np.Inf
            ):
                pass  # null case, no actual limits imposed, so skip rest
            else:
                velocitiess = get_velocities_wrt_center(
                    part,
                    spec_name,
                    part_indices,
                    center_velocity,
                    center_position,
                    rotation,
                    host_index,
                    coordinate_system,
                    return_total_velocity,
                )

                if velocity_limits_dimen == 1:
                    # velocities are absolute
                    masks = (velocitiess >= np.min(velocity_limitss)) * (
                        velocitiess < np.max(velocity_limitss)
                    )
                elif velocity_limits_dimen == 2:
                    if len(velocity_limitss) == 2:
                        # velocities are signed
                        masks = (
                            (velocitiess[0] >= np.min(velocity_limitss[0]))
                            * (velocitiess[0] < np.max(velocity_limitss[0]))
                            * (velocitiess[1] >= np.min(velocity_limitss[1]))
                            * (velocitiess[1] < np.max(velocity_limitss[1]))
                        )
                    elif len(velocity_limitss) == 3:
                        # velocities are signed
                        masks = (
                            (velocitiess[0] >= np.min(velocity_limitss[0]))
                            * (velocitiess[0] < np.max(velocity_limitss[0]))
                            * (velocitiess[1] >= np.min(velocity_limitss[1]))
                            * (velocitiess[1] < np.max(velocity_limitss[1]))
                            * (velocitiess[2] >= np.min(velocity_limitss[2]))
                            * (velocitiess[2] < np.max(velocity_limitss[2]))
                        )

                part_indices = part_indices[masks]

        part_index[spec_name] = part_indices

    if return_single_array and len(species) == 1:
        part_index = part_index[species[0]]

    return part_index


# --------------------------------------------------------------------------------------------------
# FoF group catalog
# --------------------------------------------------------------------------------------------------
def get_fof_group_catalog(
    part,
    species_name='gas',
    property_select={},
    part_indices=None,
    linking_length=20,
    particle_number_min=5,
    dimension_number=3,
    host_index=0,
):
    '''
    Get catalog of FoF groups of particles of input species.

    Parameters
    ----------
    part : dict
        catalog of particles at snapshot
    species_name : str
        name of particle species to use
    property_select : dict
        (other) properties to select on: names as keys and limits as values
    part_indices : array
        prior indices[s] of particles to select
    linking_length : float
        maximum distance to link neighbors [pc physical]
    particle_number_min : int
        minimum number of member particles to keep a FoF group
    dimension_number : int
        number of spatial dimensions to use (to run in 2-D)
    host_index : int
        index of host galaxy/halo to use to get positions and velocities around

    Returns
    -------
    grp : dictionary class
        catalog of FoF groups of particles
    '''
    Say = io.SayClass(get_fof_group_catalog)

    position_name, velocity_name = parse_coordinate_names(host_index, 'principal')

    part_spec = part[species_name]

    part_indices = parse_indices(part_spec, part_indices)

    if property_select:
        part_indices = catalog.get_indices_catalog(part_spec, property_select, part_indices)

    if len(part_indices) == 0:
        Say.say(
            '! no {} particles satisfy group selection criteria at snapshot {}'.format(
                species_name, part.snapshot['index']
            )
        )
        return

    velocities = None
    scalefactor = part_spec.snapshot['scalefactor']

    # determine which positions and velocities to use
    try:
        # ideally use physical distance from host aligned with host's principal axes
        positions = part_spec.prop(position_name, part_indices)
        Say.say(f'finding FoF groups using: {position_name}')
        has_host = True
        has_host_rotation = True
        if 'velocity' in part_spec:
            velocities = part_spec.prop(f'{velocity_name}', part_indices)
    except IndexError:
        has_host_rotation = False
        try:
            # next, try to use physical distance from host, un-rotated
            position_name = position_name.rstrip('.principal')
            positions = part_spec.prop(position_name, part_indices)
            Say.say(f'finding FoF groups using: {position_name}')
            has_host = True
            if 'velocity' in part_spec:
                velocity_name = velocity_name.rstrip('.principal')
                velocities = part_spec.prop(f'{velocity_name}', part_indices)
        except IndexError:
            # no host assigned, use raw physical coordinates
            position_name = 'position'
            positions = part_spec[position_name][part_indices] * scalefactor
            Say.say(f'finding FoF groups using: physical {position_name} in box units')
            has_host = False
            if 'velocity' in part_spec:
                velocity_name = 'velocity'
                velocities = part_spec[velocity_name][part_indices]

    if dimension_number < 3:
        # find groups in 2-D
        assert has_host_rotation
        dimension_indices = coordinate.get_dimension_indices(dimension_number)
        positions = positions[:, dimension_indices]

    # find FoF groups
    group_indices = coordinate.get_fof_groups(
        positions,
        linking_length * 1e-3,  # convert to [kpc physical], to be consistent with positions
        particle_number_min,
        # part_spec.info['box.length'],
    )

    group_number = len(group_indices)
    position_dtype = part_spec['position'].dtype

    if group_number == 0:
        Say.say('! found no {} groups at snapshot {}'.format(species_name, part.snapshot['index']))
        return

    # make dictionary for FoF group catalog
    grp = {}
    grp['indices'] = np.array(group_indices, dtype=object)
    grp['number'] = np.zeros(group_number, dtype=np.int32)  # total number of members
    # total mass of members
    grp['mass'] = np.zeros(group_number, dtype=part_spec['mass'].dtype)
    # maximum distance from COM position
    grp['radius.100'] = np.zeros(group_number, dtype=np.float32)
    grp['radius.90'] = np.zeros(group_number, dtype=np.float32)
    grp['radius.50'] = np.zeros(group_number, dtype=np.float32)
    # center-of-mass position
    grp[position_name] = np.zeros((group_number, positions.shape[1]), dtype=position_dtype)
    if velocities is not None:
        # 3-D velocity dispersion
        grp['vel.std'] = np.zeros(group_number, dtype=part_spec['velocity'].dtype)
        # center-of-mass velocity
        grp[velocity_name] = np.zeros(
            (group_number, velocities.shape[1]), dtype=part_spec['velocity'].dtype
        )
    if 'temperature' in part_spec:
        grp['temperature'] = np.zeros(group_number, dtype=part_spec['temperature'].dtype)
        grp['sound.speed'] = np.zeros(group_number, dtype=part_spec['temperature'].dtype)

    # compute properties for each group
    for gi, indices in enumerate(group_indices):
        pindices = part_indices[indices]  # update to member indices in particle catalog
        grp['indices'][gi] = pindices
        grp['number'][gi] = pindices.size

        masses = part_spec['mass'][pindices]
        grp['mass'][gi] = masses.sum()  # total mass of members

        grp[position_name][gi] = np.average(positions[indices], 0, masses)  # center-of-mass pos
        distances = positions[indices] - grp[position_name][gi]
        distances = np.sqrt(np.sum(distances**2, 1)) * 1e3  # convert to [pc physical]
        grp['radius.100'][gi] = distances.max()  # maximum distance of members
        grp['radius.90'][gi] = math.percentile_weighted(distances, 90, masses)
        grp['radius.50'][gi] = math.percentile_weighted(distances, 50, masses)

        if velocities is not None:
            # compute 3D velocity dispersion [km/s]
            # first compute center-of-mass velocity
            grp[velocity_name][gi] = np.average(velocities[indices], 0, masses)
            # compute total velocities wrt COM velocity
            velocity2s = np.sum((velocities[indices] - grp[velocity_name][gi]) ** 2, 1)
            # use average of velocity^2 (formal standard deviation)
            # grp['vel.std'][gi] = np.sqrt(np.average(velocity2s, weights=masses))
            # use median of velocity^2 (more stable against outliers)
            grp['vel.std'][gi] = np.sqrt(math.percentile_weighted(velocity2s, 50, masses))

        if 'temperature' in part_spec:
            # grp['temperature'][gi] = np.average(
            #     part_spec['temperature'][pindices], weights=masses)
            # grp['sound.speed'][gi] = np.average(
            #    part_spec.prop('sound.speed', pindices), weights=masses
            # )
            grp['temperature'][gi] = math.percentile_weighted(
                part_spec['temperature'][pindices], 50, masses
            )
            grp['sound.speed'][gi] = math.percentile_weighted(
                part_spec.prop('sound.speed', pindices), 50, masses
            )

    # assign positions and velocities in other coordinate systems
    if has_host_rotation:
        # compute un-rotated coordinates wrt the host
        unrotate_tensor = part_spec.host['rotation'][host_index].transpose()
        grp['host.distance'] = coordinate.get_coordinates_rotated(
            grp['host.distance.principal'], unrotate_tensor
        )
        if velocities is not None:
            grp['host.velocity'] = coordinate.get_coordinates_rotated(
                grp['host.velocity.principal'], unrotate_tensor
            )

    if has_host:
        # compute position in original box comoving units
        grp['position'] = (
            grp['host.distance'] / scalefactor + part_spec.host['position'][host_index]
        )
        # approximation: skip un-doing the Hubble expansion term
        grp['velocity'] = grp['host.velocity'] + part_spec.host['velocity'][host_index]

    return grp


# --------------------------------------------------------------------------------------------------
# properties within spatial apertures
# --------------------------------------------------------------------------------------------------
def get_velocity_dispersion_v_distance(
    center_positions,
    part,
    species_name='gas',
    property_select={},
    part_indices=None,
    weight_by_mass=True,
    neig_number_max=300000,
    distance_limits=[0, 3],
    distance_bin_width=0.01,
    distance_log_scale=False,
    coordinate_modifier='principal',
    host_index=0,
    periodic=False,
):
    '''
    .
    '''
    Say = io.SayClass(get_velocity_dispersion_v_distance)

    part_spec = part[species_name]

    if property_select:
        part_indices = catalog.get_indices_catalog(part_spec, property_select, part_indices)

    part_weights = None
    if weight_by_mass:
        part_weights = np.asarray(part_spec.prop('mass', part_indices))
        part_weights /= np.median(part_weights)

    if np.ndim(center_positions) == 1:
        # ensure correct shape, if input single center
        center_positions = np.array([center_positions])

    dimension_indices = coordinate.get_dimension_indices(coordinates=center_positions)
    dimension_number = len(dimension_indices)

    DistanceBin = binning.DistanceBinClass(
        distance_limits,
        distance_bin_width,
        log_scale=distance_log_scale,
        dimension_number=dimension_number,
    )
    distance_max = np.max(distance_limits)

    periodic_length = None
    if periodic:
        periodic_length = part_spec.info['box.length']

    position_name, velocity_name = parse_coordinate_names(host_index, coordinate_modifier)

    # get coordinates relative to host galaxy principal axes [kpc physical]
    part_positions = part_spec.prop(position_name, part_indices)
    part_velocities = part_spec.prop(velocity_name, part_indices)

    if dimension_number < 3:
        part_positions = part_positions[:, dimension_indices]

    assert center_positions.shape[1] == part_positions.shape[1]

    # neig_distancess, neig_indicess = coordinate.get_neighbors(
    #    center_positions,
    #    part_positions,
    #    np.max(distance_limits),
    #    neig_number_max,
    #    periodic_length,
    #    # neig_ids=part_indices,
    # )

    KDTree = spatial.KDTree(part_positions, boxsize=periodic_length)

    veldisp = {
        'distance': DistanceBin.maxs,
        #'bin.median': np.zeros((DistanceBin.number, center_positions.shape[0])),
        #'bin.average': np.zeros((DistanceBin.number, center_positions.shape[0])),
        'cum.median': np.zeros((DistanceBin.number, center_positions.shape[0])),
        'cum.average': np.zeros((DistanceBin.number, center_positions.shape[0])),
    }

    for c_i, center_position in enumerate(center_positions):
        # get neighboring particles
        part_distances, part_iis = KDTree.query(
            center_position,
            neig_number_max,
            distance_upper_bound=distance_max,
            # workers=workers,
        )

        # check that list of neighboring particles does not saturate at neig_number_max
        neig_distance_max = part_distances[-1]
        if neig_distance_max < np.Inf:
            Say.say(
                f'! center {c_i} reached neig_number_max = {neig_number_max}'
                + ' at distance = {:.2f}, < distance_max = {:.2f} kpc'.format(
                    neig_distance_max, distance_max
                )
            )
            Say.say('so you should increase neig_number_max!')
        else:
            # keep only valid neighbors
            masks = part_distances < np.Inf
            part_distances = part_distances[masks]  # ensure self is non-zero for log bins
            part_iis = part_iis[masks]

        if part_distances.size == 0:
            # no particles out to maximum distance from this center
            continue

        # get indices within distance bins of neighboring particles
        distance_bin_indices = DistanceBin.get_bin_indices(
            part_distances, round_kind='down', warn_outlier=False
        )

        # compute velocity statistics of neighboring particles within distance bin limit
        for d_i in range(DistanceBin.number):
            if 'bin.median' in veldisp or 'bin.average' in veldisp:
                # use only particles at this distance bin
                part_iis_d = part_iis[distance_bin_indices == d_i]
                if len(part_iis_d) > 1:
                    velocities = part_velocities[part_iis_d]
                    weights = None
                    if part_weights is not None:
                        weights = part_weights[part_iis_d]
                    com_velocity = np.average(velocities, 0, weights)
                    # compute total velocity^2 wrt COM velocity
                    velocity2s = np.sum((velocities - com_velocity) ** 2, 1)
                    if 'bin.average' in veldisp:
                        # use average of velocity^2 (formal standard deviation)
                        veldisp['bin.average'][d_i, c_i] = np.sqrt(
                            np.average(velocity2s, weights=weights)
                        )
                    if 'bin.median' in veldisp:
                        # use median of velocity^2 (more stable against outliers))
                        veldisp['bin.median'][d_i, c_i] = np.sqrt(
                            math.percentile_weighted(velocity2s, 50, weights)
                        )

            if 'cum.median' in veldisp or 'cum.average' in veldisp:
                # use all particles within this distance limit
                part_iis_d = part_iis[distance_bin_indices <= d_i]
                if len(part_iis_d) > 1:
                    velocities = part_velocities[part_iis_d]
                    weights = None
                    if part_weights is not None:
                        weights = part_weights[part_iis_d]
                    com_velocity = np.average(velocities, 0, weights)
                    # compute total velocity^2 wrt COM velocity
                    velocity2s = np.sum((velocities - com_velocity) ** 2, 1)
                    # use average of velocity^2 (formal standard deviation)
                    if 'cum.average' in veldisp:
                        veldisp['cum.average'][d_i, c_i] = np.sqrt(
                            np.average(velocity2s, weights=weights)
                        )
                    if 'cum.median' in veldisp:
                        # use median of velocity^2 (more stable against outliers))
                        veldisp['cum.median'][d_i, c_i] = np.sqrt(
                            math.percentile_weighted(velocity2s, 50, weights)
                        )

    for prop in np.setdiff1d(tuple(veldisp), 'distance'):
        vds = veldisp[prop]
        veldisp[prop + '.2'] = np.percentile(vds, 2.275, 1)
        veldisp[prop + '.16'] = np.percentile(vds, 16, 1)
        veldisp[prop + '.50'] = np.percentile(vds, 50, 1)
        veldisp[prop + '.84'] = np.percentile(vds, 84, 1)
        veldisp[prop + '.98'] = np.percentile(vds, 97.725, 1)
        # veldisp[prop + '.mean'] = np.mean(vds, 1, 1)
        # veldisp[prop + '.std'] = np.std(vds, 1, 1)

        """
        # only include centers and radii with non-zero measured dispersion
        veldisp[prop + '.2'] = np.zeros(DistanceBin.number) - 1
        veldisp[prop + '.16'] = np.zeros(DistanceBin.number) - 1
        veldisp[prop + '.50'] = np.zeros(DistanceBin.number) - 1
        veldisp[prop + '.84'] = np.zeros(DistanceBin.number) - 1
        veldisp[prop + '.98'] = np.zeros(DistanceBin.number) - 1
        # veldisp[prop + '.mean'] = np.zeros(DistanceBin.number) - 1
        # veldisp[prop + '.std'] = np.zeros(DistanceBin.number) - 1

        for d_i in range(DistanceBin.number):
            masks = veldisp[prop][d_i] >= 0
            vds = veldisp[prop][d_i][masks]
            if vds.size >= 4:
                veldisp[prop + '.2'][d_i] = np.percentile(vds, 2.275)
                veldisp[prop + '.16'][d_i] = np.percentile(vds, 16)
                veldisp[prop + '.50'][d_i] = np.percentile(vds, 50)
                veldisp[prop + '.84'][d_i] = np.percentile(vds, 84)
                veldisp[prop + '.98'][d_i] = np.percentile(vds, 97.725)
                # veldisp[prop + '.mean'][d_i] = np.mean(vds, 1)
                # veldisp[prop + '.std'][d_i] = np.std(vds, 1)
        """
    return veldisp


# --------------------------------------------------------------------------------------------------
# halo/galaxy major/minor axes
# --------------------------------------------------------------------------------------------------
def get_principal_axes(
    part,
    species_name='star',
    distance_max=10,
    mass_percent=None,
    age_percent=None,
    age_limits=None,
    temperature_limits=None,
    center_positions=None,
    center_velocities=None,
    host_index=None,
    part_indicess=None,
    return_single_array=True,
    verbose=True,
):
    '''
    Get dictionary of rotation tensor (reverse-sorted eigen-vectors) and axis ratios of the
    principal axes of each host galaxy/halo, defined via the moment of intertia tensor.
    Principal axes are oriented so median v_phi > 0.

    Parameters
    ----------
    part : dict
        catalog of particles at snapshot
    species : str or list
        name[s] of particle species to use
    distance_max : float
        maximum distance to select particles [kpc physical]
    mass_percent : float
        keep particles within the distance that encloses mass percent [0, 100] of all particles
        within distance_max
    age_percent : float
        use the youngest age_percent of (star) particles within distance cut
    age_limits : float
        use only (star) particles within age limits
    temperature_limits : float
        use only (gas) particles within temperature limits
    center_positions : array or array of arrays
        position[s] of center[s] [kpc comoving]
    center_velocities : array or array of arrays
        velocity[s] of center[s] [km/s]
    host_index : int
        index of host to get stored position or velocity of (if not input them)
        if None, get principal axes for all stored hosts
    part_indices : array or list of arrays
        indices of particles to use. if input list, use different particles for each center position
    return_single_array : bool
        whether to return single array (instead of array of arrays), if single host
    verbose : bool
        whether to print axis ratios

    Returns
    -------
    principal_axes = {
        'rotation': array : rotation tensor that defines (max, med, min) principal axes
        'axis.ratios': array : ratios of principal axes
    }
    '''
    Say = io.SayClass(get_principal_axes)

    part_spec = part[species_name]

    # get host/center coordintes, ensure that they are a 2-D array  even if single host
    center_positions = parse_property(part_spec, 'position', center_positions, host_index)
    if np.ndim(center_positions) == 1:
        center_positions = [center_positions]
    if 'velocity' in part_spec:
        center_velocities = parse_property(part, 'velocity', center_velocities, host_index)
        if np.ndim(center_velocities) == 1:
            center_velocities = [center_velocities]

    if species_name not in part or len(part_spec['position']) == 0:
        Say.say(
            f'! input catalog not contain {species_name} particles, cannot assign principal axes!'
        )
        return

    if verbose:
        host_name = 'host'
        if len(center_positions) > 1:
            host_name += 's'
        Say.say(f'* assigning rotation tensor for {len(center_positions)} {host_name}')
        Say.say('using {} particles at distance < {:.1f} kpc'.format(species_name, distance_max))

    principal_axes = {'rotation': [], 'axis.ratios': []}

    for center_i, center_position in enumerate(center_positions):
        part_indices = parse_indices(part_spec, part_indicess, center_i)

        distance_vectors = coordinate.get_distances(
            part_spec['position'][part_indices],
            center_position,
            part.info['box.length'],
            part.snapshot['scalefactor'],
        )  # [kpc physical]

        distances = np.sqrt(np.sum(distance_vectors**2, 1))
        masks = distances < distance_max

        if np.sum(masks) == 0:
            raise ValueError(
                '! no {} particles at distance < {:.1f} kpc'.format(species_name, distance_max)
            )

        if mass_percent is not None and mass_percent < 100:
            distance_max_percent = math.percentile_weighted(
                distances[masks], mass_percent, part_spec.prop('mass', part_indices[masks])
            )
            masks *= distances < distance_max_percent

            if verbose:
                Say.say(
                    'using distance < {:.1f} kpc that encloses {}% of mass'.format(
                        distance_max_percent, mass_percent
                    )
                )

        if np.sum(masks) == 0:
            raise ValueError(
                '! no {} particles at distance < {:.1f} kpc'.format(species_name, distance_max)
            )

        if species_name == 'star' and (
            age_percent is not None or (age_limits is not None and len(age_limits)) > 0
        ):
            if age_percent is not None and age_percent <= 100:
                age_max = math.percentile_weighted(
                    part_spec.prop('age', part_indices[masks]),
                    age_percent,
                    part_spec.prop('mass', part_indices[masks]),
                )
                age_limits_use = [0, age_max]
            else:
                age_limits_use = age_limits

            if 'form.scalefactor' not in part_spec or len(part_spec['form.scalefactor']) == 0:
                Say.say(f'! catalog not contain {species_name} ages')
                Say.say(f'so assigning principal axes using all {species_name} particles')

            if verbose:
                if age_percent and (age_limits is not None and len(age_limits) > 0):
                    Say.say('input both age_percent and age_limits, using only age_percent')
                Say.say(f'using youngest {age_percent}% of {species_name} particles')
                Say.say(
                    f'host{center_i + 1}: using {species_name} particles with'
                    + f' age = {array.get_limits_string(age_limits_use)} Gyr'
                )
            masks *= (part_spec.prop('age', part_indices) >= min(age_limits_use)) * (
                part_spec.prop('age', part_indices) < max(age_limits_use)
            )

        if species_name == 'gas' and (
            temperature_limits is not None and len(temperature_limits) > 0
        ):
            if 'temperature' not in part_spec:
                raise ValueError(f'! input temperature limits but not in {species_name} catalog')

            Say.say(
                f'host{center_i + 1}: using {species_name} particles with'
                + f' temperature = {array.get_limits_string(temperature_limits)} K'
            )
            masks *= (part_spec.prop('temperature', part_indices) >= min(temperature_limits)) * (
                part_spec.prop('temperature', part_indices) < max(temperature_limits)
            )

        rotation_tensor, axis_ratios = coordinate.get_principal_axes(
            distance_vectors[masks],
            part_spec.prop('mass', part_indices[masks]),
            verbose=False,
        )

        if center_velocities is not None and len(center_velocities) > 0:
            # test if need to flip a principal axis to ensure that median v_phi > 0
            assert 'velocity' in part_spec
            velocity_vectors = coordinate.get_velocity_differences(
                part_spec.prop('velocity', part_indices[masks]),
                center_velocities[center_i],
            )
            velocity_vectors_rot = coordinate.get_coordinates_rotated(
                velocity_vectors, rotation_tensor
            )
            distance_vectors_rot = coordinate.get_coordinates_rotated(
                distance_vectors[masks], rotation_tensor
            )
            velocity_vectors_cyl = coordinate.get_velocities_in_coordinate_system(
                velocity_vectors_rot, distance_vectors_rot, 'cartesian', 'cylindrical'
            )

            # ensure that disk rotates in right-handed direction with median v_phi > 0
            if np.median(velocity_vectors_cyl[:, 1]) < 0:
                rotation_tensor[1] *= -1
                rotation_tensor[2] *= -1
        else:
            Say.say('! warning: no center velocities input to get_principal_axes()')
            Say.say('so direction/sign of minor axis rotation is ambiguous')

        principal_axes['rotation'].append(rotation_tensor)
        principal_axes['axis.ratios'].append(axis_ratios)

    for k in principal_axes:
        principal_axes[k] = np.array(principal_axes[k])

    if verbose:
        for center_i, axis_ratios in enumerate(principal_axes['axis.ratios']):
            Say.say(
                'host{}: axis ratios: min/maj = {:.3f}, min/med = {:.3f}, med/maj = {:.3f}'.format(
                    center_i + 1, axis_ratios[0], axis_ratios[1], axis_ratios[2]
                )
            )
        print()

    if return_single_array and np.shape(center_positions)[0] == 1:
        for k in principal_axes:
            principal_axes[k] = principal_axes[k][0]

    return principal_axes


# --------------------------------------------------------------------------------------------------
# halo/galaxy radius
# --------------------------------------------------------------------------------------------------
def get_halo_properties(
    part,
    species=['dark', 'star', 'gas'],
    virial_kind='200m',
    distance_limits=[1, 600],
    distance_bin_width=0.02,
    distance_log_scale=True,
    host_index=0,
    center_position=None,
    return_single_array=True,
    verbose=True,
):
    '''
    Compute halo radius according to virial_kind.
    Return this radius, the mass from each species within this radius, and indices of input particle
    species within this radius.

    Parameters
    ----------
    part : dict
        catalog of particles at snapshot
    species : str or list
        name[s] of particle species to use: 'all' = use all in dictionary
    virial_kind : str
        virial overdensity definition
            '200m' -> average density is 200 x matter
            '200c' -> average density is 200 x critical
            'vir' -> average density is Bryan & Norman
            'fof.100m' -> edge density is 100 x matter, for FoF(ll=0.168)
            'fof.60m' -> edge density is 60 x matter, for FoF(ll=0.2)
    distance_limits : list
        min and max distance to consider [kpc physical]
    distance_bin_width : float
        width of distance bin
    distance_log_scale : bool
        whether to use logarithmic scaling for distance bins
    host_index : int
        index of host halo to get stored position of (if not input center_position)
    center_position : array
        center position to use. if None, will use default center position in catalog
    return_single_array : bool
        whether to return array (instead of dict) if input single species
    verbose : bool
        whether to print radius and mass

    Returns
    -------
    halo_prop : dict
        dictionary of halo properties:
            radius : float
                halo radius [kpc physical]
            mass : float
                mass within radius [M_sun]
            indices : array
                indices of partices within radius (if get_part_indices)
    '''
    distance_limits = np.asarray(distance_limits)

    Say = io.SayClass(get_halo_properties)

    species = parse_species(part, species)
    center_position = parse_property(part, 'position', center_position, host_index)

    HaloProperty = halo_property.HaloPropertyClass(part.Cosmology, part.snapshot['redshift'])

    DistanceBin = binning.DistanceBinClass(
        distance_limits, width=distance_bin_width, log_scale=distance_log_scale, dimension_number=3
    )

    overdensity, reference_density = HaloProperty.get_overdensity(virial_kind, units='kpc physical')
    virial_density = overdensity * reference_density

    mass_cum_in_bins = np.zeros(DistanceBin.number)
    distancess = []

    for spec_i, spec_name in enumerate(species):
        distances = coordinate.get_distances(
            part[spec_name]['position'],
            center_position,
            part.info['box.length'],
            part.snapshot['scalefactor'],
            total_distance=True,
        )  # [kpc physical]
        distancess.append(distances)
        mass_in_bins = DistanceBin.get_histogram(distancess[spec_i], part[spec_name]['mass'])
        mass_in_bins = np.cumsum(mass_in_bins.astype(np.float64))  # avoid rounding error w cumsum
        # get mass within distance minimum, for computing cumulative values
        distance_indices = np.where(distancess[spec_i] < np.min(distance_limits))[0]
        mass_cum_in_bins += np.sum(part[spec_name]['mass'][distance_indices]) + mass_in_bins

    if part.info['has.baryons'] and len(species) == 1 and species[0] == 'dark':
        # correct for baryonic mass if analyzing only dark matter in baryonic simulation
        Say.say('! using only dark particles, so correcting for baryonic mass')
        mass_factor = 1 + part.Cosmology['omega_baryon'] / part.Cosmology['omega_matter']
        mass_cum_in_bins *= mass_factor

    # cumulative densities in bins
    density_cum_in_bins = mass_cum_in_bins / DistanceBin.volumes_cum

    # get smallest radius that satisfies virial density
    for d_bin_i in range(DistanceBin.number - 1):
        if (
            density_cum_in_bins[d_bin_i] >= virial_density
            and density_cum_in_bins[d_bin_i + 1] < virial_density
        ):
            # interpolate in log space
            log_halo_radius = np.interp(
                np.log10(virial_density),
                np.log10(density_cum_in_bins[[d_bin_i + 1, d_bin_i]]),
                DistanceBin.log_maxs[[d_bin_i + 1, d_bin_i]],
            )
            halo_radius = 10**log_halo_radius
            break
    else:
        Say.say(f'! cannot determine halo R_{virial_kind}')
        if density_cum_in_bins[0] < virial_density:
            Say.say(
                'distance min = {:.1f} kpc already is below virial density = {}'.format(
                    distance_limits.min(), virial_density
                )
            )
            Say.say('decrease distance_limits')
        elif density_cum_in_bins[-1] > virial_density:
            Say.say(
                'distance max = {:.1f} kpc still is above virial density = {}'.format(
                    distance_limits.max(), virial_density
                )
            )
            Say.say('increase distance_limits')
        else:
            Say.say('not sure why!')

        return

    # get maximum of V_circ = sqrt(G M(< r) / r)
    vel_circ_in_bins = constant.km_per_kpc * np.sqrt(
        constant.grav_kpc_msun_sec * mass_cum_in_bins / DistanceBin.maxs
    )
    vel_circ_max = np.max(vel_circ_in_bins)
    vel_circ_max_radius = DistanceBin.maxs[np.argmax(vel_circ_in_bins)]

    halo_mass = 0
    part_indices = {}
    for spec_i, spec_name in enumerate(species):
        masks = distancess[spec_i] < halo_radius
        halo_mass += np.sum(part[spec_name]['mass'][masks])
        part_indices[spec_name] = array.get_arange(part[spec_name]['mass'])[masks]

    if verbose:
        if verbose is not True:
            Say.print_function_name = False
        Say.say(
            '* R_{} = {:.0f} kpc\n* M_{} = {:.2e} Msun, log = {:.2f}\n* V_max = {:.0f} km/s'.format(
                virial_kind, halo_radius, virial_kind, halo_mass, np.log10(halo_mass), vel_circ_max
            )
        )

    halo_prop = {}
    halo_prop['radius'] = halo_radius
    halo_prop['mass'] = halo_mass
    halo_prop['vel.circ.max'] = vel_circ_max
    halo_prop['vel.circ.max.radius'] = vel_circ_max_radius
    if return_single_array and len(species) == 1:
        part_indices = part_indices[species[0]]
    halo_prop['indices'] = part_indices

    return halo_prop


def get_galaxy_properties(
    part,
    species_name='star',
    edge_kind='mass.percent',
    edge_value=90,
    axis_kind='',
    distance_max=20,
    distance_bin_width=0.02,
    distance_log_scale=True,
    host_index=0,
    center_position=None,
    rotation_tensor=None,
    other_axis_distance_limits=None,
    part_indices=None,
    verbose=True,
):
    '''
    Compute galaxy radius according to edge_kind.
    Return this radius, the mass of species_name within this radius, the indices of species_name
    particles within this radius, and rotation tensor (if applicable).

    Note: Because the initial aperture radius selection is 3-D spherical, if you compute for
    example R_90 and/or Z_90, which are defined in cylindrical coordinates, they will not be
    exactly 90% (or 90% * 90% = 81%) of this initial aperture mass. In practice, I find
    R_90 + Z_90 yields ~79% of total M(< 20 kpc). While perhaps a minus, the current method does
    have nice convergence properties on R_90, Z_90, and mass within them, depending only weakly
    on initial aperture for most m12 simulations.

    Parameters
    ----------
    part : dict
        catalog of particles at snapshot
    species_name : str
        name of particle species to use
    edge_kind : str
        method to define galaxy radius:
        'mass.percent' = radius at which edge_value (percent) of stellar mass within distance_max
        'density' = radius at which density is edge_value [log(M_sun / kpc^3)]
    edge_value : float
        value to use to define galaxy radius
    mass_percent : float
        percent of mass (out to distance_max) to define radius
    axis_kind : str
        'major', 'minor', 'both'
    distance_max : float
        maximum distance to consider [kpc physical]
    distance_bin_width : float
        width of distance bin
    distance_log_scale : bool
        whether to use logarithmic scaling for distance bins
    rotation_tensor : array
        rotation tensor that defines principal axes
    host_index : int
        index of host galaxy to get stored position and rotation tensor of (if not input them)
    center_position : array
        center position [kpc comoving]. if None, will use default center position in catalog
    other_axis_distance_limits : float
        min and max distances along other axis[s] to keep particles [kpc physical]
    part_indices : array
        star particle indices (if already know which ones are close)
    verbose : bool
        whether to print radius and mass of galaxy

    Returns
    -------
    gal_prop : dict
        dictionary of galaxy properties:
            radius or radius.major & radius.minor : float
                galaxy radius[s] [kpc physical]
            mass : float
                mass within radius[s] [M_sun]
            indices : array
                indices of partices within radius[s] (if get_part_indices)
            rotation : array
                eigen-vectors that defined rotation
    '''

    def _get_galaxy_radius_mass_indices(
        masses,
        distances,
        distance_limits,
        distance_bin_width,
        distance_log_scale,
        dimension_number,
        edge_kind,
        edge_value,
        edge_mass=None,
    ):
        '''
        Get the radius (height), inclosed mass within radius/height, and particle indices within
        radius/height, defined accordinge to edge_kind and edge_value.

        Parameters
        ----------
        masses : array
            masses of particles
        distances : array
            distances of particles
        distance_limits : list
            min and max distances to use [kpc physical]
        distance_bin_width : float
            width of distance bin
        distance_log_scale : bool
            whether to use logarithmic scaling for distance bins
        dimension_number : int
            number of spatial dimensions to use (if computing densities)
        edge_kind : str
            method to define galaxy radius
        edge_value : float
            value to use to define galaxy radius
        '''
        Say = io.SayClass(_get_galaxy_radius_mass_indices)

        DistanceBin = binning.DistanceBinClass(
            distance_limits,
            width=distance_bin_width,
            log_scale=distance_log_scale,
            dimension_number=dimension_number,
        )

        # get masses in distance bins, avoid rounding error with cumsum
        mass_in_bins = DistanceBin.get_histogram(distances, masses).astype(np.float64)

        if edge_kind == 'mass.percent':
            # get mass within distance minimum, for computing cumulative values
            d_indices = np.where(distances < np.min(distance_limits))[0]
            masses_cum = np.sum(masses[d_indices]) + np.cumsum(mass_in_bins)

            if edge_mass:
                mass = edge_mass
            else:
                mass = edge_value / 100 * masses_cum.max()

            try:
                # interpolate in log space
                log_radius = np.interp(
                    np.log10(mass), math.get_log(masses_cum), DistanceBin.log_maxs
                )
            except ValueError:
                Say.say('! cannot find galaxy radius - increase distance_max')
                return

        elif edge_kind == 'density':
            log_density_in_bins = math.get_log(mass_in_bins / DistanceBin.volumes)
            # use only bins with defined density (has particles)
            d_bin_indices = np.arange(DistanceBin.number)[np.isfinite(log_density_in_bins)]
            # get smallest radius that satisfies density threshold
            for d_bin_ii, d_bin_i in enumerate(d_bin_indices):
                d_bin_i_plus_1 = d_bin_indices[d_bin_ii + 1]
                if (
                    log_density_in_bins[d_bin_i] >= edge_value
                    and log_density_in_bins[d_bin_i_plus_1] < edge_value
                ):
                    # interpolate in log space
                    log_radius = np.interp(
                        edge_value,
                        log_density_in_bins[[d_bin_i_plus_1, d_bin_i]],
                        DistanceBin.log_maxs[[d_bin_i_plus_1, d_bin_i]],
                    )
                    break
            else:
                Say.say('! cannot find object radius - increase distance_max')
                return

        radius = 10**log_radius

        masks = distances < radius
        mass = np.sum(masses[masks])
        indices = array.get_arange(masses)[masks]

        return radius, mass, indices

    # start function
    Say = io.SayClass(get_galaxy_properties)

    distance_min = 0.001  # [kpc physical]
    distance_limits = [distance_min, distance_max]

    if edge_kind == 'mass.percent':
        # using cumulative value to define edge - stable enough to decrease bin with
        distance_bin_width *= 0.1

    part_spec = part[species_name]

    center_position = parse_property(part_spec, 'position', center_position, host_index)

    if part_indices is None or len(part_indices) == 0:
        part_indices = array.get_arange(part_spec['position'].shape[0])

    distance_vectors = coordinate.get_distances(
        part_spec['position'][part_indices],
        center_position,
        part.info['box.length'],
        part.snapshot['scalefactor'],
    )  # [kpc physical]
    distances = np.sqrt(np.sum(distance_vectors**2, 1))  # scalar total distances

    masks = distances < distance_max
    part_indices = part_indices[masks]
    distance_vectors = distance_vectors[masks]
    distances = distances[masks]

    masses = part_spec.prop('mass', part_indices)

    if verbose:
        if verbose is not True:
            Say.print_function_name = False
        mass_tot = part_spec['mass'].sum()
        Say.say(
            '* M_{},sim = {} Msun, log = {:.2f}'.format(
                species_name, io.get_string_from_numbers(mass_tot, digits=2), np.log10(mass_tot)
            )
        )
        Say.say(
            '* M_{}(< {:.0f} kpc) = {} Msun, log = {:.2f}'.format(
                species_name,
                distance_max,
                io.get_string_from_numbers(masses.sum(), digits=2),
                np.log10(masses.sum()),
            )
        )

    if axis_kind:
        # radius along 2-D major axes (projected radius) or along 1-D minor axis (height)
        assert axis_kind in ['major', 'minor', 'both']

        rotation_tensor = parse_property(part, 'rotation', rotation_tensor, host_index)

        distance_vectors = coordinate.get_coordinates_rotated(
            distance_vectors, rotation_tensor=rotation_tensor
        )

        distances_cyl = coordinate.get_positions_in_coordinate_system(
            distance_vectors, 'cartesian', 'cylindrical'
        )
        # get R and Z. assume symmetry, so make Z absolute for simplicity
        major_distances, minor_distances = distances_cyl[:, 0], distances_cyl[:, 2]
        minor_distances = np.abs(minor_distances)

        if axis_kind in ['major', 'minor']:
            if axis_kind == 'minor':
                dimension_number = 1
                distances = minor_distances
                other_distances = major_distances
            elif axis_kind == 'major':
                dimension_number = 2
                distances = major_distances
                other_distances = minor_distances

            if other_axis_distance_limits is not None and len(other_axis_distance_limits) > 0:
                masks = (other_distances >= min(other_axis_distance_limits)) * (
                    other_distances < max(other_axis_distance_limits)
                )
                distances = distances[masks]
                masses = masses[masks]
                part_indices = part_indices[masks]
    else:
        # spherical average
        dimension_number = 3

    gal_prop = {}

    if axis_kind == 'both':
        # initial guess - 3-D radius at edge_value
        galaxy_radius_3d, _galaxy_mass_3d, _indices = _get_galaxy_radius_mass_indices(
            masses,
            distances,
            distance_limits,
            distance_bin_width,
            distance_log_scale,
            3,
            edge_kind,
            edge_value,
        )

        galaxy_radius_major = galaxy_radius_3d
        axes_mass_dif = 1

        # iterate to get both major and minor axes
        iterate_count_max = 1000
        iterate_count = 0
        while axes_mass_dif > 0.01:
            iterate_count += 1
            if iterate_count > iterate_count_max:
                print(
                    f'! reached maximum allowed iterations = {iterate_count_max}'
                    + f' in computing R_{edge_value} and Z_{edge_value}'
                )
                break

            # get 1-D radius along minor axis
            masks = major_distances < galaxy_radius_major
            galaxy_radius_minor, galaxy_mass_minor, _indices = _get_galaxy_radius_mass_indices(
                masses[masks],
                minor_distances[masks],
                distance_limits,
                distance_bin_width,
                distance_log_scale,
                1,
                edge_kind,
                edge_value,
            )

            # get 2-D radius along major axes
            masks = minor_distances < galaxy_radius_minor
            galaxy_radius_major, galaxy_mass_major, _indices = _get_galaxy_radius_mass_indices(
                masses[masks],
                major_distances[masks],
                distance_limits,
                distance_bin_width,
                distance_log_scale,
                2,
                edge_kind,
                edge_value,
            )

            axes_mass_dif = abs(galaxy_mass_major - galaxy_mass_minor) / (
                0.5 * (galaxy_mass_major + galaxy_mass_minor)
            )

        masks = (major_distances < galaxy_radius_major) * (minor_distances < galaxy_radius_minor)

        gal_prop['radius.major'] = galaxy_radius_major
        gal_prop['radius.minor'] = galaxy_radius_minor
        gal_prop['mass'] = galaxy_mass_major
        gal_prop['log mass'] = np.log10(galaxy_mass_major)
        gal_prop['rotation'] = rotation_tensor
        gal_prop['indices'] = part_indices[masks]

        if verbose:
            Say.say(
                '* R_{},{:.0f} major, minor = {:.1f}, {:.1f} kpc'.format(
                    species_name, edge_value, galaxy_radius_major, galaxy_radius_minor
                )
            )

    else:
        galaxy_radius, galaxy_mass, indices = _get_galaxy_radius_mass_indices(
            masses,
            distances,
            distance_limits,
            distance_bin_width,
            distance_log_scale,
            dimension_number,
            edge_kind,
            edge_value,
        )

        gal_prop['radius'] = galaxy_radius
        gal_prop['mass'] = galaxy_mass
        gal_prop['log mass'] = np.log10(galaxy_mass)
        gal_prop['indices'] = part_indices[indices]

        if verbose:
            Say.say('* R_{},{:.0f} = {:.1f} kpc'.format(species_name, edge_value, galaxy_radius))

    if verbose:
        Say.say(
            '* M_{},{} = {} Msun, log = {:.2f}'.format(
                species_name,
                edge_value,
                io.get_string_from_numbers(gal_prop['mass'], digits=2),
                gal_prop['log mass'],
            )
        )

    return gal_prop


# --------------------------------------------------------------------------------------------------
# profiles of properties
# --------------------------------------------------------------------------------------------------
class SpeciesProfileClass(binning.DistanceBinClass):
    '''
    Get profiles of either histogram/sum or stastitics (such as average, median) of given
    property for given particle species.

    __init__ is defined via  binning.DistanceBinClass
    '''

    def get_profiles(
        self,
        part,
        species=['all'],
        property_name='',
        property_statistic='sum',
        weight_property='mass',
        host_index=0,
        center_position=None,
        center_velocity=None,
        rotation=None,
        other_axis_distance_limits=None,
        property_select={},
        part_indicess=None,
    ):
        '''
        Parse inputs into either get_sum_profiles() or get_statistics_profiles().
        If you know what you want, can skip this and jump to those functions.

        Parameters
        ----------
        part : dict
            catalog of particles
        species : str or list
            name[s] of particle species to compute mass from
        property_name : str
            name of property to get statistics of
        property_statistic : str
            statistic to get profile of: 'sum', 'sum.cum', 'density', 'density.cum', 'vel.circ'
        weight_property : str
            property to weight each particle by
        host_index : int
            index of host galaxy/halo to get stored position, velocity, and/or rotation tensor of
            (if not input them)
        center_position : array
            position of center
        center_velocity : array
            velocity of center
        rotation : bool or array
            whether to rotate particles - two options:
                (a) if input array of eigen-vectors, will define rotation axes
                (b) if True, will rotate to align with principal axes stored in species dictionary
        other_axis_distance_limits : float
            min and max distances along other axis[s] to keep particles [kpc physical]
        property_select : dict
            (other) properties to select on: names as keys and limits as values
        part_indicess : array (species number x particle number)
            indices of particles from which to select

        Returns
        -------
        pros : dict
            dictionary of profiles for each particle species
        '''
        if (
            'sum' in property_statistic
            or 'vel.circ' in property_statistic
            or 'density' in property_statistic
        ):
            pros = self.get_sum_profiles(
                part,
                species,
                property_name,
                host_index,
                center_position,
                rotation,
                other_axis_distance_limits,
                property_select,
                part_indicess,
            )
        else:
            pros = self.get_statistics_profiles(
                part,
                species,
                property_name,
                weight_property,
                host_index,
                center_position,
                center_velocity,
                rotation,
                other_axis_distance_limits,
                property_select,
                part_indicess,
            )

        for k in pros:
            if '.cum' in property_statistic or 'vel.circ' in property_statistic:
                pros[k]['distance'] = pros[k]['distance.cum']
                pros[k]['log distance'] = pros[k]['log distance.cum']
            else:
                pros[k]['distance'] = pros[k]['distance.mid']
                pros[k]['log distance'] = pros[k]['log distance.mid']

        return pros

    def get_sum_profiles(
        self,
        part,
        species=['all'],
        property_name='mass',
        host_index=0,
        center_position=None,
        rotation=None,
        other_axis_distance_limits=None,
        property_select={},
        part_indicess=None,
    ):
        '''
        Get profiles of summed quantity (such as mass or density) for given property for each
        input particle species.

        Parameters
        ----------
        part : dict
            catalog of particles
        species : str or list
            name[s] of particle species to compute mass from
        property_name : str
            property to get sum of
        host_index : int
            index of host galaxy/halo to get stored position or rotation tensor of (if not input)
        center_position : list
            center position
        rotation : bool or array
            whether to rotate particles - two options:
            (a) if input array of eigen-vectors, will define rotation axes
            (b) if True, will rotate to align with principal axes stored in species dictionary
        other_axis_distance_limits : float
            min and max distances along other axis[s] to keep particles [kpc physical]
        property_select : dict
            (other) properties to select on: names as keys and limits as values
        part_indicess : array (species number x particle number)
            indices of particles from which to select

        Returns
        -------
        pros : dict
            dictionary of profiles for each particle species
        '''
        if 'gas' in species and 'consume.time' in property_name:
            pros_mass = self.get_sum_profiles(
                part,
                species,
                'mass',
                host_index,
                center_position,
                rotation,
                other_axis_distance_limits,
                property_select,
                part_indicess,
            )

            pros_sfr = self.get_sum_profiles(
                part,
                species,
                'sfr',
                host_index,
                center_position,
                rotation,
                other_axis_distance_limits,
                property_select,
                part_indicess,
            )

            pros = pros_sfr
            for k in pros_sfr['gas']:
                if 'distance' not in k:
                    pros['gas'][k] = pros_mass['gas'][k] / pros_sfr['gas'][k] / 1e9

            return pros

        pros = {}

        Fraction = math.FractionClass()

        if np.isscalar(species):
            species = [species]
        if species == ['baryon']:
            # treat this case specially for baryon fraction
            species = ['gas', 'star', 'dark', 'dark2']
        species = parse_species(part, species)

        center_position = parse_property(part, 'position', center_position, host_index)
        part_indicess = parse_property(species, 'indices', part_indicess)

        assert 0 < self.dimension_number <= 3

        for spec_i, spec_name in enumerate(species):
            part_indices = part_indicess[spec_i]
            if part_indices is None or len(part_indices) == 0:
                part_indices = array.get_arange(part[spec_name].prop(property_name))

            if property_select:
                part_indices = catalog.get_indices_catalog(
                    part[spec_name], property_select, part_indices
                )

            prop_values = part[spec_name].prop(property_name, part_indices)

            if self.dimension_number == 3:
                # simple case: profile using scalar distance
                distances = coordinate.get_distances(
                    part[spec_name]['position'][part_indices],
                    center_position,
                    part.info['box.length'],
                    part.snapshot['scalefactor'],
                    total_distance=True,
                )  # [kpc physical]

            elif self.dimension_number in [1, 2]:
                # other cases: profile along R (2 major axes) or Z (minor axis)
                if rotation is not None:
                    if rotation is True:
                        rotation_tensor = parse_property(part, 'rotation', None, host_index)
                    else:
                        assert len(rotation) > 0
                        rotation_tensor = rotation

                distancess = get_distances_wrt_center(
                    part,
                    spec_name,
                    part_indices,
                    center_position,
                    rotation_tensor,
                    host_index,
                    'cylindrical',
                )
                # ensure all distances are positive definite
                distancess = np.abs(distancess)

                if self.dimension_number == 1:
                    # compute profile along minor axis Z
                    distances = distancess[:, 2]  # Z
                    other_distances = distancess[:, 0]  # R
                elif self.dimension_number == 2:
                    # compute profile along major axes R
                    distances = distancess[:, 0]  # R
                    other_distances = distancess[:, 2]  # Z

                if other_axis_distance_limits is not None and (
                    min(other_axis_distance_limits) > 0 or max(other_axis_distance_limits) < np.Inf
                ):
                    masks = (other_distances >= min(other_axis_distance_limits)) * (
                        other_distances < max(other_axis_distance_limits)
                    )
                    distances = distances[masks]
                    prop_values = prop_values[masks]

            # defined in DistanceBinClass
            pros[spec_name] = self.get_sum_profile(distances, prop_values)

        props = [pro_prop for pro_prop in pros[species[0]] if 'distance' not in pro_prop]
        props_dist = [pro_prop for pro_prop in pros[species[0]] if 'distance' in pro_prop]

        if property_name == 'mass':
            # create dictionary for baryonic mass
            if 'star' in species or 'gas' in species:
                spec_new = 'baryon'
                pros[spec_new] = {}
                for spec_name in np.intersect1d(species, ['star', 'gas']):
                    for pro_prop in props:
                        if pro_prop not in pros[spec_new]:
                            pros[spec_new][pro_prop] = np.array(pros[spec_name][pro_prop])
                        elif 'log' in pro_prop:
                            pros[spec_new][pro_prop] = math.get_log(
                                10 ** pros[spec_new][pro_prop] + 10 ** pros[spec_name][pro_prop]
                            )
                        else:
                            pros[spec_new][pro_prop] += pros[spec_name][pro_prop]

                for pro_prop in props_dist:
                    pros[spec_new][pro_prop] = pros[species[0]][pro_prop]
                species.append(spec_new)

            if len(species) > 1:
                # create dictionary for total mass
                spec_new = 'total'
                pros[spec_new] = {}
                for spec_name in np.setdiff1d(species, ['baryon', 'total']):
                    for pro_prop in props:
                        if pro_prop not in pros[spec_new]:
                            pros[spec_new][pro_prop] = np.array(pros[spec_name][pro_prop])
                        elif 'log' in pro_prop:
                            pros[spec_new][pro_prop] = math.get_log(
                                10 ** pros[spec_new][pro_prop] + 10 ** pros[spec_name][pro_prop]
                            )
                        else:
                            pros[spec_new][pro_prop] += pros[spec_name][pro_prop]

                for pro_prop in props_dist:
                    pros[spec_new][pro_prop] = pros[species[0]][pro_prop]
                species.append(spec_new)

                # create mass fraction wrt total mass
                for spec_name in np.setdiff1d(species, ['total']):
                    for pro_prop in ['sum', 'sum.cum']:
                        pros[spec_name][pro_prop + '.fraction'] = Fraction.get_fraction(
                            pros[spec_name][pro_prop], pros['total'][pro_prop]
                        )

                        if spec_name == 'baryon':
                            # units of cosmic baryon fraction
                            pros[spec_name][pro_prop + '.fraction'] /= (
                                part.Cosmology['omega_baryon'] / part.Cosmology['omega_matter']
                            )

            # create circular velocity := sqrt (G M(< r) / r)
            for spec_name in species:
                pros[spec_name]['vel.circ'] = halo_property.get_circular_velocity(
                    pros[spec_name]['sum.cum'], pros[spec_name]['distance.cum']
                )
                pros[spec_name]['vel.circ2'] = (
                    pros[spec_name]['vel.circ'] * pros[spec_name]['vel.circ']
                )

        return pros

    def get_statistics_profiles(
        self,
        part,
        species=['all'],
        property_name='',
        weight_property='mass',
        host_index=0,
        center_position=None,
        center_velocity=None,
        rotation=None,
        other_axis_distance_limits=None,
        property_select={},
        part_indicess=None,
    ):
        '''
        Get profiles of statistics (such as median, average) for given property for each
        input particle species.

        Parameters
        ----------
        part : dict
            catalog of particles
        species : str or list
            name[s] of particle species to compute mass from
        property_name : str
            name of property to get statistics of
        host_index : int
            index of host galaxy/halo to get stored position, velocity, and/or rotation tensor of
            (if not input them)
        weight_property : str
            property to weight each particle by
        center_position : array
            position of center
        center_velocity : array
            velocity of center
        rotation : bool or array
            whether to rotate particles - two options:
            (a) if input array of eigen-vectors, will define rotation axes
            (b) if True, will rotate to align with principal axes stored in species dictionary
        other_axis_distance_limits : float
            min and max distances along other axis[s] to keep particles [kpc physical]
        property_select : dict
            (other) properties to select on: names as keys and limits as values
        part_indicess : array or list
            indices of particles from which to select

        Returns
        -------
        pros : dict
            profiles for each particle species
        '''
        pros = {}

        species = parse_species(part, species)

        center_position = parse_property(part, 'position', center_position, host_index)
        if 'velocity' in property_name:
            center_velocity = parse_property(part, 'velocity', center_velocity, host_index)
        part_indicess = parse_property(species, 'indices', part_indicess)

        assert 0 < self.dimension_number <= 3

        for spec_i, spec_name in enumerate(species):
            prop_test = property_name
            if 'velocity' in prop_test:
                prop_test = 'velocity'  # treat velocity specially because compile below
            assert part[spec_name].prop(prop_test) is not None

            part_indices = part_indicess[spec_i]
            if part_indices is None or len(part_indices) == 0:
                part_indices = array.get_arange(part[spec_name].prop(property_name))

            if property_select:
                part_indices = catalog.get_indices_catalog(
                    part[spec_name], property_select, part_indices
                )

            weights = None
            if weight_property is not None and len(weight_property) > 0:
                weights = part[spec_name].prop(weight_property, part_indices)

            if 'velocity' in property_name:
                distance_vectors = coordinate.get_distances(
                    part[spec_name]['position'][part_indices],
                    center_position,
                    part.info['box.length'],
                    part.snapshot['scalefactor'],
                )  # [kpc physical]

                velocity_vectors = coordinate.get_velocity_differences(
                    part[spec_name]['velocity'][part_indices],
                    center_velocity,
                    part[spec_name]['position'][part_indices],
                    center_position,
                    part.info['box.length'],
                    part.snapshot['scalefactor'],
                    part.snapshot['time.hubble'],
                )

                # defined in DistanceBinClass
                pro = self.get_velocity_profile(distance_vectors, velocity_vectors, weights)

                pros[spec_name] = pro[property_name.replace('host.', '')]
                for prop_name, prop_values in pro.items():
                    if 'velocity' not in prop_name:
                        pros[spec_name][prop_name] = prop_values
            else:
                prop_values = part[spec_name].prop(property_name, part_indices)

                if self.dimension_number == 3:
                    # simple case: profile using total distance [kpc physical]
                    distances = coordinate.get_distances(
                        part[spec_name]['position'][part_indices],
                        center_position,
                        part.info['box.length'],
                        part.snapshot['scalefactor'],
                        total_distance=True,
                    )
                elif self.dimension_number in [1, 2]:
                    # other cases: profile along R (2 major axes) or Z (minor axis)
                    if rotation is not None:
                        if rotation is True:
                            rotation_tensor = parse_property(part, 'rotation', None, host_index)
                        else:
                            assert len(rotation) > 0
                            rotation_tensor = rotation

                    distancess = get_distances_wrt_center(
                        part,
                        spec_name,
                        part_indices,
                        center_position,
                        rotation_tensor,
                        host_index,
                        'cylindrical',
                    )
                    distancess = np.abs(distancess)

                    if self.dimension_number == 1:
                        # compute profile along minor axis Z
                        distances = distancess[:, 2]  # Z
                        other_distances = distancess[:, 0]  # R
                    elif self.dimension_number == 2:
                        # compute profile along 2 major axes R
                        distances = distancess[:, 0]  # R
                        other_distances = distancess[:, 2]  # Z

                    if other_axis_distance_limits is not None and (
                        min(other_axis_distance_limits) >= 0
                        or max(other_axis_distance_limits) < np.Inf
                    ):
                        masks = (other_distances >= min(other_axis_distance_limits)) * (
                            other_distances < max(other_axis_distance_limits)
                        )
                        distances = distances[masks]
                        prop_values = prop_values[masks]
                        if weights is not None and len(weights) > 0:
                            weights = weights[masks]

                # defined in DistanceBinClass
                pros[spec_name] = self.get_statistics_profile(distances, prop_values, weights)

        return pros
