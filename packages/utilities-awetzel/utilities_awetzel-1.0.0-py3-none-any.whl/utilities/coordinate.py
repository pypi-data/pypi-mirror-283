'''
Utility functions for positions and velocities.

@author:
    Andrew Wetzel <arwetzel@gmail.com>
    Jenna Samuel <jsamuel@ucdavis.edu>
'''

import numpy as np
from scipy import spatial

from . import array
from . import constant
from . import io


# --------------------------------------------------------------------------------------------------
# spatial dimensions
# --------------------------------------------------------------------------------------------------
def get_dimension_indices(dimension_number=None, coordinates=None):
    '''
    Input number of spatial dimensions or array of coordinates (positions or velocities).
    Get the number of spatial dimensions and the default spatial indices for sampling a numpy array.

    Parameters
    ----------
    dimension_number : int
        number of spatial dimensions
    coordinates : array
        2-D array of coordinates (positions or velocities)

    Returns
    -------
    dimension_indices : list
        indices of spatial dimensions, to use to sample a numpy array of coordinates
    '''
    if dimension_number is not None and dimension_number > 0:
        pass
    elif coordinates is not None and np.ndim(coordinates) == 2:
        dimension_number = coordinates.shape[1]
    else:
        raise ValueError('input dimension_number = f{dimension_number}, coordinates={coordinates}')

    # default indices to (sub)select array coordinates
    if dimension_number == 3:
        dimension_indices = [0, 1, 2]
    elif dimension_number == 2:
        # sample x and y (or R and phi)
        dimension_indices = [0, 1]
    elif dimension_number == 3:
        # sample z
        dimension_indices = [2]

    return dimension_indices


# --------------------------------------------------------------------------------------------------
# coordinate transformation
# --------------------------------------------------------------------------------------------------
def get_positions_in_coordinate_system(
    position_vectors, system_from='cartesian', system_to='cylindrical'
):
    '''
    Convert input 3-D position vectors from (cartesian, cylindrical, spherical) to:
        cartesian :
            x, y, z
        cylindrical :
            R (along major axes, absolute/unsigned)
            angle phi [0, 2 * pi)
            Z (along minor axis, signed)
        spherical :
            r (absolute/unsigned)
            angle theta [0, pi)
            angle phi [0, 2 * pi)

    Parameters
    ----------
    position_vectors : array (object number x 3)
        position[s]/distance[s] wrt a center

    Returns
    -------
    positions_new : array (object number x 3)
        position[s]/distance[s] in new coordiante system
    '''
    assert system_from in ('cartesian', 'cylindrical', 'spherical')
    assert system_to in ('cartesian', 'cylindrical', 'spherical')

    if system_from == system_to:
        return position_vectors

    position_vectors = np.asarray(position_vectors)
    if np.ndim(position_vectors) == 1:
        position_vectors = np.asarray([position_vectors])

    assert np.shape(position_vectors)[1] == 3

    positions_new = np.zeros(position_vectors.shape, dtype=position_vectors.dtype)

    if system_from == 'cartesian':
        if system_to == 'cylindrical':
            # R = sqrt(x^2 + y^2)
            positions_new[:, 0] = np.sqrt(np.sum(position_vectors[:, [0, 1]] ** 2, 1))
            # phi = arctan(y / x)
            positions_new[:, 1] = np.arctan2(position_vectors[:, 1], position_vectors[:, 0])
            positions_new[:, 1][positions_new[:, 1] < 0] += 2 * np.pi  # convert to [0, 2 * pi)
            # Z = z
            positions_new[:, 2] = position_vectors[:, 2]
        elif system_to == 'spherical':
            # r = sqrt(x^2 + y^2 + z^2)
            positions_new[:, 0] = np.sqrt(np.sum(position_vectors**2, 1))
            # theta = arccos(z / r)
            positions_new[:, 1] = np.arccos(position_vectors[:, 2] / positions_new[:, 0])
            # phi = arctan(y / x)
            positions_new[:, 2] = np.arctan2(position_vectors[:, 1], position_vectors[:, 0])
            positions_new[:, 2][positions_new[:, 2] < 0] += 2 * np.pi  # convert to [0, 2 * pi)

    elif system_from == 'cylindrical':
        if system_to == 'cartesian':
            # x = R * cos(phi)
            positions_new[:, 0] = position_vectors[:, 0] * np.cos(position_vectors[:, 1])
            # y = R * sin(phi)
            positions_new[:, 1] = position_vectors[:, 0] * np.sin(position_vectors[:, 1])
            # z = Z
            positions_new[:, 2] = position_vectors[:, 2]
        elif system_to == 'spherical':
            # r = sqrt(R^2 + Z^2)
            positions_new[:, 0] = np.sqrt(position_vectors[:, 0] ** 2 + position_vectors[:, 2] ** 2)
            # theta = arctan(R / Z)
            positions_new[:, 1] = np.arctan2(position_vectors[:, 0], position_vectors[:, 2])
            # phi = phi
            positions_new[:, 2] = position_vectors[:, 1]

    elif system_from == 'spherical':
        if system_to == 'cartesian':
            # x = r * sin(theta) * cos(phi)
            positions_new[:, 0] = (
                position_vectors[:, 0]
                * np.sin(position_vectors[:, 1])
                * np.cos(position_vectors[:, 2])
            )
            # y = r * sin(theta) * sin(phi)
            positions_new[:, 1] = (
                position_vectors[:, 0]
                * np.sin(position_vectors[:, 1])
                * np.sin(position_vectors[:, 2])
            )
            # z = r * cos(theta)
            positions_new[:, 2] = position_vectors[:, 0] * np.cos(position_vectors[:, 1])
        elif system_to == 'cylindrical':
            # R = r * sin(theta)
            positions_new[:, 0] = position_vectors[:, 0] * np.sin(position_vectors[:, 1])
            # phi = phi
            positions_new[:, 1] = position_vectors[:, 2]
            # Z = r * cos(theta)
            positions_new[:, 2] = position_vectors[:, 0] * np.cos(position_vectors[:, 1])

    # if only one position vector, return as 1-D array
    if len(positions_new) == 1:
        positions_new = positions_new[0]

    return positions_new


