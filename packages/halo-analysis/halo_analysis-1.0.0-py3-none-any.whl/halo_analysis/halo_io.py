#!/usr/bin/env python3

'''
Read halo/galaxy catalogs (from Rockstar or AHF) and halo merger trees (from ConsistentTrees).

@author:
    Andrew Wetzel <arwetzel@gmail.com>
    Shea Garrison-Kimmel <sheagk@gmail.com>

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

----------
Null values
    This package initializes all halo/galaxy properties to null values of -1,
    except for properties related to 'velocity', 'position', 'distance', 'accrete', and 'energy',
    which can be physically negative, so are initialized to np.nan.

----------
Halo overdensity definition
    This package assumes that the halo finder defined a halo by computing the radius that encloses
    200 x mean matter density (R_200m).

----------
Reading a halo catalog

Within a simulation directory, read all halos in the snapshot at redshift 0 via:
    hal = halo.io.IO.read_catalogs('redshift', 0)
hal is a dictionary, with a key for each property. So, access via:
    hal[property_name]
For example:
    hal['mass']
returns a numpy array of masses, one for each halo, while
    hal['position']
returns a numpy array of positions (of dimension particle_number x 3)

----------
Default/stored properties (the most important ones)

If you read the halo catalog (out_*.list, halos_*.ascii, or halo_*.hdf5) you have:
    'id' : catalog ID, valid at just the given snapshot, indexing starts at 0
    'position' : 3-D position, along simulation's (cartesian) x,y,z grid [kpc comoving]
    'velocity' : 3-D velocity, along simulation's (cartesian) x,y,z grid [km/s]
    'mass' : default total mass - M_200m is default overdensity definition [M_sun]
    'radius' : halo radius, for 'default' overdensity definition of R_200m [kpc physical]
    'scale.radius' : NFW scale radius [kpc physical]
    'mass' : total mass defined via 200 x mean matter density [M_sun]
    'mass.vir' : total mass defined via Bryan & Norman 1998
    'mass.200c' : total mass defined via 200 x critical density [M_sun]
    'mass.bound' : total mass within R_200m that is bound to the halo [M_sun]
    'vel.circ.max' : maximum of the circular velocity profile [km/s]
    'vel.std' : standard deviation of the velocity of particles [km/s]
    'mass.lowres' : total mass of low-res DM [M_sun] (not always correct! use dark2.mass, see below)
    'host.index' : catalog index of the primary host (highest-mass) halo in catalog
    'host.distance' : 3-D distance wrt center of primary host [kpc physical]
    'host.velocity' : 3-D velocity wrt center of primary host [km/s]
    'host.velocity.tan' : tangential velocity wrt primary host [km/s]
    'host.velocity.rad' : radial velocity wrt primary host (negative = inward) [km/s]

If you set host_number > 1 (or the simulation directory name contains 'elvis') you also have:
    'host2.index' : catalog index of the secondary host in catalog
    'host2.distance' : 3-D distance wrt center of secondary host [kpc physical]
    'host2.velocity' : 3-D velocity wrt center of secondary host [km/s]
    'host2.velocity.tan' : tangential velocity wrt secondary host [km/s]
    'host2.velocity.rad' : radial velocity wrt secondary host (negative = inward) [km/s]

If you read the halo main progenitor histories (hlist*.list or halo_*.hdf5) you also have:
    'mass.half.snapshot' : snapshot when first had half of its peak mass
    'mass.peak' : maximum of mass throughout history [M_sun]
    'mass.peak.snapshot': snapshot index at which above occurs
    'vel.circ.peak' : maximum of vel.circ.max throughout history [km/s]
    'major.merger.snapshot' : snapshot index of last major merger
    'infall.first.snapshot' : snapshot index when first became a satellite
    'infall.first.mass' : mass when first fell into a host halo (became a satellite) [M_sun]
    'infall.first.vel.circ.max' : vel.circ.max when first became a satellite [km/s]
    'infall.snapshot' : snapshot index when most recently fell into a host halo
    'infall.mass' : mass when most recently fell into a host halo [M_sun]
    'infall.vel.circ.max' : vel.circ.max when most recently fell into a host halo [km/s]
    'accrete.rate' : instantaneous accretion rate [M_sun / yr]
    'accrete.rate.100Myr : mass growth rate averaged over 100 Myr [M_sun / yr]
    'accrete.rate.tdyn : mass growth rate averaged over halo dynamical time [M_sun / yr]

If you read the halo merger trees (tree*.dat or tree.hdf5) you have:
    'tid' : tree ID, unique across all halos across all snapshots (starts at 0)
    'snapshot' : snapshot index of halo
    'am.phantom' : whether halo is interpolated across snapshots
    'descendant.snapshot' : snapshot index of descendant
    'descendant.index' : tree index of descendant
    'am.progenitor.main' : whether am most massive progenitor of my descendant
    'progenitor.number' : number of progenitors
    'progenitor.main.index' : index of main (most massive) progenitor
    'progenitor.co.index' : index of next co-progenitor (with same descendant)
    'final.index' : tree index at final snapshot
    'dindex' : depth-first order (index) within tree
    'progenitor.co.dindex' : depth-first index of next co-progenitor
    'progenitor.last.dindex' : depth-first index of last progenitor - includes *all* progenitors
    'progenitor.main.last.dindex' : depth-first index of last progenitor - only via main progenitors
    'central.index' : tree index of most massive central halo (which must be a central)
    'central.local.index' : tree index of local (lowest-mass) central (which could be a satellite)
    'host.index' : tree index of the primary host (following back main progenitor branch)
    'host.distance' : 3-D distance wrt center of primary host [kpc physical]
    'host.velocity' : 3-D velocity wrt center of primary host [km/s]
    'host.velocity.tan' : tangential velocity wrt primary host [km/s]
    'host.velocity.rad' : radial velocity wrt primary host (negative = inward) [km/s]

If you set host_number > 1 (or the simulation directory name contains 'elvis') you also have:
    'host2.index' : tree index of the secondary host in catalog
    'host2.distance' : 3-D distance wrt center of secondary host [kpc physical]
    'host2.velocity' : 3-D velocity wrt center of secondary host [km/s]
    'host2.velocity.tan' : tangential velocity wrt secondary host [km/s]
    'host2.velocity.rad' : radial velocity wrt secondary host (negative = inward) [km/s]

If you read the halo star catalog (star_*.hdf5) you also have:
    'dark2.mass' : total mass of low-res DM within halo [M_sun] (more accurate than mass.lowres!)
    'star.number' : number of star particles in halo [M_sun]
    'star.mass' : mass from all star particles in halo [M_sun]
    'star.radius.50' : radius that encloses 50% of stellar mass [kpc physical]
    'star.vel.std.50' : stellar velocity dispersion (standard deviation) at R_50 [km/s]
    'star.position' : center-of-mass position of star particles [kpc comoving]
    'star.velocity' : center-of-mass velocity of star particles [km/s]
    'star.indices' : indices of member star particles in the particle catalog at the same snapshot
        example: pis = hal['star.indices'][0] for halo 0,
        then get star particle properties via part['star'][property_name][pis]
    'star.form.time.50' : time (age of Universe) when formed 50% of current stellar mass [Gyr]

If you run IO.assign_hosts_to_catalog(hal, 'star') you also have:
    (though these generally agree to within a few percent with host.dstance and host.velocity from
     the dark-matter halo catalog)
    'star.host.index' : index of primary host galaxy (highest stellar mass) in catalog
    'star.host.distance' : 3-D distance wrt center of primary host galaxy [kpc physical]
    'star.host.velocity' : 3-D velocity wrt center of primary host galaxy [km/s]
    'star.host.velocity.tan' : tangential velocity wrt primary host galaxy [km/s]
    'star.host.velocity.rad' : radial velocity wrt primary host galaxy (negative = inward) [km/s]


----------
Derived properties

hal is a HaloDictionaryClass that can compute derived properties on the fly.
Call derived (or stored) properties via:
    hal.prop(property_name)

Examples:
    hal.prop('host.distance.total')
    hal.prop('star.density.50')
    hal.prop('star.age.50')

For the halo merger trees, you can compute history-based properties:
    halt.prop('progenitor.main.indices')
    halt.prop('descendant.indices')
    halt.prop('progenitor.indices')
    halt.prop('mass.history')
    halt.prop('mass.peak')

You also can call stored properties via hal.prop(property_name).
The package will know that it is a stored property and return it as is.
For example, hal.prop('position') is the same as hal['position'].

See HaloDictionaryClass.prop() for full options for parsing of derived properties.
'''

import os
import collections
import copy
import numpy as np
from numpy import Inf
from scipy import spatial

import utilities as ut
from . import halo_default


# --------------------------------------------------------------------------------------------------
# defaults
# --------------------------------------------------------------------------------------------------
# subset of 64 snapshots indices on which to run halo finder, particle assignment, etc
snapshot_indices_subset = np.array(
    [
        20,
        26,
        33,
        41,
        52,  # z = 10 - 6
        55,
        57,
        60,
        64,
        67,  # z = 5.8 - 5.0
        71,
        75,
        79,
        83,
        88,  # z = 4.8 - 4.0
        91,
        93,
        96,
        99,
        102,
        105,
        109,
        112,
        116,
        120,  # z = 3.9 - 3.0
        124,
        128,
        133,
        137,
        142,
        148,
        153,
        159,
        165,
        172,  # z = 2.9 - 2.0
        179,
        187,
        195,
        204,
        214,
        225,
        236,
        248,
        262,
        277,  # z = 1.9 - 1.0
        294,
        312,
        332,
        356,
        382,
        412,
        446,
        486,
        534,  # z = 0.9 - 0.1
        539,
        544,
        550,
        555,
        561,
        567,
        573,
        579,
        585,  # z = 0.09 - 0.01
        600,  # z = 0
    ]
)


# minimum fraction of mass that is bound to trust a halo
BOUND_MASS_FRAC_MIN = 0.4

# maximum contamination from low-resolution dark matter to trust a halo
LOWRES_MASS_FRAC_MAX = 0.02


# --------------------------------------------------------------------------------------------------
# dictionary class to store halo catalogs
# --------------------------------------------------------------------------------------------------
class HaloDictionaryClass(dict):
    '''
    Dictionary class to store halo/galaxy properties.
    Allows production of derived quantities.
    '''

    def __init__(self):
        # internal dictionary, to translate element name to index in particle element array
        self._element_index = collections.OrderedDict()
        self._element_index['metals'] = 0
        self._element_index['helium'] = self._element_index['he'] = 1
        self._element_index['carbon'] = self._element_index['c'] = 2
        self._element_index['nitrogen'] = self._element_index['n'] = 3
        self._element_index['oxygen'] = self._element_index['o'] = 4
        self._element_index['neon'] = self._element_index['ne'] = 5
        self._element_index['magnesium'] = self._element_index['mg'] = 6
        self._element_index['silicon'] = self._element_index['si'] = 7
        self._element_index['sulfur'] = self._element_index['s'] = 8
        self._element_index['calcium'] = self._element_index['ca'] = 9
        self._element_index['iron'] = self._element_index['fe'] = 10
        # r-process 'toy' models
        self._element_index['rprocess1'] = 11
        self._element_index['rprocess2'] = 12
        self._element_index['rprocess3'] = 13
        self._element_index['rprocess4'] = 14

        self.info = {}  # meta-data about simulation and particle catalog
        self.snapshot = {}  # information about current snapshot
        self.Snapshot = None  # information about all snapshots
        self.Cosmology = None  # information about cosmology and cosmological functions
        # rotation properties of host galaxy[s]
        self.host = {'rotation': [], 'axis.ratios': []}

    def prop(self, property_name, indices=None, _dict_only=False):
        '''
        Get property, either from self dictionary or derive.
        If several properties, need to provide mathematical relationship.

        Parameters
        ----------
        property_name : str
            name of property
        indices : array
            list of indices to select on (of arbitrary dimensions)
        _dict_only : bool
            require property_name to be in self's dict - avoids endless recursion

        Returns
        -------
        values : float or array
            depending on dimensionality of input indices
        '''
        # parsing general to all catalogs ----------
        property_name = property_name.strip()  # strip white space

        # if input is in self dictionary, return as is
        if property_name in self:
            if indices is not None:
                return self[property_name][indices]
            else:
                return self[property_name]
        elif _dict_only:
            raise KeyError(f'property = {property_name} is not in self\'s dictionary')

        # math relation, combining more than one property
        if (
            '/' in property_name
            or '*' in property_name
            or '+' in property_name
            or '-' in property_name
        ):
            prop_names = property_name

            for delimiter in ['/', '*', '+', '-']:
                if delimiter in property_name:
                    prop_names = prop_names.split(delimiter)
                    break

            if len(prop_names) == 1:
                raise ValueError(f'not sure how to parse property = {property_name}')

            # make copy so not change values in input catalog
            prop_values = np.array(self.prop(prop_names[0], indices))

            for prop_name in prop_names[1:]:
                if '/' in property_name:
                    if np.isscalar(prop_values):
                        if self.prop(prop_name, indices) == 0:
                            prop_values = np.nan
                        else:
                            prop_values = prop_values / self.prop(prop_name, indices)
                    else:
                        masks = self.prop(prop_name, indices) != 0
                        prop_values[masks] = (
                            prop_values[masks] / self.prop(prop_name, indices)[masks]
                        )
                        masks = self.prop(prop_name, indices) == 0
                        prop_values[masks] = np.nan
                if '*' in property_name:
                    prop_values = prop_values * self.prop(prop_name, indices)
                if '+' in property_name:
                    prop_values = prop_values + self.prop(prop_name, indices)
                if '-' in property_name:
                    prop_values = prop_values - self.prop(prop_name, indices)

            if prop_values.size == 1:
                prop_values = np.float64(prop_values)

            return prop_values

        # math transformation of single property
        if property_name[:3] == 'log':
            return ut.math.get_log(self.prop(property_name.replace('log', ''), indices))

        if property_name[:3] == 'abs':
            return np.abs(self.prop(property_name.replace('abs', ''), indices))

        # parsing specific to halo catalog ----------
        # convert properties from DM-only simulation to baryonic equivalent
        if '.barysim' in property_name:
            values = np.array(self.prop(property_name.replace('.barysim', ''), indices))
            # if halos from a DM-only simulation, re-scale mass or V_circ,max by subtracting
            # baryonic mass fraction contained in DM particles
            if not self.info['has.baryons']:
                dm_fraction = self.Cosmology['omega_dm'] / self.Cosmology['omega_matter']
                if 'mass' in property_name:
                    values *= dm_fraction
                elif 'vel.circ.max' in property_name:
                    values *= np.sqrt(dm_fraction)

            return values

        # walk merger tree
        if 'progenitor.' in property_name or 'descendant.' in property_name:
            values = []
            if property_name in ['descendant.indices', 'progenitor.main.indices']:
                if 'descendant' in property_name:
                    # get descendants going forward in time (including self)
                    prop_name = 'descendant.index'
                elif 'progenitor' in property_name:
                    # get main progenitors going back in time (including self)
                    prop_name = 'progenitor.main.index'

                if np.isscalar(indices):
                    # input only one halo
                    hindex = indices
                    while hindex >= 0:
                        values.append(hindex)
                        hindex = self[prop_name][hindex]
                    values = np.array(values, self[prop_name].dtype)
                else:
                    # input multiple halos
                    hindices = np.array(indices)
                    while np.max(hindices) >= 0:
                        values.append(np.array(hindices, self[prop_name].dtype))
                        masks = hindices >= 0
                        hindices[masks] = self[prop_name][hindices[masks]]

                    # transpose array so it is input halo number x progenitor/descendant number
                    values = np.transpose(values)

            # get all progenitors at previous snapshot
            elif property_name == 'progenitor.indices':
                if np.isscalar(indices):
                    # input only one halo
                    hindex = self['progenitor.main.index'][indices]
                    while hindex >= 0:
                        values.append(hindex)
                        hindex = self['progenitor.co.index'][hindex]
                    values = np.array(values, self['progenitor.main.index'].dtype)
                else:
                    # input multiple halos
                    hindices = self['progenitor.main.index'][indices]
                    for hindex in hindices:
                        values_i = []
                        while hindex >= 0:
                            values_i.append(hindex)
                            hindex = self['progenitor.co.index'][hindex]
                        values.append(np.array(values_i, self['progenitor.main.index'].dtype))

            return values

        if '.history' in property_name or '.peak' in property_name or '.nadir' in property_name:
            if '.history' in property_name:
                prop_name = property_name.replace('.history', '')
            elif '.peak' in property_name:
                prop_name = property_name.replace('.peak', '')
            elif '.nadir' in property_name:
                prop_name = property_name.replace('.nadir', '')
            assert prop_name in self

            prog_hindices = self.prop('progenitor.main.indices', indices)
            values = np.zeros(prog_hindices.shape, self[prop_name].dtype) - Inf
            masks = prog_hindices >= 0
            values[masks] = self[prop_name][prog_hindices[masks]]

            if 'peak' in property_name:
                if np.isscalar(indices):
                    values = np.nanmax(values)
                else:
                    values = np.nanmax(values, 1)
            elif 'nadir' in property_name:
                if np.isscalar(indices):
                    values = np.nanmin(values)
                else:
                    values = np.nanmin(values, 1)

            return values

        if 'mass.' in property_name:
            if property_name == 'mass.lowres':
                # should not get this far if 'mass.lowres' is a stored property
                raise KeyError(f'{property_name} not stored in halo dictionary')
            elif property_name == 'mass.hires':
                # high-res mass from Rockstar
                values = self.prop('mass - mass.lowres', indices)
            elif property_name == 'lowres.mass.frac' or property_name == 'dark2.mass.frac':
                # low-res mass from Rockstar
                values = self.prop('mass.lowres / mass', indices)
                # check if catalog has direct assigment of low-res dark2 particles from snapshot
                # if so, use larger of the two low-res masses
                if 'dark2.mass' in self:
                    # low-res mass from direct assignment of particles
                    values_t = self.prop('dark2.mass / mass', indices)
                    if np.isscalar(values) and values_t > values:
                        values = values_t
                    else:
                        masks = values_t > values
                        values[masks] = values_t[masks]
            else:
                # mass from individual element
                values = self.prop('mass', indices, _dict_only=True) * self.prop(
                    property_name.replace('mass.', 'massfraction.'), indices
                )

                if property_name == 'mass.hydrogen.neutral':
                    # mass from neutral hydrogen (excluding helium, metals, and ionized hydrogen)
                    values = values * self.prop(
                        'hydrogen.neutral.fraction', indices, _dict_only=True
                    )

            return values

        if 'vel.circ.max.' in property_name:
            scale_radius_factor = 2.1626  # R(V_circ,max) = scale_radius_factor * R_scale
            scale_radius_name = 'scale.radius.klypin'

            if 'radius' in property_name:
                # radius at which V_circ,max occurs
                values = scale_radius_factor * self[scale_radius_name][indices]
            elif 'mass' in property_name:
                # mass within R(V_circ,max)
                values = (
                    self['vel.circ.max'][indices] ** 2
                    * scale_radius_factor
                    * self[scale_radius_name][indices]
                    * ut.constant.km_per_kpc
                    / ut.constant.grav_km_msun_sec
                )

            return values

        # element string -> index conversion
        if 'massfraction.' in property_name or 'metallicity.' in property_name:
            if 'hydrogen' in property_name or property_name.endswith('.h'):
                # special case: mass fraction of hydrogen (excluding helium and metals)
                values = (
                    1
                    - self.prop('massfraction', indices)[:, 0]
                    - self.prop('massfraction', indices)[:, 1]
                )

                if 'neutral' in property_name:
                    # mass fraction of neutral hydrogen (excluding Helium, metals, and ionized H)
                    values = values * self.prop(
                        'hydrogen.neutral.fraction', indices, _dict_only=True
                    )
            else:
                for element_name in property_name.split('.'):
                    if element_name in self._element_index:
                        element_index = self._element_index[element_name]
                        break
                else:
                    raise KeyError(f'not sure how to parse property = {property_name}')

                if 'star.' in property_name:
                    massfraction_name = 'star.massfraction'
                elif 'gas.' in property_name:
                    massfraction_name = 'gas.massfraction'

                if indices is None:
                    values = self[massfraction_name][:, element_index]
                else:
                    values = self[massfraction_name][indices, element_index]

            # convert to metallicity := log10(mass_fraction / mass_fraction_solar)
            if 'metallicity' in property_name:
                values = ut.math.get_log(values / ut.constant.sun_massfraction[element_name])

            return values

        # average stellar density
        if 'star.density' in property_name:
            if property_name == 'star.density':
                property_name += '.50'  # use R_50 as default radius to measure stellar density

            radius_percent = float(property_name.split('.')[-1])
            radius_name = 'star.radius.' + property_name.split('.')[-1]

            values = self.prop(radius_name, indices, _dict_only=True)
            # masks = np.isfinite(values)
            # masks[masks] *= (values[masks] > 0)
            # values[masks] = (
            #    radius_percent / 100 * self.prop('star.mass', indices, _dict_only=True)[masks] /
            #    (4 / 3 * np.pi * self.prop(radius_name, indices)[masks] ** 3))
            values = (
                radius_percent
                / 100
                * self.prop('star.mass', indices, _dict_only=True)
                / (4 / 3 * np.pi * self.prop(radius_name, indices) ** 3)
            )
            # if values.size == 1:
            #    values = np.asscalar(values)

            return values

        # velocity (dispersion) along 1 dimension
        if 'vel.' in property_name and '.1d' in property_name:
            values = self.prop(property_name.replace('.1d', ''), indices) / np.sqrt(3)

        # distance/velocity wrt center of a primary host
        if 'host' in property_name:
            if 'host.near' in property_name:
                host_name = 'host.near'
                host_index = None
            if 'host.' in property_name or 'host1.' in property_name:
                host_name = 'host.'
                host_index = 0
            elif 'host2.' in property_name:
                host_name = 'host2.'
                host_index = 1
            elif 'host3.' in property_name:
                host_name = 'host3.'
                host_index = 2
            else:
                raise ValueError(f'cannot identify host name in {property_name}')

            if 'index' in property_name:
                values = self[host_name + 'index'][indices]

            if 'distance' in property_name:
                if 'star.' in property_name:
                    values = self.prop('star.' + host_name + 'distance', indices, _dict_only=True)
                else:
                    values = self.prop(host_name + 'distance', indices, _dict_only=True)
            elif 'velocity' in property_name:
                if 'star.' in property_name:
                    values = self.prop('star.' + host_name + 'velocity', indices, _dict_only=True)
                else:
                    values = self.prop(host_name + 'velocity', indices, _dict_only=True)

            if 'principal' in property_name:
                # align with principal axes of primary host galaxy
                # for the halo tree, by default this is always the reference snapshot (z = 0)
                assert (
                    'host' in self.__dict__ and len(self.host['rotation']) > 0
                ), 'must assign hosts principal axes rotation tensor!'
                values = ut.coordinate.get_coordinates_rotated(
                    values, self.host['rotation'][host_index]
                )

            if '.cyl' in property_name or '.spher' in property_name:
                # convert to cylindrical or spherical coordinates
                if '.cyl' in property_name:
                    # along major axes R (positive definite), minor axis Z (signed),
                    # angle phi (0 to 2 * pi)
                    coordinate_system = 'cylindrical'
                elif '.spher' in property_name:
                    # along R (positive definite), theta [0, pi), phi [0, 2 * pi)
                    coordinate_system = 'spherical'

                if 'distance' in property_name:
                    values = ut.coordinate.get_positions_in_coordinate_system(
                        values, 'cartesian', coordinate_system
                    )
                elif 'velocity' in property_name or 'acceleration' in property_name:
                    if 'principal' in property_name:
                        distance_vectors = self.prop(host_name + 'distance.principal', indices)
                    else:
                        distance_vectors = self.prop(host_name + 'distance', indices)
                    values = ut.coordinate.get_velocities_in_coordinate_system(
                        values, distance_vectors, 'cartesian', coordinate_system
                    )

            if 'total' in property_name:
                # compute total (scalar) distance / velocity
                if len(values.shape) == 1:
                    shape_pos = 0
                else:
                    shape_pos = 1
                values = np.sqrt(np.sum(values**2, shape_pos))

            return values

        # stellar formation time / age
        if 'form.' in property_name or '.age' in property_name:
            if '.age' in property_name:
                values = self.snapshot['time'] - self.prop(
                    property_name.replace('.age', '.form.time'), indices
                )
            elif 'time' in property_name and 'lookback' in property_name:
                values = self.snapshot['time'] - self.prop(
                    property_name.replace('.lookback', ''), indices
                )

            return values

        # should not get this far without a return
        raise KeyError(f'not sure how to parse property = {property_name}')

    def get_indices(
        self,
        lowres_mass_frac_max=LOWRES_MASS_FRAC_MAX,
        bound_mass_frac_min=BOUND_MASS_FRAC_MIN,
        star_particle_number_min=2,
        star_mass_limits=[1, None],
        star_density_limits=[300, Inf],
        star_mass_fraction_limits=None,
        dark_star_offset_max=None,
        host_distance_limits=None,
        object_kind='',
        prior_indices=None,
    ):
        '''
        Get indices of halos/galaxies that satisfy input selection limits.
        This removes the most common cases of numerical artifacts.
        If input object_kind = 'halo' or 'galaxy', use default selection limits
        (regardless of other inputs).

        Parameters
        ----------
        lowres_mass_frac_max : float
            maximum contamination mass fraction from low-res DM
        bound_mass_frac_min : float
            minimum mass.bound/mass
        star_particle_number_min : int
            minimum number of star particles
        star_mass_limits : list
            min and max limits for stellar mass [M_sun]
        star_density_limits : list
            min and max limits for average stellar density within R_50 [M_sun / kpc^3]
        star_mass_fraction_limits : list
            min and max limits for star.mass/mass.bound
        dark_star_offset_max : float
            max offset between position or velocity of stars and halo (DM), in units of R_50 or V_50
        host_distance_limits : list
            min and max limits for distance to host [kpc physical]
        object_kind : str
            shortcut to select object type: 'halo', 'galaxy' and/or 'satellite', 'isolated'
        prior_indices : array
            prior halo indices to impose

        Returns
        -------
        hindices : array
            indices of halos/galaxies
        '''
        assert not ('isolated' in object_kind and 'satellite' in object_kind)
        assert not ('halo' in object_kind and 'galaxy' in object_kind)

        satellite_distance_limits = [5, 350]

        # default parameters for given kind
        if 'halo' in object_kind:
            star_particle_number_min = 0
            star_mass_limits = None
            star_density_limits = None
            star_mass_fraction_limits = None
        elif 'galaxy' in object_kind:
            star_particle_number_min = 6
            star_mass_limits = [1, None]
            star_density_limits = [300, Inf]

        # separate satellites and non-satellites of host
        if 'satellite' in object_kind:
            host_distance_limits = satellite_distance_limits
        elif 'isolated' in object_kind:
            host_distance_limits = [satellite_distance_limits[1], Inf]

        # handle satellites of second host
        if 'satellite2' in object_kind:
            host_distance_prop = 'host2.distance.total'
        else:
            host_distance_prop = 'host.distance.total'

        hindices = prior_indices
        if hindices is None or len(hindices) == 0:
            hindices = ut.array.get_arange(self['mass'])

        # properties common to all halos
        if lowres_mass_frac_max > 0:
            hindices = ut.array.get_indices(
                self.prop('lowres.mass.frac'), [0, lowres_mass_frac_max], hindices
            )

        if bound_mass_frac_min > 0:
            hindices = ut.array.get_indices(
                self.prop('mass.bound/mass'), [bound_mass_frac_min, Inf], hindices
            )

        # require that halo exists in merger trees
        # if 'tree.index' in hal:
        #    hindices = ut.array.get_indices(hal['tree.index'], [0, Inf], hindices)

        # properties for galaxies
        if 'star.mass' in self and np.max(self['star.mass']) > 0:
            if star_particle_number_min > 0:
                hindices = ut.array.get_indices(
                    self['star.number'], [star_particle_number_min, Inf], hindices
                )

            if star_mass_limits is not None and len(star_mass_limits) > 0:
                hindices = ut.array.get_indices(self['star.mass'], star_mass_limits, hindices)

            if star_density_limits is not None and len(star_density_limits) > 0:
                hindices = ut.array.get_indices(
                    self.prop('star.density.50'), star_density_limits, hindices
                )

            if star_mass_fraction_limits is not None and len(star_mass_fraction_limits) > 0:
                hindices = ut.array.get_indices(
                    self.prop('star.mass/mass.bound'), star_mass_fraction_limits, hindices
                )

            if dark_star_offset_max is not None and dark_star_offset_max > 0:
                position_offsets = ut.coordinate.get_distances(
                    self['position'][hindices],
                    self['star.position'][hindices],
                    self.info['box.length'],
                    self.snapshot['scalefactor'],
                    total_distance=True,
                )
                hindices = hindices[
                    position_offsets < dark_star_offset_max * self['star.radius.50'][hindices]
                ]
                velocity_offsets = ut.coordinate.get_velocity_differences(
                    self['velocity'][hindices],
                    self['star.velocity'][hindices],
                    self['position'][hindices],
                    self['star.position'][hindices],
                    self.info['box.length'],
                    self.snapshot['scalefactor'],
                    self.snapshot['time.hubble'],
                    total_velocity=True,
                )
                hindices = hindices[
                    velocity_offsets < dark_star_offset_max * self['star.vel.std.50'][hindices]
                ]

        # properties for satellites of host(s)
        if host_distance_limits is not None and len(host_distance_limits) > 0:
            hindices = ut.array.get_indices(
                self.prop(host_distance_prop), host_distance_limits, hindices
            )

        # if looking for isolated halos, make sure that not a satellite of host2
        if ('host2.distance' in self) and ('isolated' in object_kind):
            hindices = ut.array.get_indices(
                self.prop('host2.distance.total'), host_distance_limits, hindices
            )

        return hindices


