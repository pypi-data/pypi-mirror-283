'''
Select halos (for subsequent zoom-in).

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

import copy
import numpy as np
from numpy import Inf

import utilities as ut


# --------------------------------------------------------------------------------------------------
# selection
# --------------------------------------------------------------------------------------------------
class SelectClass(ut.io.SayClass):
    '''
    Select halos (for zoom-in).
    '''

    def __init__(self):
        '''
        Set default parameters for halo selection.
        '''
        self.isolate_param = {
            'distance/Rneig.limits': [4.0, Inf],
            'distance/Rself.limits': [5.0, Inf],
            'distance.limits': [],
            'neig.mass.frac.limits': [0.33, Inf],
            'neig.mass.limits': [],
        }

        # factor of 2.5x below is to select that many sigma beyond observed uncertainty
        self.satellite_param = {
            'bin.kind': 'error',
            'number': 1,
            'mass.name': 'vel.circ.max',
            'mass.limits': [92, 4.8 * 2.5],
            'distance.limits': [51, 2 * 20],
            #'velocity.rad.limits': [64, 6.8 * 2.5],
            #'velocity.tan.limits': [314, 24 * 2.5],
            #'velocity.total.limits': [321, 25 * 2.5]
            #'mass.limits': [92, 10],  # observed
            #'distance.limits': [51, 2],  # observed
            #'velocity.total.limits': [321, 25],  # observed
            #'velocity.rad.limits': [64, 7],  # observed
            #'velocity.tan.limits': [314, 24],  # observed
        }

    def select(
        self,
        hal,
        mass_name='mass',
        mass_limits=[1e12, 2e12],
        contaminate_mass_frac_max=0.01,
        hal_indices=None,
        sort_prop_name='mass',
        isolate_param=True,
        satellite_param=None,
        print_properties=True,
    ):
        '''
        Impose various cuts on halo catalog to select halos.

        Parameters
        ----------
        hal : dictionary class
            halo catalog
        mass_name : str
            mass kind to select halos
        mass_limits : list
            min and max limits for mass_name
        contaminate_mass_frac_max : float
            maximim low-res dark-matter mass fraction (if zoom-in)
        hal_indices : array
            prior selection indices of halos
        sort_prop_name : str
            property to sort halos by before listing and returning them
        isolate_param : dict or bool
            parameters for selecting isolated halos
            if True, use default parameters in self.isolate_param
        satellite_param : dict or bool
            parameters for selecting halos with satellites
            if True, use default parameters in self.satellite_param
        print_properties : bool
            whether to print properties of selected halos

        Returns
        -------
        hindices : array
            indices of selected halos
        '''
        neig_distance_max = 20000  # [kpc]
        neig_number_max = 1000

        if mass_name:
            assert mass_name in hal
        if sort_prop_name:
            assert sort_prop_name in hal

        hindices = hal_indices

        # select via halo mass
        if mass_limits and len(mass_limits) > 0:
            hindices = ut.array.get_indices(hal[mass_name], mass_limits, hindices)
            self.say(
                '* {} halos are within {} limits = [{}]'.format(
                    hindices.size, mass_name, ut.io.get_string_from_numbers(mass_limits, 2)
                )
            )

        # select via purity
        if (
            contaminate_mass_frac_max
            and 'mass.lowres' in hal
            and hal.prop('lowres.mass.frac').max() > 0
        ):
            hindices = ut.array.get_indices(
                hal.prop('lowres.mass.frac'), [0, contaminate_mass_frac_max], hindices
            )
            self.say(
                '* {} have mass contamination < {:.2f}%'.format(
                    hindices.size, contaminate_mass_frac_max
                )
            )

        NearestNeighbor = ut.catalog.NearestNeighborClass()

        # select neighbors above self mass
        NearestNeighbor.assign_to_self(
            hal,
            mass_name,
            mass_limits,
            [1, Inf],
            None,
            neig_distance_max,
            'Rneig',
            neig_number_max,
            print_diagnostics=False,
        )
        nearest = NearestNeighbor.nearest

        # select central halos
        masks = nearest['distance/Rneig'] > 1
        hindices = hindices[masks]
        self.say(f'* {hindices.size} are a central')

        # select via isolation
        if isolate_param:
            if isolate_param is True:
                isolate_param = copy.copy(self.isolate_param)  # use stored defaults

            # select isolated, defined wrt neighbor's R_halo
            if isolate_param['distance/Rneig.limits']:
                if (
                    min(isolate_param['distance/Rneig.limits']) > 1
                    or max(isolate_param['distance/Rneig.limits']) < Inf
                ):
                    nearest['distance/Rneig'] = nearest['distance/Rneig'][masks]
                    his = ut.array.get_indices(
                        nearest['distance/Rneig'], isolate_param['distance/Rneig.limits']
                    )
                    self.say(
                        '* {} ({:.1f}%) have nearest more massive halo at d/Rneig = {}'.format(
                            his.size,
                            100 * his.size / hindices.size,
                            isolate_param['distance/Rneig.limits'],
                        )
                    )
                    hindices = hindices[his]

            # select isolated, defined wrt self's R_halo
            if isolate_param['distance/Rself.limits']:
                # get neighbors above self mass * neig.mass.frac.limits
                NearestNeighbor.assign_to_self(
                    hal,
                    mass_name,
                    mass_limits,
                    isolate_param['neig.mass.frac.limits'],
                    None,
                    neig_distance_max,
                    'Rself',
                    neig_number_max,
                    hindices,
                    print_diagnostics=False,
                )
                nearest = NearestNeighbor.nearest
                his = ut.array.get_indices(
                    nearest['distance/Rself'], isolate_param['distance/Rself.limits']
                )
                self.say(
                    '* {} ({:.1f}%) have nearest halo with M/Mself = {} at d/Rself = {}'.format(
                        his.size,
                        100 * his.size / hindices.size,
                        isolate_param['neig.mass.frac.limits'],
                        isolate_param['distance/Rself.limits'],
                    )
                )
                hindices = hindices[his]

        # select via having satellite[s]
        if satellite_param:
            if satellite_param is True:
                satellite_param = copy.copy(self.satellite_param)  # use stored defaults

            if 'number' not in satellite_param:
                satellite_param['number'] = None

            # convert value + uncertainty into min + max limits
            for prop_name in satellite_param:
                if 'limits' in prop_name:
                    satellite_param[prop_name] = np.array(
                        ut.binning.get_bin_limits(
                            satellite_param[prop_name], satellite_param['bin.kind']
                        )
                    )

            # select satellites within mass limits
            if (
                'mass.name' in satellite_param
                and len(satellite_param['mass.name']) > 0
                and 'mass.limits' in satellite_param
                and len(satellite_param['mass.limits']) > 0
            ):
                sat_hindices = ut.array.get_indices(
                    hal[satellite_param['mass.name']], satellite_param['mass.limits']
                )

            # select satellites := within host halo radius
            sat_distance_max = hal['radius'][hindices].max()
            self.say(
                'selecting satellites at distance < {} kpc'.format(
                    ut.io.get_string_from_numbers(sat_distance_max, 1)
                )
            )

            a = hal.snapshot['scalefactor']
            sat_distancess, sat_indicess = ut.coordinate.get_neighbors(
                hal['position'][hindices] * a,
                hal['position'][sat_hindices] * a,
                sat_distance_max,
                neig_number_max=20,
                periodic_length=hal.info['box.length'],
                neig_ids=sat_hindices,
                return_lists=True,
                verbose=False,
            )

            # select halos with (required number of) satellites
            his_has_sat = []
            for hi, sat_distances in enumerate(sat_distancess):
                if satellite_param['number'] is not None and satellite_param['number'] >= 0:
                    if len(sat_distances) == satellite_param['number']:
                        his_has_sat.append(hi)
                else:
                    his_has_sat.append(hi)

            # convert to 1-D arrays, one entry per satellite (hosts may be repeated)
            hindices_has_sat = []
            sat_hindices = []
            sat_distances = []
            for hi in his_has_sat:
                for si, sat_hindex in enumerate(sat_indicess[hi]):
                    hindices_has_sat.append(hindices[hi])
                    sat_hindices.append(sat_hindex)
                    sat_distances.append(sat_distancess[hi][si])
            hindices_has_sat = np.array(hindices_has_sat)
            sat_hindices = np.array(sat_hindices)
            sat_distances = np.array(sat_distances)

            self.say(
                '* {} ({:.1f}%) have {} satellite[s] with {} = {}'.format(
                    len(his_has_sat),
                    100 * len(his_has_sat) / hindices.size,
                    satellite_param['number'],
                    satellite_param['mass.name'],
                    satellite_param['mass.limits'],
                )
            )

            # select via satellite distance
            if 'distance.limits' in satellite_param and len(satellite_param['distance.limits']) > 0:
                sis = ut.array.get_indices(sat_distances, satellite_param['distance.limits'])
                self.say(
                    '{} ({:.1f}%) satellite[s] at distance = {}'.format(
                        sis.size,
                        100 * sis.size / sat_hindices.size,
                        satellite_param['distance.limits'],
                    )
                )
                hindices_has_sat = hindices_has_sat[sis]
                sat_hindices = sat_hindices[sis]
                sat_distances = sat_distances[sis]

            # select via satellite total velocity
            if (
                'velocity.total.limits' in satellite_param
                and len(satellite_param['velocity.total.limits']) > 0
            ):
                sat_velocities_tot = ut.coordinate.get_velocity_differences(
                    hal['velocity'][hindices_has_sat],
                    hal['velocity'][sat_hindices],
                    hal['position'][hindices_has_sat],
                    hal['position'][sat_hindices],
                    hal.info['box.length'],
                    hal.snapshot['scalefactor'],
                    hal.snapshot['time.hubble'],
                    total_velocity=True,
                )
                sis = ut.array.get_indices(
                    sat_velocities_tot, satellite_param['velocity.total.limits']
                )
                self.say(
                    '{} ({:.1f}%) satellites with velocity.total = {}'.format(
                        sis.size,
                        100 * sis.size / sat_hindices.size,
                        satellite_param['velocity.total.limits'],
                    )
                )
                hindices_has_sat = hindices_has_sat[sis]
                sat_hindices = sat_hindices[sis]
                sat_distances = sat_distances[sis]

            orb = None

            # select via satellite radial and/or tangential velocity
            if 'velocity.rad.limits' in satellite_param or 'velocity.tan.limits' in satellite_param:
                distance_vectors = ut.coordinate.get_distances(
                    hal['position'][hindices_has_sat],
                    hal['position'][sat_hindices],
                    hal.info['box.length'],
                )
                velocity_vectors = ut.coordinate.get_velocity_differences(
                    hal['velocity'][hindices_has_sat],
                    hal['velocity'][sat_hindices],
                    hal['position'][hindices_has_sat],
                    hal['position'][sat_hindices],
                    hal.info['box.length'],
                    hal.snapshot['scalefactor'],
                    hal.snapshot['time.hubble'],
                )

                orb = ut.orbit.get_orbit_dictionary(distance_vectors, velocity_vectors)

                if (
                    'velocity.rad.limits' in satellite_param
                    and len(satellite_param['velocity.rad.limits']) > 0
                ):
                    sis = ut.array.get_indices(
                        orb['velocity.rad'], satellite_param['velocity.rad.limits']
                    )
                    self.say(
                        '{} ({:.1f}%) satellites with velocity.rad = {}'.format(
                            sis.size,
                            100 * sis.size / sat_hindices.size,
                            satellite_param['velocity.rad.limits'],
                        )
                    )
                    hindices_has_sat = hindices_has_sat[sis]
                    sat_hindices = sat_hindices[sis]
                    sat_distances = sat_distances[sis]
                    for prop_name in orb:
                        orb[prop_name] = orb[prop_name][sis]

                if (
                    'velocity.tan.limits' in satellite_param
                    and len(satellite_param['velocity.tan.limits']) > 0
                ):
                    sis = ut.array.get_indices(
                        orb['velocity.tan'], satellite_param['velocity.tan.limits']
                    )
                    self.say(
                        '{} ({:.1f}%) satellites with velocity.tan = {}'.format(
                            sis.size,
                            100 * sis.size / sat_hindices.size,
                            satellite_param['velocity.tan.limits'],
                        )
                    )
                    hindices_has_sat = hindices_has_sat[sis]
                    sat_hindices = sat_hindices[sis]
                    sat_distances = sat_distances[sis]
                    for prop_name in orb:
                        orb[prop_name] = orb[prop_name][sis]

            hindices = hindices_has_sat

        if sort_prop_name:
            his = np.argsort(hal[sort_prop_name][hindices])
            hindices = hindices[his]
            if satellite_param and len(sat_hindices) > 0:
                sat_hindices = sat_hindices[his]
                sat_distances = sat_distances[his]

        if print_properties:
            self.say('')
            for hi, hindex in enumerate(hindices):
                self.say(
                    'halo: index = {}, M = {:.2e} Msun, R = {:.1f} kpc, Vmax = {:.1f} km/s'.format(
                        hindex,
                        hal[mass_name][hindex],
                        hal['radius'][hindex],
                        hal['vel.circ.max'][hindex],
                    )
                )
                self.say(
                    '      position = [{:.2f}, {:.2f}, {:.2f}] kpc comoving'.format(
                        hal['position'][hindex, 0],
                        hal['position'][hindex, 1],
                        hal['position'][hindex, 2],
                    )
                )

                if satellite_param:
                    sat_hindex = sat_hindices[hi]
                    sat_distance = sat_distances[hi]
                    words = 'sat:  index = {}, M (bound) = {:.2e} ({:.2e}) Msun, Vmax = {:.1f} km/s'
                    self.say(
                        words.format(
                            sat_hindex,
                            hal['mass'][sat_hindex],
                            hal['mass.bound'][sat_hindex],
                            hal['vel.circ.max'][sat_hindex],
                        )
                    )
                    words = '      d = {:.1f} kpc'.format(sat_distance)
                    if orb is not None and len(orb) > 0:
                        words += ', vel tot = {:.1f}, rad = {:.1f}, tan = {:.1f} km/s\n'.format(
                            orb['velocity.total'][hi],
                            orb['velocity.rad'][hi],
                            orb['velocity.tan'][hi],
                        )
                    self.say(words, end='\n\n')

        return hindices