def get_velocities_in_coordinate_system(
    velocity_vectors, position_vectors, system_from='cartesian', system_to='cylindrical'
):
    '''
    Convert input 3-D velocity vectors from (cartesian, cylindrical, spherical) to:
        cartesian : x, y, z
        cylindrical : R (major axes), angle phi, Z (minor axis)
        spherical : r , angle theta, angle phi

    Parameters
    ----------
    velocity_vectors : array (object number x 3)
        velocity[s] wrt a center
    position_vectors : array (object number x 3)
        position[s]/distance[s] wrt a center

    Returns
    -------
    velocity_vectors_new : array (object number x 3)
        velocity[s] in new coordiante system
    '''
    assert system_from in ('cartesian', 'cylindrical', 'spherical')
    assert system_to in ('cartesian', 'cylindrical', 'spherical')

    if system_from == system_to:
        return velocity_vectors

    velocity_vectors = np.asarray(velocity_vectors)
    if np.ndim(velocity_vectors) == 1:
        velocity_vectors = np.asarray([velocity_vectors])

    position_vectors = np.asarray(position_vectors)
    if np.ndim(position_vectors) == 1:
        position_vectors = np.asarray([position_vectors])

    assert np.shape(velocity_vectors)[1] == 3 and np.shape(position_vectors)[1] == 3

    velocities_new = np.zeros(velocity_vectors.shape, dtype=velocity_vectors.dtype)

    if system_from == 'cartesian':
        # convert position vectors
        # R = {x,y}
        r = position_vectors[:, [0, 1]]
        r_norm = np.zeros(r.shape, position_vectors.dtype)
        # R_total = sqrt(x^2 + y^2)
        r_total = np.sqrt(np.sum(r**2, 1))
        masks = np.where(r_total > 0)[0]
        # need to do this way
        r_norm[masks] = np.transpose(r[masks].transpose() / r_total[masks])

        if system_to == 'cylindrical':
            # v_R = dot(v_{x,y}, R_norm)
            velocities_new[:, 0] = np.sum(velocity_vectors[:, [0, 1]] * r_norm, 1)
            # v_phi = cross(R_norm, v_{x,y})
            velocities_new[:, 1] = np.cross(r_norm, velocity_vectors[:, [0, 1]])
            # v_Z = v_z
            velocities_new[:, 2] = velocity_vectors[:, 2]
        elif system_to == 'spherical':
            # convert position vectors
            position_vectors_norm = np.zeros(position_vectors.shape, position_vectors.dtype)
            position_vectors_total = np.sqrt(np.sum(position_vectors**2, 1))
            masks = np.where(position_vectors_total > 0)[0]
            # need to do this way
            position_vectors_norm[masks] = np.transpose(
                position_vectors[masks].transpose() / position_vectors_total[masks]
            )

            # v_r = dot(v, r)
            velocities_new[:, 0] = np.sum(velocity_vectors * position_vectors_norm, 1)
            # v_theta
            a = np.transpose(
                [
                    r_norm[:, 0] * position_vectors_norm[:, 2],
                    r_norm[:, 1] * position_vectors_norm[:, 2],
                    -r_total / position_vectors_total,
                ]
            )
            velocities_new[:, 1] = np.sum(velocity_vectors * a, 1)
            # v_phi = cross(R_norm, v_{x,y})
            velocities_new[:, 2] = np.cross(r_norm, velocity_vectors[:, [0, 1]])

    elif system_from == 'cylindrical':
        raise ValueError(f'not yet support conversion from {system_from} to {system_to}')

    elif system_from == 'spherical':
        raise ValueError(f'not yet support conversion from {system_from} to {system_to}')

    # if only one velocity vector, return as 1-D array
    if len(velocities_new) == 1:
        velocities_new = velocities_new[0]

    return velocities_new