# --------------------------------------------------------------------------------------------------
# read and write halo catalogs and trees
# --------------------------------------------------------------------------------------------------
class IOClass(ut.io.SayClass):
    '''
    Read or write halo/galaxy files from Rockstar and/or ConsistentTrees.
    '''

    def __init__(
        self,
        catalog_directory=halo_default.rockstar_catalog_directory,
        lowres_mass_frac_max=LOWRES_MASS_FRAC_MAX,
    ):
        '''
        Parameters
        ----------
        catalog_directory : str
            directory (within rockstar directory) of raw text files
        lowres_mass_frac_max : float
            maximum contamination from low-resolution DM to consider a halo to be the primary host
        '''
        # set directories
        self.catalog_directory = ut.io.get_path(catalog_directory)
        self.catalog_hlist_directory = self.catalog_directory + 'hlists/'
        self.catalog_tree_directory = self.catalog_directory + 'trees/'

        # maximum contamination from low-resolution DM to consider a halo to be the primary host
        self.lowres_mass_frac_max = lowres_mass_frac_max

        # set default names for ids and indices
        self.catalog_id_name = 'id'
        self.tree_id_name = 'tid'
        self.prop_name_default = 'mass'  # default property for iterating

        # data types to store halo properties
        self.int_type = np.int32
        self.float_type = np.float32

        self.Snapshot = None

        # halo properties to ignore when reading in
        self.ignore_properties = [
            'particle.number',
            'momentum.ang.x',
            'momentum.ang.y',
            'momentum.ang.z',
            'axis.x',
            'axis.y',
            'axis.z',
            'axis.b/a.500c',
            'axis.c/a.500c',
            'axis.x.500c',
            'axis.y.500c',
            'axis.z.500c',
            'kinetic/potential',
            'mass.pe.behroozi',
            'mass.pe.diemer',
            'type',
            'star.mass.rockstar',
            'gas.mass.rockstar',
            'blackhole.mass.rockstar',
            'mass.hires',
            'core.number',
            'i.dx',
            'i.so',
            'i.ph',
            'particle.child.number',
            'max.metric',
            'descendant.central.local.' + self.tree_id_name,
            'breadth.index',
            'sam.mass.vir',
            'snapshot.index',
            'tidal.force',
            'tidal.' + self.tree_id_name,
            'accrete.rate.2tdyn',
            'accrete.rate.mass.peak',
            'accrete.rate.vel.circ.max',
            'accrete.rate.vel.circ.max.tyn',
            'mass.peak.vel.circ.max',
            'tidal.force.tdyn',
            'log.vnow/vdyn',
            'future.merger.time',
            'future.merger.id',
            'spin.at.mpeak.scale',
        ]

        # new names to give to halo properties when reading in
        self.property_new_names = {
            'id': self.catalog_id_name,
            'descid': 'descendant.' + self.catalog_id_name,
            'num_p': 'particle.number',
            'np': 'particle.number',
            'npart': 'particle.number',
            'vmax': 'vel.circ.max',
            'rvmax': 'vel.circ.max.radius',
            'rmax': 'vel.circ.max.radius',
            'vrms': 'vel.std',
            'sigv': 'vel.std',
            'x': 'position.x',
            'y': 'position.y',
            'z': 'position.z',
            'xc': 'position.x',
            'yc': 'position.y',
            'zc': 'position.z',
            'vx': 'velocity.x',
            'vy': 'velocity.y',
            'vz': 'velocity.z',
            'vxc': 'velocity.x',
            'vyc': 'velocity.y',
            'vzc': 'velocity.z',
            'jx': 'momentum.ang.x',
            'jy': 'momentum.ang.y',
            'jz': 'momentum.ang.z',
            'lx': 'momentum.ang.x',
            'ly': 'momentum.ang.y',
            'lz': 'momentum.ang.z',
            'e': 'energy',
            'spin': 'spin.peebles',
            'posuncertainty': 'position.err',
            'veluncertainty': 'velocity.err',
            'bulk_vx': 'bulk.velocity.x',
            'bulk_vy': 'bulk.velocity.y',
            'bulk_vz': 'bulk.velocity.z',
            'bulkvelunc': 'bulk.velocity.err',
            'n_core': 'core.number',
            'xoff': 'position.offset',
            'voff': 'velocity.offset',
            'mbp_offset': 'position.offset',
            'com_offset': 'position.offset.com',
            'v_esc': 'vel.escape',
            'lambda': 'spin.bullock',
            'spin_bullock': 'spin.bullock',
            'lambdae': 'spin.peebles',
            'b_to_a': 'axis.b/a',
            'c_to_a': 'axis.c/a',
            'b': 'axis.b/a',
            'c': 'axis.c/a',
            'a[x]': 'axis.x',
            'a[y]': 'axis.y',
            'a[z]': 'axis.z',
            'b_to_a(500c)': 'axis.b/a.500c',
            'c_to_a(500c)': 'axis.c/a.500c',
            'a[x](500c)': 'axis.x.500c',
            'a[y](500c)': 'axis.y.500c',
            'a[z](500c)': 'axis.z.500c',
            'eax': 'axis.a.x',
            'eay': 'axis.a.y',
            'eaz': 'axis.a.z',
            'ebx': 'axis.b.x',
            'eby': 'axis.b.y',
            'ebz': 'axis.b.z',
            'ecx': 'axis.c.x',
            'ecy': 'axis.c.y',
            'ecz': 'axis.c.z',
            'rs': 'scale.radius',
            'r2': 'scale.radius',
            'rs_klypin': 'scale.radius.klypin',
            't/|u|': 'kinetic/potential',
            'm_pe_behroozi': 'mass.pe.behroozi',
            'm_pe_diemer': 'mass.pe.diemer',
            'idx': 'i.dx',
            'i_so': 'i.so',
            'i_ph': 'i.ph',
            'num_cp': 'particle.child.number',
            'mmetric': 'max.metric',
            'sm': 'star.mass.rockstar',
            'm_star': 'star.mass.ahf',
            'n_star': 'star.particle.number.ahf',
            'gas': 'gas.mass.rockstar',
            'm_gas': 'gas.mass.ahf',
            'n_gas': 'gas.particle.number.ahf',
            'bh': 'blackhole.mass.rockstar',
            'bh_mass': 'blackhole.mass.rockstar',
            'mvir': 'mass.vir',
            'rvir': 'radius.vir',
            'type': 'type',  # to avoid getting yelled at
            'ovdens': 'ahf.overdensity',
            'nbins': 'ahf.profiles.nbins',
            'fmhires': 'ahf.frac.highres',
            'ekin': 'energy.kinetic',
            'epot': 'energy.potential',
            'hosthalo': 'parent.' + self.catalog_id_name,
            'numsubstruct': 'substructure.number',
            'surfp': 'surface.pressure.ahf',
            'phi0': 'phi0.ahf',
            'cnfw': 'concentration.nfw.ahf',
        }

        # properties to store as integers
        self.integer_properties = [
            self.catalog_id_name,
            'descendant.' + self.catalog_id_name,
            'particle.number',
            'core.number',
            'type',
            'i.dx',
            'i.so',
            'i.ph',
            'particle.child.number' 'parent.' + self.catalog_id_name,
            'substructure.number',
            'star.particle.number.ahf',
            'gas.particle.number.ahf',
            'ahf.profiles.nbins',
        ]

    def read_catalogs(
        self,
        snapshot_value_kind='redshift',
        snapshot_values=0,
        simulation_directory=halo_default.simulation_directory,
        rockstar_directory=halo_default.rockstar_directory,
        catalog_hdf5_directory=halo_default.rockstar_catalog_hdf5_directory,
        file_kind='hdf5',
        species='star',
        assign_species_pointers=False,
        host_number=1,
        assign_hosts_rotation=False,
        all_snapshot_list=True,
        simulation_name='',
    ):
        '''
        Read catalog of halos at snapshot[s] from Rockstar and/or ConsistentTrees.
        Return as list of dictionary classes.

        Parameters
        ----------
        snapshot_value_kind : string
            snapshot value kind: 'index', 'redshift', 'scalefactor'
        snapshot_values : int or float or list thereof
            index[s] or redshifts[s] or scale-factor[s] of snapshot file[s]
            if 'all' or None, read all snapshots with halo catalogs
        simulation_directory : string
            base directory of simulation
        rockstar_directory : string
            directory  of rockstar halo files
        catalog_hdf5_directory : str
            directory (within rockstar directory) of processed HDF5 halo files
        file_kind : string
            kind of catalog file to read: 'out', 'ascii', 'hlist', 'hdf5', 'ahf'
        species : str or list
            name[s] of particle species to read + assign to halos
        assign_species_pointers : bool
            whether to assign species particle pointer indices to reference snapshot (usually z = 0)
        host_number : int
            number of hosts to assign and compute coordinates relative to
            if 0 or None, skip host assignment
        assign_hosts_rotation : bool
            whether to read and assign principal axes rotation tensor of each host galaxy
        all_snapshot_list : bool
            if reading multiple snapshots, whether to create a list of halo catalogs of length
            equal to all snapshots in simulation (so halo catalog index = snapsht index)
        simulation_name : string
            name of simulation to store for future identification

        Returns
        -------
        hals : dictionary class or list thereof
            catalog[s] of halos at snapshot[s]
        '''
        Particle = ParticleClass(catalog_hdf5_directory)

        # parse input properties
        assert file_kind in ['out', 'ascii', 'hlist', 'hdf5', 'star', 'gas', 'dark', 'ahf']
        simulation_directory = ut.io.get_path(simulation_directory)
        rockstar_directory = ut.io.get_path(rockstar_directory)
        catalog_hdf5_directory = ut.io.get_path(catalog_hdf5_directory)

        self.Snapshot = ut.simulation.read_snapshot_times(simulation_directory)
        snapshot_indices = self.Snapshot.parse_snapshot_values(snapshot_value_kind, snapshot_values)

        hals = [[] for _ in self.Snapshot['index']]  # list of halo catalogs across all snapshots

        # get names of all halo files to read
        path_file_names, file_values = self._get_catalog_file_names_and_values(
            simulation_directory + rockstar_directory,
            catalog_hdf5_directory,
            snapshot_indices,
            file_kind,
        )

        if len(path_file_names) == 0:
            raise OSError(
                'cannot find any halo catalog files of type {} in:  {}'.format(
                    file_kind, simulation_directory + rockstar_directory.lstrip('./')
                )
            )

        # get snapshot indices corresponding to existing halo files
        if 'hlist' in file_kind:
            file_snapshot_indices = self.Snapshot.parse_snapshot_values(
                'scalefactor', file_values, verbose=False
            )
        else:
            file_snapshot_indices = file_values

        if host_number is not None and host_number > 0:
            # if 'elvis' is in simulation directory name, force 2 hosts
            host_number = ut.catalog.get_host_number_from_directory(
                host_number, simulation_directory, os
            )

        # initialize
        Cosmology = None

        # read halos at all input snapshots
        for path_file_name, snapshot_index in zip(path_file_names, file_snapshot_indices):
            # read halos
            if 'hdf5' in path_file_name:
                hal, header = self._io_catalog_hdf5(
                    simulation_directory + rockstar_directory,
                    catalog_hdf5_directory,
                    snapshot_index,
                )
            elif 'out' in path_file_name or 'ascii' in path_file_name or 'hlist' in path_file_name:
                hal, header = self._read_catalog_text(path_file_name)
            elif 'ahf' in file_kind:
                hal, header = self._read_catalog_ahf(path_file_name)

            if len(hal) > 0:
                # assign cosmological parameters via cosmology class
                if Cosmology is None:
                    Cosmology = self._get_cosmology(simulation_directory, header)
                hal.Cosmology = Cosmology

                # assign information on all snapshots
                hal.Snapshot = self.Snapshot

                self._assign_simulation_information(
                    hal, header, snapshot_index, file_kind, simulation_directory, simulation_name
                )

                if 'hdf5' in file_kind and species is not None and len(species) > 0:
                    # try assigning particle species properties, if file exists
                    Particle.io_species_hdf5(
                        species,
                        hal,
                        None,
                        simulation_directory,
                        rockstar_directory,
                        catalog_hdf5_directory,
                        assign_species_pointers,
                        verbose=True,
                    )

                if host_number is not None and host_number > 0:
                    # assign primary host[s]
                    self.assign_hosts_to_catalog(hal, 'halo', host_number)
                    hal.info['host.number'] = host_number

                if assign_hosts_rotation:
                    # assign principle axes rotation tensor of each host galaxy
                    self.assign_hosts_rotation(hal, simulation_directory)

            # if read single snapshot, return as dictionary instead of list
            if len(file_snapshot_indices) == 1:
                hals = hal
            else:
                hals[snapshot_index] = hal
                if snapshot_index != file_snapshot_indices[-1]:
                    print()

        if len(file_snapshot_indices) > 1 and not all_snapshot_list:
            hals = [hal for hal in hals if len(hal)]

        return hals

    def read_catalogs_simulations(
        self,
        snapshot_value_kind='redshift',
        snapshot_value=0,
        simulation_directories=None,
        rockstar_directory=halo_default.rockstar_directory,
        catalog_hdf5_directory=halo_default.rockstar_catalog_hdf5_directory,
        file_kind='hdf5',
        species='star',
        assign_species_pointers=False,
        host_number=1,
        assign_hosts_rotation=False,
        all_snapshot_list=True,
    ):
        '''
        Read catalog of halos at single snapshot across various simulations.
        Return as list of dictionary classes.

        Parameters
        ----------
        snapshot_value_kind : str
            snapshot value kind: 'index', 'redshift', 'scalefactor'
        snapshot_value : int or float or list thereof
            index[s] or redshifts[s] or scale-factor[s] of snapshot file[s]
            if 'all' or None, read all snapshots with halo catalogs
        simulation_directories : list of strings
            directories of simulations
        rockstar_directory : str
            sub-directory (within simulation_directory) of halo files
        catalog_hdf5_directory : str
            directory (within rockstar directory) of processed HDF5 halo files
        file_kind : str
            kind of catalog file to read:
                'out', 'ascii', 'hlist', 'hdf5', 'star', 'gas', 'dark', 'ahf'
        species : str or list
            name[s] of particle species to read + assign to halos
        assign_species_pointers : bool
            whether to assign species particle pointer indices to reference snapshot (usually z = 0)
        host_number : int
            number of hosts to assign and compute coordinates relative to
            if 0 or None, skip host assignment
        assign_hosts_rotation : bool
            whether to read and assign principal axes rotation tensor of each host galaxy
        all_snapshot_list : bool
            if reading multiple snapshots, whether to create a list of halo catalogs of length
            equal to all snapshots in simulation (so halo catalog index = snapsht index)

        Returns
        -------
        hals : list of dictionary classes
            catalogs of halos across simulations
        '''
        # parse list of directories
        if np.ndim(simulation_directories) == 0:
            raise ValueError(
                f'input simulation_directories = {simulation_directories} but need to input list'
            )
        elif np.ndim(simulation_directories) == 1:
            # assign null names
            simulation_directories = list(
                zip(simulation_directories, ['' for _ in simulation_directories])
            )
        elif np.ndim(simulation_directories) == 2:
            pass
        elif np.ndim(simulation_directories) >= 3:
            raise ValueError(
                'not sure how to parse simulation_directories = {simulation_directories}'
            )

        hals = []
        directories_read = []
        for simulation_directory, simulation_name in simulation_directories:
            try:
                hal = self.read_catalogs(
                    snapshot_value_kind,
                    snapshot_value,
                    simulation_directory,
                    rockstar_directory,
                    catalog_hdf5_directory,
                    file_kind,
                    species,
                    assign_species_pointers,
                    host_number,
                    assign_hosts_rotation,
                    all_snapshot_list,
                    simulation_name,
                )

                hals.append(hal)
                directories_read.append(simulation_directory)

            except Exception:
                self.say(
                    '! cannot read halo catalog at {} = {} in {}'.format(
                        snapshot_value_kind, snapshot_value, simulation_directory
                    )
                )

        if len(hals) == 0:
            self.say(f'! cannot read any halo catalogs at {snapshot_value_kind} = {snapshot_value}')
            return

        return hals

    def _header_to_dtypes(self, path_file_name):
        def isint(string):
            try:
                int(string)
                return True
            except ValueError:
                return False

        it = self.int_type
        ft = self.float_type

        with open(path_file_name, 'r', encoding='utf-8') as f:
            header = f.readline()

        colnames = header.lower().lstrip('#').split()

        # strip off the column numbers if they're included (they are on hlists)
        if colnames[0].endswith('(0)') or colnames[0].endswith('(1)'):
            for ci, colname in enumerate(colnames):
                colnames[ci] = colname.rsplit('(')[0]

        # things to deal with that I don't straight rename:
        # mvir and mXXXXX, rvir or rXXXXX,
        # mXXXXX_hires and mXXXXX_lowres
        # mbound_xxxx -> mass.bound

        # so, super annoyingly
        # -- in the ascii files: m200b is the total mass and mbound_200b is the bound mass
        # -- in the out files: m200b is the bound mass, m200b_all is the total mass
        # handle this by looking for the mbound_ string
        explicit_bound = False
        if 'mbound_' in header:
            explicit_bound = True

        # in AHF, we only get one mass, so we just call it mass; in rockstar, we get several
        rockstar_masses = False
        if 'mbound_' in header or '_all' in header:
            rockstar_masses = True

        dtype_list = []
        added_columns = []
        for col in colnames:
            # first handle mass and radius in AHF
            if not rockstar_masses and col == 'mvir':
                out = 'mass'
                assert out not in added_columns  # should only be one
                dtype_list.append((out, ft))
                added_columns.append(out)

            elif not rockstar_masses and col == 'rvir':
                out = 'radius'
                assert out not in added_columns  # should only be one
                dtype_list.append((out, ft))
                added_columns.append(out)

            # have I defined it's new name explicity?
            elif col in self.property_new_names:
                out = self.property_new_names[col]
                assert out not in added_columns
                if out in self.integer_properties:
                    dtype_list.append((out, it))
                else:
                    dtype_list.append((out, ft))
                added_columns.append(out)

            # have I defined it's new name (minus an _gas or _star) explicity?
            elif (col.endswith('_gas') or col.endswith('_star')) and (
                col.rsplit('_', 1)[0] in self.property_new_names
            ):
                spec_name = col.split('_')[-1]
                root = self.property_new_names[col.rsplit('_', 1)[0]]
                out = spec_name + '.' + root
                assert out not in added_columns
                if root in self.integer_properties:
                    dtype_list.append((out, it))
                else:
                    dtype_list.append((out, ft))
                added_columns.append(out)

            # otherwise, is it a modified version of a name I know how to handle?
            elif 'mbound_' in col:
                out = 'mass.bound'
                assert out not in added_columns  # should only be one
                dtype_list.append((out, ft))
                added_columns.append(out)

            elif '_hires' in col:
                out = 'mass.hires'
                assert out not in added_columns  # should only be one
                dtype_list.append((out, ft))
                added_columns.append(out)

            elif '_lowres' in col:
                out = 'mass.lowres'
                assert out not in added_columns  # should only be one
                dtype_list.append((out, ft))
                added_columns.append(out)

            # is it a mass or radius?
            elif col[0] in ['m', 'r'] and isint(col.split('_')[0][1:-1]):
                # should find anything like m200c, r200c, m200b, m2500c, m200b_all, etc.
                prefix = 'mass.' if col[0] == 'm' else 'radius.'
                if not explicit_bound:
                    # mbound isn't set explicitly, so check if this is an _all
                    if '_all' in col:
                        # then this is total mass, and just gets called 'mass'
                        out = 'mass'
                        assert out not in added_columns
                        dtype_list.append((out, ft))
                        added_columns.append(out)
                        continue
                    # this isn't an 'all' column, but is it the bound equivalent?
                    elif col + '_all' in colnames:
                        out = 'mass.bound'
                        assert out not in added_columns  # should only be one
                        dtype_list.append((out, ft))
                        added_columns.append(out)
                        continue

                # if not caught in the above, then this is just an M_200b or R_200b or
                # something like that
                if col[-1] in ['b', 'm']:
                    # then I'm working with a mass/radius wrt. the background, so use the 'm' suffix
                    suffix = 'm'
                else:
                    # then I (should be/am) working with a mass/radius wrt critical,
                    # so use the 'c' suffix
                    suffix = 'c'

                prop_name = prefix + col[1:-1] + suffix
                if prop_name == 'mass.200m' or prop_name == 'radius.200m':
                    prop_name = prop_name.split('.')[0]
                assert prop_name not in added_columns
                dtype_list.append((prop_name, ft))
                added_columns.append(prop_name)
            else:
                assert col not in added_columns
                self.say(f'! warning: cannot rename {col}; taking as is')
                dtype_list.append((col, ft))
                added_columns.append(col)

        return dtype_list

    def _read_catalog_text(self, path_file_name):
        '''
        Read catalog of halos at snapshot from Rockstar text file[s] (halos_*.ascii or out_*.list)
        or from ConsistentTrees halo history text file (hlist*.list).

        Parameters
        ----------
        path_file_name : str
            path + file name of halo file - if multiple blocks, input 0th one

        Returns
        -------
        hal : class
            catalog of halos at snapshot
        header : dict
            header information
        '''
        it = self.int_type
        ft = self.float_type

        # store as dictionary class
        hal = HaloDictionaryClass()
        header = {}

        # read header to get cosmology ----------
        with open(path_file_name, 'r', encoding='utf-8') as file_in:
            if 'ascii' in path_file_name or 'out' in path_file_name:
                for line in file_in:
                    if 'a = ' in line:
                        index = line.rfind('a = ')
                        header['scalefactor'] = float(line[index + 4 : index + 12])
                    if 'h = ' in line:
                        index = line.rfind('h = ')
                        header['hubble'] = float(line[index + 4 : index + 12])
                    if 'Om = ' in line:
                        index = line.rfind('Om = ')
                        header['omega_matter'] = float(line[index + 5 : index + 13])
                    if 'Ol = ' in line:
                        index = line.rfind('Ol = ')
                        header['omega_lambda'] = float(line[index + 5 : index + 13])
                    if 'Box size: ' in line:
                        index = line.rfind('Box size: ')
                        header['box.length/h'] = float(line[index + 10 : index + 19])
                        # convert to [kpc/h comoving]
                        header['box.length/h'] *= ut.constant.kilo_per_mega
                    if 'Particle mass: ' in line:
                        index = line.rfind('Particle mass: ')
                        header['dark.particle.mass'] = float(line[index + 15 : index + 26])

                header['dark.particle.mass'] /= header['hubble']  # convert to [M_sun]

            elif 'hlist' in path_file_name or 'tree' in path_file_name:
                for line in file_in:
                    if 'h0 = ' in line:
                        index = line.rfind('h0 = ')
                        header['hubble'] = float(line[index + 5 : index + 13])
                    if 'Omega_M = ' in line:
                        index = line.rfind('Omega_M = ')
                        header['omega_matter'] = float(line[index + 10 : index + 18])
                    if 'Omega_L = ' in line:
                        index = line.rfind('Omega_L = ')
                        header['omega_lambda'] = float(line[index + 10 : index + 18])
                    if 'box size = ' in line:
                        index = line.rfind('box size = ')
                        header['box.length/h'] = float(line[index + 11 : index + 20])
                        # convert to [kpc/h comoving]
                        header['box.length/h'] *= ut.constant.kilo_per_mega

                header['dark.particle.mass'] = np.nan

        # initialize rest of cosmological parameters for later
        header['omega_baryon'] = None
        header['sigma_8'] = None
        header['n_s'] = None

        if 'ascii' in path_file_name:
            # get all file blocks
            file_name_base = path_file_name.replace('.0.', '.*.')
            path_file_names = ut.io.get_file_names(file_name_base)
            # loop over multiple blocks per snapshot

            # read first line of first file to get the header information to create column names
            dtypes = self._header_to_dtypes(path_file_names[0])
            for file_block_index, path_file_name in enumerate(path_file_names):
                hal_read = np.loadtxt(path_file_name, encoding='utf-8', comments='#', dtype=dtypes)

                for prop_name in hal_read.dtype.names:
                    if prop_name not in self.ignore_properties:
                        if file_block_index == 0:
                            hal[prop_name] = hal_read[prop_name]
                        else:
                            hal[prop_name] = np.append(hal[prop_name], hal_read[prop_name])

            self.say(f'* read {hal[self.prop_name_default].size} halos from:')
            for path_file_name in path_file_names:
                self.say(path_file_name.lstrip('./'))
            self.say('')

        elif 'out' in path_file_name:
            dtypes = self._header_to_dtypes(path_file_name)
            hal_read = np.loadtxt(path_file_name, encoding='utf-8', comments='#', dtype=dtypes)

            for prop_name in hal_read.dtype.names:
                if prop_name not in self.ignore_properties:
                    hal[prop_name] = hal_read[prop_name]

            self.say(
                '* read {} halos from:  {}\n'.format(
                    hal[self.prop_name_default].size, path_file_name.lstrip('./')
                )
            )

        elif 'hlist' in path_file_name:
            hal_read = np.loadtxt(
                path_file_name,
                encoding='utf-8',
                comments='#',
                usecols=range(87),  # ignore any added fields in newer versions of ConsistentTrees
                dtype=[
                    # properties copied from merger tree
                    ('scalefactor', ft),  # [convert to snapshot index] of halo
                    (self.tree_id_name, it),  # tree ID (unique across all snapshots)
                    ('descendant.scalefactor', ft),  # [snapshot index] of descendant
                    ('descendant.' + self.tree_id_name, it),  # [tree index] of descendant
                    ('progenitor.number', it),  # number of progenitors
                    ('central.local.' + self.tree_id_name, it),  # [tree index] of local central
                    ('central.' + self.tree_id_name, it),  # [tree index] of most massive central
                    ('descendant.central.local.' + self.tree_id_name, it),
                    ('am.phantom', it),  # whether halo is interpolated across snapshots
                    ('sam.mass.vir', ft),  # ignore
                    ('mass.bound', ft),  # bound mass
                    ('radius', ft),  # halo radius
                    ('scale.radius', ft),  # NFW scale radius
                    ('vel.std', ft),  # velocity dispersion
                    ('am.progenitor.main', it),  # whether am most massive progenitor of descendant
                    ('major.merger.scalefactor', ft),  # [snapshot index] of last major merger
                    ('vel.circ.max', ft),  # maximum of circular velocity
                    ('position.x', ft),
                    ('position.y', ft),
                    ('position.z', ft),  # center position
                    ('velocity.x', ft),
                    ('velocity.y', ft),
                    ('velocity.z', ft),  # center velocity
                    ('momentum.ang.x', ft),
                    ('momentum.ang.y', ft),
                    ('momentum.ang.z', ft),
                    ('spin.peebles', ft),  # dimensionless spin parameter
                    ('breadth.index', it),  # (same as tree index?)
                    ('dindex', it),  # depth-first order (index) within tree
                    ('final.' + self.tree_id_name, it),  # [tree index] at final snapshot
                    (self.catalog_id_name, it),  # catalog ID at snapshot frdom rockstar catalog
                    ('snapshot.index', it),
                    ('progenitor.co.dindex', it),  # depth-first index of next co-progenitor
                    ('progenitor.last.dindex', it),  # depth-first index of last progenitor
                    ('progenitor.main.last.dindex', it),  # ... of last prog on main prog branch
                    ('tidal.force', ft),  # strongest tidal force from any halo (Rhalo / Rhill)
                    ('tidal.' + self.tree_id_name, it),  # [tree index] of above neighboring halo
                    ('scale.radius.klypin', ft),  # NFW scale radius from radius(vel.circ.max)
                    ('mass', ft),  # total mass within halo radius (including unbound)
                    ('mass.vir', ft),
                    ('mass.200c', ft),
                    ('mass.500c', ft),
                    ('mass.180m', ft),
                    ('position.offset', ft),  # offset of density peak from particle average
                    ('velocity.offset', ft),
                    ('spin.bullock', ft),  # dimensionless spin from Bullock++ (J/(sqrt(2)*GMVR))
                    ('axis.b/a', ft),  # ratio of 2nd & 3rd to 1st largest shape ellipsoid axes
                    ('axis.c/a', ft),  # (Allgood et al 2006)
                    ('axis.x', ft),
                    ('axis.y', ft),
                    ('axis.z', ft),
                    ('axis.b/a.500c', ft),
                    ('axis.c/a.500c', ft),
                    ('axis.x.500c', ft),
                    ('axis.y.500c', ft),
                    ('axis.z.500c', ft),
                    ('kinetic/potential', ft),  # ratio of kinetic to potential energies [ignore]
                    ('mass.pe.behroozi', ft),  # pseudo-evolution corrected mass
                    ('mass.pe.diemer', ft),  # pseudo-evolution corrected mass
                    ('type', it),  # ???
                    ('star.mass.rockstar', ft),  #
                    ('gas.mass.rockstar', ft),  #
                    ('blackhole.mass.rockstar', ft),  #
                    ('mass.hires', ft),  # mass in high-res DM particles (not always correct!)
                    ('mass.lowres', ft),  # mass in low-res DM particles (not always correct!)
                    # below properties computed from main progenitor history
                    ('infall.mass', ft),  # mass before fell into host halo (becoming a satellite)
                    ('mass.peak', ft),  # peak mass throughout history
                    ('infall.vel.circ.max', ft),  # vel.circ.max before fall into a host halo
                    ('vel.circ.peak', ft),  # peak vel.circ.max throughout history
                    ('mass.half.scalefactor', ft),  # [snapshot] when first half current mass
                    ('accrete.rate', ft),  # mass growth rate between snapshots
                    ('accrete.rate.100Myr', ft),  # mass growth rate averaged over 100 Myr
                    ('accrete.rate.tdyn', ft),  # mass growth rate averaged over dynamical time
                    ('accrete.rate.2tdyn', ft),  # mass growth rate averaged over 2 t_dyn
                    ('accrete.rate.mass.peak', ft),  #
                    ('accrete.rate.vel.circ.max', ft),  #
                    ('accrete.rate.vel.circ.max.tyn', ft),  #
                    ('mass.peak.scalefactor', ft),  # [snapshot] when reached mass.peak
                    ('infall.scalefactor', ft),  # [snapshot] before fell into host halo
                    ('infall.first.scalefactor', ft),  # [snapshot] before first fell into host halo
                    ('infall.first.mass', ft),  # mass before first fell into host halo
                    ('infall.first.vel.circ.max', ft),  # vel.circ.max before first fell in
                    ('mass.peak.vel.circ.max', ft),  # vel.circ.max at time of mass.peak
                    ('tidal.force.tdyn', ft),  # dimensionless tidal force ave over dynamical time
                    ('log.vnow/vdyn', ft),  # log10[Vmax_now / (Vmax@(Tdyn ago) OR Vmax@Mpeak)]
                    ('future.merger.time', ft),  # time [Gyr] until merges into larger halo
                    ('future.merger.id', ft),  # id of main progenitor of halo into which will merge
                    # ('spin.at.mpeak.scale', ft),  # ???
                ],
            )

            header['scalefactor'] = hal_read['scalefactor'][0]

            for prop_name in hal_read.dtype.names:
                if (
                    prop_name not in self.ignore_properties
                    and prop_name != 'scalefactor'
                    and ('.' + self.tree_id_name) not in prop_name
                    and 'dindex' not in prop_name
                ):
                    hal[prop_name] = hal_read[prop_name]

            self.say(
                '* read {} halos from:  {}\n'.format(
                    hal[self.prop_name_default].size, path_file_name.lstrip('./')
                )
            )

        del hal_read

        # convert properties
        for prop_name in hal:
            # if only 1 halo, make sure is array
            if hal[prop_name].size == 1:
                hal[prop_name] = np.array([hal[prop_name]], hal[prop_name].dtype)
            if 'mass' in prop_name and 'scalefactor' not in prop_name:
                hal[prop_name] *= 1 / header['hubble']  # to [M_sun]
            elif 'radius' in prop_name:
                hal[prop_name] *= header['scalefactor'] / header['hubble']  # to [kpc physical]
            elif 'position' in prop_name:
                hal[prop_name] *= ut.constant.kilo_per_mega / header['hubble']  # to [kpc comoving]
            elif 'momentum.ang' in prop_name:
                hal[prop_name] *= (header['scalefactor'] / header['hubble']) ** 2  # to [kpc phys]
            elif 'energy' in prop_name:
                hal[prop_name] *= header['scalefactor'] / header['hubble']  # to [kpc physical]
            elif 'index' in prop_name and np.min(hal[prop_name]) == -1:
                # ensure null pointer index is safely out of range
                hindices = np.where(hal[prop_name] == -1)[0]
                hal[prop_name][hindices] -= hal[prop_name].size

        # assign derived masses
        if 'mass' in hal:
            hal['mass.200m'] = hal['mass']  # pointer for clarity
        if 'star.mass.rockstar' in hal:
            hal['baryon.mass.rockstar'] = hal['gas.mass.rockstar'] + hal['star.mass.rockstar']
            hal['dark.mass'] = hal['mass'] - hal['baryon.mass.rockstar']

        # convert position and velocity to halo number x dimension number array
        for prop_name in [
            'position',
            'velocity',
            'bulk.velocity',
            'momentum.ang',
            'axis',
            'axis.500c',
        ]:
            if prop_name + '.x' in hal:
                hal[prop_name] = np.transpose(
                    [hal[prop_name + '.x'], hal[prop_name + '.y'], hal[prop_name + '.z']]
                )
                del (hal[prop_name + '.x'], hal[prop_name + '.y'], hal[prop_name + '.z'])

        # convert properties of snapshot scale-factor to snapshot index
        for prop_name in list(hal.keys()):
            if '.scalefactor' in prop_name:
                prop_name_new = prop_name.replace('.scalefactor', '.snapshot')
                hal[prop_name_new] = (
                    np.zeros(hal[self.prop_name_default].size, self.int_type)
                    - self.Snapshot['index'].size
                    - 1
                )  # initialize safely
                hindices = ut.array.get_indices(hal[prop_name], [1e-10, 1.00001])
                if hindices.size:
                    hal[prop_name_new][hindices] = self.Snapshot.get_snapshot_indices(
                        'scalefactor', hal[prop_name][hindices]
                    )
                del hal[prop_name]

        if hal[self.prop_name_default].size > 0:
            # assign conversion between halo id and index
            ut.catalog.assign_id_to_index(hal, self.catalog_id_name)

        return hal, header

    def _read_catalog_ahf(self, path_file_name, hubble=1.0, scalefactor=-1.0):
        '''
        Read halo catalogs from AHF text file[s].

        Parameters
        ----------
        file_names : str
            name of halo catalog file
        hubble : float
            Hubble paramter (H0 / 100 km/s) for unit conversions. only needed
            if MUSIC conf file isn't available to get hubble paramter from
        scalefactor : float
            scalefactor, for converting from comoving to physical coordinates.
            if not passed in, then extracted from the filename (but note the
            filename only has the redsfhit to 3 digits, z = x.xxx)

        Returns
        -------
        hal : class
            halo catalog at snapshot
        '''

        if len(path_file_name) == 0:
            self.say("!! warning! no file passed in to read! expect error.")

        path_file_name_base = path_file_name.replace('.0000.', '.*.')
        path_file_names = ut.io.get_file_names(path_file_name_base)

        # store as dictionary class ----------
        hal = HaloDictionaryClass()

        # attempt to read the cosmology from the MUSIC .conf file
        print("-- attempting to read cosmology...")
        hal.Cosmology = self._get_cosmology(cosmo=dict())
        if 'hubble' in hal.Cosmology:
            if hal.Cosmology['hubble'] is not None:
                hubble = hal.Cosmology['hubble']
                self.say('* using hubble paramter = {hubble}', end='')
        else:
            if hubble == 1.0:
                self.say(
                    '!! warning: cannot find hubble paramter, and not passed in,'
                    + ' so returning in h-inverse units'
                )

        # get the redshift/scale factor from the AHF file name
        if scalefactor <= 0:
            rshift = float(path_file_names[0].split('.z')[-1].split('.AHF')[0])
            scalefactor = 1.0 / (1 + rshift)
            self.say('and a scale-factor = {scalefactor}\n')

        # read header to column names
        dtypes = self._header_to_dtypes(path_file_names[0])

        # loop over (potentially) multiple blocks per snapshot
        for file_block_index, path_file_name in enumerate(path_file_names):
            hal_read = np.loadtxt(path_file_name, encoding='utf-8', comments='#', dtype=dtypes)

            for prop_name in hal_read.dtype.names:
                if prop_name not in self.ignore_properties:
                    if file_block_index == 0:
                        hal[prop_name] = hal_read[prop_name]
                    else:
                        hal[prop_name] = np.append(hal[prop_name], hal_read[prop_name])

        self.say('* read {} halos from:'.format(hal['id'].size))
        for path_file_name in path_file_names:
            self.say(path_file_name.lstrip('./'))
        self.say('')

        del hal_read

        # convert properties
        for prop_name in hal:
            # if only 1 halo, make sure is array
            if hal[prop_name].size == 1:
                hal[prop_name] = np.array([hal[prop_name]], hal[prop_name].dtype)
            if 'mass' in prop_name:
                hal[prop_name] *= 1 / hubble  # to [M_sun]
            elif 'radius' in prop_name:
                hal[prop_name] *= scalefactor / hubble  # to [kpc physical]
            elif 'position' in prop_name:
                # hal[prop_name] *= ut.constant.kilo_per_mega / hubble  # to [kpc comoving]
                # to [kpc comoving] - in the newest version of AHF I (Shea) have,
                # it output pos in kpc/h, so just divide by hubble
                hal[prop_name] *= 1 / hubble
            elif 'momentum.ang' in prop_name:
                hal[prop_name] *= (scalefactor / hubble) ** 2  # to [kpc physical]
            elif 'energy' in prop_name:
                hal[prop_name] *= scalefactor / hubble  # to [kpc physical]

        # assign derived quantities ----------
        hal['lowres.mass.frac'] = 1.0 - hal['ahf.frac.highres']
        # hal['radius'] = hal['radius.'+default_vir_type]
        # hal['mass'] = hal['mass.'+default_vir_type]
        if 'gas.mass.ahf' in hal:
            hal['baryon.mass.ahf'] = hal['gas.mass.ahf'] + hal['star.mass.ahf']
            hal['dark.mass'] = hal['mass'] - hal['baryon.mass.ahf']
            hal['mass.lowres'] = hal['dark.mass'] * hal['lowres.mass.frac']
        else:
            hal['mass.lowres'] = hal['mass'] * hal['lowres.mass.frac']

        hal['vel.circ.max.1d'] = hal['vel.circ.max'] / np.sqrt(3)
        hal['vel.std.1d'] = hal['vel.std'] / np.sqrt(3)

        # convert position and velocity to halo number x dimension number array
        for prop_name in [
            'position',
            'velocity',
            'bulk.velocity',
            'momentum.ang',
            'axis',
            'axis.500c',
            'axis.a',
            'axis.b',
            'axis.c',
            'gas.ahf.momentum.ang',
            'gas.ahf.axis.a',
            'gas.ahf.axis.b',
            'gas.ahf.axis.c',
            'star.ahf.momentum.ang',
            'star.ahf.axis.a',
            'star.ahf.axis.b',
            'star.ahf.axis.c',
        ]:
            if prop_name + '.x' in hal:
                # swap .ahf to the end, as it should be for keeping with the style of other props
                if 'ahf' in prop_name:
                    idx = prop_name.index('.ahf')
                    oprop = prop_name[:idx] + prop_name[idx + len('.ahf') :] + '.ahf'
                else:
                    oprop = prop_name
                hal[oprop] = np.transpose(
                    [hal[prop_name + '.x'], hal[prop_name + '.y'], hal[prop_name + '.z']]
                )
                del (hal[prop_name + '.x'], hal[prop_name + '.y'], hal[prop_name + '.z'])

        for prop_name in list(hal.keys()):
            if '.scalefactor' in prop_name:
                prop_name_new = prop_name.replace('.scalefactor', '.snapshot')
                hal[prop_name_new] = (
                    np.zeros(hal[self.prop_name_default].size, self.int_type)
                    - self.Snapshot['index'].size
                    - 1
                )  # initialize safely
                hindices = ut.array.get_indices(hal[prop_name], [1e-10, 1.00001])
                if hindices.size:
                    hal[prop_name_new][hindices] = self.Snapshot.get_snapshot_indices(
                        'scalefactor', hal[prop_name][hindices]
                    )
                del hal[prop_name]

        # assign auxilliary information to the header ----------
        # assign information on snapshot time
        header = {}
        header['scalefactor'] = scalefactor
        header['hubble'] = hubble
        if 'omega_matter' in hal.Cosmology:
            header['omega_matter'] = hal.Cosmology['omega_matter']
            header['omega_lambda'] = hal.Cosmology['omega_lambda']
        header['box.length/h'] = None  # not stored
        header['index'] = self.Snapshot.get_snapshot_indices('scalefactor', scalefactor)
        header['redshift'] = 1.0 / scalefactor - 1
        header['time'] = (hal.Cosmology.get_time(scalefactor, 'scalefactor'),)
        header['time.lookback'] = hal.Cosmology.get_time(0) - hal.Cosmology.get_time(
            scalefactor, 'scalefactor'
        )
        header['time.hubble'] = ut.constant.Gyr_per_sec / hal.Cosmology.get_hubble_parameter(0)

        header['dark.particle.mass'] = None

        return hal, header

    def _io_catalog_hdf5(
        self,
        rockstar_directory=halo_default.rockstar_directory,
        catalog_hdf5_directory=halo_default.rockstar_catalog_hdf5_directory,
        snapshot_index=None,
        hal=None,
    ):
        '''
        Read/write halo catalog at a snapshot to/from HDF5 file.
        If reading, return as dictionary class.

        Parameters
        ----------
        rockstar_directory : str
            directory (wrt a simulation_directory) of rockstar files
        catalog_hdf5_directory : str
            directory (within rockstar directory) of processed HDF5 halo files
        snapshot_index : int
            index of snapshot
        hal : class
            catalog of halos at snapshot, if writing

        Returns
        -------
        hal : class
            catalog of halos at snapshot
        '''
        # parse inputs
        assert snapshot_index is not None or hal is not None
        file_path = ut.io.get_path(rockstar_directory) + ut.io.get_path(catalog_hdf5_directory)
        if not snapshot_index:
            snapshot_index = hal.snapshot['index']

        file_name = 'halo_{:03d}'.format(snapshot_index)
        path_file_name = file_path + file_name

        if hal is not None:
            # write to file
            file_path = ut.io.get_path(file_path, create_path=True)

            properties_add = []
            for prop_name in hal.info:
                if not isinstance(hal.info[prop_name], str):
                    hal['info:' + prop_name] = np.array(hal.info[prop_name])
                    properties_add.append('info:' + prop_name)

            for prop_name in hal.snapshot:
                hal['snapshot:' + prop_name] = np.array(hal.snapshot[prop_name])
                properties_add.append('snapshot:' + prop_name)

            for prop_name in hal.Cosmology:
                hal['cosmology:' + prop_name] = np.array(hal.Cosmology[prop_name])
                properties_add.append('cosmology:' + prop_name)

            ut.io.file_hdf5(path_file_name, hal)

            for prop_name in properties_add:
                del hal[prop_name]

        else:
            # read from file

            # store as dictionary class
            hal = HaloDictionaryClass()
            header = {}

            try:
                # try to read from file
                hal_read = ut.io.file_hdf5(path_file_name, verbose=False)

                for prop_name, hal_prop in hal_read.items():
                    if 'info:' in prop_name:
                        hal_prop_name = prop_name.split(':')[-1]
                        header[hal_prop_name] = float(hal_prop)
                    elif 'snapshot:' in prop_name:
                        hal_prop_name = prop_name.split(':')[-1]
                        if hal_prop_name == 'index':
                            header[hal_prop_name] = int(hal_prop)
                        else:
                            header[hal_prop_name] = float(hal_prop)
                    elif 'cosmology:' in prop_name:
                        hal_prop_name = prop_name.split(':')[-1]
                        header[hal_prop_name] = float(hal_prop)
                    else:
                        hal[prop_name] = hal_prop

                # hack to get the AHF catalogs working again
                if (
                    (self.prop_name_default not in hal)
                    and (self.prop_name_default == 'mass')
                    and ('mass.vir' in hal)
                ):
                    self.say("-- warning:  setting 'mass' = 'mass.vir'")
                    hal[self.prop_name_default] = hal['mass.vir']

                self.say(
                    '* read {} halos from:  {}.hdf5'.format(
                        hal[self.prop_name_default].size, path_file_name.lstrip('./')
                    )
                )

                # for positive-definite properties, convert null values from nan to -1
                for prop_name in hal:
                    if (
                        'velocity' not in prop_name
                        and 'position' not in prop_name
                        and 'distance' not in prop_name
                        and 'accrete' not in prop_name
                        and 'energy' not in prop_name
                    ):
                        masks = np.isnan(hal[prop_name])
                        if np.max(masks):
                            hal[prop_name][masks] = -1

            except OSError as exc:
                raise OSError(f'! cannot read halo catalog at snapshot {snapshot_index}') from exc

            return hal, header

    def _get_catalog_file_names_and_values(
        self,
        rockstar_directory=halo_default.rockstar_directory,
        catalog_hdf5_directory=halo_default.rockstar_catalog_hdf5_directory,
        snapshot_indices=None,
        file_kind='out',
    ):
        '''
        Get name[s] and snapshot value[s] (index or scale-factor) of halo catalog file[s] from
        Rockstar or AHF.

        Parameters
        ----------
        rockstar_directory : str
            directory (wrt simulation_directory) of rockstar files
        catalog_hdf5_directory : str
            directory (within rockstar directory) of processed HDF5 halo files
        snapshot_indices : int or array thereof
            index of snapshot
        file_kind : str
            kind of file: 'out', 'ascii', 'hlist', 'ahf', 'hdf5', 'star', 'gas', 'dark',

        Returns
        -------
        path_file_names : list
            path + name[s] of halo file[s]
        file_values : list
            snapshot value[s] (index or scale-factor) of halo file[s]
        '''
        assert file_kind in ['out', 'ascii', 'hlist', 'hdf5', 'star', 'gas', 'dark', 'ahf']

        snapshot_values = snapshot_indices

        rockstar_directory = ut.io.get_path(rockstar_directory)
        catalog_hdf5_directory = ut.io.get_path(catalog_hdf5_directory)

        if 'out' in file_kind:
            file_name_base = 'out_*.list'
            file_number_type = int
            directory = ut.io.get_path(rockstar_directory) + self.catalog_directory
        elif 'ascii' in file_kind:
            file_name_base = 'halos_*.ascii'
            file_number_type = float
            directory = ut.io.get_path(rockstar_directory) + self.catalog_directory
        elif 'hlist' in file_kind:
            file_name_base = 'hlist_*.list'
            file_number_type = float
            directory = ut.io.get_path(rockstar_directory) + self.catalog_hlist_directory
            snapshot_values = self.Snapshot['scalefactor'][snapshot_indices]
        elif 'ahf' in file_kind:
            directory = ut.io.get_path(rockstar_directory) + self.catalog_directory
            file_name_base = '*.z*.*.AHF_halos'
            file_number_type = float
        elif 'hdf5' in file_kind:
            if 'star' in file_kind:
                file_name_base = 'star_*.hdf5'
            elif 'gas' in file_kind:
                file_name_base = 'gas_*.hdf5'
            elif 'dark' in file_kind:
                file_name_base = 'dark_*.hdf5'
            else:
                file_name_base = 'halo_*.hdf5'
            file_number_type = int
            directory = rockstar_directory + catalog_hdf5_directory
        elif 'star' in file_kind:
            file_name_base = 'star_*.hdf5'
            file_number_type = int
            directory = rockstar_directory + catalog_hdf5_directory
        elif 'gas' in file_kind:
            file_name_base = 'gas_*.hdf5'
            file_number_type = int
            directory = rockstar_directory + catalog_hdf5_directory
        elif 'dark' in file_kind:
            file_name_base = 'dark_*.hdf5'
            file_number_type = int
            directory = rockstar_directory + catalog_hdf5_directory

        # get names and indices/scale-factors of all files that match name base
        # this can include multiple snapshots and/or multiple blocks per snapshot
        path_file_names_all, file_values_all = ut.io.get_file_names(
            directory + file_name_base, file_number_type, verbose=False
        )

        if snapshot_values is not None:
            path_file_names = []
            file_values = []
            for file_i, file_value in enumerate(file_values_all):
                if 'hlist' in file_kind:
                    # hlist files are labeled via scale-factor
                    if np.min(np.abs(file_value - snapshot_values)) < 1e-5:
                        path_file_names.append(path_file_names_all[file_i])
                        file_values.append(file_value)
                elif 'ahf' in file_kind:
                    # convert the redshift into the index
                    index = self.Snapshot.get_snapshot_indices('redshift', file_value)
                    if np.max(index == snapshot_values):
                        path_file_names.append(path_file_names_all[file_i])
                        file_values.append(index)
                else:
                    # all other files are labeled via snapshot index
                    # keep only block 0 if multiple blocks per snapshot
                    if np.max(file_value == snapshot_values):
                        path_file_names.append(path_file_names_all[file_i])
                        file_values.append(file_value)

            if np.isscalar(snapshot_values):
                snapshot_values = [snapshot_values]  # ensure is list
            if len(snapshot_values) > 1 and len(snapshot_values) != len(path_file_names):
                self.say(
                    '! input {} snapshot indices but found only {} halo catalog files'.format(
                        len(snapshot_values), len(path_file_names)
                    )
                )
        else:
            # return all that found
            path_file_names = path_file_names_all
            file_values = file_values_all

        if len(path_file_names) == 0:
            self.say(
                '! cannot find halo {} files in:  {}'.format(file_kind, directory.lstrip('./'))
            )

        return path_file_names, file_values

    def _get_cosmology(self, simulation_directory=halo_default.simulation_directory, cosmo={}):
        '''
        Get Cosmology class of cosmological parameters.
        If all cosmological parameters in input cosmo dictionary, use them.
        Else, try to read cosmological parameters from MUSIC initial condition config file.
        Else, assume AGORA cosmology as default.

        Parameters
        ----------
        simulation_directory : str
            directory of simulation
        cosmo : dict
            dictionary that includes cosmological parameters

        Returns
        -------
        Cosmology : class
            stores and computes cosmological parameters
        '''

        def _check_value(line, value_test=None):
            frac_dif_max = 0.01
            value = float(line.split('=')[-1].strip())
            if 'h0' in line:
                value /= 100
            if value_test is not None:
                frac_dif = np.abs((value - value_test) / value)
                if frac_dif > frac_dif_max:
                    print(f'! read {line}, but previously assigned = {value_test}')
            return value

        if (
            cosmo
            and cosmo.get('omega_lambda') is not None
            and cosmo.get('omega_matter') is not None
            and cosmo.get('omega_baryon') is not None
            and cosmo.get('hubble') is not None
            and cosmo.get('sigma_8') is not None
            and cosmo.get('n_s') is not None
        ):
            pass
        else:
            try:
                # try to find MUSIC file, assuming named *.conf
                simulation_directory = ut.io.get_path(simulation_directory)
                file_name_find = simulation_directory + '*/*.conf'
                path_file_name = ut.io.get_file_names(file_name_find)[0]
                self.say(
                    '* reading cosmological parameters from:  {}\n'.format(
                        path_file_name.lstrip('./')
                    )
                )
                # read cosmological parameters
                with open(path_file_name, 'r', encoding='utf-8') as file_in:
                    for line in file_in:
                        line = line.lower().strip().strip('\n')  # ensure lowercase for safety
                        if 'omega_l' in line:
                            cosmo['omega_lambda'] = _check_value(line, cosmo.get('omega_lambda'))
                        elif 'omega_m' in line:
                            cosmo['omega_matter'] = _check_value(line, cosmo.get('omega_matter'))
                        elif 'omega_b' in line:
                            cosmo['omega_baryon'] = _check_value(line, cosmo.get('omega_baryon'))
                        elif 'h0' in line:
                            cosmo['hubble'] = _check_value(line, cosmo.get('hubble'))
                        elif 'sigma_8' in line:
                            cosmo['sigma_8'] = _check_value(line, cosmo.get('sigma_8'))
                        elif 'nspec' in line:
                            cosmo['n_s'] = _check_value(line, cosmo.get('n_s'))
            except (OSError, IndexError):
                self.say('! cannot find MUSIC config file:  {}'.format(file_name_find.lstrip('./')))
                self.say('! assuming missing cosmological parameters from the AGORA box')
                if cosmo.get('omega_baryon') is None:
                    cosmo['omega_baryon'] = 0.0455
                    self.say('assuming omega_baryon = {}'.format(cosmo['omega_baryon']))
                if cosmo.get('sigma_8') is None:
                    cosmo['sigma_8'] = 0.807
                    self.say('assuming sigma_8 = {}'.format(cosmo['sigma_8']))
                if cosmo.get('n_s') is None:
                    cosmo['n_s'] = 0.961
                    self.say('assuming n_s = {}'.format(cosmo['n_s']))
                self.say('')

        Cosmology = ut.cosmology.CosmologyClass(
            cosmo['omega_lambda'],
            cosmo['omega_matter'],
            cosmo['omega_baryon'],
            cosmo['hubble'],
            cosmo['sigma_8'],
            cosmo['n_s'],
        )

        return Cosmology

    def _assign_simulation_information(
        self, hal, header, snapshot_index, file_kind, simulation_directory='', simulation_name=''
    ):
        '''
        Add information about snapshot to halo catalog.
        Append as dictionaries to halo dictionary class.

        Parameters
        ----------
        hal : dict class
            catalog of halos at snapshot
        header : dictionary
            header information from halo text file
        snapshot_index : int
            index of snapshot
        file_kind : str
            kind of catalog file to read: 'out', 'ascii', 'hlist', 'hdf5', 'star', 'gas', 'dark'
        simulation_directory : str
            directory of simulation
        simulation_name : str
            name of simulation to store for future identification
        '''
        simulation_directory = ut.io.get_path(simulation_directory)

        # assign information on current snapshot
        redshift = 1 / header['scalefactor'] - 1
        hal.snapshot = {
            'index': snapshot_index,
            'scalefactor': header['scalefactor'],
            'redshift': redshift,
            'time': hal.Cosmology.get_time(header['scalefactor'], 'scalefactor'),
            'time.lookback': (
                hal.Cosmology.get_time(0)
                - hal.Cosmology.get_time(header['scalefactor'], 'scalefactor')
            ),
            'time.hubble': ut.constant.Gyr_per_sec / hal.Cosmology.get_hubble_parameter(redshift),
        }

        # assign general information about simulation
        if not simulation_name and simulation_directory != './':
            simulation_name = simulation_directory.split('/')[-2]
            simulation_name = simulation_name.replace('_', ' ')
            simulation_name = simulation_name.replace('res', 'r')

        # hacks to get the elvis on FIRE AHF catalogs working again...
        if 'dark.particle.mass' not in header:
            header['dark.particle.mass'] = None
        if 'box.length' in header and 'box.length/h' not in header:
            header['box.length/h'] = header['box.length'] * header['hubble']

        hal.info = {
            'dark.particle.mass': header['dark.particle.mass'],
            'box.length/h': header['box.length/h'],
            'box.length': (
                None
                if header['box.length/h'] is None
                else header['box.length/h'] / header['hubble']
            ),
            'catalog.kind': 'halo.catalog',
            'file.kind': file_kind,
            'has.baryons': ut.catalog.get_is_baryonic_from_directory(simulation_directory, os),
            'host.number': 0,
            'simulation.name': simulation_name,
        }
        if hal.info['has.baryons']:
            hal.info['gas.particle.mass'] = (
                None
                if header['dark.particle.mass'] is None
                else (
                    header['dark.particle.mass']
                    * hal.Cosmology['omega_baryon']
                    / hal.Cosmology['omega_dm']
                )
            )

    def assign_hosts_to_catalog(self, hal, host_kind='halo', host_number=1):
        '''
        Assign primary host halo/galaxy[s] and coordinates relative to it/them.

        Parameters
        ----------
        hal : dictionary class
            catalog of halos at snapshot
        host_kind : str
            property to determine primary host: 'halo', 'star'
        host_number : int
            number of hosts to assign
        '''
        if host_number is True:
            host_number = 1
        elif host_number < 1:
            self.say(f'input host_number = {host_number}, skipping host assignment')
            return

        for host_rank in range(host_number):
            # host_index_name = ut.catalog.get_host_name(host_rank) + 'index'
            # if host_index_name not in hal:
            # always (re)assign host[s] (even if exist in catalog)
            self._assign_host_to_catalog(hal, host_kind, host_rank)

        if host_number > 1:
            # multiple hosts - assign nearest one to each halo
            self.say('* assigning nearest primary host')
            host_distancess = np.zeros(
                (hal['host.index'].size, host_number), dtype=hal['host.distance'].dtype
            )
            for host_rank in range(host_number):
                host_name = ut.catalog.get_host_name(host_rank)
                host_distancess[:, host_rank] = hal.prop(host_name + 'distance.total')

            host_nearest_indices = np.argmin(host_distancess, 1)

            # initialize all halos to the primary host
            for prop_name in list(hal.keys()):
                if 'host.' in prop_name and 'near.' not in prop_name:
                    prop_name_near = prop_name.replace('host.', 'host.near.')
                    hal[prop_name_near] = np.array(hal[prop_name])

            # assign other hosts
            for host_rank in range(1, host_number):
                hindices = np.where(host_nearest_indices == host_rank)[0]
                if hindices.size:
                    host_name = ut.catalog.get_host_name(host_rank)
                    self.say(
                        '{} halos are closest to {}'.format(
                            hindices.size, host_name.replace('.', '')
                        )
                    )
                    for prop_name in hal:
                        if host_name in prop_name and 'near.' not in prop_name:
                            prop_name_near = prop_name.replace(host_name, 'host.near.')
                            hal[prop_name_near][hindices] = hal[prop_name][hindices]
        print()

    def _assign_host_to_catalog(self, hal, host_kind='halo', host_rank=0):
        '''
        Assign the primary (or secondary etc) host halo/galaxy, and assign the position and velocity
        relative to it to all halos.
        Define the host as being the host_rank highest halo orderd by host_prop_name,
        with sufficiently low contamination from low-resolution dark matter.

        If host_kind is 'halo', define primary host as most massive halo in catalog,
        and use coordinates in halo catalog.
        If host_kind is 'star', define primary host as highest stellar mass galaxy in catalog,
        and use coordinate defined via stars.

        Parameters
        ----------
        hal : dictionary class
            catalog of halos at snapshot
        host_kind : str
            property to determine primary host: 'halo', 'star'
        host_rank : int
            which host (sorted by host_prop_name) to assign
        '''
        assert host_kind in ['halo', 'star']

        host_name = ut.catalog.get_host_name(host_rank)

        if host_kind == 'halo':
            host_prop_name = 'mass'  # property to use to determine primary host
            spec_prefix = ''
        elif host_kind == 'star':
            host_prop_name = 'star.mass'  # property to use to determine primary host
            spec_prefix = 'star.'
            host_name = spec_prefix + host_name

        self.say(
            '* assigning primary {} and coordinates wrt it to halo catalog...'.format(
                host_name.rstrip('.')
            ),
            end='',
        )

        # assign primary host coordinates only to halos with well defined mass
        hindices = ut.array.get_indices(hal.prop(host_prop_name), [1e-10, Inf])
        if 'mass.lowres' in hal:
            # check if halo catalog has low-res dark-matter mass stored, if so, select via it
            hindices_pure = ut.array.get_indices(
                hal.prop('lowres.mass.frac'), [0, self.lowres_mass_frac_max], hindices
            )
        else:
            self.say('! halo catalog does not have dark-matter \'mass.lowres\'')
            self.say('  cannot use it to select pure halos from which to select the host')
            hindices_pure = hindices

        host_index = hindices_pure[np.argsort(hal[host_prop_name][hindices_pure])][-host_rank - 1]

        hal[host_name + 'index'] = (
            np.zeros(hal[host_prop_name].size, dtype=self.int_type) + host_index
        )

        # distance to primary host
        hal[host_name + 'distance'] = (
            np.zeros(hal[spec_prefix + 'position'].shape, hal[spec_prefix + 'position'].dtype)
            * np.nan
        )
        hal[host_name + 'distance'][hindices] = ut.coordinate.get_distances(
            hal[spec_prefix + 'position'][hindices],
            hal[spec_prefix + 'position'][host_index],
            hal.info['box.length'],
            hal.snapshot['scalefactor'],
        )  # [kpc physical]

        # velocity wrt primary host
        hal[host_name + 'velocity'] = (
            np.zeros(hal[spec_prefix + 'velocity'].shape, hal[spec_prefix + 'velocity'].dtype)
            * np.nan
        )
        hal[host_name + 'velocity'][hindices] = ut.coordinate.get_velocity_differences(
            hal[spec_prefix + 'velocity'][hindices],
            hal[spec_prefix + 'velocity'][host_index],
            hal[spec_prefix + 'position'][hindices],
            hal[spec_prefix + 'position'][host_index],
            hal.info['box.length'],
            hal.snapshot['scalefactor'],
            hal.snapshot['time.hubble'],
        )

        # orbital velocities wrt primary host - use only halos with well defined host distance
        hindices = hindices[np.where(hal.prop(host_name + 'distance.total', hindices) > 0)[0]]

        distances_norm = np.transpose(
            hal[host_name + 'distance'][hindices].transpose()
            / hal.prop(host_name + 'distance.total', hindices)
        )  # need to do this way

        hal[host_name + 'velocity.tan'] = (
            np.zeros(hal[host_prop_name].size, hal[spec_prefix + 'velocity'].dtype) * np.nan
        )
        hal[host_name + 'velocity.tan'][hindices] = np.sqrt(
            np.sum(np.cross(hal[host_name + 'velocity'][hindices], distances_norm) ** 2, 1)
        )
        hal[host_name + 'velocity.tan'][host_index] = 0

        hal[host_name + 'velocity.rad'] = (
            np.zeros(hal[host_prop_name].size, hal[spec_prefix + 'velocity'].dtype) * np.nan
        )
        hal[host_name + 'velocity.rad'][hindices] = np.sum(
            hal[host_name + 'velocity'][hindices] * distances_norm, 1
        )
        hal[host_name + 'velocity.rad'][host_index] = 0

        self.say('finished')

    def _transfer_properties_catalog(self, hal_1, hal_2):
        '''
        Transfer/assign properties from hal_2 catalog to hal_1 catalog (at same snapshot).
        Primary use: transfer properties from ConsistentTrees halo history catalog (hlist) to
        Rockstar halo catalog.

        Parameters
        ----------
        hal_1 : dictionary class
            catalog of halos at snapshot
        hal_2 : dictionary class
            another catalog of same halos at same snapshot
        '''
        # parse input catalogs
        assert hal_1.snapshot['index'] == hal_2.snapshot['index']

        pointer_name = self.catalog_id_name + '.to.index'

        if pointer_name not in hal_1 or len(hal_1[pointer_name]) == 0:
            ut.catalog.assign_id_to_index(hal_1, self.catalog_id_name)

        hal_2_indices = ut.array.get_indices(
            hal_2[self.catalog_id_name], [0, hal_1[self.catalog_id_name].max() + 1]
        )
        hal_1_indices = hal_1[pointer_name][hal_2[self.catalog_id_name][hal_2_indices]]
        masks = hal_1_indices >= 0
        hal_1_indices = hal_1_indices[masks]
        hal_2_indices = hal_2_indices[masks]

        # sanity check - compare shared properties
        self.say('\n* shared properties with offsets: min, med, max, N_offset')
        for prop_name in hal_2:
            if prop_name in hal_1 and prop_name != pointer_name:
                prop_difs = hal_1[prop_name][hal_1_indices] - hal_2[prop_name][hal_2_indices]
                if np.abs(np.min(prop_difs)) > 1e-4 and np.abs(np.max(prop_difs)) > 1e-4:
                    self.say(
                        '{}: [{}, {}, {}] {}'.format(
                            prop_name,
                            np.min(prop_difs),
                            np.median(prop_difs),
                            np.max(prop_difs),
                            np.sum(np.abs(prop_difs) > 0),
                        )
                    )

        self.say('* assigning new properties')
        for prop_name in hal_2:
            if prop_name not in hal_1 and prop_name != pointer_name:
                self.say(f'{prop_name}')
                dtype = hal_2[prop_name].dtype
                null_value = -1
                # for properties that can be physically negative, initialize null values to nan
                if dtype == np.float32 or dtype == np.float64:
                    if (
                        'velocity' in prop_name
                        or 'position' in prop_name
                        or 'distance' in prop_name
                        or 'accrete' in prop_name
                        or 'energy' in prop_name
                    ):
                        null_value = np.nan
                # ensure snapshot index is safely negative to return error if called
                elif 'snapshot' in prop_name:
                    null_value = -hal_1.Snapshot['index'].size - 1

                hal_1[prop_name] = (
                    np.zeros(hal_1[self.catalog_id_name].size, hal_2[prop_name].dtype) + null_value
                )
                hal_1[prop_name][hal_1_indices] = hal_2[prop_name][hal_2_indices]

    # halo merger trees ----------
    def read_tree(
        self,
        simulation_directory=halo_default.simulation_directory,
        rockstar_directory=halo_default.rockstar_directory,
        catalog_hdf5_directory=halo_default.rockstar_catalog_hdf5_directory,
        file_kind='hdf5',
        species=None,
        species_snapshot_indices=None,
        assign_species_pointers=False,
        host_number=1,
        assign_hosts_rotation=False,
        simulation_name='',
        verbose=True,
    ):
        '''
        Read catalog of halo merger trees from ConsistentTrees (tree_*.dat or tree.hdf5).
        Return as dictionary class.

        Parameters
        ----------
        simulation_directory : str
            directory of simulation
        rockstar_directory : str
            sub-directory (within simulation_directory) of halo files
        catalog_hdf5_directory : str
            directory (within rockstar directory) of processed HDF5 halo files
        file_kind : str
            kind of halo tree file to read: 'text', 'hdf5'
        species : str or list
            name[s] of particle species to read + assign to halos
        species_snapshot_indices : array
            list of snapshot indices at which to assign particle species to tree
            if None, assign at all snapshots with particle species data
        assign_species_pointers : bool
            whether to assign species particle pointer indices to reference snapshot (usually z = 0)
        host_number : int
            number of hosts to assign and compute coordinates relative to
            if 0 or None, skip host assignment
        assign_hosts_rotation : bool
            whether to read and assign principal axes rotation tensor of each host galaxy
        simulation_name : str
            name of simulation to store for future identification
        verbose : bool
            whether to print diagnostics

        Returns
        -------
        halt : dictionary class or list thereof
            catalog of halo merger trees across all snapshots
        '''
        # parse input properties
        simulation_directory = ut.io.get_path(simulation_directory)
        rockstar_directory = ut.io.get_path(rockstar_directory)
        catalog_hdf5_directory = ut.io.get_path(catalog_hdf5_directory)
        assert file_kind in ['text', 'hdf5']

        # assign information about all snapshot times
        self.Snapshot = ut.simulation.read_snapshot_times(simulation_directory)

        if file_kind == 'text':
            halt, header = self._read_tree_text(simulation_directory + rockstar_directory)
        elif file_kind == 'hdf5':
            halt, header = self._io_tree_hdf5(
                simulation_directory + rockstar_directory, catalog_hdf5_directory
            )

        # assign auxilliary information
        # assign cosmological parameters via cosmology class
        halt.Cosmology = self._get_cosmology(simulation_directory, header)

        # assign information about all snapshot times
        halt.Snapshot = self.Snapshot

        # assign general information about simulation
        if not simulation_name and simulation_directory != './':
            simulation_name = simulation_directory.split('/')[-2]
            simulation_name = simulation_name.replace('_', ' ')
            simulation_name = simulation_name.replace('res', 'r')

        halt.info = {
            'box.length/h': header['box.length/h'],
            'box.length': header['box.length/h'] / header['hubble'],
            'catalog.kind': 'halo.tree',
            'file.kind': file_kind,
            'has.baryons': ut.catalog.get_is_baryonic_from_directory(simulation_directory, os),
            'host.number': 0,
            'simulation.name': simulation_name,
        }

        if 'hdf5' in file_kind and species:
            # try assigning particle species properties, if file exists
            self._assign_species_to_tree(
                halt,
                species,
                species_snapshot_indices,
                assign_species_pointers,
                simulation_directory,
                rockstar_directory,
                catalog_hdf5_directory,
                verbose=verbose,
            )

        if host_number is not None and host_number > 0:
            # if 'elvis' is in simulation directory name, force 2 hosts
            host_number = ut.catalog.get_host_number_from_directory(
                host_number, simulation_directory, os
            )
            self.assign_hosts_to_tree(halt, 'halo', host_number)
            halt.info['host.number'] = host_number

        if assign_hosts_rotation:
            self.assign_hosts_rotation(halt, simulation_directory)

        return halt

    def read_trees_simulations(
        self,
        simulation_directories,
        rockstar_directory=halo_default.rockstar_directory,
        catalog_hdf5_directory=halo_default.rockstar_catalog_hdf5_directory,
        file_kind='hdf5',
        species='star',
        species_snapshot_indices=None,
        assign_species_pointers=False,
        host_number=1,
    ):
        '''
        Read catalog of halo merger trees across different simulations.
        Return as list of dictionary classes.

        Parameters
        ----------
        simulation_directories : list of strings
            directories of simulations
        rockstar_directory : str
            sub-directory (within simulation_directory) of halo files
        catalog_hdf5_directory : str
            directory (within rockstar directory) of processed HDF5 halo files
        file_kind : str
            kind of halo tree file to read: 'text', 'hdf5'
        species : str or list
            name[s] of particle species to read + assign to halos
        species_snapshot_indices : array
            list of snapshot indices at which to assign particle species to tree
            if None, assign at all snapshots with particle species data
        assign_species_pointers : bool
            whether to assign species particle pointer indices to reference snapshot (usually z = 0)
        host_number : int
            number of hosts to assign and compute coordinates relative to.
            if 0 or None, skip host assignment

        Returns
        -------
        halts : list of dictionary classes
            catalogs of halo merger trees across simulations
        '''
        # parse list of directories
        if np.ndim(simulation_directories) == 0:
            raise ValueError(
                f'input simulation_directories = {simulation_directories} but need to input list'
            )
        elif np.ndim(simulation_directories) == 1:
            # assign null names
            simulation_directories = list(
                zip(simulation_directories, ['' for _ in simulation_directories])
            )
        elif np.ndim(simulation_directories) == 2:
            pass
        elif np.ndim(simulation_directories) >= 3:
            raise ValueError(
                f'not sure how to parse simulation_directories = {simulation_directories}'
            )

        rockstar_directory = ut.io.get_path(rockstar_directory)

        halts = []
        directories_read = []
        for simulation_directory, simulation_name in simulation_directories:
            try:
                halt = self.read_tree(
                    simulation_directory,
                    rockstar_directory,
                    catalog_hdf5_directory,
                    file_kind,
                    species,
                    species_snapshot_indices,
                    assign_species_pointers,
                    host_number,
                    simulation_name,
                )

                halts.append(halt)
                directories_read.append(simulation_directory)

            except Exception:
                self.say(f'! cannot read halo merger trees in {simulation_directory}')

        if len(halts) == 0:
            self.say('! cannot read any halo merger trees')
            return

        return halts

    def _read_tree_text(self, rockstar_directory=halo_default.rockstar_directory):
        '''
        Read catalog of halo merger trees (text file) from ConsistentTrees (tree_*.dat).
        Return as dictionary class.

        Parameters
        ----------
        rockstar_directory : str
            directory (full path) of rockstar halo files

        Returns
        -------
        halt : dictionary class
            catalog of halo merger trees across all snapshots
        '''
        it = self.int_type
        ft = self.float_type

        def _tree_header_to_dtype(fname):
            with open(fname, 'r', encoding='utf-8') as f:
                headline = f.readline().lstrip('#').strip()
            colnames = [col.split('(')[0] for col in headline.split()]

            dtypes = [
                ('scalefactor', ft),  # [convert to snapshot index] of halo
                (self.tree_id_name, it),  # tree ID (unique across all snapshots)
                ('descendant.scalefactor', ft),  # [convert to snapshot index] of descendant
                ('descendant.' + self.tree_id_name, it),  # [convert to tree index] of descendant
                ('progenitor.number', it),  # number of progenitors
                # [convert to tree index] of local (least mass) central (can be a satellite)
                ('central.local.' + self.tree_id_name, it),
                # [convert to tree index] of most massive central
                ('central.' + self.tree_id_name, it),
                ('descendant.central.local.' + self.tree_id_name, it),  # [ignore]
                ('am.phantom', it),  # whether halo is interpolated across snapshots
                ('sam.mass.vir', ft),  # [ignore]
                ('mass.bound', ft),  # bound mass
                ('radius', ft),  # halo radius
                ('scale.radius', ft),  # NFW scale radius
                ('vel.std', ft),  # velocity dispersion
                ('am.progenitor.main', it),  # whether am most massive progenitor of my descendant
                ('major.merger.scalefactor', ft),  # [convert to snapshot index] of last maj merger
                ('vel.circ.max', ft),  # maximum of circular velocity
                ('position.x', ft),
                ('position.y', ft),
                ('position.z', ft),  # center position
                ('velocity.x', ft),
                ('velocity.y', ft),
                ('velocity.z', ft),  # center velocity
                ('momentum.ang.x', ft),
                ('momentum.ang.y', ft),
                ('momentum.ang.z', ft),  # [ignore]
                ('spin.peebles', ft),  # dimensionless spin parameter
                ('breadth.index', it),  # (same as tree index) [ignore]
                ('dindex', it),  # depth-first order (index) within tree
                ('final.' + self.tree_id_name, it),  # [convert to tree index] at final snapshot
                (self.catalog_id_name, it),  # catalog ID from rockstar
                ('snapshot.index', it),  # [ignore]
                # depth-first index of next co-progenitor
                ('progenitor.co.dindex', it),
                # depth-first index of last progenitor (earliest time), including *all* progenitors
                ('progenitor.last.dindex', it),
                # depth-first index of last progenitor (earliest time), only along main prog branch
                ('progenitor.main.last.dindex', it),
                ('tidal.force', ft),  # [ignore]
                ('tidal.' + self.tree_id_name, it),  # [ignore]
            ]
            assert len(colnames) >= len(dtypes)

            if colnames[len(dtypes)] == 'Rs_Klypin' and colnames[-1] == 'M200b_lowres':
                # default (rockstar) values
                return dtypes + [
                    ('scale.radius.klypin', ft),  # NFW scale radius from radius(vel.circ.max)
                    ('mass', ft),  # total mass within halo radius (including unbound)
                    ('mass.vir', ft),
                    ('mass.200c', ft),
                    ('mass.500c', ft),
                    ('mass.180m', ft),
                    # offset of density peak from particle average position
                    ('position.offset', ft),
                    ('velocity.offset', ft),
                    ('spin.bullock', ft),  # dimensionless spin, Bullock et al (J/(sqrt(2)*GMVR))
                    # ratio of 2nd & 3rd to 1st largest shape ellipsoid axes (Allgood et al 2006)
                    ('axis.b/a', ft),
                    ('axis.c/a', ft),
                    ('axis.x', ft),
                    ('axis.y', ft),
                    ('axis.z', ft),  # [ignore]
                    ('axis.b/a.500c', ft),
                    ('axis.c/a.500c', ft),  # [ignore]
                    ('axis.x.500c', ft),
                    ('axis.y.500c', ft),
                    ('axis.z.500c', ft),  # [ignore]
                    ('kinetic/potential', ft),  # ratio of kinetic to potential energy [ignore]
                    ('mass.pe.behroozi', ft),  # [ignore]
                    ('mass.pe.diemer', ft),  # [ignore]
                    ('type', it),  # [ignore]
                    ('star.mass.rockstar', ft),  # [ignore for now]
                    ('gas.mass.rockstar', ft),  # [ignore for now]
                    ('blackhole.mass.rockstar', ft),  # [ignore for now]
                    ('mass.hires', ft),  # mass in high-res DM particles [ignore]
                    ('mass.lowres', ft),  # mass in low-res DM particles (not always correct!)
                ]

            else:
                renamer = {
                    'rmax': 'vel.circ.max.radius',
                    'r2': 'scale.radius.ahf',
                    'sigv': 'vel.std.ahf',
                    'cnfw': 'concentration.nfw',
                }
            # also need to turn mass.bound into mass:
            index = dtypes.index(('mass.bound', ft))
            dtypes[index] = ('mass', ft)

            for ii in range(len(dtypes), len(colnames)):
                # all extra columns should be floats; no reason to track extra integers
                col = colnames[ii].lower()
                if col in renamer:
                    dtypes.append((renamer[col], ft))
                else:
                    dtypes.append((col, ft))
            return dtypes

        file_name = 'tree_0_0_0.dat'
        path_file_name = (
            ut.io.get_path(rockstar_directory) + self.catalog_tree_directory + file_name
        )

        # store as dictionary class ----------
        halt = HaloDictionaryClass()
        header = {}

        # read header to get cosmology ----------
        with open(path_file_name, 'r', encoding='utf-8') as file_in:
            for line in file_in:
                if 'h0 = ' in line:
                    index = line.rfind('h0 = ')
                    header['hubble'] = float(line[index + 5 : index + 13])
                if 'Omega_M = ' in line:
                    index = line.rfind('Omega_M = ')
                    header['omega_matter'] = float(line[index + 10 : index + 18])
                if 'Omega_L = ' in line:
                    index = line.rfind('Omega_L = ')
                    header['omega_lambda'] = float(line[index + 10 : index + 18])
                if 'box size = ' in line:
                    index = line.rfind('box size = ')
                    header['box.length/h'] = float(line[index + 11 : index + 20])
                    # convert to [kpc/h comoving]
                    header['box.length/h'] *= ut.constant.kilo_per_mega

            header['dark.particle.mass'] = np.nan

        # initialize rest of cosmological parameters for later
        header['omega_baryon'] = None
        header['sigma_8'] = None
        header['n_s'] = None

        dtype_list = _tree_header_to_dtype(path_file_name)

        halt_read = np.loadtxt(
            path_file_name,
            encoding='utf-8',
            comments='#',
            skiprows=49,  # because ConsistentTrees writes total number of halos here
            dtype=dtype_list,
            # archive
            # dtype=[
            #     ('scalefactor', ft),  # [convert to snapshot index] of halo
            #     (self.tree_id_name, it),  # tree ID (unique across all snapshots)
            #     ('descendant.scalefactor', ft),  # [convert to snapshot index] of descendant
            #     ('descendant.' + self.tree_id_name, it),  # [convert to tree index] of descendant
            #     ('progenitor.number', it),  # number of progenitors
            #     # [convert to tree index] of local (least mass) central (can be a satellite)
            #     ('central.local.' + self.tree_id_name, it),
            #     # [convert to tree index] of most massive central
            #     ('central.' + self.tree_id_name, it),
            #     ('descendant.central.local.' + self.tree_id_name, it),  # [ignore]
            #     ('am.phantom', it),  # whether halo is interpolated across snapshots
            #     ('sam.mass.vir', ft),  # [ignore]
            #     ('mass.bound', ft),  # bound mass
            #     ('radius', ft),  # halo radius
            #     ('scale.radius', ft),  # NFW scale radius
            #     ('vel.std', ft),  # velocity dispersion
            #     ('am.progenitor.main', it),  # whether am most massive progenitor of my descendant
            #     ('major.merger.scalefactor', ft),  # [convert to snapshot index] of last maj merge
            #     ('vel.circ.max', ft),  # maximum of circular velocity
            #     ('position.x', ft), ('position.y', ft), ('position.z', ft),  # center position
            #     ('velocity.x', ft), ('velocity.y', ft), ('velocity.z', ft),  # center velocity
            #     ('momentum.ang.x', ft), ('momentum.ang.y', ft), ('momentum.ang.z', ft),  # [skip]
            #     ('spin.peebles', ft),  # dimensionless spin parameter
            #     ('breadth.index', it),  # (same as tree index) [ignore]
            #     ('dindex', it),  # depth-first order (index) within tree
            #     ('final.' + self.tree_id_name, it),  # [convert to tree index] at final snapshot
            #     (self.catalog_id_name, it),  # catalog ID from rockstar
            #     ('snapshot.index', it),  # [ignore]
            #     # depth-first index of next co-progenitor
            #     ('progenitor.co.dindex', it),
            #     # depth-first index of last progenitor (earliest time), including all progenitors
            #     ('progenitor.last.dindex', it),
            #     # depth-first index of last progenitor (earliest time), along main prog branch
            #     ('progenitor.main.last.dindex', it),
            #     ('tidal.force', ft),  # [ignore]
            #     ('tidal.' + self.tree_id_name, it),  # [ignore]
            #     # everything below here can be different if not rockstar inputs
            #     ('scale.radius.klypin', ft),  # NFW scale radius from radius(vel.circ.max)
            #     ('mass', ft),  # total mass within halo radius (including unbound)
            #     ('mass.vir', ft), ('mass.200c', ft), ('mass.500c', ft), ('mass.180m', ft),
            #     # offset of density peak from particle average position
            #     ('position.offset', ft), ('velocity.offset', ft),
            #     ('spin.bullock', ft),  # dimensionless spin from Bullock et al (J/(sqrt(2)*GMVR))
            #     # ratio of 2nd & 3rd to 1st largest shape ellipsoid axes (Allgood et al 2006)
            #     ('axis.b/a', ft), ('axis.c/a', ft),
            #     ('axis.x', ft), ('axis.y', ft), ('axis.z', ft),  # [ignore]
            #     ('axis.b/a.500c', ft), ('axis.c/a.500c', ft),  # [ignore]
            #     ('axis.x.500c', ft), ('axis.y.500c', ft), ('axis.z.500c', ft),  # [ignore]
            #     ('kinetic/potential', ft),  # ratio of kinetic to potential energy [ignore]
            #     ('mass.pe.behroozi', ft),  # [ignore]
            #     ('mass.pe.diemer', ft),  # [ignore]
            #     ('type', it),  # [ignore]
            #     ('star.mass.rockstar', ft),  # [ignore for now]
            #     ('gas.mass.rockstar', ft),  # [ignore for now]
            #     ('blackhole.mass.rockstar', ft),  # [ignore for now]
            #     ('mass.hires', ft),  # mass in high-res DM particles (not always correct!)
            #     ('mass.lowres', ft),  # mass in low-res DM particles (not always correct!)
            # ]
        )

        for prop_name in halt_read.dtype.names:
            if prop_name not in self.ignore_properties:
                halt[prop_name] = halt_read[prop_name]

        self.say(
            '* read {} halos from:  {}\n'.format(
                halt[self.prop_name_default].size, path_file_name.lstrip('./')
            )
        )

        del halt_read

        # convert properties
        for prop_name in halt:
            if 'mass' in prop_name and 'scalefactor' not in prop_name:
                halt[prop_name] *= 1 / header['hubble']  # [M_sun]
            elif 'radius' in prop_name:
                halt[prop_name] *= halt['scalefactor'] / header['hubble']  # [kpc physical]
            elif 'position' in prop_name:
                halt[prop_name] *= ut.constant.kilo_per_mega / header['hubble']  # [kpc comoving]
            elif 'momentum.ang' in prop_name:
                halt[prop_name] *= (halt['scalefactor'] / header['hubble']) ** 2  # [kpc physical]
            elif 'energy' in prop_name:
                halt[prop_name] *= halt['scalefactor'] / header['hubble']  # [kpc physical]
            elif 'index' in prop_name and np.min(halt[prop_name]) == -1:
                # ensure null pointer index  is safely out of range
                hindices = np.where(halt[prop_name] == -1)[0]
                halt[prop_name][hindices] -= halt[prop_name].size

        # assign derived masses
        halt['mass.200m'] = halt['mass']  # pointer for clarity/convenience
        if 'star.mass.rockstar' in halt:
            halt['baryon.mass.rockstar'] = halt['gas.mass.rockstar'] + halt['star.mass.rockstar']
            halt['dark.mass'] = halt['mass'] - halt['baryon.mass.rockstar']

        # convert position and velocity to halo number x dimension number array
        for prop_name in [
            'position',
            'velocity',
            'bulk.velocity',
            'momentum.ang',
            'axis',
            'axis.500c',
        ]:
            if prop_name + '.x' in halt:
                halt[prop_name] = np.transpose(
                    [halt[prop_name + '.x'], halt[prop_name + '.y'], halt[prop_name + '.z']]
                )
                del (halt[prop_name + '.x'], halt[prop_name + '.y'], halt[prop_name + '.z'])

        # convert properties of snapshot scale-factor to snapshot index
        for prop_name in list(halt.keys()):
            if 'scalefactor' in prop_name:
                prop_name_new = prop_name.replace('scalefactor', 'snapshot')
                # initialize safely out of bounds
                halt[prop_name_new] = (
                    np.zeros(halt[prop_name].size, np.int32) - self.Snapshot['index'].size - 1
                )
                hindices = ut.array.get_indices(halt[prop_name], [1e-10, 1.0001])
                if hindices.size:
                    halt[prop_name_new][hindices] = self.Snapshot.get_snapshot_indices(
                        'scalefactor', halt[prop_name][hindices]
                    )
                del halt[prop_name]

        # convert halo tree id pointer to pointers
        ut.catalog.assign_id_to_index(halt, self.tree_id_name)
        for prop_name in list(halt.keys()):
            if '.' + self.tree_id_name in prop_name:
                prop_name_new = prop_name.replace(self.tree_id_name, 'index')
                halt[prop_name_new] = ut.array.get_array_null(halt[prop_name].size)
                hindices = ut.array.get_indices(halt[prop_name], [0, Inf])
                halt[prop_name_new][hindices] = halt[self.tree_id_name + '.to.index'][
                    halt[prop_name][hindices]
                ]
                del halt[prop_name]

        # assign progenitor information from descendant information
        # first assign main (most massive) progenitor
        am_prog_indices = np.where(
            (halt['am.progenitor.main'] > 0) * (halt['snapshot'] < halt['snapshot'].max())
        )[0]
        desc_hindices = halt['descendant.index'][am_prog_indices]
        assert np.min(desc_hindices) >= 0
        halt['progenitor.main.index'] = ut.array.get_array_null(
            halt['descendant.index'].size, halt['descendant.index'].dtype
        )
        halt['progenitor.main.index'][desc_hindices] = am_prog_indices
        # assign co-progenitors if multiple progenitors
        halt['progenitor.co.index'] = ut.array.get_array_null(
            halt['progenitor.main.index'].size, halt['progenitor.main.index'].dtype
        )
        has_mult_prog_hindices = np.where(halt['progenitor.number'] > 1)[0]
        for has_mult_prog_hindex in has_mult_prog_hindices:
            prog_indices = np.where(halt['descendant.index'] == has_mult_prog_hindex)[0]
            assert halt['am.progenitor.main'][prog_indices[0]]  # sanity check
            for prog_i, prog_hindex in enumerate(prog_indices[:-1]):
                halt['progenitor.co.index'][prog_hindex] = prog_indices[prog_i + 1]

        return halt, header

    def _io_tree_hdf5(
        self,
        rockstar_directory=halo_default.rockstar_directory,
        catalog_hdf5_directory=halo_default.rockstar_catalog_hdf5_directory,
        halt=None,
    ):
        '''
        Read/write catalog of halo merger trees across snapshots to/from HDF5 file.
        If reading, return as dictionary class.

        Parameters
        ----------
        rockstar_directory : str
            directory (full path) of rockstar halo files
        catalog_hdf5_directory : str
            directory (within rockstar directory) of processed HDF5 halo files
        halt : dictionary class
            catalog of halo merger trees, if writing

        Returns
        -------
        halt : dictionary class
            catalog of halo merger trees across all snapshots
        '''
        file_name = 'tree.hdf5'

        file_path = ut.io.get_path(rockstar_directory) + ut.io.get_path(catalog_hdf5_directory)
        path_file_name = file_path + file_name

        if halt is not None:
            # write to file
            assert halt.info['catalog.kind'] == 'halo.tree'
            file_path = ut.io.get_path(file_path, create_path=True)

            properties_add = []
            for prop_name in halt.info:
                if not isinstance(halt.info[prop_name], str):
                    halt['info:' + prop_name] = np.array(halt.info[prop_name])
                    properties_add.append('info:' + prop_name)

            for prop_name in halt.Cosmology:
                halt['cosmology:' + prop_name] = np.array(halt.Cosmology[prop_name])
                properties_add.append('cosmology:' + prop_name)

            ut.io.file_hdf5(path_file_name, halt)

            for prop_name in properties_add:
                del halt[prop_name]

        else:
            # store as dictionary class
            halt = HaloDictionaryClass()
            header = {}

            try:
                # try to read from file
                halt_read = ut.io.file_hdf5(path_file_name, verbose=False)

                for prop_name, halt_prop in halt_read.items():
                    if 'info:' in prop_name:
                        hal_prop_name = prop_name.split(':')[-1]
                        header[hal_prop_name] = float(halt_prop)
                    elif 'cosmology:' in prop_name:
                        hal_prop_name = prop_name.split(':')[-1]
                        header[hal_prop_name] = float(halt_prop)
                    else:
                        halt[prop_name] = halt_prop

                self.say(
                    '* read {} halos from:  {}'.format(
                        halt[self.prop_name_default].size, path_file_name.lstrip('./')
                    )
                )

            except OSError as exc:
                s = '! cannot find halo merger tree file:  {}'.format(path_file_name.lstrip('./'))
                raise OSError(s) from exc

            return halt, header

    def assign_hosts_to_tree(self, halt, host_kind='halo', host_number=1):
        '''
        Assign one or multiple primary host halo/galaxy and relative coordinates.

        Parameters
        ----------
        hal : dictionary class
            catalog of halos at snapshot
        host_kind : str
            property to determine primary host: 'halo', 'star'
        host_number : int
            number of hosts to assign and compute coordinates relative to
        '''
        if host_number is True:
            host_number = 1
        elif host_number < 1:
            self.say(f'input host_number = {host_number}, skipping host assignment')
            return

        for host_rank in range(host_number):
            host_index_name = ut.catalog.get_host_name(host_rank) + 'index'
            if host_index_name not in halt:
                self._assign_host_to_tree(halt, host_kind, host_rank)

        if host_number > 1:
            # multiple hosts - assign nearest one to each halo

            # initialize all halos relative to the primary host
            for prop_name in list(halt.keys()):
                if 'host.' in prop_name and 'near.' not in prop_name:
                    prop_name_near = prop_name.replace('host.', 'host.near.')
                    halt[prop_name_near] = np.array(halt[prop_name])

            snapshot_indices = np.arange(halt['snapshot'].min(), halt['snapshot'].max() + 1)

            for snapshot_index in snapshot_indices:
                hindices = np.where(halt['snapshot'] == snapshot_index)[0]
                if hindices.size:
                    host_distancess = np.zeros(
                        (hindices.size, host_number), dtype=halt['host.distance'].dtype
                    )

                    for host_rank in range(host_number):
                        host_name = ut.catalog.get_host_name(host_rank)
                        host_distancess[:, host_rank] = halt.prop(
                            host_name + 'distance.total', hindices
                        )

                    host_nearest_indices = np.argmin(host_distancess, 1)

                    # assign halos whose nearest is not the primary
                    for host_rank in range(1, host_number):
                        hindices_h = hindices[np.where(host_nearest_indices == host_rank)[0]]
                        if hindices_h.size:
                            host_name = ut.catalog.get_host_name(host_rank)
                            for prop_name in halt:
                                if host_name in prop_name and 'near.' not in prop_name:
                                    prop_name_near = prop_name.replace(host_name, 'host.near.')
                                    halt[prop_name_near][hindices_h] = halt[prop_name][hindices_h]
        print()

    def _assign_host_to_tree(self, halt, host_kind='halo', host_rank=0):
        '''
        Assign primary (secondary, etc) host halo/galaxy and position + velocity wrt it.
        Determine host as being host_rank order sorted by host_prop_name.
        Require host to have low contamination from low-resolution dark matter at final snapshot.
        Determine host at final snapshot and follow back its main progenitor via tree.

        If host_kind is 'halo', define primary host as most massive halo in catalog,
        and use coordinates in halo catalog.
        If host_kind is 'star', define primary host as highest stellar mass galaxy in catalog,
        and use coordinate defined via stars.

        Parameters
        ----------
        halt : dictionary class
            catalog of halo merger trees across all snapshots
        host_kind : str
            property to determine primary host: 'halo', 'star'
        host_rank : int
            rank of host halo (sorted by host_prop_name) to assign
        '''
        assert host_kind in ['halo', 'star']

        host_name = ut.catalog.get_host_name(host_rank)

        if host_kind == 'halo':
            host_prop_name = 'mass'  # property to use to determine primary host
            spec_prefix = ''
        elif host_kind == 'star':
            host_prop_name = 'star.mass'  # property to use to determine primary host
            spec_prefix = 'star.'
            host_name = spec_prefix + host_name

        self.say(
            '* assigning primary {} and coordinates wrt it to merger trees...'.format(
                host_name.rstrip('.')
            ),
            end='',
        )

        # initialize arrays
        halt[host_name + 'index'] = ut.array.get_array_null(halt[self.prop_name_default].size)
        halt[host_name + 'distance'] = (
            np.zeros(halt[spec_prefix + 'position'].shape, halt[spec_prefix + 'position'].dtype)
            * np.nan
        )
        halt[host_name + 'velocity'] = (
            np.zeros(halt[spec_prefix + 'velocity'].shape, halt[spec_prefix + 'velocity'].dtype)
            * np.nan
        )
        halt[host_name + 'velocity.tan'] = (
            np.zeros(halt[host_prop_name].size, halt[spec_prefix + 'velocity'].dtype) * np.nan
        )
        halt[host_name + 'velocity.rad'] = (
            np.zeros(halt[host_prop_name].size, halt[spec_prefix + 'velocity'].dtype) * np.nan
        )

        # get host at final snapshot
        snapshot_index = halt['snapshot'].max()
        hindices = ut.array.get_indices(halt['snapshot'], snapshot_index)
        if 'mass.lowres' in halt:
            hindices = ut.array.get_indices(
                halt.prop('lowres.mass.frac'), [0, self.lowres_mass_frac_max], hindices
            )
        else:
            self.say('! halo tree does not have dark-matter \'mass.lowres\'')
            self.say('  cannot use it to select pure halos from which to select the host')

        # get host_rank'th halo
        host_index = hindices[np.argsort(halt[host_prop_name][hindices])][-host_rank - 1]

        # follow back main progenitor
        while host_index >= 0:
            snapshot_index = halt['snapshot'][host_index]

            hindices = ut.array.get_indices(halt['snapshot'], snapshot_index)

            halt[host_name + 'index'][hindices] = host_index

            # assign host coordinates only to halos with well defined mass
            hindices = ut.array.get_indices(halt.prop(host_prop_name), [1e-10, Inf], hindices)

            # distance to primary host
            halt[host_name + 'distance'][hindices] = ut.coordinate.get_distances(
                halt[spec_prefix + 'position'][hindices],
                halt[spec_prefix + 'position'][host_index],
                halt.info['box.length'],
                halt.Snapshot['scalefactor'][snapshot_index],
            )

            # velocity wrt primary host
            halt[host_name + 'velocity'][hindices] = ut.coordinate.get_velocity_differences(
                halt[spec_prefix + 'velocity'][hindices],
                halt[spec_prefix + 'velocity'][host_index],
                halt[spec_prefix + 'position'][hindices],
                halt[spec_prefix + 'position'][host_index],
                halt.info['box.length'],
                halt.Snapshot['scalefactor'][snapshot_index],
                ut.constant.Gyr_per_sec
                / halt.Cosmology.get_hubble_parameter(halt.Snapshot['redshift'][snapshot_index]),
            )

            # orbital velocities wrt primary host - only those with well defined host distance
            hindices = ut.array.get_indices(
                halt.prop(host_name + 'distance.total'), [1e-10, Inf], hindices
            )

            distances_norm = np.transpose(
                halt[host_name + 'distance'][hindices].transpose()
                / halt.prop(host_name + 'distance.total', hindices)
            )  # need to do this way

            halt[host_name + 'velocity.tan'][hindices] = np.sqrt(
                np.sum(np.cross(halt[host_name + 'velocity'][hindices], distances_norm) ** 2, 1)
            )
            halt[host_name + 'velocity.tan'][host_index] = 0

            halt[host_name + 'velocity.rad'][hindices] = np.sum(
                halt[host_name + 'velocity'][hindices] * distances_norm, 1
            )
            halt[host_name + 'velocity.rad'][host_index] = 0

            # get host's main progenitor
            host_index = halt['progenitor.main.index'][host_index]
            if (
                host_index >= 0
                and halt['snapshot'][host_index] > 0
                and halt['snapshot'][host_index] != snapshot_index - 1
            ):
                self.say(
                    '! {} main progenitor skips snapshot {}'.format(
                        host_name.replace('.', ''), snapshot_index - 1
                    )
                )

        self.say('finished')

    def _convert_tree(self, halt):
        '''
        Experimental.
        '''
        snapshot_index_max = halt['snapshot'].max()
        snapshot_index_min = halt['snapshot'].min()

        halo_number_max = 0
        halo_number_max_snapshot = None
        snapshot_indices = np.arange(snapshot_index_min, snapshot_index_max + 1)
        for snapshot_index in snapshot_indices:
            hindices = np.where(halt['snapshot'] == snapshot_index)[0]
            if hindices.size > halo_number_max:
                halo_number_max = hindices.size
                halo_number_max_snapshot = snapshot_index

        # start at final snapshot, work back to assign main progenitor indices
        hindices_final = np.where(halt['snapshot'] == halt['snapshot'].max())[0]

        self.say(f'number of halos = {hindices_final.size} at snapshot {snapshot_index_max}')
        self.say(f'max number of halos = {halo_number_max} at snapshot{halo_number_max_snapshot}')

        # make halo merger tree pointers
        catalog_shape = (halo_number_max, snapshot_index_max + 1)
        dtype = ut.array.parse_int_dtype(halt['snapshot'].size)
        hindicess = np.zeros(catalog_shape, dtype=dtype) - halt['snapshot'].size - 1

        # halos sorted by tree depth
        halt_indices_depth = np.argsort(halt['dindex'])

        for hii, hindex in enumerate(hindices_final):
            hindices_final = halt_indices_depth[
                hindex : halt['progenitor.main.last.dindex'][hindex] + 1
            ]
            halt_snapshot_indices = halt['snapshot'][hindices_final]
            hindicess[hii][halt_snapshot_indices] = hindices_final

        for prop_name in halt:
            props = halt[prop_name]
            if np.ndim(props) == 1:
                halt[prop_name] = np.zeros(catalog_shape, props.dtype) - 1
                if props.dtype in [np.int32, np.int64]:
                    halt[prop_name] -= halt['snapshot'].size

                masks = hindicess >= 0
                halt[prop_name][masks] = props[hindicess[masks]]

    def get_catalog_from_tree(self, halt, snapshot_index):
        '''
        Parameters
        ----------
        halt : dict class
            catalog of halo merger trees across all snapshots
        snapshot_index : int
            index of snapshot at which to get halo catalog

        Returns
        -------
        hal : dictionary class
            catalog of halos at snapshot_index
        '''
        hal = HaloDictionaryClass()

        hindices_at_snapshot = np.where(halt['snapshot'] == snapshot_index)[0]
        for prop_name in halt:
            if prop_name != 'snapshot':
                if isinstance(halt[prop_name], list):
                    hal[prop_name] = [[] for _ in hindices_at_snapshot]
                    for hii, hi in enumerate(hindices_at_snapshot):
                        hal[prop_name][hii] = halt[prop_name][hi]
                else:
                    hal[prop_name] = halt[prop_name][hindices_at_snapshot]

        hal.info = halt.info
        hal.Cosmology = halt.Cosmology
        hal.Snapshot = halt.Snapshot
        hal.snapshot = {
            'index': snapshot_index,
            'scalefactor': halt.Snapshot['scalefactor'][snapshot_index],
            'redshift': halt.Snapshot['redshift'][snapshot_index],
            'time': halt.Snapshot['time'][snapshot_index],
            'time.hubble': ut.constant.Gyr_per_sec
            / hal.Cosmology.get_hubble_parameter(halt.Snapshot['redshift'][snapshot_index]),
        }

        return hal

    # both halo catalog at snapshot and merger trees across snapshots ----------
    def _convert_id_to_index_catalogs_tree(self, hals, halt):
        '''
        Convert ids to indices for pointers between halo catalogs and halo merger tree.

        Parameters
        ----------
        hals : list of dictionary classes
            catalog of halos at each snapshot
        halt : dictionary class
            catalog of halo merger trees across all snapshots
        '''
        # parse input catalogs
        assert len(hals) > 0
        for hal in hals:  # do this way in case list of halo catalogs has empty snapshots
            if len(hal) > 0:
                assert hal.info['catalog.kind'] == 'halo.catalog'
                break
        assert halt.info['catalog.kind'] == 'halo.tree'

        # set pointer names
        catalog_pointer_name = self.catalog_id_name + '.to.index'
        tree_pointer_name = self.tree_id_name + '.to.index'

        self.say('\n* converting pointer id to index between halo catalogs and merger tree')

        halt['catalog.index'] = ut.array.get_array_null(halt[self.tree_id_name].size)
        if tree_pointer_name not in halt or len(halt[tree_pointer_name]) == 0:
            ut.catalog.assign_id_to_index(halt, self.tree_id_name)

        for hal in hals:
            if len(hal) > 0 and len(hal[self.catalog_id_name]) > 0:
                # get real (non-phantom) halos at this snapshot in trees
                halt_indices = np.where(
                    (halt['am.phantom'] == 0) * (halt['snapshot'] == hal.snapshot['index'])
                )[0]

                if halt_indices.size:
                    if catalog_pointer_name not in hal or len(hal[catalog_pointer_name]) == 0:
                        ut.catalog.assign_id_to_index(hal, self.catalog_id_name)

                    # assign halo catalog index to tree - all halos in trees should be in catalog
                    hal_ids = halt[self.catalog_id_name][halt_indices]
                    assert hal_ids.min() >= 0
                    hal_indices = hal[catalog_pointer_name][hal_ids]
                    assert hal_indices.min() >= 0
                    halt['catalog.index'][halt_indices] = hal_indices

                    # assign halo tree indices to halo catalog - note: not all halos are in trees
                    for prop_name in list(hal.keys()):
                        if self.tree_id_name in prop_name:
                            prop_name_new = 'tree.' + prop_name.replace(self.tree_id_name, 'index')
                            hal[prop_name_new] = (
                                np.zeros(
                                    hal[self.catalog_id_name].size, halt[self.tree_id_name].dtype
                                )
                                - halt[self.tree_id_name].size
                                - 1
                            )
                            hal_indices = np.where(hal[prop_name] >= 0)[0]
                            if hal_indices.size:
                                halt_ids = hal[prop_name][hal_indices]
                                assert halt_ids.min() >= 0
                                halt_indices = halt[tree_pointer_name][halt_ids]
                                assert halt_indices.min() >= 0
                                hal[prop_name_new][hal_indices] = halt_indices
                            del hal[prop_name]

                if catalog_pointer_name in hal:
                    del hal[catalog_pointer_name]

        del halt[self.catalog_id_name]
        del halt[tree_pointer_name]

    def _assign_species_to_tree(
        self,
        halt,
        species='star',
        species_snapshot_indices=None,
        assign_species_pointers=False,
        simulation_directory=halo_default.simulation_directory,
        rockstar_directory=halo_default.rockstar_directory,
        catalog_hdf5_directory=halo_default.rockstar_catalog_hdf5_directory,
        verbose=False,
    ):
        '''
        Read halo catalogs with particle species properties and assign to halo merger trees.

        Parameters
        ----------
        halt : dictionary class
            catalog of halo merger trees across all snapshots
        species : str or list
            name[s] of particle species to read + assign to halos
        species_snapshot_indices : array
            list of snapshot indices at which to assign particle species to tree
            if None, assign at all snapshots with particle species data
        assign_species_pointers : bool
            whether to assign species particle pointer indices to reference snapshot (usually z = 0)
        simulation_directory : str
            directory of simulation
        rockstar_directory : str
            sub-directory (within simulation_directory) of halo files
        catalog_hdf5_directory : str
            directory (within rockstar directory) of processed HDF5 halo files
        verbose : bool
            whether to print diagnostics
        '''
        Particle = ParticleClass(catalog_hdf5_directory)

        # parse input parameters
        assert halt.info['catalog.kind'] == 'halo.tree'
        if species is True:
            species = 'star'
        if np.isscalar(species):
            species = [species]
        simulation_directory = ut.io.get_path(simulation_directory)
        rockstar_directory = ut.io.get_path(rockstar_directory)
        catalog_hdf5_directory = ut.io.get_path(catalog_hdf5_directory)

        # get all halo species file names to read
        path_file_names, file_snapshot_indices = self._get_catalog_file_names_and_values(
            simulation_directory + rockstar_directory,
            catalog_hdf5_directory,
            species_snapshot_indices,
            file_kind=species[0],
        )

        if len(path_file_names) == 0:
            self.say(
                f'! found no halo {species} files in:  {simulation_directory + rockstar_directory}',
                verbose,
            )
            return
        else:
            self.say(f'\n* assigning {species} properties to halo merger trees')

        # check if input subset list of snapshot indices at which to assign particles
        if species_snapshot_indices is not None:
            snapshot_indices = np.intersect1d(species_snapshot_indices, file_snapshot_indices)
        else:
            snapshot_indices = file_snapshot_indices

        # snapshot_indices = snapshot_indices[::-1]  # reverse order to start closest to z = 0

        if not verbose:
            # generate progress bar, if not doing a verbose print
            pbar = self.make_progress_bar(snapshot_indices.size, f'reading {species} particles')
            pbar.start()

        for snapshot_ii, snapshot_index in enumerate(snapshot_indices):
            hal = Particle.io_species_hdf5(
                species,
                None,
                snapshot_index,
                simulation_directory,
                rockstar_directory,
                catalog_hdf5_directory,
                assign_species_pointers,
                verbose=verbose,
            )

            for spec_name in species:
                if spec_name + '.mass' not in hal:
                    # skip this snapshot if no particle species assigned to halos
                    continue
                elif spec_name + '.mass' not in halt:
                    # initialize arrays for halo merger trees
                    for prop_name in hal:
                        if self.catalog_id_name not in prop_name:
                            if verbose:
                                self.say(f'{prop_name}', verbose)

                            if spec_name in prop_name and '.indices' in prop_name:
                                halt[prop_name] = [[] for _ in halt[self.prop_name_default]]
                            else:
                                value_min = np.min(hal[prop_name].min(), -1)
                                shape = list(hal[prop_name].shape)
                                shape[0] = halt[self.prop_name_default].size
                                halt[prop_name] = np.zeros(shape, hal[prop_name].dtype) + value_min

                # get real (non-phantom) halos in tree at this snapshot
                halt_indices = np.where(
                    (halt['am.phantom'] == 0) * (halt['snapshot'] == hal.snapshot['index'])
                )[0]
                if halt_indices.size:
                    # assign halo catalog index to trees - all halos in trees should be in catalog
                    hal_indices = halt['catalog.index'][halt_indices]
                    assert hal_indices.min() >= 0

                    if verbose:
                        # check if any halos with particle species are not in tree
                        hal_indices_no_tree = np.setdiff1d(
                            np.arange(hal[spec_name + '.mass'].size), hal_indices
                        )
                        hal_indices_no_tree_has_species = ut.array.get_indices(
                            hal[spec_name + '.number'], [1, Inf], hal_indices_no_tree
                        )
                        if hal_indices_no_tree_has_species.size:
                            string = (
                                '\n! snapshot {}: {} halos have {} particles but are not in tree'
                            )
                            self.say(
                                string.format(
                                    hal.snapshot['index'],
                                    hal_indices_no_tree_has_species.size,
                                    spec_name,
                                )
                            )
                            self.say(
                                'max M_{} = {:.1e}'.format(
                                    spec_name,
                                    hal[spec_name + '.mass'][hal_indices_no_tree_has_species].max(),
                                )
                            )

                    # transfer particle species properties from catalog to trees
                    for prop_name in hal:
                        if self.catalog_id_name not in prop_name:
                            if spec_name in prop_name and '.indices' in prop_name:
                                for halt_index, hal_index in zip(halt_indices, hal_indices):
                                    if len(hal[prop_name][hal_index]) > 0:
                                        halt[prop_name][halt_index] = hal[prop_name][hal_index]
                            else:
                                halt[prop_name][halt_indices] = hal[prop_name][hal_indices]
            if not verbose:
                pbar.update(snapshot_ii)

        if not verbose:
            pbar.finish()

        if 'star' in species or 'gas' in species:
            halt.info['has.baryons'] = True

    def _transfer_properties_catalogs_tree(self, hals, halt, verbose=False):
        '''
        Transfer properties between hals (list of Rockstar halo catalogs at each snapshot)
        and halt (ConsistentTrees halo merger trees across all snaphsots).

        Parameters
        ----------
        hals : list of dictionary classes
            catalog of halos at each snapshot
        halt : dictionary class
            catalog of halo merger trees across all snapshots
        '''
        # parse input catalogs
        assert halt.info['catalog.kind'] == 'halo.tree'
        assert len(hals) > 0
        for hal in hals:  # do this way in case list of halo catalogs has empty snapshots
            if len(hal) > 0:
                assert hal.info['catalog.kind'] == 'halo.catalog'

                # initialize arrays for halo merger trees
                self.say('* assigning properties to halo merger tree catalog:')
                for prop_name in hal:
                    if (
                        prop_name not in halt
                        and 'id' not in prop_name
                        and prop_name != 'tree.index'
                        and 'host' not in prop_name
                        and 'star.' not in prop_name
                        and 'gas.' not in prop_name
                    ):
                        self.say(f'{prop_name}')
                        value_min = np.min(hal[prop_name].min(), -1)
                        halt[prop_name] = (
                            np.zeros(halt[self.prop_name_default].size, hal[prop_name].dtype)
                            + value_min
                        )
                break

        for hal in hals:
            if len(hal) > 0 and len(hal[self.prop_name_default]) > 0:
                # get real (non-phantom) halos at this snapshot in trees
                halt_indices = np.where(
                    (halt['am.phantom'] == 0) * (halt['snapshot'] == hal.snapshot['index'])
                )[0]
                if halt_indices.size:
                    # assign halo catalog index to trees - all halos in trees should be in catalog
                    hal_indices = halt['catalog.index'][halt_indices]
                    assert hal_indices.min() >= 0

                    if verbose:
                        # sanity check - compare shared properties
                        self.say('* shared properties with offsets: [min, med, max], N_offset')
                        for prop_name in halt:
                            if (
                                prop_name in hal
                                and hal[prop_name][hal_indices].min() > 0
                                and halt[prop_name][halt_indices].min() > 0
                            ):
                                prop_difs = (
                                    halt[prop_name][halt_indices] - hal[prop_name][hal_indices]
                                )
                                if (
                                    np.abs(np.min(prop_difs)) > 1e-4
                                    and np.abs(np.max(prop_difs)) > 1e-4
                                ):
                                    self.say(
                                        '{}: [{}, {}, {}] {}'.format(
                                            prop_name,
                                            np.min(prop_difs),
                                            np.median(prop_difs),
                                            np.max(prop_difs),
                                            np.sum(np.abs(prop_difs) > 0),
                                        )
                                    )

                    # transfer properties from catalog to trees
                    for prop_name in hal:
                        if (
                            prop_name not in halt
                            and 'id' not in prop_name
                            and prop_name != 'tree.index'
                            and 'host' not in prop_name
                            and 'star.' not in prop_name
                            and 'gas.' not in prop_name
                        ):
                            halt[prop_name][halt_indices] = hal[prop_name][hal_indices]

    def _hals_to_halt(
        self,
        simulation_directory=halo_default.simulation_directory,
        rockstar_directory=halo_default.rockstar_directory,
        catalog_hdf5_directory=halo_default.rockstar_catalog_hdf5_directory,
        hals=None,
        return_hals=False,
        mmp_prop='vel.circ.max',
        res_prop='vel.circ.max',
        res_cut=5,
    ):
        '''
        Build a catalog of halo trees out of a list of halo catalogs.

        Parameters
        ----------
        hals : list of dictionary classes
            catalogs of halos at each snapshot

        Returns
        -------
        halt : dictionary class
            halo merger trees
        '''

        def _pair(k1, k2):
            '''
            #, safe=True):

            Cantor pairing function
            http://en.wikipedia.org/wiki/Pairing_function#Cantor_pairing_function
            '''
            z = np.rint(0.5 * (k1 + k2) * (k1 + k2 + 1) + k2).astype('int')
            # if safe and (k1, k2) != depair(z):
            #    raise ValueError("{} and {} cannot be paired".format(k1, k2))
            return z

        from math import floor, ceil

        id_prop = 'id'
        fill_value = -1
        fill_index = -(2**31)

        halt = HaloDictionaryClass()

        if hals is None:
            hals = self.read_catalogs(
                'index',
                None,
                simulation_directory,
                rockstar_directory,
                catalog_hdf5_directory,
                file_kind='hdf5',
                species=None,
                all_snapshot_list=False,
            )
            if 'descendant.id' not in hals[-1]:
                self.say("\n* reading descendant ids from original out.lists...", end='\n\t')
                for ii, hal in enumerate(hals):
                    if len(hal) == 0:
                        continue
                    if len(hal[id_prop]) == 0:
                        hals[ii] = []  # make empty halo catalogs be empty lists
                        continue

                    snapshot = hal.snapshot['index']
                    orig_desc_id = np.loadtxt(
                        simulation_directory
                        + '/'
                        + rockstar_directory
                        + '/'
                        + self.catalog_directory
                        + '/'
                        + 'out_{:03}.list'.format(snapshot),
                        encoding='utf-8',
                        usecols=[1],
                        dtype=int,
                    )

                    hal['descendant.' + id_prop] = orig_desc_id
                    if ii % int(floor(len(hals) / 10)) == 0:
                        self.say("{}..".format(int(ceil(100 * ii / len(hals)))), end='')
                self.say('done')

        for hal in hals:  # do this way in case input list of halo catalogs has empty snapshot
            if len(hal) > 0:
                break

        # ensure that we have the datasets we need to construct the tree
        assert (id_prop in hal) and ('descendant.' + id_prop in hal)

        # copy over some basic data
        halt.info = copy.copy(hal.info)
        halt.Snapshot = copy.copy(hal.Snapshot)
        halt.Cosmology = copy.copy(hal.Cosmology)
        halt._element_index = copy.copy(hal._element_index)

        halt.info['catalog.kind'] = 'halo.tree'

        num_halos = [hal[id_prop].size if len(hal) > 0 else 0 for hal in hals]
        total_halos = np.sum(num_halos)

        self.say(f'\n* creating datasets for {total_halos} halos...')

        # descendant snapshot is the next snapshot that isn't empty
        descendant_snapshot = np.empty(len(hals), dtype=int)
        descendant_snapshot[-1] = -1
        for ii in range(len(hals) - 1):
            index = ii + 1
            while True:
                if index == len(hals):
                    index = -1
                    break
                if len(hals[index]) > 0:
                    break
                index += 1
            descendant_snapshot[ii] = index

        for key in hal.keys():
            prototype = hal[key]
            dtype = prototype.dtype
            if len(prototype.shape) > 1:
                shape = (total_halos, prototype.shape[1])
            else:
                shape = total_halos

            halt[key] = np.empty(shape, dtype=dtype)
            halt[key].fill(fill_value)

        halt['am.phantom'] = np.zeros(total_halos, dtype=int)

        for key in [
            'progenitor.main.index',
            'progenitor.co.index',
            'descendant.index',
            'catalog.index',
            'am.progenitor.main',
            'snapshot',
            'descendant.snapshot',
            'final.index',
            'catalog.' + id_prop,
            'catalog.descendant.' + id_prop,
            'catalog.' + id_prop + '.to.index',
        ]:
            halt[key] = np.empty(total_halos, dtype=int)
            halt[key].fill(fill_index)

        # now start filling in, beginning at the end
        self.say(f'\n* copying over data for {len(hals)} snapshots...')
        left = 0
        for snapshot in range(len(hals))[::-1]:
            right = left + num_halos[snapshot]
            if num_halos[snapshot] == 0:
                continue

            halt['snapshot'][left:right] = snapshot
            halt['descendant.snapshot'][left:right] = descendant_snapshot[snapshot]
            halt['catalog.index'][left:right] = np.arange(num_halos[snapshot], dtype=int)

            # store pointers to the trees in the halo catalogs just in case
            hals[snapshot]['tree.index'] = np.arange(left, right, dtype=int)

            # copy properties over, and encode the ids
            for prop_name in hals[snapshot]:
                if id_prop in prop_name:
                    # want to convert any id arrays to new values
                    if prop_name == id_prop:
                        halt[prop_name][left:right] = _pair(snapshot, hals[snapshot][prop_name])
                    elif prop_name == 'descendant.' + id_prop:
                        # this one is slightly trickier
                        # 1. to match the pairing in that snapshot,
                        #   I (Shea) need to use the next snapshot as the key
                        # 2. don't try to pair the negative ids
                        msk = hals[snapshot][prop_name] >= 0
                        vals = np.empty_like(hals[snapshot][prop_name])
                        vals.fill(-1)
                        vals[msk] = _pair(snapshot + 1, hals[snapshot][prop_name][msk])
                        halt[prop_name][left:right] = vals
                    elif prop_name == 'id.to.index':
                        # nothing special here, just copy it over below
                        pass
                    else:
                        raise KeyError(
                            'unanticipated dataset in halo catalogs:'
                            + f' {prop_name} has {id_prop} in it; do not know how to handle'
                        )

                    # and also save the original value
                    halt['catalog.' + prop_name][left:right] = hals[snapshot][prop_name]
                else:
                    halt[prop_name][left:right] = hals[snapshot][prop_name]

            # move on to the previous snapshot
            left = right

        # now convert the IDs to indices and build the tree
        tree_root_indices = np.arange(0, num_halos[-1], dtype=int)
        self.say(f'\n* building {tree_root_indices.size} trees out the id datasets...')
        # self.say('\t'+r'%done:', end=' ')
        for tree_idx in tree_root_indices:
            if halt.prop(res_prop, tree_idx) < res_cut:
                continue
            self.say(
                '\tstarting tree {} of {} (log M = {:.1f})...'.format(
                    tree_idx, tree_root_indices[-1], halt.prop('log mass', tree_idx)
                ),
                end='',
            )

            # list of indices that I'm currently getting progenitors for;
            # i.e. all halos in the tree at a given snapshot
            # start with just the root index
            current_working_indices = [tree_idx]

            # list of indices that I've already moved past
            finished_indices = []

            # loop until I run out of progenitors
            while len(current_working_indices) > 0:
                # list of all progenitors of all halos in the tree at this timestep
                progenitor_indices = []
                for idx in current_working_indices:
                    # find where the descendant id is my id
                    prog_indices = np.where(
                        halt.prop('descendant.' + id_prop) == halt.prop(id_prop, idx)
                    )[0]

                    # mark the progenitors' descendant index:
                    halt['descendant.index'][prog_indices] = idx

                    # now figure out which of the progenitors is the main branch of this halo
                    # remember, *every* halo with any progenitors has a main progenitor
                    # even if that halo is not a main progenitor itself
                    if prog_indices.size:
                        prog_vals = halt.prop(mmp_prop, prog_indices)
                        sorti = np.argsort(prog_vals)[::-1]
                        sorted_prog_indices = prog_indices[sorti]

                        # the index in the tree corresponding to the prog_value is the
                        # progenitor.main.index of the halo I'm working on
                        halt['progenitor.main.index'][idx] = sorted_prog_indices[0]

                        # then we assign progenitor.co.index down the line -- co.indices are at the
                        # same redshift/snapshot
                        for ii in range(1, sorted_prog_indices.size):
                            # doesn't loop if only one entry
                            halt['progenitor.co.index'][sorted_prog_indices[ii - 1]] = (
                                sorted_prog_indices[ii]
                            )

                        progenitor_indices += list(prog_indices)

                # now shift my working indices to those I'm done with
                finished_indices += current_working_indices

                # and work on the progenitors
                current_working_indices = copy.copy(progenitor_indices)

            # now store the index of the root of the tree for all halos in the tree
            all_tree_indices = np.array(finished_indices, dtype=int)
            halt['final.index'][all_tree_indices] = tree_idx
            self.say(
                "found {:,} total halos in the tree ({:.1f} %done)".format(
                    all_tree_indices.size, tree_idx * 100.0 / tree_root_indices[-1]
                )
            )

        self.say("done!")

        if return_hals:
            return halt, hals
        return halt

    def _ytree_to_halt(self, arbor, simulation_directory=halo_default.simulation_directory):
        '''
        Convert a ytree arbor into a valid halt.

        Parameters
        ----------
        arbor :
            arbor, or path to pass to ytree.load. ideally can be anything
            that ytree can load, though I can't promise it'll for anything
            other than an out.list (or an arbor created from an out.list)

        Returns
        -------
        halt : dictionary class
            halo merger tree
        '''
        target_max_snapshot = 600

        # pylint: disable=import-error
        import ytree  # pyright: ignore reportMissingImports

        if isinstance(arbor, str):
            arbor_path = str(arbor)
            arbor = ytree.load(arbor)
            if not arbor_path.endswith('arbor.h5'):
                self.say("\n* saving then loading arbor to boost performance...")
                fn = arbor.save_arbor()
                arbor = ytree.load(fn)
                self.say(f'if running again, can pass in arbor = {fn}')

        assert isinstance(type(type(arbor)), ytree.arbor.arbor.RegisteredArbor)

        id_prop = 'id'
        renamer = {
            'halo_id': 'catalog.' + id_prop,
            'desc_id': 'catalog.descendant.' + id_prop,
            'scale_radius': 'scale.radius',
            'spin_bullock': 'spin.bullock',
            'Vmax': 'vel.circ.max',
            'velocity_dispersion': 'vel.std',
            'spin_parameter': 'spin.peebles',
            'rs_klypin': 'scale.radius.klypin',
            # 'virial_radius':'radius',
            'R200b': 'radius',
            'M200b_all': 'mass',
            'M200b': 'mass.bound',
            'M200c': 'mass.200c',
            'M500c': 'mass.500c',
            'M180b': 'mass.180m',
            'm200b_hires': 'mass.hires',
            'm200b_lowres': 'mass.lowres',
        }

        converter = {
            'scale_radius': 'kpc',
            'R200b': 'kpc',
            'Vmax': 'km/s',
            'position': 'kpc',
            # 'mass': 'Msun',
            'rs_klypin': 'kpc',
            'M200b_all': 'Msun',
            'M200b': 'Msun',
            'M200c': 'Msun',
            'M500c': 'Msun',
            'M180b': 'Msun',
        }

        fill_value = -1
        fill_index = -(2**31)

        halt = HaloDictionaryClass()

        # copy over some basic data
        halt.info = {
            'box.length/h': arbor.box_size.to('kpc/h').value.item(),
            'box.length': arbor.box_size.to('kpc').value.item(),
            'simulation.name': '',
            'catalog.kind': 'halo.tree',
        }

        halt.Snapshot = ut.simulation.read_snapshot_times(simulation_directory)
        halt.Cosmology = self._get_cosmology(simulation_directory, cosmo=dict())

        # figure out how many halos we have...
        num_trees = arbor.size
        self.say(f'\n* getting all the halos in {num_trees} trees...')

        tsize = np.array([t['tree'].size for t in arbor])
        total_halos = tsize.sum()

        self.say(f'\n* setting up fields for {total_halos} halos')
        # set up fields in the arbor for my use and create empty datasets to hold the results
        for key in [
            'uid',
            'desc_uid',
            'progenitor.main.index',
            'progenitor.main.uid',
            'progenitor.co.uid',
            'progenitor.co.index',
            'progenitor.number',
            'descendant.index',
            'snapshot',
            'descendant.snapshot',
            'final.index',
            'final.uid',
            'am.progenitor.main',
        ]:
            halt[key] = np.empty(total_halos, dtype=int)
            halt[key].fill(fill_index)

        keys_to_copy = []
        for key in ['position', 'velocity', 'redshift'] + list(renamer.keys()):
            if key == 'position':
                halt_key = 'position'
                halt[halt_key] = np.empty((total_halos, 3))
                arbor.add_alias_field('my_' + halt_key, 'position', units='kpc')
            elif key == 'velocity':
                halt_key = 'velocity'
                halt[halt_key] = np.empty((total_halos, 3))
                arbor.add_alias_field('my_' + halt_key, 'velocity', units='km/s')

            elif key in arbor.field_list or key in arbor.derived_field_list:
                if key in renamer:
                    halt_key = renamer[key]
                else:
                    halt_key = key

                halt[halt_key] = np.empty(total_halos)
                if key in converter:
                    arbor.add_alias_field('my_' + halt_key, key, units=converter[key])
                else:
                    arbor.add_alias_field('my_' + halt_key, key)
            else:
                continue

            keys_to_copy.append('my_' + halt_key)

        arbor.add_alias_field('my_desc_uid', 'desc_uid')
        keys_to_copy.append('my_desc_uid')

        arbor.add_alias_field('my_uid', 'uid')
        keys_to_copy.append('my_uid')

        #  def _lrmassfrac(field, data):
        #     return data['m200b_lowres'] / data['M200b_all']

        # arbor.add_derived_field('my_massfraction.lowres', _lrmassfrac, units='')
        # keys_to_copy.append('my_massfraction.lowres')

        trim = len('my_')

        offset = 0

        unsorted_nodes = np.empty(total_halos, dtype=object)

        self.say('\n* getting properties of all the nodes')

        # more accurate ETA comes from the tree index,
        # since handling a large tree takes only marginally longer than a small tree
        progress_bar = self.make_progress_bar(num_trees, 'progress')
        progress_bar.start()

        for arbor_index, tree_size in enumerate(tsize):
            root = arbor[arbor_index]

            left = offset
            right = offset + tree_size

            unsorted_nodes[left:right] = root['tree']
            for key in keys_to_copy:
                halt[key[trim:]][left:right] = root['tree', key]
            halt['final.uid'][left:right] = int(root['uid'])

            offset += tree_size
            progress_bar.update(arbor_index)
        progress_bar.finish()

        self.say('\n* re-ordering and creating index arrays...')

        for key in ['uid', 'desc_uid']:
            # , 'progenitor.main.uid']:
            halt[key] = halt[key].astype(int)

        all_uids = np.array(halt['uid'])
        assert np.unique(all_uids).size == all_uids.size

        # now I can sort and build the object that tells me how to go from uid to index

        # want two objects here:
        # 1 sorts the nodes by uid from small to large -- this is just argsort
        # 2 tells you where each uid is in *in the sorted arrays*
        sorter = np.argsort(all_uids)
        sorted_uids = all_uids[sorter]

        if (all_uids.max() == all_uids.size - 1) and all_uids.min() == 0:
            # if the uids can be indices (i.e. all unique, start and 1 and end at len(all_uids)),
            # then just need to re-order
            uid_to_sorted_index = np.arange(all_uids.size, dtype=int)
        else:
            # otherwise, need to create the linker
            # do it via an array -- may waste some ram,
            # but quicker to index en-mass than look up one by one
            indices = np.arange(all_uids.size, dtype=int)
            uid_to_sorted_index = np.empty(all_uids.max() + 1, dtype=int)
            uid_to_sorted_index.fill(fill_index)
            uid_to_sorted_index[sorted_uids] = indices

        # now resort everything...
        sorted_nodes = unsorted_nodes[sorter]
        for key in halt:
            halt[key] = halt[key][sorter]
        halt['index'] = np.arange(total_halos, dtype=int)

        assert (halt['uid'] == sorted_uids).all()

        # now everything is sorted, so can turn the uids into indices and build progenitor arrays

        # slow (but hopefully safe) way to do the progenitors/descendant/etc all at once
        progress_bar = self.make_progress_bar(sorted_nodes.size, 'indexing progenitors')
        progress_bar.start()
        for halt_index, node in enumerate(sorted_nodes):
            assert node['uid'] == halt['uid'][halt_index]
            ancestors = node.ancestors
            if ancestors is None:
                halt['progenitor.main.index'][halt_index] = fill_index
                halt['progenitor.number'][halt_index] = 0
            else:
                anc_vals = np.array([n['Vmax'] for n in ancestors])
                # go from large to small Vmax -- largest is the main progenitor
                this_sort = np.argsort(anc_vals)[::-1]
                ancestors = np.array(ancestors)[this_sort]
                for ii, ancestor in enumerate(ancestors):
                    if ii == 0:
                        mp_index = uid_to_sorted_index[int(ancestor['uid'])]
                        halt['progenitor.main.index'][halt_index] = mp_index
                        halt['am.progenitor.main'][mp_index] = 1
                    else:
                        last_coprog_index = uid_to_sorted_index[int(ancestors[ii - 1]['uid'])]
                        halt['progenitor.co.index'][last_coprog_index] = uid_to_sorted_index[
                            int(ancestor['uid'])
                        ]
                halt['progenitor.number'][halt_index] = len(ancestors)

            # above if statements will mark am.progenitor.main of a given halo while dealing with
            # its descendant
            # so we need to deal with cases with no descendant by hand here
            # easy though -- no descendant => must be a main branch halo cause it's a root
            if node['desc_uid'] <= 0:
                halt['am.progenitor.main'][halt_index] = 1

            progress_bar.update(halt_index)
        progress_bar.finish()

        # ok so that takes care of the progenitors; descendant is easier and can be done below

        # not quite every halo has a descendant so have to be careful here
        halt['descendant.index'] = np.empty(total_halos, dtype=int)
        halt['descendant.index'].fill(fill_index)
        have_descs = halt['desc_uid'] >= 0
        halt['descendant.index'][have_descs] = uid_to_sorted_index[halt['desc_uid'][have_descs]]

        # every halo has a final.index
        halt['final.index'] = uid_to_sorted_index[halt['final.uid']]

        # nothing is a phantom cause this came from a rockstar tree
        halt['am.phantom'] = np.zeros(total_halos, dtype=int)

        # now have to fill in the snapshot and descendant snapshot...
        unique_redshifts = np.unique(halt['redshift'])
        snapshots = np.arange(unique_redshifts.size, dtype=int)
        if snapshots.max() < target_max_snapshot:
            snapshots = snapshots + (target_max_snapshot - snapshots.max())

        # largest redshift corresponds to smallest snapshot
        sorti = np.argsort(unique_redshifts)
        redshift_to_snapshots = dict(zip(unique_redshifts[sorti[::-1]], snapshots))
        halt['snapshot'] = np.vectorize(redshift_to_snapshots.__getitem__)(halt['redshift'])

        # now the descendant.snapshot should be easier, since I can use the descendant.index to
        # fill based on snapshot
        halt['descendant.snapshot'] = np.empty(total_halos, dtype=int)
        halt['descendant.snapshot'].fill(fill_value)

        valid_desc_indices = halt['descendant.index'][have_descs]
        halt['descendant.snapshot'][have_descs] = halt['snapshot'][valid_desc_indices]

        self.say("done!")

        return halt

    def _ytree_to_halt_via_yt(
        self, filename_or_arbor, simulation_directory=halo_default.simulation_directory
    ):
        '''
        convert anything that ytree can read (or a ytree arbor itself)
        into a halt via the ytree interface in yt-4.0

        Parameters
        ----------
        filename_or_arbor :
            arbor, path to arbor, or path to pass to ytree.load.  ideally
            can be anything  that ytree can load, though I can't promise
            it'll work for anything other than an out.list (or an arbor
            created from an out.list)

        Returns
        -------
        halt : dictionary class
            halo merger tree
        '''
        target_max_snapshot = 600

        # pylint: disable=import-error
        import yt  # pyright: ignore reportMissingImports

        # if we did not pass in a string, it better be an arbor
        # which we save then set up to load with yt:
        if not isinstance(filename_or_arbor, str):
            filename_or_arbor = filename_or_arbor.save_arbor()

        # if it is a string, it can either be a saved arbor.h5 file (in which case we're good)
        # or it can be something we load with ytree than save
        elif not filename_or_arbor.endswith('arbor.h5'):
            import ytree  # pylint: disable=import-error  # pyright: ignore reportMissingImports

            arbor = ytree.load(filename_or_arbor)
            filename_or_arbor = arbor.save_arbor()
            del arbor

        ds = yt.load(filename_or_arbor)
        all_data = ds.all_data()

        id_prop = 'id'
        renamer = {
            'halo_id': 'catalog.' + id_prop,
            'desc_id': 'catalog.descendant.' + id_prop,
            'scale_radius': 'scale.radius',
            'spin_bullock': 'spin.bullock',
            'Vmax': 'vel.circ.max',
            'velocity_dispersion': 'vel.std',
            'spin_parameter': 'spin.peebles',
            'rs_klypin': 'scale.radius.klypin',
            'R200b': 'radius',
            'M200b_all': 'mass',
            'M200b': 'mass.bound',
            'M200c': 'mass.200c',
            'M500c': 'mass.500c',
            'M180b': 'mass.180m',
            'm200b_hires': 'mass.hires',
            'm200b_lowres': 'mass.lowres',
        }

        converter = {
            'scale_radius': 'kpc',
            'R200b': 'kpc',
            'Vmax': 'km/s',
            'position': 'kpc',
            'rs_klypin': 'kpc',
            'M200b_all': 'Msun',
            'M200b': 'Msun',
            'M200c': 'Msun',
            'M500c': 'Msun',
            'M180b': 'Msun',
        }

        fill_value = -1
        fill_index = -(2**31)

        halt = HaloDictionaryClass()

        # copy over some basic data
        halt.info = {
            'box.length/h': ds.box_size.to('kpc/h').value.item(),
            'box.length': ds.box_size.to('kpc').value.item(),
            'simulation.name': '',
            'catalog.kind': 'halo.tree',
        }

        halt.Snapshot = ut.simulation.read_snapshot_times(simulation_directory)

        cosmo = {
            'hubble': ds.hubble_constant,
            'omega_matter': ds.omega_matter,
            'omega_lambda': ds.omega_lambda,
        }
        halt.Cosmology = self._get_cosmology(simulation_directory, cosmo=cosmo)

        # grab the uids of all the halos to
        # 1. figure out how many I have
        # 2. sort them
        # 3. build the uid -> index machinery I'll need later

        all_uids = all_data['uid'].astype(int).value
        assert np.unique(all_uids).size == all_uids.size
        total_halos = all_uids.size

        # now I can sort and build the object that tells me how to go from uid to index

        # want two objects here:
        # 1 sorts the nodes by uid from small to large -- this is just argsort
        # 2 tells you where each uid is in *in the sorted arrays*
        sorter = np.argsort(all_uids)
        sorted_uids = all_uids[sorter]

        if (all_uids.max() == all_uids.size - 1) and all_uids.min() == 0:
            # if the uids can be indices (i.e. all unique, start and 1 and end at len(all_uids)),
            # then just need to re-order
            uid_to_sorted_index = np.arange(all_uids.size, dtype=int)
        else:
            # otherwise, need to create the linker
            # do it via an array -- may waste some ram,
            # but quicker to index en-mass than look up one by one
            indices = np.arange(all_uids.size, dtype=int)
            uid_to_sorted_index = np.empty(all_uids.max() + 1, dtype=int)
            uid_to_sorted_index.fill(fill_index)
            uid_to_sorted_index[sorted_uids] = indices

        # now I can pull the data and directly sort it
        halt['index'] = np.arange(total_halos, dtype=int)
        halt['uid'] = sorted_uids

        self.say(f'\n* copying/re-arranging data for {total_halos} halos')
        # # set up fields in the arbor for my use and create empty datasets to hold the results
        # for key in ['uid', 'desc_uid', 'progenitor.main.index', 'progenitor.main.uid',
        #     'progenitor.co.uid', 'progenitor.co.index', 'progenitor.number', 'descendant.index',
        #     'snapshot', 'descendant.snapshot', 'final.index', 'final.uid', 'am.progenitor.main']:
        #     halt[key] = np.empty(total_halos, dtype=int)
        #     halt[key].fill(fill_index)

        halt['position'] = np.empty((total_halos, 3), dtype=float)
        halt['velocity'] = np.empty((total_halos, 3), dtype=float)
        for ii, axis in enumerate(['x', 'y', 'z']):
            halt['position'][:, ii] = all_data['position_' + axis][sorter].to('kpc').value
            halt['velocity'][:, ii] = all_data['velocity_' + axis][sorter].to('km/s').value

        self.say('- copied position and velocity')

        halt['desc_uid'] = all_data['desc_uid'][sorter].value
        halt['redshift'] = all_data['redshift'][sorter].value

        self.say('copied desc_uid and redshift')

        for key, name in renamer.items():
            if ('all', key) in ds.field_list:
                if key in converter:
                    halt[name] = all_data[key][sorter].to(converter[key]).value
                else:
                    halt[name] = all_data[key][sorter].value
                self.say(f'copied {key} as {name}')

        for key in ['uid', 'desc_uid']:
            halt[key] = halt[key].astype(int)

        # now everything is sorted, so can turn the uids into indices and build progenitor arrays

        # not quite every halo has a descendant so have to be careful here
        halt['descendant.index'] = np.empty(total_halos, dtype=int)
        halt['descendant.index'].fill(fill_index)
        have_descs = halt['desc_uid'] >= 0
        halt['descendant.index'][have_descs] = uid_to_sorted_index[halt['desc_uid'][have_descs]]

        # slow (but hopefully safe) way to do the progenitors/descendant/etc all at once
        halt['progenitor.main.index'] = np.empty(total_halos, dtype=int)
        halt['progenitor.main.index'].fill(fill_index)

        halt['progenitor.co.index'] = np.empty(total_halos, dtype=int)
        halt['progenitor.co.index'].fill(fill_index)

        halt['am.progenitor.main'] = np.zeros(total_halos, dtype=int)
        halt['progenitor.number'] = np.zeros(total_halos, dtype=int)

        progress_bar = self.make_progress_bar(total_halos, 'indexing progenitors')
        progress_bar.start()
        for halt_index, uid in enumerate(halt['uid']):
            ancestors = halt['desc_uid'] == uid
            nprog = np.count_nonzero(ancestors)
            if nprog == 0:
                halt['progenitor.main.index'][halt_index] = fill_index
                halt['progenitor.number'][halt_index] = 0
            else:
                ancestor_indices = halt['index'][ancestors]

                ancestor_values = halt['vel.circ.max'][ancestor_indices]
                this_sort = np.argsort(ancestor_values)[::-1]

                ancestor_indices = ancestor_indices[this_sort]
                for ii in range(ancestor_indices.size):
                    if ii == 0:
                        mp_index = ancestor_indices[ii]
                        halt['progenitor.main.index'][halt_index] = mp_index
                        halt['am.progenitor.main'][mp_index] = 1
                    else:
                        last_coprog_index = ancestor_indices[ii - 1]
                        halt['progenitor.co.index'][last_coprog_index] = ancestor_indices[ii]
                halt['progenitor.number'][halt_index] = ii + 1
            # ok so that takes care of the progenitors; descendant is easier and can be done below

            # above if statements will mark am.progenitor.main of a given halo while dealing with
            # its descendant
            # so we need to deal with cases with no descendant by hand here
            # easy though -- no descendant => must be a main branch halo cause it's a root
            if halt['desc_uid'][halt_index] < 0:
                halt['am.progenitor.main'][halt_index] = 1

            progress_bar.update(halt_index)
        progress_bar.finish()

        # every halo has a final.index, but this is actually harder now
        # fastest way is probably a flat loop that avoids redoing those I've already dealt with
        halt['final.index'] = np.empty(total_halos, dtype=int)
        halt['final.index'].fill(fill_index)

        redshift_sorter = np.argsort(halt['redshift'])[::-1]

        self.say('- assigning root indices...', end='')
        for halt_index in redshift_sorter:
            if halt['final.index'] >= 0:
                continue

            descendant_indices = halt.prop('descendant.indices')
            halt['final.index'][descendant_indices] = descendant_indices[-1]
        self.say('done')

        # nothing is a phantom cause this came from a rockstar tree
        halt['am.phantom'] = np.zeros(total_halos, dtype=int)

        # now have to fill in the snapshot and descendant snapshot...
        unique_redshifts = np.unique(halt['redshift'])
        snapshots = np.arange(unique_redshifts.size, dtype=int)
        if snapshots.max() < target_max_snapshot:
            snapshots = snapshots + (target_max_snapshot - snapshots.max())

        # largest redshift corresponds to smallest snapshot
        sorti = np.argsort(unique_redshifts)
        redshift_to_snapshots = dict(zip(unique_redshifts[sorti[::-1]], snapshots))
        halt['snapshot'] = np.vectorize(redshift_to_snapshots.__getitem__)(halt['redshift'])

        # now the descendant.snapshot should be easier, since I can use the descendant.index
        # to fill based on snapshot
        halt['descendant.snapshot'] = np.empty(total_halos, dtype=int)
        halt['descendant.snapshot'].fill(fill_value)

        valid_desc_indices = halt['descendant.index'][have_descs]
        halt['descendant.snapshot'][have_descs] = halt['snapshot'][valid_desc_indices]

        self.say("done!")

        return halt

    def _connect_progenitors(
        self,
        halt,
        max_snapshot_skip=10,
        distance_tolerance=50,
        match_property='vel.circ.max',
        match_tolerance=0.33,
        nearest_or_best='best',
    ):
        '''
        connect together halos w/o progenitors with halos w/o at descendant
        at earlier times

        Parameters
        ----------
        halt : dictionary class
            halo merger tree
        max_snapshot_skip : int
            max snapshots to search backwards
        distance_tolerance : float
            maximium distance to search
        match_property : str
            property to match on
        match_tolerance : float
            how much match_tolerance is allowed to vary by

        Returns
        -------
        halt :  dictionary class
            halo merger tree with fixed links
        '''
        assert nearest_or_best in ['nearest', 'best']

        all_indices = np.arange(halt.prop('uid').size, dtype=int)

        # indices of halos that don't have a progenitor (could be real, could be problematic)
        no_progenitor_indices = all_indices[halt.prop('progenitor.main.index') < 0]

        # indices of halos that don't have a descendant before the final snapshot
        # these are the systems that could be the progenitors of no_progenitor_indices
        early_truncated_indices = all_indices[
            (halt.prop('descendant.index') < 0)
            & (halt.prop('snapshot') < halt.prop('snapshot').max())
        ]

        early_truncated_snapshots = halt.prop('snapshot', early_truncated_indices)
        early_truncated_vals = halt.prop(match_property, early_truncated_indices)
        early_truncated_positions = halt.prop('position', early_truncated_indices)

        available = np.ones(early_truncated_indices.size, dtype=bool)
        forged_connections = 0

        self.say('\n* searching for progenitors:')
        self.say('- {:,} halos lack a progenitor'.format(no_progenitor_indices.size))
        self.say(
            '- {:,} halos at snapshot < {} lack a descendant'.format(
                early_truncated_indices.size, halt['snapshot'].max()
            )
        )

        progress_bar = self.make_progress_bar(no_progenitor_indices.size, 'progress')
        progress_bar.start()

        for ii, index in enumerate(no_progenitor_indices):
            my_snapshot = halt.prop('snapshot', index)

            # look for halos no longer than max_snapshot_skip ago, but don't go below 0
            snapshot_min = max([my_snapshot - max_snapshot_skip, 0])

            # have to go back at least 2
            # trust that if it were in the previous snapshot the
            # halo finder would have assigned it correctly
            snapshot_max = my_snapshot - 2

            my_position = halt.prop('position', index)

            my_val = halt.prop(match_property, index)
            max_prop = my_val * (1 + match_tolerance)
            min_prop = my_val * (1 - match_tolerance)

            candidate_msk = (
                (early_truncated_snapshots <= snapshot_max)
                & (early_truncated_snapshots >= snapshot_min)
                & (early_truncated_vals <= max_prop)
                & (early_truncated_vals >= min_prop)
                & available
            )

            candidate_vals = early_truncated_vals[candidate_msk]
            candidate_indices = early_truncated_indices[candidate_msk]
            candidate_positions = early_truncated_positions[candidate_msk]
            candidate_distances = ut.coordinate.get_distances(
                my_position, candidate_positions, total_distance=True
            )

            good_candidate_msk = candidate_distances <= distance_tolerance

            good_cand_indices = candidate_indices[good_candidate_msk]
            good_cand_vals = candidate_vals[good_candidate_msk]
            good_cand_dists = candidate_distances[good_candidate_msk]

            progress_bar.update(ii)

            if good_cand_indices.size == 1:  # easy scenario -- just fix this
                prog_index = good_cand_indices[0]
            elif good_cand_indices.size > 1 and nearest_or_best == 'best':
                prog_index = good_cand_indices[np.argmin(np.abs(good_cand_vals - my_val))]
            elif good_cand_indices.size > 1 and nearest_or_best == 'nearest':
                prog_index = good_cand_indices[np.argmin(good_cand_dists)]
            elif good_cand_indices.size == 0:
                continue

            # if I got here that I have a prog_index to match with index
            halt['progenitor.main.index'][index] = prog_index
            halt['progenitor.number'][index] += 1
            halt['descendant.index'][prog_index] = index
            halt['descendant.snapshot'][prog_index] = halt['snapshot'][index]
            halt['final.index'][prog_index] = halt['final.index'][index]

            # remove this halo from contention for later systems
            loc = np.where(early_truncated_indices == prog_index)[0][0]
            available[loc] = False
            forged_connections += 1

        progress_bar.finish()

        print(f'\n* forged {forged_connections} connections')
        return halt

    def rewrite_as_hdf5(
        self,
        simulation_directory=halo_default.simulation_directory,
        rockstar_directory=halo_default.rockstar_directory,
        catalog_hdf5_directory=halo_default.rockstar_catalog_hdf5_directory,
    ):
        '''
        Read Rockstar halo catalogs at all snapshots, and ConsistentTrees history files and merger
        tree files (if they exist).
        Re-write as HDF5 files.

        Parameters
        ----------
        simulation_directory : str
            directory of simulation
        rockstar_directory : str
            sub-directory (within simulation_directory) of halo files
        catalog_hdf5_directory : str
            directory (within rockstar directory) of processed HDF5 halo files
        '''
        simulation_directory = ut.io.get_path(simulation_directory)
        rockstar_directory = ut.io.get_path(rockstar_directory)
        catalog_hdf5_directory = ut.io.get_path(catalog_hdf5_directory)

        # read halo catalogs
        # do not assign primary host[s] now (do it when reading the HDF5 catalog file, because fast)
        hals = self.read_catalogs(
            'index',
            'all',
            simulation_directory,
            rockstar_directory,
            catalog_hdf5_directory,
            file_kind='out',
            host_number=None,
        )
        if isinstance(hals, dict):
            hals = [hals]  # ensure list if catalog only at single snapshot

        try:
            # try to read halo history catalogs
            halhs = self.read_catalogs(
                'index',
                'all',
                simulation_directory,
                rockstar_directory,
                catalog_hdf5_directory,
                file_kind='hlist',
                host_number=None,
            )
            # transfer history properties to halo catalog
            for hal, halh in zip(hals, halhs):
                if len(hal) > 0 and len(halh) > 0:
                    self._transfer_properties_catalog(hal, halh)
            del halhs
        except OSError:
            self.say('! cannot read halo history catalogs (hlist)')

        try:
            # try to read halo merger trees
            # by default, assign primary host halo[s], and save them to HDF5 file,
            # because this computation is expensive across the trees (but trivial for a catalog)
            halt = self.read_tree(
                simulation_directory, rockstar_directory, catalog_hdf5_directory, file_kind='text'
            )
            self._convert_id_to_index_catalogs_tree(hals, halt)
            self._io_tree_hdf5(
                simulation_directory + rockstar_directory, catalog_hdf5_directory, halt
            )
        except OSError:
            self.say('! cannot read halo merger trees')

        for hal in hals:
            if len(hal) > 0:
                # write as HDF5 files
                self._io_catalog_hdf5(
                    simulation_directory + rockstar_directory,
                    catalog_hdf5_directory,
                    hal.snapshot['index'],
                    hal,
                )

    # assign additional properties ----------
    def assign_hosts_rotation(
        self,
        hal,
        simulation_directory=halo_default.simulation_directory,
        track_directory=None,
        verbose=False,
    ):
        '''
        Read and assign rotation tensor of each host galaxy across all snasphots,
        as computed from the star particles (by default).
        Assign default host[s] (via .host) as those at the current snapshot, or for the halo tree,
        those at the final snapshot (usually z = 0).

        Parameters
        ----------
        hal : dictionary class
            catalog of halos at snapshot OR catalog of halo merger trees across all snapshots
        simulation_directory : str
            directory of simulation
        track_directory : str
            directory of files for particle pointers, formation coordinates, and host coordinates
        '''
        from gizmo_analysis import gizmo_track

        # maximum offset (before warning) between host in halo catalog versus read in [kpc comoving]
        host_position_dif_max = 10

        # read file with coordinates and rotation tensor of each host galaxy across all snapshots
        # also assign (via .host) those host[s] at the current snapshot
        # (or at the final snapshot, typically z = 0, if input a halo merger tree)
        ParticleCoordinate = gizmo_track.ParticleCoordinateClass()
        ParticleCoordinate.io_hosts_coordinates(
            hal,
            simulation_directory,
            track_directory,
            verbose=verbose,
        )

        # sanity checks beteen the hosts in the halo catalog/tree and read-in particle coordinates
        # ensure that both use same number of hosts
        host_number = hal.info['host.number']
        assert hal.host['position'].shape[0] == host_number

        # ensure that hosts have same/similar positions
        for host_i in range(host_number):
            host_index = hal.prop(f'host{host_i + 1}.index', 0)
            host_position = hal.prop('position', host_index)
            host_position_dif = np.sqrt(np.sum((host_position - hal.host['position'][host_i]) ** 2))
            if host_position_dif > host_position_dif_max:
                self.say(f'! host{host_i} position is offset by {host_position_dif} kpc comoving')
                self.say('between the halo catalog and the host galaxy read in for the rotation')
                self.say('so these are likely different galaxies/halos!')

    def assign_nearest_neighbor(
        self,
        hal,
        mass_name='mass',
        mass_limits=[1e7, Inf],
        neig_mass_frac_limits=[1.0, Inf],
        neig_distance_max=3800,
        neig_distance_scale='Rneig',
        neig_number_max=5000,
    ):
        '''
        Assign information about nearest neighbor halo
        (nearest := minimum in terms of physical distance or d/R_halo)
        to each halo in mass range in catalog.

        Parameters
        ----------
        hal : list
            catalog of halos at snapshot
        mass_name : str
            mass kind
        mass_limits : list
            min and max limits for mass_name
        neig_mass_frac_limits : float
            min and max mass_name (wrt self) to keep neighbors
        neig_distance_max : int
            maximum search distance [kpc physical]
        neig_distance_scale : str
            distance kind to compute minimum of:
                'physical' or '' = use physical distance
                'Rneig' = scale to distance/R_halo(neig)
                'Rself' = scale to distance/R_halo(self)
        neig_number_max : int
            maximum number of neighbors to search for within maximum distance
        '''
        NearestNeighbor = ut.catalog.NearestNeighborClass()

        NearestNeighbor.assign_to_self(
            hal,
            mass_name,
            mass_limits,
            neig_mass_frac_limits,
            [min(mass_limits), Inf],
            neig_distance_max,
            neig_distance_scale,
            neig_number_max,
        )

        NearestNeighbor.assign_to_catalog(hal)

    def sort_by_property(self, hal, property_name='mass'):
        '''
        Sort halos (in descending order) by property_name.

        Parameters
        ----------
        hal : dictionary class
            catalog of halos at snapshot
        property_name : str
            name of property to sort by
        '''
        hindices = ut.array.get_arange(hal[property_name])

        # put halos with significant contamination from low-resolution DM at end of list
        pure_hindices = hindices[hal.prop('lowres.mass.frac') < self.lowres_mass_frac_max]
        contam_hindices = hindices[hal.prop('lowres.mass.frac') >= self.lowres_mass_frac_max]
        pure_hindices = pure_hindices[np.argsort(hal[property_name][pure_hindices])[::-1]]
        contam_hindices = contam_hindices[np.argsort(hal[property_name][contam_hindices])[::-1]]
        hindices = np.append(pure_hindices, contam_hindices)

        for prop_name in hal:
            hal[prop_name] = hal[prop_name][hindices]

    def assign_orbits(self, hal, host_rank=0):
        '''
        Assign orbital properties wrt each host.

        Parameters
        ----------
        hal : dictionary class
            catalog of halos at snapshot
        host_rank : int
        '''
        self.say(f'* assigning orbital properties wrt {host_rank}')

        host_position_name = 'position'  # code does not assign star particles to primary host
        host_velocity_name = 'velocity'  # so it does not have a star/gas position or velocity

        position_velocity_names = [
            ['position', 'velocity']
            # ['star.position', 'star.velocity'],
        ]

        host_index_name = ut.catalog.get_host_name(host_rank) + 'index'

        # sanity check
        for position_name, velocity_name in tuple(position_velocity_names):
            if position_name not in hal or velocity_name not in hal:
                position_velocity_names.remove([position_name, velocity_name])

        for position_name, velocity_name in position_velocity_names:
            distance_vectors = ut.coordinate.get_distances(
                hal[position_name],
                hal[host_position_name][hal[host_index_name]],
                hal.info['box.length'],
                hal.snapshot['scalefactor'],
            )  # [kpc physical]

            velocity_vectors = ut.coordinate.get_velocity_differences(
                hal[velocity_name],
                hal[host_velocity_name][hal[host_index_name]],
                hal[position_name],
                hal[host_position_name][hal[host_index_name]],
                hal.info['box.length'],
                hal.snapshot['scalefactor'],
                hal.snapshot['time.hubble'],
            )

            orb = ut.orbit.get_orbit_dictionary(distance_vectors, velocity_vectors)

            for prop_name, orb_prop in orb.items():
                hal[host_index_name.replace('index', '') + prop_name] = orb_prop

    # utility for running rockstar
    def write_snapshot_indices(
        self,
        snapshot_selection='all',
        simulation_directory='../../',
        rockstar_directory=halo_default.rockstar_directory,
        out_file_name='snapshot_indices.txt',
    ):
        '''
        Read all snapshot indices of the simulation, read indices that already have a halo catalog,
        print to file a list of snapshot indices that halo finder needs to run on.
        By default, set to run from within the Rockstar sub-directory.

        Parameters
        ----------
        snapshot_selection : str
            options: 'all', 'subset'
        simulation_directory : str
            directory of simulation
        rockstar_directory : str
            directory (within simulation_directory) of rockstar halo files
        out_file_name : str
            name of output file to list snapshot indices to run on
        '''
        snapshot_index_min = 3  # exclude snapshots before this - unlikely to have any halos

        # parse inputs
        simulation_directory = ut.io.get_path(simulation_directory)
        rockstar_directory = ut.io.get_path(rockstar_directory)
        assert snapshot_selection in ['all', 'subset']
        if snapshot_selection == 'all':
            Snapshot = ut.simulation.read_snapshot_times(simulation_directory)
            snapshot_indices = Snapshot['index']
        elif snapshot_selection == 'subset':
            snapshot_indices = snapshot_indices_subset

        try:
            _file_names, file_indices = self._get_catalog_file_names_and_values(
                simulation_directory + rockstar_directory, file_kind='out'
            )

            # keep only indices that do not have existing halo catalog file
            snapshot_indices = np.setdiff1d(snapshot_indices, file_indices)

            # ensure one overlapping snapshot - creates descendant index bug?!
            # snapshot_indices = np.sort(np.append(file_indices.max(), snapshot_indices))
        except OSError:
            self.say('! cannot read any halo catalog files, so writing all snapshot indices')

        # exclude eary snashots
        snapshot_indices = snapshot_indices[snapshot_indices >= snapshot_index_min]

        with open(out_file_name, 'w', encoding='utf-8') as file_out:
            for snapshot_index in snapshot_indices:
                file_out.write('{:03d}\n'.format(snapshot_index))

        self.say(
            'snapshot indices: number = {}, min = {}, max = {}'.format(
                snapshot_indices.size, snapshot_indices.min(), snapshot_indices.max()
            )
        )
        self.say(f'wrote to file:  {out_file_name}')

    def write_catalog_to_text(
        self, hal, hal_indices=None, part=None, directory=halo_default.simulation_directory
    ):
        '''
        Write properties of input halo/catalog catalog to a text file.

        Parameters
        ----------
        hal : dict
            catalog of halos at snapshot
        hal_indices : array-like
            indices of halos to write
        part : dict
            catalog of particles at snapshot
        '''
        species_name = 'star'  # write galaxy properties of this particle species

        if np.isscalar(hal_indices):
            hal_indices = [hal_indices]

        directory = ut.io.get_path(directory)

        for hi in hal_indices:
            file_name = 'halo_{}.txt'.format(hal['id'][hi])

            path_file_name = ut.io.get_path(directory) + file_name

            with open(path_file_name, 'w', encoding='utf-8') as file_out:
                Write = ut.io.WriteClass(file_out)

                Write.write('# halo id = {}'.format(hal['id'][hi]), print_stdout=True)
                Write.write(
                    '# star mass = {:.3e}'.format(hal.prop('star.mass', hi)), print_stdout=True
                )
                Write.write(
                    '# star particle number = {:d}'.format(hal.prop('star.number', hi)),
                    print_stdout=True,
                )
                Write.write(
                    '# velocity dispersion: star = {:.1f}, halo = {:.1f} km/s'.format(
                        hal.prop('star.vel.std')[hi], hal.prop('vel.std', hi)
                    ),
                    print_stdout=True,
                )
                # Write.write('# star R_50 = {:.2f} kpc'.format(hal.prop('star.radius.50', hi)))
                Write.write(
                    '# form lookback-time: 50% = {:.3f}, 95% = {:.3f}, 100% = {:.3f} Gyr'.format(
                        hal.prop('star.form.time.50.lookback', hi),
                        hal.prop('star.form.time.95.lookback', hi),
                        hal.prop('star.form.time.100.lookback', hi),
                    ),
                    print_stdout=True,
                )
                # Write.write('# star metallicity: total = {:.3f}, [Fe/H] = {:.3f}'.format(
                #            hal.prop('star.metallicity.metals', hi),
                #            hal.prop('star.metallicity.iron', hi)))
                Write.write(
                    '# distance from nearest host = {:.1f} kpc'.format(
                        hal.prop('host.near.distance.total', hi)
                    ),
                    print_stdout=True,
                )
                Write.write(
                    '# current age of Universe = {:.3f} Gyr'.format(hal.snapshot['time']),
                    print_stdout=True,
                )

                # Write.write('position = {:.2f}, {:.2f}, {:.2f} kpc'.format(
                #            hal.prop('star.position')[hi, 0], hal.prop('star.position')[hi, 1],
                #            hal.prop('star.position')[hi, 2]))

                part_indices = hal[species_name + '.indices'][hi]

                orb = ut.particle.get_orbit_dictionary(
                    part,
                    species_name,
                    part_indices,
                    part.host['position'][0],
                    part.host['velocity'][0],
                    return_single_dict=False,
                )

                Write.write('# columns:')
                Write.write(
                    '#  id mass[M_sun] formation-lookback-time[Gyr]'
                    + ' mass-fraction(He, C, N, O, Ne, Mg, Si, S, Ca, Fe)'
                    + ' distance(x, y, z, total)[kpc] velocity-radial[km/s]'
                )

                for pii, pi in enumerate(part_indices):
                    if species_name == 'star':
                        string = (
                            '{} {:.3e} {:.3f} {:.3e} {:.3e} {:.3e} {:.3e} {:.3e} {:.3e} {:.3e}'
                            + ' {:.3e} {:.3e} {:.3f} {:.3f} {:.3f} {:.3f} {:.1f}'
                        )
                        Write.write(
                            string.format(
                                part[species_name].prop('id', pi),
                                part[species_name].prop('mass', pi),
                                part[species_name].prop('age', pi),
                                part[species_name].prop('massfraction')[pi, 1],
                                part[species_name].prop('massfraction')[pi, 2],
                                part[species_name].prop('massfraction')[pi, 3],
                                part[species_name].prop('massfraction')[pi, 4],
                                part[species_name].prop('massfraction')[pi, 5],
                                part[species_name].prop('massfraction')[pi, 6],
                                part[species_name].prop('massfraction')[pi, 7],
                                part[species_name].prop('massfraction')[pi, 8],
                                part[species_name].prop('massfraction')[pi, 9],
                                orb['distance'][pii, 0],
                                orb['distance'][pii, 1],
                                orb['distance'][pii, 2],
                                orb['distance.total'][pii],
                                orb['velocity.rad'][pii],
                            )
                        )