# --------------------------------------------------------------------------------------------------
# rotation of position or velocity
# --------------------------------------------------------------------------------------------------
def get_coordinates_rotated(coordinate_vectors, rotation_tensor=None, rotation_angles=None):
    '''
    Get 3-D coordinate[s] (distance or velocity vector[s]) that are rotated by input rotation
    vectors or input rotation angles.
    If rotation_tensor, need to input vectors that are orthogonal.
    If rotation_angles, rotate by rotation_angles[0] about x-axis, then by rotation_angles[1] about
    y-axis, then by rotation_angles[2] about z-axis.

    Parameters
    ----------
    coordinate_vectors : array (object number x dimension number)
        coordinate[s] (distance[s] or velocity[s]) wrt a center of rotation
    rotation_tensor : array
        *orthogonal* rotation vectors (such as max, med, min eigen-vectors)
    rotation_angles : array
        rotation angles about x-axis, y-axis, z-axis [radians]

    Returns
    -------
    coordinate_vectors_rotated : array (object number x dimension number)
        coordinate[s] (distance[s] or velocity[s]) in rotated basis
    '''
    dtype = coordinate_vectors.dtype
    # sanity check in case input coordinate_vectors as int
    if dtype == np.int32 or dtype == np.int64:
        dtype = np.float64

    if rotation_tensor is not None:
        # sanity check - ensure input rotation vectors are orthogonal
        tolerance = 1e-6
        if (
            np.abs(np.dot(rotation_tensor[0], rotation_tensor[1])) > tolerance
            or np.abs(np.dot(rotation_tensor[0], rotation_tensor[2])) > tolerance
            or np.abs(np.dot(rotation_tensor[1], rotation_tensor[2])) > tolerance
        ):
            raise ValueError('input rotation_tensor is not orthogonal')

    elif rotation_angles is not None:
        m11 = np.cos(rotation_angles[1]) * np.cos(rotation_angles[2])
        m12 = np.cos(rotation_angles[0]) * np.sin(rotation_angles[2]) + np.sin(
            rotation_angles[0]
        ) * np.sin(rotation_angles[1]) * np.cos(rotation_angles[2])
        m13 = np.sin(rotation_angles[0]) * np.sin(rotation_angles[2]) - np.cos(
            rotation_angles[0]
        ) * np.sin(rotation_angles[1]) * np.cos(rotation_angles[2])
        m21 = -np.cos(rotation_angles[1]) * np.sin(rotation_angles[2])
        m22 = np.cos(rotation_angles[0]) * np.cos(rotation_angles[2]) - np.sin(
            rotation_angles[0]
        ) * np.sin(rotation_angles[1]) * np.sin(rotation_angles[2])
        m23 = np.sin(rotation_angles[0]) * np.cos(rotation_angles[2]) + np.cos(
            rotation_angles[0]
        ) * np.sin(rotation_angles[1]) * np.sin(rotation_angles[2])
        m31 = np.sin(rotation_angles[1])
        m32 = -np.sin(rotation_angles[0]) * np.cos(rotation_angles[1])
        m33 = np.cos(rotation_angles[0]) * np.cos(rotation_angles[1])

        rotation_tensor = np.array([[m11, m12, m13], [m21, m22, m23], [m31, m32, m33]], dtype=dtype)

    else:
        raise ValueError('need to input either rotation angles or rotation vectors')

    # have to do this way
    coordinate_vectors_rotated = np.asarray(
        np.dot(coordinate_vectors, rotation_tensor.transpose()), dtype=dtype
    )

    return coordinate_vectors_rotated


def get_principal_axes(position_vectors, weights=None, use_moi=False, verbose=True):
    '''
    Compute principal axes of input position_vectors (which should be wrt a center),
    defined via the moment of inertia tensor.
    Get reverse-sorted rotation_tensor and axis ratios of these principal axes.

    Parameters
    ----------
    position_vectors : array (object number x dimension number)
        position[s] or distance[s] wrt a center
    weights : array
        weight for each position (usually mass) - if None, assume all have same weight
    use_moi : bool
        whether to use the moment of inertia tensor, instead of the second moment of the
        mass distribution, forthe diagonal components input to get the rotation tensor
        this choice only affect the resultant axis ratios, not the resultant rotation tensor
    verbose : bool
        whether to print axis ratios

    Returns
    -------
    rotation_tensor : array
        max, med, min eigen-vectors that define the rotation tensor
    axis_ratios : array
        ratios of principal axes
    '''
    if weights is None or len(weights) == 0:
        weights = 1
    else:
        weights = weights / np.median(weights)

    if position_vectors.shape[1] == 3:
        # 3-D
        if use_moi:
            # use moment of inertia to define for diagonal terms
            xx = np.sum(weights * (position_vectors[:, 1] ** 2 + position_vectors[:, 2] ** 2))
            yy = np.sum(weights * (position_vectors[:, 0] ** 2 + position_vectors[:, 2] ** 2))
            zz = np.sum(weights * (position_vectors[:, 0] ** 2 + position_vectors[:, 1] ** 2))
            xy = yx = np.sum(weights * position_vectors[:, 0] * position_vectors[:, 1])
            xz = zx = np.sum(weights * position_vectors[:, 0] * position_vectors[:, 2])
            yz = zy = np.sum(weights * position_vectors[:, 1] * position_vectors[:, 2])

            moi_tensor = [[xx, -xy, -xz], [-yx, yy, -yz], [-zx, -zy, zz]]
        else:
            # default: use second moment of mass distribution for diagonal terms
            xx = np.sum(weights * position_vectors[:, 0] ** 2)
            yy = np.sum(weights * position_vectors[:, 1] ** 2)
            zz = np.sum(weights * position_vectors[:, 2] ** 2)
            xy = yx = np.sum(weights * position_vectors[:, 0] * position_vectors[:, 1])
            xz = zx = np.sum(weights * position_vectors[:, 0] * position_vectors[:, 2])
            yz = zy = np.sum(weights * position_vectors[:, 1] * position_vectors[:, 2])

            moi_tensor = [[xx, xy, xz], [yx, yy, yz], [zx, zy, zz]]

    elif position_vectors.shape[1] == 2:
        # 2-D
        xx = np.sum(weights * position_vectors[:, 0] ** 2)
        yy = np.sum(weights * position_vectors[:, 1] ** 2)
        xy = yx = np.sum(weights * position_vectors[:, 0] * position_vectors[:, 1])

        moi_tensor = [[xx, xy], [yx, yy]]

    eigen_values, rotation_tensor = np.linalg.eig(moi_tensor)

    # order eigen-vectors by eigen-values, from largest to smallest
    eigen_indices_sorted = np.argsort(eigen_values)[::-1]
    eigen_values = eigen_values[eigen_indices_sorted]
    # eigen_values /= eigen_values.max()  # renormalize to 1
    # make rotation_tensor[0, 1, 2] be eigen_vectors that correspond to eigen_values[0, 1, 2]
    rotation_tensor = rotation_tensor.transpose()[eigen_indices_sorted]
    # ensure that rotation tensor satisfies right-hand rule
    rotation_tensor[2] = np.cross(rotation_tensor[0], rotation_tensor[1])

    if position_vectors.shape[1] == 3:
        axis_ratios = np.sqrt(
            [
                eigen_values[2] / eigen_values[0],
                eigen_values[2] / eigen_values[1],
                eigen_values[1] / eigen_values[0],
            ]
        )

        if verbose:
            print(
                '* principal axes:  min/maj = {:.3f}, min/med = {:.3f}, med/maj = {:.3f}'.format(
                    axis_ratios[0], axis_ratios[1], axis_ratios[2]
                )
            )

    elif position_vectors.shape[1] == 2:
        axis_ratios = eigen_values[1] / eigen_values[0]

        if verbose:
            print('* principal axes:  min/maj = {:.3f}'.format(axis_ratios))

    return rotation_tensor, axis_ratios


# --------------------------------------------------------------------------------------------------
# position distances
# --------------------------------------------------------------------------------------------------
def get_positions_periodic(positions, periodic_length=None):
    '''
    Get position in range [0, periodic_length).

    Parameters
    ----------
    positions : float or array
    periodic_length : float
        periodicity length (if none, return array as is)
    '''
    if periodic_length is None:
        return positions

    if np.isscalar(positions):
        if positions >= periodic_length:
            positions -= periodic_length
        elif positions < 0:
            positions += periodic_length
    else:
        positions[positions >= periodic_length] -= periodic_length
        positions[positions < 0] += periodic_length

    return positions


def get_position_differences(position_difs, periodic_length=None):
    '''
    Get distance / separation vector, in range [-periodic_length/2, periodic_length/2).

    Parameters
    ----------
    position_difs : array
        position difference[s]
    periodic_length : float
        periodicity length (if none, return array as is)
    '''
    if not periodic_length:
        return position_difs
    else:
        if np.isscalar(periodic_length) and periodic_length <= 1:
            print(f'! got unusual periodic_length = {periodic_length}')

    if np.isscalar(position_difs):
        if position_difs >= 0.5 * periodic_length:
            position_difs -= periodic_length
        elif position_difs < -0.5 * periodic_length:
            position_difs += periodic_length
    else:
        position_difs[position_difs >= 0.5 * periodic_length] -= periodic_length
        position_difs[position_difs < -0.5 * periodic_length] += periodic_length

    return position_difs


def get_distances(
    positions_1=None, positions_2=None, periodic_length=None, scalefactor=None, total_distance=False
):
    '''
    Get vector or total/scalar distance[s] between input position vectors.
    If input scale-factors, will convert distance from comoving to physical.

    Parameters
    ----------
    positions_1 : array
        position[s]
    positions_2 : array
        position[s]
    periodic_length : float
        periodic length (if none, not use periodic)
    scalefactor : float or array
        expansion scale-factor (to convert comoving to physical)
    total : bool
        whether to compute total/scalar (instead of vector) distance

    Returns
    -------
    distances : array (object number x dimension number, or object number)
        vector or total/scalar distance[s]
    '''
    if not isinstance(positions_1, np.ndarray):
        positions_1 = np.array(positions_1)
    if not isinstance(positions_2, np.ndarray):
        positions_2 = np.array(positions_2)

    if len(positions_1.shape) == 1 and len(positions_2.shape) == 1:
        shape_pos = 0
    else:
        shape_pos = 1

    distances = get_position_differences(positions_1 - positions_2, periodic_length)

    if total_distance:
        distances = np.sqrt(np.sum(distances**2, shape_pos))

    if scalefactor is not None:
        if scalefactor > (1 + 1e-4) or scalefactor <= 0:
            print(f'! got unusual scalefactor = {scalefactor}')
        distances *= scalefactor

    return distances


def get_distances_angular(positions_1=None, positions_2=None, sphere_angle=360):
    '''
    Get angular separation[s] between input positions, valid for small separations.

    Parameters
    ----------
    positions_1, positions_2 : arrays
        positions in [RA, dec]
    sphere_angle : float
        angular size of sphere 360 [degrees], 2 * pi [radians]

    Returns
    -------
    angular distances : array (object number x angular dimension number)
    '''
    if sphere_angle == 360:
        angle_scale = constant.radian_per_degree
    elif sphere_angle == 2 * np.pi:
        angle_scale = 1
    else:
        raise ValueError(f'angle of sphere = {sphere_angle} does not make sense')

    if np.ndim(positions_1) == 1 and positions_1.size == 2:
        ras_1, decs_1 = positions_1[0], positions_1[1]
    else:
        ras_1, decs_1 = positions_1[:, 0], positions_1[:, 1]

    if np.ndim(positions_2) == 1 and positions_2.size == 2:
        ras_2, decs_2 = positions_2[0], positions_2[1]
    else:
        ras_2, decs_2 = positions_2[:, 0], positions_2[:, 1]

    return np.sqrt(
        (
            get_position_differences(ras_1 - ras_2, sphere_angle)
            * np.cos(angle_scale * 0.5 * (decs_1 + decs_2))
        )
        ** 2
        + (decs_1 - decs_2) ** 2
    )