IO = IOClass()


class ParticleClass(ut.io.SayClass):
    '''
    Assign indices and properties of particles to halos.
    '''

    def __init__(
        self,
        simulation_directory='../../',
        catalog_hdf5_directory=halo_default.rockstar_catalog_hdf5_directory,
    ):
        '''
        Initialize variables.
        '''
        self.simulation_directory = ut.io.get_path(simulation_directory)
        self.catalog_hdf5_directory = ut.io.get_path(catalog_hdf5_directory)
        self.catalog_id_name = 'id'
        self.prop_name_default = 'mass'  # default property for iterating
        self.Snapshot = None

    def io_species_hdf5(
        self,
        species='star',
        hal=None,
        snapshot_index=None,
        simulation_directory=halo_default.simulation_directory,
        rockstar_directory=halo_default.rockstar_directory,
        catalog_hdf5_directory=halo_default.rockstar_catalog_hdf5_directory,
        assign_species_pointers=False,
        host_number=None,
        write=False,
        verbose=False,
    ):
        '''
        THIS IS THE MAIN FUNCTION FOR INTERFACING WITH THE HALO PARTICLE SPECIES FILES.
        Read/write halo catalog with particle species properties to/from HDF5 file.
        If writing, write only species properties (not all halo properties).
        If reading, either assign species properties to input halo catalog or return new halo
        catalog with just particle species properties.

        Parameters
        ----------
        species : str or list
            name[s] of particle species to read/write: 'star', 'gas', 'dark'
        hal : class
            catalog of halos at snapshot
        snapshot_index : int
            index of snapshot
        simulation_directory : str
            directory of simulation
        rockstar_directory : str
            directory (full path) of rockstar halo files
        catalog_hdf5_directory : str
            directory (within rockstar directory) of processed HDF5 halo files
        assign_species_pointers : bool
            whether to assign species particle pointer indices to reference snapshot (usually z = 0)
        host_number : int
            number of hosts to assign and compute coordinates relative to,
            using species to compute coordinates
            if 0 or None, skip host assignment
        write : bool
            whether to write file (instead of read)
        verbose : bool
            whether to print diagnostics

        Returns
        -------
        hal : dictionary class
            halo catalog with particle species properties
        '''
        if species is True:
            species = 'star'  # default
        if np.isscalar(species):
            species = [species]
        simulation_directory = ut.io.get_path(simulation_directory)
        rockstar_directory = ut.io.get_path(rockstar_directory)
        catalog_hdf5_directory = ut.io.get_path(catalog_hdf5_directory)

        # parse inputs
        file_path = simulation_directory + rockstar_directory + catalog_hdf5_directory

        assert hal is not None or snapshot_index is not None
        if snapshot_index is None:
            snapshot_index = hal.snapshot['index']

        file_name = ''
        if 'star' in species:
            file_name += 'star_'
        if 'gas' in species:
            file_name += 'gas_'
        if 'dark' in species:
            file_name += 'dark_'
        file_name += '{:03d}'.format(snapshot_index)

        path_file_name = file_path + file_name

        if write:
            # write to file
            file_path = ut.io.get_path(file_path, create_path=True)

            # create temporary catalog to store species properties
            hal_spec = HaloDictionaryClass()
            # add species properties
            for prop_name in hal:
                if 'star.' in prop_name:
                    hal_spec[prop_name] = hal[prop_name]
            # add mass fraction from low-resolution DM
            hal_spec['dark2.mass'] = hal['dark2.mass']
            # add halo catalog id
            hal_spec[self.catalog_id_name] = hal[self.catalog_id_name]

            properties_add = []
            for prop_name in hal.info:
                if not isinstance(hal.info[prop_name], str):
                    hal_spec['info:' + prop_name] = np.array(hal.info[prop_name])
                    properties_add.append('info:' + prop_name)

            for prop_name in hal.snapshot:
                hal_spec['snapshot:' + prop_name] = np.array(hal.snapshot[prop_name])
                properties_add.append('snapshot:' + prop_name)

            for prop_name in hal.Cosmology:
                hal_spec['cosmology:' + prop_name] = np.array(hal.Cosmology[prop_name])
                properties_add.append('cosmology:' + prop_name)

            ut.io.file_hdf5(path_file_name, hal_spec)

        else:
            # read from file

            if hal is None:
                create_catalog = True
                # create new dictionary class to store halo catalog
                hal = HaloDictionaryClass()
            else:
                create_catalog = False
            header = {}

            try:
                # read
                hal_read = ut.io.file_hdf5(path_file_name, verbose=False)
            except OSError:
                self.say('! cannot find halo file:  {}'.format(path_file_name.lstrip('./')))
                return hal

            for prop_name, hal_read_prop in hal_read.items():
                if 'info:' in prop_name:
                    hal_prop_name = prop_name.split(':')[-1]
                    header[hal_prop_name] = float(hal_read_prop)
                elif 'snapshot:' in prop_name:
                    hal_prop_name = prop_name.split(':')[-1]
                    if hal_prop_name == 'index':
                        header[hal_prop_name] = int(hal_read_prop)
                    else:
                        header[hal_prop_name] = float(hal_read_prop)
                elif 'cosmology:' in prop_name:
                    hal_prop_name = prop_name.split(':')[-1]
                    header[hal_prop_name] = float(hal_read_prop)
                else:
                    if prop_name == self.catalog_id_name and prop_name in hal:
                        # sanity check - make sure halo ids match
                        if hal[prop_name].size != hal_read_prop.size:
                            raise ValueError(
                                f'{path_file_name} catalog is different size than input catalog'
                            )
                        if np.max(hal[prop_name] != hal_read_prop):
                            raise ValueError(
                                f'{path_file_name} has mis-matched ids from input catalog'
                            )
                    else:
                        hal[prop_name] = hal_read_prop

                        # parse specific properties (for older star particle files)
                        if prop_name == 'star.mass.neutral':
                            # spurrious assignment
                            del hal[prop_name]
                            continue

                        # for positive-definite properties, change null values from nan to -1
                        if (
                            'velocity' not in prop_name
                            and 'position' not in prop_name
                            and 'distance' not in prop_name
                            and '.indices' not in prop_name
                        ):
                            masks = np.isnan(hal[prop_name])
                            if np.max(masks):
                                hal[prop_name][masks] = -1

                        if 'massfraction' in prop_name:
                            # 32-bit float is plenty, change null values from 0 to -1
                            if hal[prop_name].dtype == np.float64:
                                hal[prop_name] = hal[prop_name].astype(np.float32) - 1

                        if prop_name == 'lowres.mass.frac':
                            # backward compatability with old star particle files
                            if 'mass' in hal:
                                # convert low-res mass fraction to low-res mass
                                hal['dark2.mass'] = 0 * hal['mass']
                                masks = np.isfinite(hal['lowres.mass.frac'])
                                hal['dark2.mass'][masks] *= hal['lowres.mass.frac'][masks]
                            del hal['lowres.mass.frac']

            if (
                len(hal) == 0
                or self.catalog_id_name not in hal
                or hal[self.catalog_id_name].size == 0
            ):
                self.say('! halo file {} contains no halos'.format(path_file_name.lstrip('./')))
                return hal

            have_species_number = 0
            for spec_name in species:
                if spec_name + '.number' in hal and len(hal[spec_name + '.number']) > 0:
                    have_species_number = np.sum(hal[spec_name + '.number'] > 0)

            self.say(
                '* read {} halos, {} have {} particles, from:  {}.hdf5'.format(
                    hal[self.catalog_id_name].size,
                    have_species_number,
                    ut.array.scalarize(species),
                    path_file_name.lstrip('./'),
                ),
                verbose,
            )

            if create_catalog:
                # not input existing halo catalog, so add simulation information
                hal.info = {
                    'dark.particle.mass': header['dark.particle.mass'],
                    'gas.particle.mass': header['gas.particle.mass'],
                    'box.length/h': header['box.length/h'],
                    'box.length': header['box.length'],
                    'catalog.kind': 'halo.catalog',
                    'file.kind': 'hdf5',
                    'has.baryons': False,
                    'simulation.name': '',
                }

                hal.snapshot = {
                    'index': header['index'],
                    'scalefactor': header['scalefactor'],
                    'redshift': header['redshift'],
                    'time': header['time'],
                    'time.lookback': header['time.lookback'],
                    'time.hubble': header['time.hubble'],
                }

                hal.Snapshot = ut.simulation.read_snapshot_times(simulation_directory)

                # just a place-holder dictionary
                hal.Cosmology = {
                    'omega_lambda': header['omega_lambda'],
                    'omega_matter': header['omega_matter'],
                    'omega_baryon': header['omega_baryon'],
                    'omega_curvature': header['omega_curvature'],
                    'omega_dm': header['omega_dm'],
                    'baryon.fraction': header['baryon.fraction'],
                    'hubble': header['hubble'],
                    'sigma_8': header['sigma_8'],
                    'n_s': header['n_s'],
                    'w': header['w'],
                }

            if 'star' in species or 'gas' in species:
                hal.info['has.baryons'] = True  # ensure baryonic flag

            if assign_species_pointers and have_species_number > 0:
                # assign particle pointer indices to halos
                from gizmo_analysis import gizmo_track

                # read particle pointer indices
                try:
                    ParticlePointer = gizmo_track.ParticlePointerClass()
                    Pointer = ParticlePointer.io_pointers(
                        snapshot_index=snapshot_index, simulation_directory=simulation_directory
                    )

                    # assign particle pointer indices for each species to halos
                    for spec_name in species:
                        # get pointer indices
                        pointer_indices = Pointer.get_pointers(
                            spec_name, spec_name, forward=True, return_single_array=True
                        )

                        # create new dictionary key
                        pointer_name = f'{spec_name}.z0.indices'

                        # initalize via copying current particle indices
                        hal[pointer_name] = copy.copy(hal[spec_name + '.indices'])

                        # get halos with species
                        hal_indices = np.where(hal[spec_name + '.mass'] > 0)[0]

                        # assign pointer indices
                        for hal_i in hal_indices:
                            hal[pointer_name][hal_i] = pointer_indices[
                                hal[spec_name + '.indices'][hal_i]
                            ]

                except OSError:
                    self.say(
                        '! cannot find {} particle pointer file at snapshot {} in {}'.format(
                            species[0], snapshot_index, simulation_directory
                        )
                    )

            if host_number is not None and host_number > 0:
                # if 'elvis' is in simulation directory name, force 2 hosts
                host_number = ut.catalog.get_host_number_from_directory(
                    host_number, simulation_directory, os
                )
                if hal.info['host.number'] is not None:
                    assert host_number == hal.info['host.number']
                # assign primary host[s]
                for spec_name in species:
                    IO.assign_hosts_to_catalog(hal, species, host_number)

            if create_catalog:
                return hal

    def assign_particle_indices(
        self,
        hal,
        part,
        species=['star'],
        mass_limits=[1e5, Inf],
        vel_circ_max_limits=[3, Inf],
        lowres_mass_frac_max=LOWRES_MASS_FRAC_MAX,
        bound_mass_frac_min=BOUND_MASS_FRAC_MIN,
        halo_radius_factor_max=0.8,
        radius_max=30,
        velocity_factor_max=2.0,
        gal_radius_mass_fraction=90,
        gal_radius_factor=1.5,
        particle_number_min=2,
        particle_number_fraction_converge=0.01,
        require_rockstar_species_mass=False,
    ):
        '''
        Identify particles of input species that are members of a halo
        (using cuts in position, velocity, and velocity dispersion).
        Assign to each halo the total number of member particles of input species and their indices
        in the particle catalog.

        Work down in halo sort_prop_name to prioritize particle assignment.
        Once assigned, exclude particles from future halo assignment, so each particle is assigned
        to only one halo.

        Parameters
        ----------
        hal : dict
            catalog of halos at snapshot
        part : dict
            catalog of particles at snapshot
        species : str or list
            name[s] of particle species to read + assign to halos
        mass_limits : list
            min and max limits of total mass to keep halo [M_sun]
        vel_circ_max_limits : list
            min and max limits of vel.circ.max to keep halo [km/s]
        lowres_mass_frac_max : float
            maximum fraction of total mass contaminated by low-resolution DM to keep halo
        bound_mass_frac_min : float
            minimum mass.bound/mass to keep halo
        halo_radius_factor_max : float
            max radius wrt halo (in units of halo radius) to consider particles as members
        radius_max : list
            max radius wrt halo center to consider particles as members [kpc physical]
        velocity_factor_max : float
            maximum velocity wrt halo and galaxy (in units of halo and galaxy velocity dispersion)
            to keep particle
        gal_radius_mass_fraction : float
            mass fraction to define galaxy edge
        gal_radius_factor : float
            multiplier for R_{gal_radius_mass_fraction} to keep particle
        particle_number_min : int
             minimum number of species particles within halo to consider it
        particle_number_fraction_converge : float
            fractional change in particle number to stop iterating cuts in radius and velocity
        require_rockstar_species_mass : bool
            whether to require rockstar species mass > 0 to consider halo
        '''
        # property to sort halos by to prioritize particle assignment
        sort_prop_name = 'vel.circ.max'

        species = ut.particle.parse_species(part, species)

        prop_limits = {
            'lowres.mass.frac': [0, lowres_mass_frac_max],
            'mass.bound/mass': [bound_mass_frac_min, Inf],
            'mass': mass_limits,
            'vel.circ.max': vel_circ_max_limits,
        }

        for spec_name in species:
            hal[spec_name + '.indices'] = [[] for _ in hal[self.prop_name_default]]
            dtype = ut.array.parse_int_dtype(part[spec_name]['mass'].size)
            hal[spec_name + '.number'] = np.zeros(hal[self.prop_name_default].size, dtype)

        hal_indices = ut.catalog.get_indices_catalog(hal, prop_limits)

        self.say(
            '* assigning {} particle indices to {} halos within property limits'.format(
                ut.array.scalarize(species), hal_indices.size
            )
        )

        # sort in decreasing order by mass/velocity (to limit particle overlap)
        hal_indices = hal_indices[np.argsort(hal.prop(sort_prop_name, hal_indices))[::-1]]

        for spec_name in species:
            if require_rockstar_species_mass:
                hal_indices = ut.array.get_indices(
                    hal.prop(spec_name + '.mass.rockstar'), [1, Inf], hal_indices
                )

                self.say(
                    '{} halos have {} mass: max = {:.2e} M_sun'.format(
                        hal_indices.size,
                        spec_name,
                        hal.prop(spec_name + '.mass.rockstar', hal_indices).max(),
                    )
                )

            # only use particles unassigned to larger halos
            part_indices_unassigned = ut.array.get_arange(part[spec_name]['mass'])
            halo_assigned_number = 0

            # pbar = self.make_progress_bar(hal_indices.size)
            # pbar.start()

            for _hal_ii, hal_i in enumerate(hal_indices):
                # pbar.update(_hal_ii)

                # keep particles within
                #   halo_radius_factor_max x halo radius
                #   velocity_factor_max x halo internal velocity
                distance_max = halo_radius_factor_max * hal.prop('radius', hal_i)
                if radius_max < distance_max:
                    distance_max = radius_max
                distance_limits = [0, distance_max]

                halo_vel_max = max(hal['vel.std'][hal_i], hal['vel.circ.max'][hal_i])
                velocity_limits = [0, velocity_factor_max * halo_vel_max]

                part_indices = ut.particle.get_indices_within_coordinates(
                    part,
                    spec_name,
                    part_indices_unassigned,
                    distance_limits,
                    hal.prop('position', hal_i),
                    velocity_limits,
                    hal.prop('velocity', hal_i),
                )

                # assign weight to each particle
                if spec_name == 'dark':
                    # no need to use mass weights for dark matter
                    weights = None
                elif part_indices.size >= particle_number_min:
                    # normalize mass weights by median for numerical stability
                    weights = part[spec_name]['mass'][part_indices] / np.median(
                        part[spec_name]['mass'][part_indices]
                    )

                # iterate to remove particles with outlier positions and velocities
                part_number_frac_dif = 1
                while (
                    part_indices.size >= particle_number_min
                    and part_number_frac_dif > particle_number_fraction_converge
                ):
                    part_number_prev = part_indices.size

                    # select particles via position ----------
                    gal_position = ut.coordinate.get_center_position(
                        part[spec_name]['position'][part_indices],
                        weights,
                        part.info['box.length'],
                        center_position=hal.prop('position', hal_i),
                    )

                    part_gal_distances = ut.coordinate.get_distances(
                        part[spec_name]['position'][part_indices],
                        gal_position,
                        part.info['box.length'],
                        part.snapshot['scalefactor'],
                        total_distance=True,
                    )

                    # use particle weights
                    # gal_radius = ut.math.percentile_weighted(
                    #    part_distances, gal_radius_mass_fraction, weights)
                    # skip particle weights for speed
                    gal_radius = np.percentile(part_gal_distances, gal_radius_mass_fraction)

                    # keep particles within gal_radius_factor x R_{gal_radius_mass_fraction}
                    # of galaxy center
                    masks = part_gal_distances < gal_radius_factor * gal_radius
                    part_indices = part_indices[masks]
                    if weights is not None:
                        weights = weights[masks]
                    if part_indices.size < particle_number_min:
                        break

                    # keep particles also within gal_radius_factor x R_{gal_radius_mass_fraction}
                    # of halo center
                    part_halo_distances = ut.coordinate.get_distances(
                        part[spec_name]['position'][part_indices],
                        hal.prop('position', hal_i),
                        part.info['box.length'],
                        part.snapshot['scalefactor'],
                        total_distance=True,
                    )
                    masks = part_halo_distances < gal_radius_factor * gal_radius
                    part_indices = part_indices[masks]
                    if weights is not None:
                        weights = weights[masks]
                    if part_indices.size < particle_number_min:
                        break

                    # select particles via velocity ----------
                    # get COM velocity of particles
                    gal_velocity = ut.coordinate.get_center_velocity(
                        part[spec_name]['velocity'][part_indices], weights
                    )

                    # total velocity of each particle wrt center velocity
                    part_vel2s = np.sum(
                        (part[spec_name]['velocity'][part_indices] - gal_velocity) ** 2, 1
                    )

                    # compute velocity dispersion of particles
                    # formal standard deviation
                    # part_vel_std = np.sqrt(np.average(part_vel2s, weights=weights))
                    # use median to avoid bias from outliers
                    # part_vel_std = np.sqrt(ut.math.percentile_weighted(part_vel2s, 50, weights))
                    gal_vel_std = np.sqrt(np.median(part_vel2s))  # skip mass weights for speed
                    # cap velocity dispersion at halo value (sanity check)
                    gal_vel_std = min(gal_vel_std, halo_vel_max)

                    # keep only particles with velocity near center velocity
                    masks = part_vel2s < (velocity_factor_max * gal_vel_std) ** 2
                    part_indices = part_indices[masks]
                    if weights is not None:
                        weights = weights[masks]
                    if part_indices.size < particle_number_min:
                        break

                    part_number_frac_dif = np.abs(
                        (part_indices.size - part_number_prev) / part_number_prev
                    )

                if part_indices.size >= particle_number_min:
                    halo_assigned_number += 1
                    hal[spec_name + '.indices'][hal_i] = part_indices
                    hal[spec_name + '.number'][hal_i] = len(part_indices)
                    part_indices_unassigned = np.setdiff1d(part_indices_unassigned, part_indices)
                    # part_indices_assigned = np.append(part_indices_assigned, part_indices)

            # pbar.finish()
            self.say(
                'assigned {} indices to {} halos with >= {} particles'.format(
                    spec_name, halo_assigned_number, particle_number_min
                )
            )
        print()
        hal[spec_name + '.indices'] = np.array(hal[spec_name + '.indices'], dtype=object)

    def assign_particle_properties(
        self,
        hal,
        part,
        species=['star'],
        properties=[
            'position',
            'velocity',
            'mass',
            'radius.50',
            'radius.90',
            'vel.std',
            'vel.std.50',
            #'vel.circ.50',
            'massfraction',
            'form.time.50',
            'form.time.90',
            'form.time.95',
            'form.time.100',
            'form.time.dif.68',
        ],
    ):
        '''
        Given particle species that are a member of each halo, assign their collective properties.

        For gas, might want to add mass.neutral.

        Parameters
        ----------
        hal : dict
            catalog of halos at snapshot
        part : dict
            catalog of particles at snapshot
        species : str or list
            name[s] of particle species to assign to halos
        properties : str or list
            properties to assign to halo
        '''
        species = ut.particle.parse_species(part, species)

        for spec_name in species:
            if spec_name + '.indices' not in hal:
                self.say(f'! halo catalog does not have {spec_name}.indices')

            for prop_name in properties:
                hal_prop_name = spec_name + '.' + prop_name

                if prop_name == 'position' and 'position' in hal:
                    hal[hal_prop_name] = np.array(hal['position']) * np.nan
                elif prop_name == 'velocity' and 'velocity' in hal:
                    hal[hal_prop_name] = np.array(hal['velocity']) * np.nan
                elif prop_name == 'massfraction' and 'massfraction' in part[spec_name]:
                    hal[hal_prop_name] = (
                        np.zeros(
                            (
                                hal.prop(self.prop_name_default).size,
                                part[spec_name]['massfraction'].shape[1],
                            ),
                            part[spec_name]['massfraction'].dtype,
                        )
                        - 1
                    )
                    hal._element_index = part[spec_name]._element_index
                else:
                    hal[hal_prop_name] = (
                        np.zeros(
                            hal.prop(self.prop_name_default).size,
                            hal.prop(self.prop_name_default).dtype,
                        )
                        - 1
                    )

        for spec_name in species:
            hal_indices = ut.array.get_indices(hal.prop(spec_name + '.number'), [1, Inf])

            self.say(f'* assigning {spec_name} properties to {hal_indices.size} halos')

            for _hal_ii, hal_i in enumerate(hal_indices):
                pis = hal[spec_name + '.indices'][hal_i]

                if 'mass' in part[spec_name]:
                    mass_weights = part[spec_name]['mass'][pis] / np.median(
                        part[spec_name]['mass'][pis]
                    )
                else:
                    mass_weights = None

                for prop_name in properties:
                    hal_prop_name = spec_name + '.' + prop_name

                    if prop_name == 'position' and 'position' in part[spec_name]:
                        hal[hal_prop_name][hal_i] = ut.coordinate.get_center_position(
                            part[spec_name]['position'][pis], mass_weights, part.info['box.length']
                        )

                    elif prop_name == 'velocity' and 'velocity' in part[spec_name]:
                        hal[hal_prop_name][hal_i] = ut.coordinate.get_center_velocity(
                            part[spec_name]['velocity'][pis], mass_weights
                        )

                    elif prop_name == 'massfraction' and 'massfraction' in part[spec_name]:
                        for element_i in range(part[spec_name]['massfraction'].shape[1]):
                            hal[hal_prop_name][hal_i, element_i] = np.sum(
                                part[spec_name]['massfraction'][pis, element_i] * mass_weights
                            ) / np.sum(mass_weights)

                    elif prop_name == 'mass' and 'mass' in part[spec_name]:
                        hal[hal_prop_name][hal_i] = part[spec_name]['mass'][pis].sum()

                    elif 'vel.std' in prop_name or 'vel.circ' in prop_name:
                        distance_max = None
                        if '.50' in prop_name or '.90' in prop_name:
                            # impose maximum distance on particles
                            mass_percent = prop_name.rsplit('.', maxsplit=1)[-1]
                            if spec_name == 'dark':
                                distance_max = 0.6  # radius to measure dark matter [kpc]
                            else:
                                distance_max = hal.prop('star.radius.' + mass_percent, hal_i)

                            distances = ut.coordinate.get_distances(
                                part[spec_name]['position'][pis],
                                hal.prop(spec_name + '.position', hal_i),
                                part.info['box.length'],
                                part.snapshot['scalefactor'],
                                total_distance=True,
                            )  # [kpc physical]

                            distance_masks = distances < distance_max
                            if np.sum(distance_masks) < 2:
                                continue

                            if 'vel.circ' in prop_name:
                                mass = np.sum(part[spec_name]['mass'][pis[distance_masks]])
                                hal[hal_prop_name][hal_i] = ut.halo_property.get_circular_velocity(
                                    mass, distance_max
                                )

                        if 'vel.std' in prop_name:
                            # compute velocity dispersion (3D standard deviation)
                            weights = np.array(mass_weights)
                            if distance_max:
                                weights = mass_weights[distance_masks]

                            velocity2s = np.sum(
                                (
                                    part[spec_name]['velocity'][pis]
                                    - hal[spec_name + '.velocity'][hal_i]
                                )
                                ** 2,
                                1,
                            )
                            if distance_max:
                                velocity2s = velocity2s[distance_masks]

                            # use average of velocity ** 2 (formal standard deviation)
                            # vel_std = np.sqrt(np.average(velocity2s, weights=weights))
                            # use median of velocity ** 2 (more stable to velocity_dif_max)
                            vel_std = np.sqrt(ut.math.percentile_weighted(velocity2s, 50, weights))

                            hal[hal_prop_name][hal_i] = vel_std

                    if spec_name == 'star':
                        if 'radius' in prop_name:
                            mass_percent = float(prop_name.rsplit('.', maxsplit=1)[-1])

                            gal_prop = ut.particle.get_galaxy_properties(
                                part,
                                spec_name,
                                'mass.percent',
                                mass_percent,
                                distance_max=hal.prop('radius', hal_i),
                                distance_bin_width=0.01,
                                distance_log_scale=True,
                                center_position=hal.prop(spec_name + '.position', hal_i),
                                part_indices=pis,
                                verbose=False,
                            )

                            hal[hal_prop_name][hal_i] = gal_prop['radius']

                        if 'form.time' in prop_name:
                            if (
                                '.50' in prop_name
                                or '.90' in prop_name
                                or '.95' in prop_name
                                or '.100' in prop_name
                            ):
                                percent = float(prop_name.rsplit('.', maxsplit=1)[-1])
                                hal[hal_prop_name][hal_i] = ut.math.percentile_weighted(
                                    part[spec_name].prop('form.time', pis), percent, mass_weights
                                )
                            elif '.dif.68' in prop_name:
                                val_16, val_84 = ut.math.percentile_weighted(
                                    part[spec_name].prop('form.time', pis), [16, 84], mass_weights
                                )
                                hal[hal_prop_name][hal_i] = val_84 - val_16

                    if spec_name == 'gas':
                        if prop_name == 'mass.neutral':
                            hal[hal_prop_name][hal_i] = (
                                part[spec_name].prop('mass.neutral', pis).sum()
                            )

            print()

        # assign 'star' properties to halos in dark-matter only simulation to compare
        if 'dark' in species and hal['star.mass.rockstar'].max() == 0:
            for prop_name in properties:
                hal['star.' + prop_name] = hal['dark.' + prop_name]

    def assign_lowres_mass(self, hal, part):
        '''
        Assign low-resolution dark matter (dark2) mass within R_halo.

        Parameters
        ----------
        hal : dict
            catalog of halos at snapshot
        part : dict
            catalog of particles at snapshot
        '''
        spec_name = 'dark2'
        mass_name = 'dark2.mass'

        # initialize halos to 100% low-res mass
        hal[mass_name] = np.zeros(hal.prop('mass').size, hal.prop('mass').dtype) + 1

        # some halos are completely low-res mass, yet do not have low-res particles near them (?!)
        # keep them as 100% low-res DM and skip henceforth
        hal_indices = ut.array.get_indices(hal.prop('mass.hires') > 0.1 * hal.prop('mass').min())

        hal[mass_name][hal_indices] = 0

        self.say(f'* assigning low-resolution {spec_name} mass to {hal_indices.size} halos')

        KDTree = spatial.KDTree(part[spec_name]['position'], boxsize=part.info['box.length'])

        lowres_spec_mass_max = np.max(part[spec_name]['mass'])

        for hi in hal_indices:
            # convert to [kpc comoving]
            hal_radius = hal['radius'][hi] / hal.snapshot['scalefactor']

            # set maximum number of particles expected, via halo mass and particle mass
            particle_number = int(np.clip(hal.prop('mass', hi) / lowres_spec_mass_max, 1e4, 1e7))

            distances, indices = KDTree.query(
                hal['position'][hi], particle_number, distance_upper_bound=hal_radius, workers=1
            )

            masks = distances < hal_radius
            if True in masks:
                hal[mass_name][hi] += np.sum(part[spec_name]['mass'][indices[masks]])

        print()

    def write_catalogs_with_species(
        self,
        species=['star'],
        snapshot_value_kind='index',
        snapshot_values='all',
        mass_limits=[1e5, Inf],
        vel_circ_max_limits=[3, Inf],
        particle_number_min=2,
        proc_number=1,
    ):
        '''
        Read halo catalog and particles from snapshot, assign given particle species to halos,
        write to HDF5 file in halo catalog directory.
        By default, set up to run from within halo finder (rockstar) sub-directory of simulation.

        Parameters
        ----------
        species : str or list
            name[s] of particle species to assign to halos
        snapshot_value_kind : str
            snapshot number kind: 'index', 'redshift', 'scalefactor'
        snapshot_values : int or float or list thereof or 'all'
            index[s] or redshifts[s] or scale-factor[s] of snapshot file[s]
            if 'all', use all snapshots
        mass_limits : list
            min and max halo mass for assigning species particles
        vel_circ_max_limits : list
            min and max halo vel.circ.max for assigning species particles
        particle_number_min : int
            minimum number of species particles within halo to consider it
        proc_number : int
            number of parallel processes to run
        '''
        if np.isscalar(species):
            species = [species]  # ensure is list

        # read list of all snapshots
        Snapshot = ut.simulation.read_snapshot_times(self.simulation_directory)
        snapshot_indices = Snapshot.parse_snapshot_values(snapshot_value_kind, snapshot_values)
        # skip snapshot 0
        if snapshot_indices[0] == 0:
            snapshot_indices = snapshot_indices[1:]

        args_list = []
        for snapshot_index in snapshot_indices:
            args_list.append(
                (
                    species,
                    snapshot_index,
                    mass_limits,
                    vel_circ_max_limits,
                    particle_number_min,
                )
            )

        ut.io.run_in_parallel(
            self._write_catalog_with_species,
            args_list,
            proc_number=proc_number,
            verbose=True,
        )

    def _write_catalog_with_species(
        self,
        species,
        snapshot_index,
        mass_limits,
        vel_circ_max_limits,
        particle_number_min,
    ):
        '''
        Read halo catalog and particles from snapshot, assign given particle species to halos,
        write species properties of those halos to HDF5 file.
        By default, set up to run from within rockstar halo directory of simulation.

        Parameters
        ----------
        species : str or list
            name[s] of particle species to assign to halos
        snapshot_index : int
            index of snapshot
        mass_limits : list
            min and max halo mass for assigning species particles
        vel_circ_max_limits : list
            min and max halo vel.circ.max for assigning species particles
        particle_number_min : int
            minimum number of species particles within halo to consider it
        '''
        from gizmo_analysis import gizmo_io

        # assign as current directory (assume am in within halo sub-directory)
        current_directory = os.getcwd().split('/')
        rockstar_directory = current_directory[-2] + '/' + current_directory[-1]

        part = gizmo_io.Read.read_snapshots(
            species + ['dark2'],
            'index',
            snapshot_index,
            self.simulation_directory,
            assign_hosts=False,
        )

        # read halo catalog
        hal = IO.read_catalogs(
            'index',
            snapshot_index,
            self.simulation_directory,
            rockstar_directory,
            self.catalog_hdf5_directory,
            file_kind='hdf5',
            species=None,
        )

        # assign nearest neighboring halos
        # IO.assign_nearest_neighbor(hal, mass_limits=mass_limits)

        # assign contamination mass from low-resolution dark matter
        self.assign_lowres_mass(hal, part)

        # assign indices of particles
        self.assign_particle_indices(
            hal,
            part,
            species,
            mass_limits,
            vel_circ_max_limits,
            particle_number_min=particle_number_min,
        )

        # assign galaxy properties from member particles
        self.assign_particle_properties(hal, part, species)

        # write to HDF5 file
        self.io_species_hdf5(
            species,
            hal,
            None,
            self.simulation_directory,
            rockstar_directory,
            self.catalog_hdf5_directory,
            write=True,
        )

    def write_species_pointers(
        self,
        species=['star'],
        snapshot_value_kind='index',
        snapshot_values='all',
        proc_number=1,
    ):
        '''
        TEST
        At each snapshot, read halo catalog and particle pointer indices to the reference snapshot,
        assign array of particle pointer indices to each halo with species particles,
        append to exsting halo catalog species HDF5 file.
        By default, set up to run from within halo finder (rockstar) sub-directory of simulation.

        Parameters
        ----------
        species : str or list
            name[s] of particle species to assign to halos
        snapshot_value_kind : str
            snapshot number kind: 'index', 'redshift', 'scalefactor'
        snapshot_values : int or float or list thereof
            index[s] or redshifts[s] or scale-factor[s] of snapshot file[s]
            if 'all' or None, use all snapshots
        proc_number : int
            number of parallel processes to run
        '''
        if np.isscalar(species):
            species = [species]  # ensure is list

        # read list of all snapshots
        self.Snapshot = ut.simulation.read_snapshot_times(self.simulation_directory)
        snapshot_indices = self.Snapshot.parse_snapshot_values(snapshot_value_kind, snapshot_values)

        args_list = [(species, snapshot_index) for snapshot_index in snapshot_indices]

        ut.io.run_in_parallel(
            self._write_species_pointers,
            args_list,
            proc_number=proc_number,
            verbose=True,
        )

    def _write_species_pointers(self, species, snapshot_index):
        '''
        TEST
        See documentation in write_species_pointers().
        '''
        from gizmo_analysis import gizmo_track

        # assign as current directory (assume am in within halo sub-directory)
        current_directory = os.getcwd().split('/')
        rockstar_directory = current_directory[-2] + '/' + current_directory[-1]

        # read halo catalog
        hal = self.io_species_hdf5(
            species,
            None,
            snapshot_index,
            self.simulation_directory,
            rockstar_directory,
            self.catalog_hdf5_directory,
            verbose=True,
        )

        # read particle pointer indices
        ParticlePointer = gizmo_track.ParticlePointerClass(species)
        Pointer = ParticlePointer.io_pointers(
            snapshot_index=snapshot_index, simulation_directory=self.simulation_directory
        )

        # assign particle pointer indices for each species to halos
        for spec_name in species:
            # get pointer indices
            pointer_indices = Pointer.get_pointers(
                spec_name, spec_name, forward=True, return_single_array=True
            )

            # create new dictionary key
            pointer_name = f'{spec_name}.z0.indices'

            # initalize via copying current particle indices
            hal[pointer_name] = copy.copy(hal[spec_name + '.indices'])

            # get halos with species
            hal_indices = np.where(hal[spec_name + '.mass'] > 0)[0]

            # assign pointer indices
            for hal_i in hal_indices:
                hal[pointer_name][hal_i] = pointer_indices[hal[spec_name + '.indices'][hal_i]]

        # write to HDF5 file
        self.io_species_hdf5(
            species,
            hal,
            None,
            self.simulation_directory,
            rockstar_directory,
            self.catalog_hdf5_directory,
            write=True,
        )

    def fix_lowres_mass_catalogs(
        self,
        snapshot_indices='all',
        proc_number=1,
    ):
        '''
        Read halo catalog and particles from snapshot, re-assign low-res mass.

        Parameters
        ----------
        snapshot_indices : list of ints or float
            snapshot index[s] or 'all'
        proc_number : int
            number of parallel processes to run
        '''
        if np.isscalar(snapshot_indices):
            snapshot_indices = [snapshot_indices]

        # read list of all snapshots
        self.Snapshot = ut.simulation.read_snapshot_times(self.simulation_directory)
        snapshot_indices = self.Snapshot.parse_snapshot_values('index', snapshot_indices)

        # assign as current directory (assume am in within halo sub-directory)
        current_directory = os.getcwd().split('/')
        rockstar_directory = current_directory[-2] + '/' + current_directory[-1]

        # get names of all halo species files to read
        _path_file_names, snapshot_indices = IO._get_catalog_file_names_and_values(
            self.simulation_directory + rockstar_directory,
            self.catalog_hdf5_directory,
            snapshot_indices,
            'star',
        )

        args_list = [(snapshot_index) for snapshot_index in snapshot_indices]

        ut.io.run_in_parallel(
            self._fix_lowres_mass_catalog, args_list, proc_number=proc_number, verbose=True
        )

    def _fix_lowres_mass_catalog(
        self,
        snapshot_index=0,
    ):
        '''
        Read halo catalog and particles from snapshot, re-assign low-res mass.

        Parameters
        ----------
        snapshot_index : int
            snapshot index
        '''
        from gizmo_analysis import gizmo_io

        # assign as current directory (assume am in within halo sub-directory)
        current_directory = os.getcwd().split('/')
        rockstar_directory = current_directory[-2] + '/' + current_directory[-1]

        # read halo catalog
        hal = IO.read_catalogs(
            'index',
            snapshot_index,
            self.simulation_directory,
            rockstar_directory,
            self.catalog_hdf5_directory,
            file_kind='hdf5',
        )

        # read particles
        part = gizmo_io.Read.read_snapshots(
            'dark2',
            'index',
            snapshot_index,
            self.simulation_directory,
            assign_hosts=False,
            check_properties=False,
        )

        # re-assign contamination mass from low-resolution dark matter
        self.assign_lowres_mass(hal, part)

        # write to HDF5 file
        self.io_species_hdf5(
            'star',
            hal,
            None,
            self.simulation_directory,
            rockstar_directory,
            self.catalog_hdf5_directory,
            write=True,
        )


# --------------------------------------------------------------------------------------------------
# output
# --------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------
# run from command line
# --------------------------------------------------------------------------------------------------

def main():
    '''.'''
    if len(os.sys.argv) <= 1:
        raise OSError('specify function: snapshots, hdf5')

    function_kind = str(os.sys.argv[1])
    assert 'snapshots' in function_kind or 'hdf5' in function_kind

    # assume am in rockstar sub-directory
    current_directory = os.getcwd().split('/')
    rockstar_directory = current_directory[-2] + '/' + current_directory[-1]

    if 'snapshots' in function_kind:
        snapshot_selection = 'all'
        if len(os.sys.argv) == 3:
            snapshot_selection = str(os.sys.argv[2])
        IO.write_snapshot_indices(snapshot_selection, '../../', rockstar_directory)

    elif 'hdf5' in function_kind:
        IO.rewrite_as_hdf5('../../', rockstar_directory)


if __name__ == '__main__':
    main()