# --------------------------------------------------------------------------------------------------
# velocity conversion
# --------------------------------------------------------------------------------------------------
def get_velocity_differences(
    velocity_vectors_1=None,
    velocity_vectors_2=None,
    position_vectors_1=None,
    position_vectors_2=None,
    periodic_length=None,
    scalefactor=None,
    hubble_time=None,
    total_velocity=False,
):
    '''
    Get relative velocity[s] [km/s] between input velocity vectors.
    If input positions as well, add Hubble flow to velocities.

    Parameters
    ----------
    velocity_vectors_1 : array (object number x dimension number)
        velocity[s] [km/s]
    velocity_vectors_2 : array (object number x dimension number)
        velocity[s]  [km/s]
    position_vectors_1 : array (object number x dimension number)
        position[s] associated with velocity_vector_1 [kpc comoving]
    position_vectors_2 : array (object number x dimension number)
        position[s] associated with velocity_vector_2 [kpc comoving]
    periodic_length : float
        periodicity length [kpc comoving]
    scalefactor : float
        expansion scale-factor
    hubble_time : float
        1 / H(z) [Gyr]
    total_velocity : bool
        whether to compute total/scalar (instead of vector) velocity

    Returns
    -------
    velocity_difs  : array (object number x dimension number, or object number)
        velocity differences [km/s]
    '''
    if np.ndim(velocity_vectors_1) == 1 and np.ndim(velocity_vectors_1) == 1:
        dimension_shape = 0
    else:
        dimension_shape = 1

    velocity_difs = velocity_vectors_1 - velocity_vectors_2  # [km/s]

    if position_vectors_1 is not None and position_vectors_2 is not None:
        # add hubble flow: dr/dt = a * dx/dt + da/dt * x = a(t) * dx/dt + r * H(t)
        # [kpc / Gyr]
        vels_hubble = (
            scalefactor
            / hubble_time
            * get_distances(position_vectors_1, position_vectors_2, periodic_length)
        )
        vels_hubble *= constant.km_per_kpc / constant.sec_per_Gyr  # [km/s]
        velocity_difs += vels_hubble

    if total_velocity:
        velocity_difs = np.sqrt(np.sum(velocity_difs**2, dimension_shape))

    return velocity_difs


# --------------------------------------------------------------------------------------------------
# center of mass: position and velocity
# --------------------------------------------------------------------------------------------------
def get_center_position(
    positions,
    weights=None,
    periodic_length=None,
    position_number_min=32,
    center_position=None,
    distance_max=np.Inf,
):
    '''
    Get position of center of mass, using iterative zoom-in.

    Parameters
    ----------
    positions : array (particle number x dimension number)
        position[s]
    weights : array
        weight for each position (usually mass) - if None, assume all have same weight
    periodic_length : float
        periodic box length
    position_number_min : int
        minimum number of positions within distance to keep zooming in
    center_position : array
        initial center position to use
    distance_max : float
        maximum distance to consider initially

    Returns
    -------
    center_position : array
        position vector of center of mass
    '''
    distance_bins = np.array(
        [
            np.Inf,
            1000,
            700,
            500,
            300,
            200,
            150,
            100,
            70,
            50,
            30,
            20,
            15,
            10,
            7,
            5,
            3,
            2,
            1.5,
            1,
            0.7,
            0.5,
            0.3,
            0.2,
            0.15,
            0.1,
            0.07,
            0.05,
            0.03,
            0.02,
            0.015,
            0.01,
            0.007,
            0.005,
            0.003,
            0.002,
            0.0015,
            0.001,
        ]
    )
    distance_bins = distance_bins[distance_bins <= distance_max]

    if weights is not None:
        assert positions.shape[0] == weights.size
        # normalize weights by median, improves numerical stability
        weights = np.asarray(weights) / np.median(weights)

    if center_position is None or len(center_position) == 0:
        center_position = np.zeros(positions.shape[1], positions.dtype)
    else:
        center_position = np.array(center_position, positions.dtype)

    if positions.shape[0] > 2147483647:
        idtype = np.int64
    else:
        idtype = np.int32
    part_indices = np.arange(positions.shape[0], dtype=idtype)

    for dist_i, dist_max in enumerate(distance_bins):
        # direct method ----------
        distance2s = (
            get_position_differences(positions[part_indices] - center_position, periodic_length)
            ** 2
        )
        distance2s = np.sum(distance2s, 1)

        # get particles within distance max
        masks = distance2s < dist_max**2
        part_indices_dist = part_indices[masks]

        # store particles slightly beyond distance max for next interation
        masks = distance2s < (1.5 * dist_max) ** 2
        part_indices = part_indices[masks]

        # kd-tree method ----------
        # if dist_i == 0:
        # create tree if this is the first distance bin
        #    KDTree = spatial.KDTree(positions, boxsize=part.info['box.length'])
        #    particle_number_max = positions.shape[0]

        # distances, indices = KDTree.query(
        #    center_position, particle_number_max, distance_upper_bound=dist_max, workers=2)

        # masks = (distances < dist_max)
        # part_indices_dist = indices[masks]
        # particle_number_max = part_indices_dist.size

        # check whether reached minimum total number of particles within distance
        # but force at least one loop over distance bins to get *a* center
        if part_indices_dist.size <= position_number_min and dist_i > 0:
            return center_position

        if weights is None:
            weights_use = weights
        else:
            weights_use = weights[part_indices_dist]

        # ensure that np.average uses 64-bit internally for accuracy, but returns as input dtype
        center_position = np.average(
            positions[part_indices_dist].astype(np.float64), 0, weights_use
        ).astype(positions.dtype)

    return center_position


def get_center_velocity(
    velocities,
    weights=None,
    positions=None,
    center_position=None,
    distance_max=20,
    periodic_length=None,
):
    '''
    Get velocity of center of mass.
    If no input masses, assume all masses are the same.

    Parameters
    ----------
    velocities : array (particle number x dimension_number)
        velocity[s]
    weights : array
        weight for each position (usually mass) - if None, assume all have same weight
    positions : array (particle number x dimension number)
        positions, if want to select by this
    center_position : array
        center position, if want to select by this
    distance_max : float
        maximum position difference from center to use particles
    periodic_length : float
        periodic box length

    Returns
    -------
    center_velocity : array
        velocity vector of center of mass
    '''
    masks = np.full(velocities.shape[0], True)

    # ensure that use only finite values
    for dimen_i in range(velocities.shape[1]):
        masks *= np.isfinite(velocities[:, dimen_i])

    if positions is not None and center_position is not None and len(center_position) > 0:
        assert velocities.shape == positions.shape
        distance2s = np.sum(
            get_position_differences(positions - center_position, periodic_length) ** 2, 1
        )
        masks *= distance2s < distance_max**2

    if weights is not None:
        assert velocities.shape[0] == weights.size
        # normalizing weights by median seems to improve numerical stability
        weights = weights[masks] / np.median(weights[masks])

    if not masks.any():
        print('! cannot compute host/center velocity')
        print('  no positions within distance_max = {:.3f} kpc comoving'.format(distance_max))
        print('  nearest = {:.3f} kpc comoving'.format(np.sqrt(distance2s.min())))
        return np.r_[np.nan, np.nan, np.nan]

    # ensure that np.average uses 64-bit internally for accuracy, but returns as input dtype
    return np.average(velocities[masks].astype(np.float64), 0, weights).astype(velocities.dtype)


# --------------------------------------------------------------------------------------------------
# neighbors
# --------------------------------------------------------------------------------------------------
def get_neighbors(
    center_positions,
    neig_positions=None,
    neig_distance_max=1e10,
    neig_number_max=3000,
    periodic_length=None,
    neig_ids=None,
    exclude_self=True,
    return_lists=False,
    verbose=True,
    workers=2,
):
    '''
    Get distances and indices of neig_number_max nearest neig_positions relative to
    center_positions, using k-d tree.

    Parameters
    ----------
    center_positions : array (object number x dimension number)
        positions around which to get neighbors
    neig_positions : array (object number x dimension number)
        positions of neighbors. If None, use center_positions.
    neig_distance_max : float
        maximum distance for neighbors
    neig_number_max : int
        maximum number of neighbors per center
    periodic_length : float
        periodic length
    neig_ids : array
        ids of neighbors to return instead of indices of neig_positions
    exclude_self : bool
        whether to exclude any neighbors at 0 distance (primarily, to exclude self)
    return_lists : bool
        whether to return neig_distancess and neig_indicess as lists, instead of numpy arrays
    verbose : bool
        whether to print diagnostics along the way
    workers : int
        number of parallel processes to use in k-d tree

    Returns
    -------
    neig_distances : list of arrays
        distances of neighbors for each center position
    neig_indices: list of arrays
        indices (of neig_positions array) or ids (of input neig_ids array) of neighbors
        for each center position
    '''
    Say = io.SayClass(get_neighbors)

    # ensure that position arrays are object number x dimension number
    if np.ndim(center_positions) == 1:
        center_positions = np.array([center_positions])
    if neig_positions is None:
        neig_positions = center_positions
    elif np.ndim(neig_positions) == 1:
        neig_positions = np.array([neig_positions])
    if center_positions.shape[1] != neig_positions.shape[1]:
        raise ValueError(
            'center_positions.shape[1] = {} != neig_positions.shape[1] {}'.format(
                center_positions.shape[1], neig_positions.shape[1]
            )
        )
    center_number = center_positions.shape[0]
    neig_number = neig_positions.shape[0]
    assert neig_distance_max >= 0
    assert isinstance(neig_number_max, int)

    if periodic_length and neig_distance_max >= 0.5 * periodic_length:
        Say.say('! input neighbor distance max = {:.3f}'.format(neig_distance_max))
        Say.say('which is > 0.5 x periodic_length ({:.3f})'.format(periodic_length))
        Say.say(
            'imposing distance max = 0.5 * periodic_length = {:.3f}'.format(0.5 * periodic_length)
        )
        neig_distance_max = np.clip(neig_distance_max, 0, 0.5 * periodic_length)

    if verbose:
        d_max = io.get_string_from_numbers(neig_distance_max, 3, strip=False)
        Say.say(
            f'finding up to {neig_number_max} neighbors at distance <= {d_max}'
            + f' around {center_number} centers'
        )

        if periodic_length:
            Say.say('using periodic boundary of length = {:.3f}'.format(periodic_length))

    if exclude_self:
        neig_number_max += 1

    KDTree = spatial.KDTree(neig_positions, boxsize=periodic_length)

    if verbose:
        Say.say(f'built kd-tree for {neig_number} neighbor positions')

    neig_distancess, neig_indicess = KDTree.query(
        center_positions,
        neig_number_max,
        distance_upper_bound=neig_distance_max,
        workers=workers,
    )

    reach_neig_number_max = np.sum(neig_distancess[:, -1] < np.Inf)
    if reach_neig_number_max > 0:
        fraction = 100 * reach_neig_number_max / center_number
        if exclude_self:
            neig_number_max -= 1
        Say.say(
            '! {} ({:.1f}%) centers reached neig_number_max = {}'.format(
                reach_neig_number_max, fraction, neig_number_max
            )
        )
        Say.say('you should increase neig_number_max to ensure a complete neighbor sample!')
    elif verbose:
        neig_number_got_max = np.sum(neig_distancess < np.Inf, 1).max()
        Say.say(f'got maximum number of neighbors = {neig_number_got_max}')

    if exclude_self:
        # check if any first entry is at 0 distance, if so, exclude it (self)
        masks = neig_distancess[:, 0] < 1e-10
        neig_distancess[masks, :-1] = neig_distancess[masks, 1:]  # shift array left by 1
        neig_distancess[masks, -1] = np.Inf  # fill in last value as null
        neig_indicess[masks, :-1] = neig_indicess[masks, 1:]  # shift array left by 1
        neig_indicess[masks, -1] = np.max(neig_indicess)  # fill in last value as null

    if verbose:
        masks = neig_distancess <= neig_distance_max
        Say.say(
            'got {:d} neighbors in distance range = [{}, {}]'.format(
                neig_distancess[masks].size,
                io.get_string_from_numbers(neig_distancess[masks].min(), 3, strip=True),
                io.get_string_from_numbers(neig_distancess[masks].max(), 3, strip=True),
            )
        )

    # ensure safely negative indices for null values
    masks = neig_distancess > neig_distance_max
    neig_indicess[masks] = -(max(center_number, neig_number) + 1)

    if neig_ids is not None and len(neig_ids):
        # convert neighbor position indices to input neighbor ids
        masks = neig_distancess <= neig_distance_max
        neig_indicess[masks] = neig_ids[neig_indicess[masks]]
        neig_indicess = neig_indicess.astype(neig_ids.dtype)

    # convert to data type of input positions
    neig_distancess = neig_distancess.astype(center_positions.dtype)

    if return_lists:
        # convert numpy array to list of arrays of non-null values
        neig_distancess_t = np.array(neig_distancess)
        neig_indicess_t = np.array(neig_indicess)
        neig_distancess = [np.array([], dtype=neig_distancess.dtype) for _ in range(center_number)]
        neig_indicess = [np.array([], dtype=neig_indicess.dtype) for _ in range(center_number)]
        for ci in range(center_number):
            masks = (neig_distancess_t[ci] <= neig_distance_max) * (neig_distancess_t[ci] > 1e-10)
            neig_distancess[ci] = neig_distancess_t[ci, masks]
            neig_indicess[ci] = neig_indicess_t[ci, masks]

    return neig_distancess, neig_indicess


def get_fof_groups(
    positions,
    linking_length,
    member_number_min=10,
    periodic_length=None,
    ids=None,
    verbose=True,
):
    '''
    Get list of FoF groups using input linking_length applied to positions, using k-d tree.

    Parameters
    ----------
    positions : array (object number x dimension number)
        positions to get groups of
    linking_length : float
        maximum distance to link neighbors into a group
    member_number_min : int
        minimum number of positions in a group to keep it
    periodic_length : float
        periodic length
    ids : array
        id for each position, to return instead of index of each position
    verbose : bool
        whether to print diagnostics along the way

    Returns
    -------
    groups : list of arrays
        indices of members of groups
    '''
    Say = io.SayClass(get_fof_groups)

    assert linking_length > 0
    assert member_number_min > 1

    # ensure that position arrays are object number x dimension number
    if np.ndim(positions) == 1:
        positions = np.array([positions])
    position_number = positions.shape[0]
    assert position_number > 0

    d_max = io.get_string_from_numbers(linking_length, 3, strip=True)
    if periodic_length is not None and periodic_length > 0:
        pl = io.get_string_from_numbers(periodic_length, 3, strip=True)

    if verbose:
        Say.say(
            f'finding FoF groups with >= {member_number_min} members'
            + f' using linking length = {d_max} kpc'
        )
        if periodic_length:
            Say.say(f'and using periodic boundary length = {pl}')

        Say.say(f'input {position_number:,} positions')
    if periodic_length and linking_length >= 0.5 * periodic_length:
        Say.say(f'! input linking_length = {d_max} > 0.5 * periodic_length ({pl})')
        linking_length = np.clip(linking_length, 0, 0.5 * periodic_length)
        d_max = io.get_string_from_numbers(linking_length, 3, strip=True)
        Say.say(f'imposing linking_length = 0.5 * periodic_length = {d_max}')

    KDTree = spatial.KDTree(positions, boxsize=periodic_length)
    pairs = KDTree.query_pairs(linking_length, output_type='ndarray')  # returns pairs [i,j], i < j

    if verbose:
        Say.say(f'found {pairs.shape[0]:,} pairs within linking length')

    # sort pairs by index of first in pair
    pairs = pairs[np.argsort(pairs[:, 0])]

    int_dtype = array.parse_int_dtype(position_number)
    group_indices = array.get_array_null(position_number)
    group_number = 0
    groups = []

    for p0index, p1index in pairs:
        p0_group_index = group_indices[p0index]
        p1_group_index = group_indices[p1index]

        if p0_group_index < 0 and p1_group_index < 0:
            # neither position is in a group, start a new one
            groups.append([p0index, p1index])
            group_indices[p0index] = group_number
            group_indices[p1index] = group_number
            group_number += 1

        elif p0_group_index >= 0 and p1_group_index < 0:
            # first position is in a group, but second one is not, so add it
            groups[p0_group_index].append(p1index)
            group_indices[p1index] = p0_group_index

        elif p0_group_index < 0 and p1_group_index >= 0:
            # second position is in a group, but first one is not, add it
            groups[p1_group_index].append(p0index)
            group_indices[p0index] = p1_group_index

        elif p0_group_index >= 0 and p1_group_index >= 0:
            # both position are in a group
            if p0_group_index == p1_group_index:
                # both are in the same group, nothing more to do
                pass
            else:
                # need to join 2 different groups - add to group with smallest index
                if p0_group_index < p1_group_index:
                    group_index = p0_group_index
                    group_index_old = p1_group_index
                else:
                    group_index = p1_group_index
                    group_index_old = p0_group_index

                # add the second group to the first one
                groups[group_index].extend(groups[group_index_old])
                # remove the second group from list as a separate group
                groups[group_index_old] = []
                # update the group index for positions in the second group
                masks = group_indices == group_index_old
                group_indices[masks] = group_index

    # convert list of lists to list of arrays, sorted by index
    groups_keep = []
    group_member_number_max = 0
    for pindices in groups:
        if len(pindices) >= member_number_min:
            if ids is not None and len(ids):
                # convert index of each position to input id
                pindices = ids[pindices]
            pindices = np.asarray(pindices, dtype=int_dtype)
            if pindices.size > group_member_number_max:
                group_member_number_max = pindices.size
            groups_keep.append(pindices)
    groups = groups_keep

    if verbose:
        group_number = len(groups)
        if group_number > 0:
            number_in_group = np.concatenate(groups).size
        else:
            number_in_group = 0
        fraction_in_group = '{:.1f}'.format(100 * number_in_group / position_number)
        Say.say(
            f'got {group_number:,} FoF groups,'
            + f' comprising {number_in_group:,} ({fraction_in_group}%) members'
        )
        Say.say(f'largest group has {group_member_number_max} members')

    return groups


# --------------------------------------------------------------------------------------------------
# volume of region
# --------------------------------------------------------------------------------------------------
def get_volume_of_convex_hull(positions):
    '''
    Compute volume of convex hull that encloses input positions.

    Parameters
    ----------
    positions : array (object number x dimension number)
        positions

    Returns
    -------
    float
        volume within convex hull around positions
    '''

    def _get_tetrahedron_volume(a, b, c, d):
        return np.abs(np.einsum('ij,ij->i', a - d, np.cross(b - d, c - d))) / 6

    ConvexHull = spatial.ConvexHull(positions)  # pylint: disable=no-member
    DelaunayTes = spatial.Delaunay(positions[ConvexHull.vertices])  # pylint: disable=no-member
    tets = DelaunayTes.points[DelaunayTes.simplices]

    return np.sum(_get_tetrahedron_volume(tets[:, 0], tets[:, 1], tets[:, 2], tets[:, 3]))


# --------------------------------------------------------------------------------------------------
# coordinates in redshift space
# --------------------------------------------------------------------------------------------------
def convert_velocity_redshift(value_name, values, solve_exact=True):
    '''
    Get velocity/redshift along the line of sight from redshift/velocity [km/s].
    Independent of cosmology.

    Parameters
    ----------
    value_name : str
        'redshift', 'velocity'
    values : float or array
        redshift/velocity value[s]
    solve_exact : bool
        whether to use exact solution or faster approximation

    Returns
    -------
    array
        velocities [km/s] or redshifts
    '''
    if value_name == 'redshift':
        # input redshift, get velocity
        if solve_exact:
            return (
                ((1 + values) ** 2 - 1)
                / ((1 + values) ** 2 + 1)
                * constant.speed_light
                * constant.kilo_per_centi
            )
        else:
            return constant.speed_light * values * constant.kilo_per_centi

    elif value_name == 'velocity':
        # input velocity, get redshift
        if solve_exact:
            return (
                (1 + values * constant.centi_per_kilo / constant.speed_light)
                / (1 - values * constant.centi_per_kilo / constant.speed_light)
            ) ** 0.5 - 1
        else:
            return values * constant.centi_per_kilo / constant.speed_light


def get_position_difs_from_redshift_difs(redshift_difs, hubble_times):
    '''
    Get position difference [kpc comoving] from redshift difference (redshift-space distortion).
    *** distance is *approximate*, valid in non-relativistic limit.

    Parameters
    ----------
    redshift_difs : float or array
        redshift difference[s]
    hubble_times : float or array
        hubble time[s] = 1 / H [Gyr]

    Returns
    -------
    array
        position differences [kpc comoving]
    '''
    return convert_velocity_redshift('redshift', redshift_difs, solve_exact=False) * hubble_times


def get_position_difs_from_velocity_difs(velocity_difs, hubble_times, redshifts):
    '''
    Get position difference [kpc comoving] from velocity difference (redshifts-space distortion).

    Parameters
    ----------
    velocity_difs : floar or array
        peculiar velocity[s] [km/s]
    hubble_time : float or array
        hubble time[s] = 1 / H [Gyr]
    redshifts : float or array

    Returns
    -------
    array
        position differences [kpc comoving]
    '''
    return (
        velocity_difs / (1 + redshifts) * constant.kpc_per_km / constant.Gyr_per_sec
    ) * hubble_times


def get_positions_in_redshift_space(
    positions, velocities, hubble_times, redshifts, periodic_length=None
):
    '''
    Get position[s] [kpc comoving] in redshifts space, convolving real position[s] with
    redshifts-space distortion.

    Parameters
    ----------
    positions : float or array
        actual position[s] [kpc comoving]
    velocities : float or array
        peculiar velocity[s] [km/s]
    hubble_times : float or array
        hubble time[s] = 1 / H [Gyr]
    periodic_length : float
        periodicity length

    Returns
    -------
    array
        positions [kpc comoving]
    '''
    return positions(
        positions + get_position_difs_from_velocity_difs(velocities, hubble_times, redshifts),
        periodic_length,
    )
