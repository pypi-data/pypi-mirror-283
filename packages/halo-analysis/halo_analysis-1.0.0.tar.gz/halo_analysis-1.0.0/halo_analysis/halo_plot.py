'''
Plot and analyze halo catalogs (generated via Rockstar or AHF) and halo merger trees
(generated via ConsistentTrees).

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
from numpy import Inf
from matplotlib import pyplot as plt
from matplotlib import ticker

import utilities as ut


# --------------------------------------------------------------------------------------------------
# utility
# --------------------------------------------------------------------------------------------------
def print_properties(hal, hal_indices, properties=None, digits=3):
    '''
    Print useful properties of halo[s].

    Parameters
    ----------
    hal : dict
        catalog of halos
    hal_indices : int or array
        index[s] of halo[s]
    properties : str or list
        name[s] of properties to print
    digits : int
        number of digits after period
    '''
    Say = ut.io.SayClass(print_properties)

    hal_indices = ut.array.arrayize(hal_indices)

    if properties:
        # print input properties
        if properties == 'default':
            properties = [
                'id',
                'mass',
                'mass.vir',
                'mass.200c',
                'vel.circ.max',
                'spin.bullock',
                'spin.peebles',
                'position',
            ]

        for hi in hal_indices:
            print(f'halo index = {hi}')
            for prop_name in properties:
                string = ut.io.get_string_from_numbers(hal[prop_name][hi], digits)
                print(f'{prop_name} = {string}')
            print()

    else:
        # print default (galaxy) properties
        for hi in hal_indices:
            Say.say(f'halo index = {hi}')
            Say.say('host distance = {:.1f} kpc'.format(hal.prop('host.distance.total', hi)))
            print()

            Say.say('halo')
            Say.say(
                '* M_total = {} Msun'.format(ut.io.get_string_from_numbers(hal.prop('mass', hi), 2))
            )
            Say.say(
                '* M_bound/M_total = {}'.format(
                    ut.io.get_string_from_numbers(hal.prop('mass.bound/mass', hi), 3)
                )
            )
            Say.say(
                '* V_circ,max = {} km/s'.format(
                    ut.io.get_string_from_numbers(hal.prop('vel.circ.max', hi), 1)
                )
            )
            Say.say(
                '* V_std = {} km/s'.format(
                    ut.io.get_string_from_numbers(hal.prop('vel.std', hi), 1)
                )
            )
            Say.say(
                '* R_halo = {} kpc'.format(ut.io.get_string_from_numbers(hal.prop('radius', hi), 1))
            )
            print()

            if 'star.mass' in hal and np.nanmax(hal['star.mass']) > 0:
                Say.say('star')
                Say.say('* N_star = {:d}'.format(hal.prop('star.number', hi)))
                Say.say(
                    '* M_star = {} M_sun'.format(
                        ut.io.get_string_from_numbers(
                            hal.prop('star.mass', hi), 2, exponential=True
                        )
                    )
                )
                # Say.say('star mass: rockstar = {:.2e}, mine = {:.2e}, ratio = {:.2f}'.format(
                #        hal.prop('star.mass.rockstar', hi), hal.prop('star.mass', hi),
                #        hal.prop('star.mass/star.mass.rockstar', hi)))
                Say.say(
                    '* M_star/M_bound = {}'.format(
                        ut.io.get_string_from_numbers(hal.prop('star.mass/mass.bound', hi), 4)
                    )
                )
                Say.say(
                    '* R_50 = {}, R_90 = {} kpc'.format(
                        ut.io.get_string_from_numbers(hal.prop('star.radius.50', hi), 2),
                        ut.io.get_string_from_numbers(hal.prop('star.radius.90', hi), 2),
                    )
                )
                Say.say(
                    '* density(R_50) = {} M_sun/kpc^3'.format(
                        ut.io.get_string_from_numbers(
                            hal.prop('star.density.50', hi), 2, exponential=True
                        )
                    )
                )
                Say.say(
                    '* V_std = {}, V_std(R_50) = {} km/s'.format(
                        ut.io.get_string_from_numbers(hal.prop('star.vel.std', hi), 1),
                        ut.io.get_string_from_numbers(hal.prop('star.vel.std.50', hi), 1),
                    )
                )
                Say.say(
                    '* age: 50% = {:.2f}, 100% = {:.2f}, 68% dif = {:.3f} Gyr'.format(
                        hal.prop('star.form.time.50.lookback', hi),
                        hal.prop('star.form.time.100.lookback', hi),
                        hal.prop('star.form.time.dif.68', hi),
                    )
                )

                Say.say(
                    '* [Z/H] = {:.1f}, [Fe/H] = {:.1f}'.format(
                        hal.prop('star.metallicity.metals', hi),
                        hal.prop('star.metallicity.iron', hi),
                    )
                )

                print()

                Say.say('star v dark')
                distance = ut.coordinate.get_distances(
                    hal.prop('star.position', hi),
                    hal.prop('position', hi),
                    hal.info['box.length'],
                    total_distance=True,
                )
                Say.say(
                    '* position offset = {:.0f} pc, {:0.2f} R_50'.format(
                        distance * 1000, distance / hal.prop('star.radius.50', hi)
                    )
                )
                velocity = ut.coordinate.get_velocity_differences(
                    hal.prop('star.velocity', hi),
                    hal.prop('velocity', hi),
                    hal.prop('star.position', hi),
                    hal.prop('position', hi),
                    hal.info['box.length'],
                    hal.snapshot['scalefactor'],
                    hal.snapshot['time.hubble'],
                    total_velocity=True,
                )
                Say.say(
                    '* velocity offset = {:.1f} km/s, {:0.2f} V_std(R_50)'.format(
                        velocity, velocity / hal.prop('star.vel.std.50', hi)
                    )
                )
                print()

            if 'gas.mass' in hal and np.max(hal['gas.mass']) > 0:
                try:
                    Say.say(
                        'gas mass: rockstar = {:.2e}, mine = {:.2e}, ratio = {:.2f}'.format(
                            hal.prop('gas.mass.rockstar')[hi],
                            hal.prop('gas.mass')[hi],
                            hal.prop('gas.mass/gas.mass.rockstar')[hi],
                        )
                    )
                except KeyError:
                    Say.say('gas mass = {:.3e}'.format(hal.prop('gas.mass', hi)))

                Say.say('gas/star mass = {:.3f}'.format(hal.prop('gas.mass/star.mass', hi)))

                try:
                    Say.say(
                        'neutral hydrogen: mass = {:.3e}, gas/star mass = {:.3f}'.format(
                            hal.prop('gas.mass.neutral', hi),
                            hal.prop('gas.mass.neutral/star.mass', hi),
                        )
                    )
                except KeyError:
                    pass

            # Say.say('position = {:.2f}, {:.2f}, {:.2f} kpc'.format(
            #        hal.prop('star.position')[hi, 0], hal.prop('star.position')[hi, 1],
            #        hal.prop('star.position')[hi, 2]))
            print()


# --------------------------------------------------------------------------------------------------
# utilities
# --------------------------------------------------------------------------------------------------
def get_indices_diffuse(
    halt,
    snapshot_index_limits=[450, 600.1],
    star_mass_limits=[2e5, 2e6],
    star_radius_limits=[2, Inf],
    star_vel_std_limits=[3, 18],
    star_metallicity_limits=[-3, -0.5],
    star_mpeak_fraction_limits=[0, 0.3],
    use_history=False,
):
    '''
    .
    '''
    Say = ut.io.SayClass(get_indices_diffuse)

    his = halt.get_indices()
    his = ut.array.get_indices(halt['snapshot'], snapshot_index_limits, his)
    his = ut.array.get_indices(halt['star.mass'], star_mass_limits, his)

    if use_history:
        his = his[
            ut.array.get_indices(
                halt.prop('star.mass / star.mass.peak', his), star_mpeak_fraction_limits
            )
        ]
    else:
        his = ut.array.get_indices(halt['star.radius.50'], star_radius_limits, his)
        his = ut.array.get_indices(halt['star.vel.std.50'], star_vel_std_limits, his)
        his = ut.array.get_indices(halt.prop('star.metallicity.fe'), star_metallicity_limits, his)

    for hi in his:
        his_p = halt.prop('progenitor.main.indices', hi)
        # remove main progenitors from list
        his = np.setdiff1d(his, his_p[1:])

    for hi in his:
        his_p = halt.prop('progenitor.main.indices', hi)
        m_peak_hi = his_p[np.nanargmax(halt.prop('star.mass', his_p))]
        d_min = halt.prop('host.distance.total', his_p).min()
        d_min_hi = his_p[np.nanargmin(halt.prop('host.distance.total', his_p))]

        # get anologues at similar mass
        his_m = ut.array.get_indices(halt['snapshot'], snapshot_index_limits)
        his_m = ut.array.get_indices(
            halt['star.mass'], [halt['star.mass'][hi] * 0.6, halt['star.mass'][hi] * 1.5], his_m
        )

        Say.say(
            '* hi {} | si {} z {:.1f} | Nstar {:3d} | Mpeak si {}, z {:.1f}'.format(
                hi,
                halt['snapshot'][hi],
                halt.Snapshot['redshift'][halt['snapshot'][hi]],
                halt['star.number'][hi],
                halt['snapshot'][m_peak_hi],
                halt.Snapshot['redshift'][halt['snapshot'][m_peak_hi]],
            )
        )

        string = (
            'M, peak {}, {} | R_50, @peak (med) {:.1f}, {:.1f} ({:.1f})'
            + ' | Vdisp, @peak (med) {:.1f}, {:.1f} ({:.1f})'
            + '\n  Fe (med) {:.1f} ({:.1f})'
            + ' | d, @peak, min {:.0f}, {:.0f}, {:.0f}, z(d_min) {:.1f}'
        )

        Say.say(
            string.format(
                ut.io.get_string_from_numbers(halt['star.mass'][hi], digits=1),
                ut.io.get_string_from_numbers(halt.prop('star.mass', m_peak_hi), digits=1),
                halt['star.radius.50'][hi],
                halt.prop('star.radius.50', m_peak_hi),
                np.median(halt.prop('star.radius.50', his_m)),
                halt['star.vel.std.50'][hi],
                halt.prop('star.vel.std.50', m_peak_hi),
                np.median(halt.prop('star.vel.std.50', his_m)),
                halt.prop('star.metallicity.fe', hi),
                np.median(halt.prop('star.metallicity.fe', his_m)),
                halt.prop('host.distance.total', hi),
                halt.prop('host.distance.total', m_peak_hi),
                d_min,
                halt.Snapshot['redshift'][halt['snapshot'][d_min_hi]],
            )
        )

    print()


# --------------------------------------------------------------------------------------------------
# mass function
# --------------------------------------------------------------------------------------------------
def plot_number_v_mass(
    hals=None,
    gal=None,
    mass_names='mass',
    mass_limits=None,
    mass_width=0.2,
    mass_log_scale=True,
    host_distance_limitss=[[1, 350]],
    object_kind='halo',
    hal_indicess=None,
    gal_indices=None,
    number_kind='number.cum',
    number_limits=None,
    number_log_scale=True,
    include_above_limits=True,
    plot_file_name=False,
    plot_directory='.',
    figure_index=1,
):
    '''
    Plot number (cumulative or differential) v mass_name.

    Parameters
    ----------
    hals : dict or list
        catalog[s] of halos at snapshot
    gal : dict
        catalog of galaxies to compare against
    mass_names : str or list
        halo mass kind[s] to plot
    mass_limits : list
        min and max limits for mass_name
    mass_width : float
        width of mass_name bin
    mass_log_scale : bool
        whether to use logarithmic scaling for mass_name bins
    host_distance_limitss : list or list of lists
        min and max limits of distance to host [kpc physical]
    object_kind : str
        shortcut for halo kind to plot: 'halo', 'galaxy', 'cluster' and/or 'satellite', 'isolated'
    hal_indicess : array or list of arrays
        halo indices to plot
    gal_indices : array
        galaxy indices to plot
    number_kind : str
        mass function kind to plot: 'number',  'number.dif', 'number.cum'
    number_limits : list
        min and max limits to impose on y-axis
    number_log_scale : bool
        whether to use logarithmic scaling for y axis
    include_above_limits : bool
        whether to include mass_name values above limits for cumulative
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory in which to write figure file
    figure_index : int
        index of figure for matplotlib
    '''
    if hals is None:
        hals = []
    if isinstance(hals, dict):
        hals = [hals]
    if np.isscalar(mass_names):
        mass_names = [mass_names]
    if len(mass_names) == 1 and len(hals) > 1:
        mass_names = [mass_names[0] for _ in hals]

    mass_name_default = mass_names[0]

    if host_distance_limitss is not None:
        host_distance_limitss = np.array(host_distance_limitss)
        if np.ndim(host_distance_limitss) == 1:
            host_distance_limitss = np.array([host_distance_limitss])
        host_distance_bin_number = host_distance_limitss.shape[0]
    else:
        host_distance_bin_number = 1

    if not isinstance(hal_indicess, list):
        hal_indicess = [hal_indicess for _ in hals]

    assert number_kind in ['number', 'number.dif', 'number.cum']

    MassBin = ut.binning.BinClass(
        mass_limits, mass_width, include_max=True, log_scale=mass_log_scale
    )

    hal_number_values, hal_number_uncs = np.zeros(
        [2, len(hals), host_distance_bin_number, MassBin.number]
    )

    # get counts for halos
    for hal_i, hal in enumerate(hals):
        mass_name = mass_names[hal_i]

        if hal_indicess[hal_i] is None or len(hal_indicess[hal_i]) == 0:
            hal_indices = ut.array.get_arange(hal.prop(mass_name))
        else:
            hal_indices = hal_indicess[hal_i]

        for dist_i, host_distance_limits in enumerate(host_distance_limitss):
            his_d = hal.get_indices(
                object_kind=object_kind,
                host_distance_limits=host_distance_limits,
                prior_indices=hal_indices,
            )

            if len(his_d) > 0:
                hal_number_d = MassBin.get_distribution(
                    hal.prop(mass_name, his_d), include_above_limits=include_above_limits
                )
                hal_number_values[hal_i, dist_i] = hal_number_d[number_kind]
                hal_number_uncs[hal_i, dist_i] = hal_number_d[number_kind + '.err']

    # get mass function for observed galaxies
    host_names = ['MW', 'M31']
    gal_mass_name = mass_name_default.replace('.part', '')
    if gal is not None and gal_mass_name in gal:
        gal_number_values, gal_number_uncs = np.zeros(
            [2, 2, host_distance_bin_number, MassBin.number]
        )

        for dist_i, host_distance_limits in enumerate(host_distance_limitss):
            gis = ut.array.get_indices(
                gal['host.distance.total'], host_distance_limits, gal_indices
            )

            for host_i, host_name in enumerate(host_names):
                gis_h = gis[gal['host.name'][gis] == host_name.encode()]

                gal_number_h = MassBin.get_distribution(
                    gal[gal_mass_name][gis_h], include_above_limits=include_above_limits
                )
                gal_number_values[host_i, dist_i] = gal_number_h[number_kind]
                gal_number_uncs[host_i, dist_i] = gal_number_h[number_kind + '.err']

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    mass_funcs_all = []
    if hal_number_values.size:
        mass_funcs_all.append(hal_number_values)
    if gal is not None:
        mass_funcs_all.append(gal_number_values)

    ut.plot.set_axes_scaling_limits(
        subplot, mass_log_scale, mass_limits, None, number_log_scale, number_limits, mass_funcs_all
    )

    # increase minor ticks along y-axis
    if not number_log_scale:
        subplot.yaxis.set_minor_locator(plt.MultipleLocator(2))

    if not mass_log_scale:
        subplot.xaxis.set_minor_locator(plt.MultipleLocator(1))

    # set x-axis label
    axis_x_label = ut.plot.Label.get_label(gal_mass_name)
    subplot.set_xlabel(axis_x_label)

    # set y-axis label
    mass_label = ut.plot.Label.get_label(gal_mass_name, get_units=False).strip('$')
    if 'dif' in number_kind:
        axis_y_label = f'${{\\rm d}}n / {{\\rm d}}log({mass_label})$'
    elif 'cum' in number_kind:
        if len(host_distance_limitss) > 0 and len(host_distance_limitss[0]) > 0:
            axis_y_label = f'$N_{{\\rm satellite}}(> {mass_label})$'
        else:
            axis_y_label = f'$N(> {mass_label})$'
    else:
        axis_y_label = f'$N({mass_label})$'
    subplot.set_ylabel(axis_y_label)

    colors = ut.plot.get_colors(len(hals))
    line_styles = ut.plot.get_line_styles(host_distance_bin_number)

    x_values = MassBin.get_bin_values(number_kind)

    # plot observed galaxies
    host_label_dict = {
        'MW': {'color': 'black', 'linestyle': '--'},
        'M31': {'color': 'black', 'linestyle': ':'},
    }

    if gal is not None and gal_mass_name in gal:
        for dist_i, host_distance_limits in enumerate(host_distance_limitss):
            for host_i, host_name in enumerate(host_names):
                label = host_name.replace('MW', 'Milky Way').replace('M31', 'M31 (Andromeda)')
                subplot.plot(
                    x_values,
                    gal_number_values[host_i, dist_i],
                    # gal_number_uncs[hal_i],
                    color=host_label_dict[host_name]['color'],
                    linestyle=host_label_dict[host_name]['linestyle'],
                    linewidth=3.0,
                    alpha=0.8,
                    label=label,
                )

    # plot halos
    for hal_i, hal in enumerate(hals):
        for dist_i, host_distance_limits in enumerate(host_distance_limitss):
            linewidth = 3.0
            alpha = 0.9
            color = colors[hal_i]

            label = hal.info['simulation.name']

            # ensure n = 1 is clear on log plot
            y_values = hal_number_values[hal_i, dist_i]
            if number_log_scale:
                y_values = np.clip(y_values, 0.5, Inf)

            subplot.plot(
                x_values,
                y_values,
                # hal_number_uncs[hal_i],
                color=color,
                linestyle=line_styles[dist_i],
                linewidth=linewidth,
                alpha=alpha,
                label=label,
            )

    if len(hals) > 1 or gal is not None or len(host_distance_limitss) > 1:
        legend = subplot.legend(loc='best')
        legend.get_frame()

    if plot_file_name is True or plot_file_name == '':
        redshift_label = ''
        galaxy_label = ''
        if len(hals) > 0:
            redshift_label = ut.plot.get_time_label('redshift', hals[0].snapshot)
        if gal is not None:
            galaxy_label = '_lg'
        if not len(hals) > 0 and '.part' in mass_name_default:
            mass_name_default = mass_name_default.replace('.part', '')
        plot_file_name = f'{number_kind}_v_{mass_name_default}{galaxy_label}{redshift_label}'
    ut.plot.parse_output(plot_file_name, plot_directory)


def plot_fraction_has_baryon_v_mass(
    hals,
    baryon_mass_name='star.mass',
    baryon_mass_limits=[1, Inf],
    mass_name='mass',
    mass_limits=None,
    mass_width=0.2,
    mass_log_scale=True,
    host_distance_limitss=[[0, 350]],
    axis_y_limits=[0, 1],
    axis_y_log_scale=False,
    plot_file_name=False,
    plot_directory='.',
    figure_index=1,
):
    '''
    Plot fraction of halos with baryons versus mass_name.

    Parameters
    ----------
    hals : dict or list
        catalog[s] of halos at snapshot
    baryon_mass_name : str
        baryon metric to use: 'star.mass', 'gas.mass', 'baryon.mass'
    mass_name : str
        halo mass kind
    mass_limits : list
        min and max limits for mass_name
    mass_width : float
        width of mass_name bin
    mass_log_scale : bool
        whether to use logarithmic scaling for mass_name bins
    host_distance_limitss : list or list of lists
        min and max limits of distance to host [kpc physical]
    axis_y_limits : list
        min and max limits for y-axis
    axis_y_log_scale : bool
        whether to use logarithmic scaling for y axis
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory in which to write figure file
    figure_index : int
        index of figure for matplotlib
    '''
    Fraction = ut.math.FractionClass(uncertainty_kind='beta')

    if isinstance(hals, dict):
        hals = [hals]

    if host_distance_limitss is not None:
        host_distance_limitss = np.array(host_distance_limitss)
        if np.ndim(host_distance_limitss) == 1:
            host_distance_limitss = np.array([host_distance_limitss])
        host_distance_bin_number = host_distance_limitss.shape[0]

    MassBin = ut.binning.BinClass(mass_limits, mass_width, log_scale=mass_log_scale)

    has_baryon_frac = {
        'value': np.zeros([len(hals), host_distance_bin_number, MassBin.number]),
        'error': np.zeros([len(hals), host_distance_bin_number, 2, MassBin.number]),
        'number': np.zeros([len(hals), host_distance_bin_number, MassBin.number]),
    }

    for hal_i, hal in enumerate(hals):
        his = ut.array.get_indices(hal.prop(mass_name), mass_limits)

        for dist_i, host_distance_limits in enumerate(host_distance_limitss):
            his_d = hal.get_indices(
                object_kind='halo', host_distance_limits=host_distance_limits, prior_indices=his
            )

            his_d_baryon = ut.array.get_indices(
                hal.prop(baryon_mass_name), baryon_mass_limits, his_d
            )

            halo_numbers_d = MassBin.get_histogram(hal.prop(mass_name, his_d))
            baryon_numbers_d = MassBin.get_histogram(hal.prop(mass_name, his_d_baryon))

            print(halo_numbers_d)
            print(baryon_numbers_d)

            has_baryon_frac['number'][hal_i, dist_i] = halo_numbers_d

            (
                has_baryon_frac['value'][hal_i, dist_i],
                has_baryon_frac['error'][hal_i, dist_i],
            ) = Fraction.get_fraction(baryon_numbers_d, halo_numbers_d)

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)
    # , left=0.17, right=0.96, top=0.96, bottom=0.14)

    ut.plot.set_axes_scaling_limits(
        subplot,
        mass_log_scale,
        mass_limits,
        None,
        axis_y_log_scale,
        axis_y_limits,
        has_baryon_frac['value'],
    )

    subplot.set_xlabel(ut.plot.Label.get_label(mass_name))
    label = 'fraction with $M_{{\\rm {}}}$'.format(
        baryon_mass_name.replace('.mass', '').replace('.part', '')
    )
    subplot.set_ylabel(label, fontsize=30)

    colors = ut.plot.get_colors(len(hals))
    line_styles = ut.plot.get_line_styles(host_distance_bin_number)

    for hal_i, hal in enumerate(hals):
        for dist_i, host_distance_limits in enumerate(host_distance_limitss):
            label = None
            if host_distance_limits is not None and len(host_distance_limits) > 0:
                label = ut.plot.Label.get_label('host.distance.total', host_distance_limits)
            # if dist_i == 0:
            #    label = hal.info['simulation.name']

            pis = ut.array.get_indices(has_baryon_frac['number'][hal_i, dist_i], [1, Inf])
            subplot.plot(
                MassBin.mids[pis],
                has_baryon_frac['value'][hal_i, dist_i, pis],
                # frac_errs[hal_i, dist_i, :, pis],
                color=colors[hal_i],
                linestyle=line_styles[dist_i],
                label=label,
                alpha=0.7,
            )

    legend = subplot.legend(loc='best')
    legend.get_frame()

    if plot_file_name is True or plot_file_name == '':
        plot_file_name = 'has.{}.fraction_v_{}'.format(
            baryon_mass_name.replace('.part', ''), mass_name
        )
        plot_file_name += ut.plot.get_time_label('redshift', hals[0].snapshot)
    ut.plot.parse_output(plot_file_name, plot_directory)


# --------------------------------------------------------------------------------------------------
# number v distance
# --------------------------------------------------------------------------------------------------
def plot_number_v_distance(
    hals=None,
    gal=None,
    mass_name='mass',
    mass_limitss=[[]],
    distance_limits=[1, 1000],
    distance_bin_width=0.1,
    distance_log_scale=True,
    object_kind='halo',
    hal_indicess=None,
    gal_indices=None,
    gal_host_names=['MW', 'M31'],
    number_kind='sum',
    number_limits=None,
    number_log_scale=True,
    plot_file_name=False,
    plot_directory='.',
    figure_index=1,
):
    '''
    Plot mass function, that is, number (cumulative or differential) v mass_name.

    Parameters
    ----------
    hals : dict or list
        catalog[s] of halos at snapshot
    gal : dict
        catalog of galaxies to compare against
    mass_name : str
        halo mass kind to plot
    mass_limitss : list or list of lists
        min and max limits of halo mass
    distance_limits : list
        min and max distance from host [kpc physical]
    distance_bin_width : float
        width of distance bin
    distance_log_scale : bool
        whether to use logarithmic scaling for distance bins
    object_kind : str
        shortcut for halo kind to plot: 'halo', 'galaxy', 'cluster' and/or 'satellite', 'isolated'
    hal_indicess : array or list of arrays
        indices of halos to plot
    gal_indices : array
        indices of galaxies to plot
    gal_host_names : list
        names of hosts for observed galaxy catalog
    number_kind : str
         number kind to plot: 'sum', 'sum.cum', 'fraction', 'fraction.cum', 'density'
    number_limits : list
        min and max limits to impose on y-axis
    number_log_scale : bool
        whether to use logarithmic scaling for y axis
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory in which to write figure file
    figure_index : int
        index of figure for matplotlib
    '''
    dimension_number = 3

    if hals is None:
        hals = []
    if isinstance(hals, dict):
        hals = [hals]

    if mass_limitss is not None:
        mass_limitss = np.array(mass_limitss)
        if np.ndim(mass_limitss) == 1:
            mass_limitss = np.array([mass_limitss])
        mass_number = mass_limitss.shape[0]

    if not isinstance(hal_indicess, list):
        hal_indicess = [hal_indicess for _ in hals]

    DistanceBin = ut.binning.DistanceBinClass(
        distance_limits,
        distance_bin_width,
        include_max=True,
        log_scale=distance_log_scale,
        dimension_number=dimension_number,
    )

    hal_number = {}

    # get numbers for halos
    if hals is not None and len(hals) > 0:
        for hal_i, hal in enumerate(hals):
            if hal_indicess[hal_i] is None or len(hal_indicess[hal_i]) == 0:
                hal_indices = ut.array.get_arange(hal.prop(mass_name))
            else:
                hal_indices = hal_indicess[hal_i]

            hal_number_h = {}

            for _m_i, mass_limits in enumerate(mass_limitss):
                his_m = ut.array.get_indices(hal.prop(mass_name), mass_limits, hal_indices)
                his_m = hal.get_indices(object_kind=object_kind, prior_indices=his_m)

                hal_number_m = DistanceBin.get_sum_profile(hal.prop('host.distance.total', his_m))
                ut.array.append_dictionary(hal_number_h, hal_number_m)
            ut.array.append_dictionary(hal_number, hal_number_h)
        ut.array.arrayize_dictionary(hal_number)

    # get numbers for observed galaxies
    if gal is not None and mass_name in gal:
        gal_number = {}
        for gal_host_name in gal_host_names:
            # gis_h = gis[gal['host.name'][gis] == host_name.encode()]
            gis_h = ut.array.get_indices(gal['host.name'], gal_host_name.encode(), gal_indices)
            gal_number_h = {}
            for m_i, mass_limits in enumerate(mass_limitss):
                gis_m = ut.array.get_indices(gal[mass_name], mass_limits, gis_h)
                gal_number_m = DistanceBin.get_sum_profile(gal['host.distance.total'][gis_m])
                ut.array.append_dictionary(gal_number_h, gal_number_m)
            ut.array.append_dictionary(gal_number, gal_number_h)
        ut.array.arrayize_dictionary(gal_number)

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    if hals is not None and len(hals) > 0:
        numbers_all = hal_number[number_kind]
    elif gal is not None:
        numbers_all = gal_number[number_kind]

    ut.plot.set_axes_scaling_limits(
        subplot,
        distance_log_scale,
        distance_limits,
        None,
        number_log_scale,
        number_limits,
        numbers_all,
    )

    # if distance_log_scale:
    #    subplot.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.0f'))

    subplot.set_xlabel('distance $\\left[ {\\rm kpc} \\right]$')

    if '.cum' in number_kind:
        axis_y_label = '$N_{{\\rm satellite}}(< d)$'
    else:
        if distance_log_scale:
            axis_y_label = '${\\rm d}n/{\\rm d}log(d) \\, \\left[ {\\rm kpc^{-3}} \\right]$'
        else:
            axis_y_label = '${\\rm d}n/{\\rm d}d \\, \\left[ {\\rm kpc^{-2}} \\right]$'
    subplot.set_ylabel(axis_y_label)

    colors = ut.plot.get_colors(len(hals))
    line_styles = ut.plot.get_line_styles(mass_number)

    distance_kind = 'distance.mid'
    if '.cum' in number_kind:
        distance_kind = 'distance.cum'

    # plot observed galaxies
    host_label_dict = {
        'MW': {'color': 'black', 'linestyle': '--'},
        'M31': {'color': 'black', 'linestyle': ':'},
    }
    if gal is not None and mass_name in gal:
        for m_i, mass_limits in enumerate(mass_limitss):
            for host_i, host_name in enumerate(gal_host_names):
                label = host_name  # .replace('MW', 'Milky Way').replace('M31', 'M31 (Andromeda)')

                y_values = gal_number[number_kind][host_i, m_i]
                # ensure n = 1 is clear on log plot
                if 'sum' in number_kind and number_log_scale:
                    y_values = np.clip(y_values, 0.5, Inf)
                masks = np.where(y_values > -1)[0]

                subplot.plot(
                    gal_number[distance_kind][host_i, m_i][masks],
                    y_values[masks],
                    color=host_label_dict[host_name]['color'],
                    linestyle=host_label_dict[host_name]['linestyle'],
                    linewidth=3.0,
                    alpha=0.8,
                    label=label,
                )

    # plot halos
    if hals is not None and len(hals) > 0:
        for hal_i, hal in enumerate(hals):
            for m_i, _mass_limits in enumerate(mass_limitss):
                linewidth = 3.0
                alpha = 0.9
                color = colors[hal_i]

                label = None
                if m_i == 0:
                    label = hal.info['simulation.name']
                    # label = 'Latte simulation'

                y_values = hal_number[number_kind][hal_i, m_i]
                # ensure n = 1 is clear on log plot
                if 'sum' in number_kind and number_log_scale:
                    y_values = np.clip(y_values, 0.5, Inf)

                # if '57000' in hal.info['simulation.name']:
                #    #label = 'Latte low-res'
                #    label = None
                #    linewidth = 1.5
                #    #if 'star.mass' in mass_name_default:
                #    #    y_values[x_values < 3e7] = np.nan
                #    #elif 'star.vel.std' in mass_name_default:
                #    #    y_values[x_values < 9] = np.nan
                #    #color = colors[0]
                #    color = ut.plot.get_color('blue.lite')

                masks = np.where(y_values > -1)[0]
                subplot.plot(
                    hal_number[distance_kind][hal_i, m_i][masks],
                    y_values[masks],
                    color=color,
                    linestyle=line_styles[m_i],
                    linewidth=linewidth,
                    alpha=alpha,
                    label=label,
                )

    if len(hals) > 1 or gal is not None:
        legend = subplot.legend(loc='best')
        legend.get_frame()

    if plot_file_name is True or plot_file_name == '':
        galaxy_label = ''
        if gal is not None:
            galaxy_label = '_lg'
        redshift_label = ''
        if len(hals) > 0:
            redshift_label = ut.plot.get_time_label('redshift', hals[0].snapshot)
        plot_file_name = f'number.{number_kind}_v_distance{galaxy_label}{redshift_label}'
    ut.plot.parse_output(plot_file_name, plot_directory)


# --------------------------------------------------------------------------------------------------
# properties
# --------------------------------------------------------------------------------------------------
def plot_property_v_property(
    hals=None,
    gal=None,
    x_property_name='mass.bound',
    x_property_limits=None,
    x_property_log_scale=True,
    y_property_name='star.mass',
    y_property_limits=None,
    y_property_log_scale=True,
    host_distance_limitss=None,
    near_halo_distance_limits=None,
    hal_indicess=None,
    plot_histogram=False,
    property_bin_number=200,
    plot_file_name=False,
    plot_directory='.',
    figure_index=1,
):
    '''
    Plot property v property.

    Parameters
    ----------
    hals : dict
        catalog[s] of halos at snapshot
    gal : dict
        catalog of galaxies
    x_property_name : str
        name of property for x-axis
    x_property_limits : list
        min and max limits to impose on x_property_name
    x_property_log_scale : bool
        whether to use logarithmic scaling for x axis
    y_property_name : str
        name of property for y-axis
    y_property_limits : list
        min and max limits to impose on y_property_name
    y_property_log_scale : bool
        whether to use logarithmic scaling for y axis
    host_distance_limitss : list
        min and max limits for distance from galaxy
    near_halo_distance_limits : list
        distance to nearest halo [d / R_neig]
    hal_indicess : array or list of arrays
    plot_histogram : bool
        whether to plot 2-D histogram instead of individual points
    property_bin_number : int
        number of bins along each axis (if histogram)
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory in which to write figure file
    figure_index : int
        ndex of figure for matplotlib
    '''

    def _get_label_distance(cat, distance_limits):
        '''
        .
        '''
        if 'halo' in cat.info['catalog.kind']:
            label = 'simulated'
        elif 'galaxy' in cat.info['catalog.kind']:
            label = 'observed'
        elif 'group' in cat.info['catalog.kind']:
            return None

        if np.max(distance_limits) < 400:
            label += ' satellite'
        elif np.min(distance_limits) > 100:
            label += ' isolated'

        return label

    Say = ut.io.SayClass(plot_property_v_property)

    if hals is None:
        hals = []
    elif isinstance(hals, dict):
        hals = [hals]

    if host_distance_limitss is not None:
        host_distance_limitss = np.array(host_distance_limitss)
        if np.ndim(host_distance_limitss) == 1:
            host_distance_limitss = np.array([host_distance_limitss])
        host_distance_bin_number = host_distance_limitss.shape[0]
    else:
        host_distance_bin_number = 1
        host_distance_limitss = [None]

    if not isinstance(hal_indicess, list):
        hal_indicess = [hal_indicess]

    x_property_values = []
    y_property_values = []

    for hal_i, hal in enumerate(hals):
        his = hal_indicess[hal_i]
        if his is None:
            his = ut.array.get_arange(hal['mass'])

        if near_halo_distance_limits is not None:
            his = ut.array.get_indices(
                hal['nearest.distance/Rneig'], near_halo_distance_limits, his
            )

        x_prop_vals_h = []
        y_prop_vals_h = []

        for host_distance_limits in host_distance_limitss:
            if host_distance_limits is not None and len(host_distance_limits) > 0:
                his_d = ut.array.get_indices(
                    hal.prop('host.distance.total'), host_distance_limits, his
                )
            else:
                his_d = his

            x_prop_vals_d = hal.prop(x_property_name, his_d)
            y_prop_vals_d = hal.prop(y_property_name, his_d)
            # if 'metallicity' in y_property_name:
            #    y_prop_vals_d = ut.math.get_log(y_prop_vals_d)

            Say.say(
                '{} range = [{:.3e}, {:.3e}], med = {:.3e}'.format(
                    x_property_name,
                    x_prop_vals_d.min(),
                    x_prop_vals_d.max(),
                    np.median(x_prop_vals_d),
                )
            )
            Say.say(
                '{} range = [{:.3e}, {:.3e}], med = {:.3e}'.format(
                    y_property_name,
                    y_prop_vals_d.min(),
                    y_prop_vals_d.max(),
                    np.median(y_prop_vals_d),
                )
            )

            # if ('gas.mass' in y_property_name and 'star.mass' in y_property_name and
            #'/' in y_property_name):
            #    y_prop_vals_d = y_prop_vals_d.clip(1.2e-4, Inf)

            if x_property_limits:
                indices = ut.array.get_indices(x_prop_vals_d, x_property_limits)
                x_prop_vals_d = x_prop_vals_d[indices]
                y_prop_vals_d = y_prop_vals_d[indices]

            if y_property_limits:
                indices = ut.array.get_indices(y_prop_vals_d, y_property_limits)
                x_prop_vals_d = x_prop_vals_d[indices]
                y_prop_vals_d = y_prop_vals_d[indices]

            if len(x_prop_vals_d) == 0 or len(y_prop_vals_d) == 0:
                Say.say('! no halos in bin')
                return

            # print(his_d[indices])

            x_prop_vals_h.append(x_prop_vals_d)
            y_prop_vals_h.append(y_prop_vals_d)

        x_property_values.append(x_prop_vals_h)
        y_property_values.append(y_prop_vals_h)

    x_property_values = np.array(x_property_values)
    y_property_values = np.array(y_property_values)

    gal_x_property_values = []
    gal_y_property_values = []

    if gal is not None:
        # compile observed galaxies
        gal_x_property_name = x_property_name.replace('.part', '')
        gal_y_property_name = y_property_name.replace('.part', '')
        gis_m = ut.array.get_indices(gal[gal_x_property_name], x_property_limits)
        for dist_i, host_distance_limits in enumerate(host_distance_limitss):
            gis_d = ut.array.get_indices(gal['host.distance.total'], host_distance_limits, gis_m)
            # gis_d = gis[gal['host.name'][gis] == b'MW']

            gal_x_property_values.append(gal.prop(gal_x_property_name, gis_d))
            gal_y_property_values.append(gal.prop(gal_y_property_name, gis_d))

        gal_x_property_values = np.array(gal_x_property_values)
        gal_y_property_values = np.array(gal_y_property_values)

    if len(hals) > 1:
        colors = ut.plot.get_colors(len(hals))
    else:
        colors = ut.plot.get_colors(max(host_distance_bin_number, 2))

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    axis_x_limits, axis_y_limits = ut.plot.set_axes_scaling_limits(
        subplot,
        x_property_log_scale,
        x_property_limits,
        x_property_values,
        y_property_log_scale,
        y_property_limits,
        y_property_values,
    )

    axis_x_label = ut.plot.Label.get_label(x_property_name)
    subplot.set_xlabel(axis_x_label)
    axis_y_label = ut.plot.Label.get_label(y_property_name)
    subplot.set_ylabel(axis_y_label, fontsize=30)

    label = None

    if plot_histogram:
        # plot histogram
        for hal_i, hal in enumerate(hals):
            for dist_i, host_distance_limits in enumerate(host_distance_limitss):
                if x_property_log_scale:
                    x_property_values[hal_i, dist_i] = ut.math.get_log(
                        x_property_values[hal_i, dist_i]
                    )

                if y_property_log_scale:
                    y_property_values[hal_i, dist_i] = ut.math.get_log(
                        y_property_values[hal_i, dist_i]
                    )

                if host_distance_limits is not None and len(host_distance_limits) > 0:
                    label = ut.plot.Label.get_label('host.distance.total', host_distance_limits)

            valuess, _xs, _ys = np.histogram2d(
                x_property_values[hal_i, dist_i],
                y_property_values[hal_i, dist_i],
                property_bin_number,
            )
            # norm=LogNorm()

            subplot.imshow(
                valuess.transpose(),
                # norm=LogNorm(),
                cmap=plt.cm.YlOrBr,  # pylint: disable=no-member
                aspect='auto',
                # interpolation='nearest',
                interpolation='none',
                extent=(axis_x_limits[0], axis_x_limits[1], axis_y_limits[0], axis_y_limits[1]),
                vmin=np.min(valuess),
                vmax=np.max(valuess),
                label=label,
            )

        # plt.colorbar()

    else:
        # plot galaxies as individual points

        # plot observed galaxies
        if gal is not None:
            alpha = 0.5
            if hals is None or len(hals) == 0:
                alpha = 0.7
            for dist_i, host_distance_limits in enumerate(host_distance_limitss):
                if host_distance_limits is not None and len(host_distance_limits) > 0:
                    # label = ut.plot.get_label_distance(
                    #       'host.distance.total', host_distance_limits)
                    label = _get_label_distance(gal, host_distance_limits)

                subplot.plot(
                    gal_x_property_values[dist_i],
                    gal_y_property_values[dist_i],
                    '*',
                    color=colors[dist_i],
                    markersize=12,
                    alpha=alpha,
                    label=label,
                )

        if (
            'mass' in x_property_name
            and 'star.mass' in y_property_name
            and '/' not in y_property_name
        ):
            # subplot.plot([1e1, 1e14], [1e1, 1e14], ':', color='black', linewidth=2, alpha=0.3)
            # subplot.plot([1e1, 1e14], [1e-1, 1e12], '--', color='black', linewidth=2, alpha=0.2)
            mass_peaks = 10 ** np.arange(1, 12, 0.1)
            mstars_from_mpeaks = 3e6 * (mass_peaks / 1e10) ** 1.92
            subplot.plot(
                mass_peaks, mstars_from_mpeaks, '--', color='black', linewidth=2, alpha=0.3
            )

        # """
        if 'star.mass' in x_property_name and 'metallicity' in y_property_name:
            # subplot.plot(metal_fire['star.mass'], metal_fire['star.metallicity'], 'o',
            #             color='gray', markersize=8, alpha=0.5, label='FIRE isolated')

            for k in ['MW', 'M31', 'isolated']:
                if k == 'MW':
                    color = colors[0]
                    label = 'observed satellite'
                elif k == 'M31':
                    color = colors[0]
                    label = None
                else:
                    color = colors[1]
                    label = 'observed isolated'

                subplot.plot(
                    metallicity_kirby['star.mass'][k],
                    metallicity_kirby['star.metallicity'][k],
                    '*',
                    color=color,
                    markersize=6,
                    alpha=0.5,
                    label=label,
                )

        # """

        # plot simulated galaxies
        markers = ['.', '.']
        # marker_sizes = [22, 7]
        marker_sizes = [3, 3]
        for hal_i, hal in enumerate(hals):
            if len(hals) > 1:
                label = hal.info['simulation.name']
                color = colors[hal_i]

            for dist_i, host_distance_limits in enumerate(host_distance_limitss):
                if (
                    len(hals) == 1
                    and host_distance_limits is not None
                    and len(host_distance_limits) > 1
                ):
                    # label = ut.plot.get_label_distance(
                    #       'host.distance.total', host_distance_limits)
                    label = _get_label_distance(hal, host_distance_limits)
                    color = colors[dist_i]

                subplot.plot(
                    x_property_values[hal_i, dist_i],
                    y_property_values[hal_i, dist_i],
                    markers[hal_i],
                    color=color,
                    markersize=marker_sizes[hal_i],
                    alpha=0.8,
                    label=label,
                )

    if label is not None:
        legend = subplot.legend(loc='best')
        legend.get_frame()

    if plot_file_name is True or plot_file_name == '':
        plot_file_name = y_property_name + '_v_' + x_property_name
        if hals is None and gal is not None:
            plot_file_name += '_lg'
        if hals is not None and len(hals) > 0:
            plot_file_name += ut.plot.get_time_label('redshift', hals[0].snapshot)
        else:
            plot_file_name = plot_file_name.replace('.part', '')
    ut.plot.parse_output(plot_file_name, plot_directory)


def plot_property_v_distance(
    hals=None,
    mass_name='mass',
    mass_limitss=[[]],
    distance_limits=[0, 400],
    distance_bin_width=1,
    distance_log_scale=False,
    property_name='host.velocity.tan',
    property_statistic='median',
    property_limits=None,
    property_log_scale=False,
    object_kind='halo',
    hal_indicess=None,
    plot_file_name=False,
    plot_directory='.',
    figure_index=1,
):
    '''
    Plot property v distance, in bins of mass_name.

    Parameters
    ----------
    hals : dict or list
        catalog[s] of halos at snapshot
    mass_name : str
        halo mass kind to plot
    mass_limitss : list or list of lists
        min and max limits of halo mass
    distance_limits : list
        min and max distance from host [kpc physical]
    distance_bin_width : float
        width of distance bin
    distance_log_scale : bool
        whether to use logarithmic scaling for distance bins
    property_name : str
        name of property to plot
    property_statistic : str
        statistic of property to plot
    property_limits : list
        min and max limits to show property on y-axis
    property_log_scale : bool
        whether to use logarithmic scaling for property on y-axis
    object_kind : str
        shortcut for halo kind to plot: 'halo', 'galaxy', 'cluster' and/or 'satellite', 'isolated'
    hal_indicess : array or list of arrays
        indices of halos to plot
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory in which to write figure file
    figure_index : int
        index of figure for matplotlib
    '''
    dimension_number = 3

    if hals is None:
        hals = []
    if isinstance(hals, dict):
        hals = [hals]

    if mass_limitss is not None:
        mass_limitss = np.array(mass_limitss)
        if np.ndim(mass_limitss) == 1:
            mass_limitss = np.array([mass_limitss])
        mass_number = mass_limitss.shape[0]

    if not isinstance(hal_indicess, list):
        hal_indicess = [hal_indicess for _ in hals]

    DistanceBin = ut.binning.DistanceBinClass(
        distance_limits,
        distance_bin_width,
        include_max=True,
        log_scale=distance_log_scale,
        dimension_number=dimension_number,
    )

    hal_stat = {}

    # get statistics for halos
    if hals is not None and len(hals) > 0:
        for hal_i, hal in enumerate(hals):
            if hal_indicess[hal_i] is None or len(hal_indicess[hal_i]) == 0:
                hal_indices = ut.array.get_arange(hal.prop(mass_name))
            else:
                hal_indices = hal_indicess[hal_i]

            hal_stat_h = {}

            for _m_i, mass_limits in enumerate(mass_limitss):
                his_m = ut.array.get_indices(hal.prop(mass_name), mass_limits, hal_indices)
                his_m = hal.get_indices(object_kind=object_kind, prior_indices=his_m)

                hal_stat_m = DistanceBin.get_statistics_profile(
                    hal.prop('host.distance.total', his_m), hal.prop(property_name, his_m)
                )
                ut.array.append_dictionary(hal_stat_h, hal_stat_m)
            ut.array.append_dictionary(hal_stat, hal_stat_h)
        # ut.array.arrayize_dictionary(hal_stat)

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    ut.plot.set_axes_scaling_limits(
        subplot, distance_log_scale, distance_limits, None, property_log_scale, property_limits
    )

    subplot.set_xlabel('distance $\\left[ {\\rm kpc} \\right]$')
    subplot.set_ylabel(property_name)
    # subplot.set_ylabel('$V_{tan} / ( \sqrt{2} V_{rad} )$')

    colors = ut.plot.get_colors(len(hals))
    line_styles = ut.plot.get_line_styles(mass_number)

    # plot halos
    if hals is not None and len(hals) > 0:
        for hal_i, hal in enumerate(hals):
            for m_i, _mass_limits in enumerate(mass_limitss):
                linewidth = 3.0
                alpha = 0.9
                color = colors[hal_i]

                label = hal.info['simulation.name']
                print(label)

                subplot.plot(
                    hal_stat['distance.mid'][hal_i][m_i],
                    hal_stat[property_statistic][hal_i][m_i],
                    color=color,
                    linestyle=line_styles[m_i],
                    linewidth=linewidth,
                    alpha=alpha,
                    label=label,
                )

    if len(hals) > 1:
        legend = subplot.legend(loc='best')
        legend.get_frame()

    if plot_file_name is True or plot_file_name == '':
        redshift_label = ''
        if len(hals) > 0:
            redshift_label = ut.plot.get_time_label('redshift', hals[0].snapshot)
        plot_file_name = f'{property_name}.{property_statistic}_v_distance{redshift_label}'
    ut.plot.parse_output(plot_file_name, plot_directory)


def plot_quiescent_fraction_v_mass(
    gal,
    mass_name='star.mass',
    mass_limits=[1e5, 1e10],
    mass_width=1.0,
    qufrac_limits=[-0.005, 1.005],
    distance_max=300,
    gas_mass_ratio_qu=0.1,
    plot_file_name=False,
    plot_directory='.',
):
    '''
    Plot quiescent fraction v mass_name.

    Parameters
    ----------
    gal : dict
        catalog of galaxies in the Local Group
    mass_name : str
        galaxy mass kind
    mass_limits : list
        min and max limits for mass_name
    mass_width : float
        width of mass bin
    qufrac_limits : list
        min and max limits for quiescent fraction
    distance_max : float
        maximum distance from host [kpc physical]
    gas_mass_ratio_qu : float
        maximum ratio of gas.mass / star.mass to be quiescent
    file_name : str
        name of plot file to write
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory to write figure file
    '''
    mass_log_scale = True

    # get quiescent fraction in Local Group
    MassBin = ut.binning.BinClass(mass_limits, mass_width, log_scale=mass_log_scale)
    QuFracLG = ut.math.FractionClass(MassBin.number, uncertainty_kind='beta')

    gis = ut.array.get_indices(gal[mass_name], mass_limits)
    gis = ut.array.get_indices(gal['host.distance.total'], [0, distance_max], gis)

    for mi in range(MassBin.number):
        mass_bin_limits = MassBin.get_bin_limits(mi)
        gis_m = ut.array.get_indices(gal[mass_name], mass_bin_limits, gis)
        gis_m_qu = ut.array.get_indices(gal.prop('gas.mass.ratio'), [0, gas_mass_ratio_qu], gis_m)
        QuFracLG.assign_to_dict(mi, gis_m_qu.size, gis_m.size)

    print(QuFracLG['denom'])
    print(QuFracLG['numer'])
    print(QuFracLG['value'])

    qufrac = {}

    qufrac['saga'] = {
        'star.mass': 10 ** np.array([6.78, 7.39, 7.73, 7.97, 8.14, 8.57, 9.11]),
        'mean': [0.05, 0.22, 0.22, 0.22, 0.17, 0.06, 0.05],
        '84': [0.13, 0.32, 0.32, 0.32, 0.26, 0.13, 0.12],
        '16': [0, 0.12, 0.12, 0.12, 0.07, 0, 0],
        '100': [0.65, 0.49, 0.43, 0.36, 0.29, 0.15, 0.13],
    }

    # simulations
    qufrac['fire'] = {
        'star.mass': 10 ** np.array([5.24, 5.74, 6.24, 6.74, 7.24, 7.74, 8.24, 8.74, 9.24]),
        'mean': [1.0, 1.0, 1.0, 1.0, 0.81, 0.438, 0.375, 0.0, 0.0],  # mean across each host
        #'mean': [1.0, 1.0, 1.0, 1.0, 0.81, 0.3125, 0.3125, 0.0, 0.0], # from 2021-12-19
        'median': [1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        'std': [0.0, 0.0, 0.0, 0.0, 0.328, 0.464, 0.415, 0.0, 0.0],
        '16': [1.0, 1.0, 1.0, 1.0, 0.584, 0.0, 0.0, 0.0, 0.0],
        '84': [1.0, 1.0, 1.0, 1.0, 1.0, 0.94, 0.94, 0.0, 0.0],
        'min': [1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'max': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0],
    }

    # smaller bins
    qufrac['fire'] = {
        'star.mass': 10 ** np.array([5.5, 6.5, 7.5, 8.5, 9.5]),
        'mean': [1.0, 1.0, 0.61796537, 0.18181818, 0.0],  # mean across each host
        'median': [1.0, 1.0, 0.71428571, 0.0, 0.0],
        '16': [1.0, 1.0, 0.2, 0.0, 0.0],
        '84': [1.0, 1.0, 1.0, 0.5, 0.0],
    }

    # Akins et al
    qufrac['changa'] = {
        'star.mass': np.array([3.16e5, 3.16e6, 3.16e7, 3.16e8, 3.16e9]),
        'mean': [1.0, 0.899, 0.697, 0.125, 0.002],
        '84': [1, 1, 0.697, 0.398, 0.335],  # computed via standard deviation
        '16': [0.867, 0.79, 0.26, 0, 0],
    }

    qufrac['auriga'] = {
        'star.mass': 10 ** np.array([6.47, 7.41, 8.34, 9.28, 10.22]),
        'mean': [0.929, 0.617, 0.175, 0, 0],
        '84': [0.945, 0.659, 0.227, 0.033, 0.100],
        '16': [0.907, 0.573, 0.132, 0, 0],
    }

    qufrac['apostle'] = {
        'star.mass': 10 ** np.array([6.47, 7.41, 8.34, 9.28, 10.22]),
        'mean': [0.978, 0.688, 0.304, 0.063, 0],
        '84': [0.987, 0.750, 0.407, 0.152, 0.167],
        '16': [0.961, 0.617, 0.218, 0.024, 0],
    }

    for sim_name, sim_value in qufrac.items():
        for prop_name in qufrac[sim_name]:
            sim_value[prop_name] = np.asarray(sim_value[prop_name])

    # plot ----------
    _fig, subplot = ut.plot.make_figure()

    ut.plot.set_axes_scaling_limits(subplot, True, mass_limits, y_limits=qufrac_limits)

    subplot.yaxis.set_minor_locator(ticker.AutoMinorLocator(4))

    subplot.set_xlabel('satellite stellar mass [${{\\rm M}}_\\odot$]', fontsize=22)
    subplot.set_ylabel('satellite quiescent fraction', fontsize=21)

    # color blind friendly
    colors = [
        (0.99, 0.26, 0),  # red
        (0.9, 0.62, 0),  # orange
        (0, 0.62, 0.45),  # green
        (0, 0.44, 0.69),  # blue
    ]

    # simulations
    simulation_name = 'fire'
    subplot.fill_between(
        qufrac[simulation_name]['star.mass'],
        qufrac[simulation_name]['16'],
        qufrac[simulation_name]['84'],
        # qufrac[simulation_name]['mean'] + qufrac[simulation_name]['std'],
        # qufrac[simulation_name]['mean'] - qufrac[simulation_name]['std'],
        alpha=0.2,
        color=colors[0],
        linestyle='solid',
        edgecolor=None,
    )
    subplot.plot(
        qufrac[simulation_name]['star.mass'],
        qufrac[simulation_name]['mean'],
        alpha=0.8,
        color=colors[0],
        label='FIRE:Latte+ELVIS',
    )

    simulation_name = 'changa'
    subplot.fill_between(
        qufrac[simulation_name]['star.mass'],
        qufrac[simulation_name]['16'],
        qufrac[simulation_name]['84'],
        alpha=0.2,
        color=colors[1],
        edgecolor=None,
    )
    subplot.plot(
        qufrac[simulation_name]['star.mass'],
        qufrac[simulation_name]['mean'],
        alpha=0.8,
        color=colors[1],
        linestyle='dashed',
        label='CHANGA:DCJL',
    )

    simulation_name = 'auriga'
    subplot.fill_between(
        qufrac[simulation_name]['star.mass'],
        qufrac[simulation_name]['16'],
        qufrac[simulation_name]['84'],
        alpha=0.2,
        color=colors[2],
        edgecolor=None,
    )
    subplot.plot(
        qufrac[simulation_name]['star.mass'],
        qufrac[simulation_name]['mean'],
        alpha=0.8,
        color=colors[2],
        linestyle='dotted',
        label='Auriga',
    )

    simulation_name = 'apostle'
    subplot.fill_between(
        qufrac[simulation_name]['star.mass'],
        qufrac[simulation_name]['16'],
        qufrac[simulation_name]['84'],
        alpha=0.2,
        color=colors[3],
        edgecolor=None,
    )
    subplot.plot(
        qufrac[simulation_name]['star.mass'],
        qufrac[simulation_name]['mean'],
        alpha=0.8,
        color=colors[3],
        linestyle='dashdot',
        label='APOSTLE',
    )

    # observations
    subplot.errorbar(
        MassBin.mids,
        QuFracLG['value'],
        QuFracLG['error'].transpose(),
        color='black',
        marker='s',
        markersize=8,
        alpha=0.8,
        linestyle='',
        label='MW+M31',
    )

    subplot.errorbar(
        qufrac['saga'][mass_name],
        qufrac['saga']['mean'],
        [
            qufrac['saga']['mean'] - qufrac['saga']['mean'],
            qufrac['saga']['100'] - qufrac['saga']['mean'],
        ],
        color='darkblue',
        marker='',
        markersize=8,
        alpha=0.4,
        linestyle='',
    )

    subplot.errorbar(
        qufrac['saga'][mass_name],
        qufrac['saga']['mean'],
        [
            qufrac['saga']['mean'] - qufrac['saga']['16'],
            qufrac['saga']['84'] - qufrac['saga']['mean'],
        ],
        color='darkblue',
        marker='o',
        markersize=8,
        alpha=0.8,
        linestyle='',
        label='SAGA',
    )

    ut.plot.make_legends(subplot, location='lower left', fontsize=10)

    if plot_file_name is True or plot_file_name == '':
        plot_file_name = f'qu.frac_v_{mass_name}'
    ut.plot.parse_output(plot_file_name, plot_directory, dpi=600)


# --------------------------------------------------------------------------------------------------
# observations
# --------------------------------------------------------------------------------------------------
metallicity_kirby = {
    # stellar metallicity [Fe/H] from Kirby et al 2013
    'star.mass': {
        'MW': 10
        ** np.array(
            [
                7.39,
                6.69,
                6.59,
                6.07,
                5.84,
                5.73,
                5.51,
                5.48,
                4.57,
                4.28,
                3.93,
                3.90,
                3.73,
                3.68,
                3.14,
            ]
        ),
        'isolated': 10 ** np.array([8.01, 7.92, 6.92, 6.82, 6.47, 6.15, 5.13]),
        'M31': 10
        ** np.array([8.67, 7.83, 8.00, 7.17, 6.96, 6.88, 6.26, 5.79, 5.90, 5.89, 5.58, 5.38, 5.15]),
    },
    'star.mass.err': {
        # uncertainty in log Mstar (in dex)
        'MW': np.array(
            [0.14, 0.13, 0.21, 0.13, 0.2, 0.2, 0.1, 0.09, 0.14, 0.13, 0.15, 0.2, 0.23, 0.22, 0.13]
        ),
        'isolated': np.array([0.09, 0.06, 0.08, 0.08, 0.09, 0.05, 0.2]),
        'M31': np.array(
            [0.05, 0.05, 0.05, 0.13, 0.08, 0.05, 0.12, 0.09, 0.3, 0.16, 0.3, 0.44, 0.4]
        ),
    },
    'star.metallicity': {
        'MW': -1
        * np.array(
            [
                1.04,
                1.45,
                1.68,
                1.63,
                1.94,
                2.13,
                1.98,
                1.91,
                2.39,
                2.1,
                2.45,
                2.12,
                2.18,
                2.25,
                2.14,
            ]
        ),
        'isolated': -1 * np.array([1.19, 1.05, 1.43, 1.39, 1.58, 1.44, 1.74]),
        'M31': -1
        * np.array([0.92, 1.12, 0.83, 1.62, 1.47, 1.33, 1.84, 1.94, 1.35, 1.70, 2.21, 1.93, 2.46]),
    },
    'star.metallicity.err': {
        'MW': np.array(
            [
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.01,
                0.04,
                0.03,
                0.07,
                0.05,
                0.05,
                0.04,
                0.05,
            ]
        ),
        'isolated': np.array([0.01, 0.01, 0.02, 0.01, 0.02, 0.03, 0.04]),
        'M31': np.array([0.13, 0.36, 0.25, 0.21, 0.37, 0.17, 0.05, 0.18, 0.2, 0.2, 0.01, 0.2, 0.2]),
    },
}

# stellar metallicity from SDSS (Gallazzi et al 2005), in Z / Z_solar
metallicity_gallazzi = {
    'star.mass': 10
    ** np.array(
        [
            8.91,
            9.11,
            9.31,
            9.51,
            9.72,
            9.91,
            10.11,
            10.31,
            10.51,
            10.72,
            10.91,
            11.11,
            11.31,
            11.51,
            11.72,
            11.91,
        ]
    ),
    'percent.50': -1
    * np.array(
        [
            0.60,
            0.61,
            0.65,
            0.61,
            0.52,
            0.41,
            0.23,
            0.11,
            0.01,
            0.04,
            0.07,
            0.10,
            0.12,
            0.13,
            0.14,
            0.15,
        ]
    ),
    'percent.16': -1
    * np.array(
        [
            1.11,
            1.07,
            1.10,
            1.03,
            0.97,
            0.9,
            0.8,
            0.65,
            0.41,
            0.24,
            0.14,
            0.09,
            0.06,
            0.04,
            0.03,
            0.03,
        ]
    ),
    'percent.84': np.array(
        [0, 0, -0.05, -0.01, 0.05, 0.09, 0.14, 0.17, 0.2, 0.22, 0.24, 0.25, 0.26, 0.28, 0.29, 0.3]
    ),
}

metallicity_fire = {
    # stellar and gas metallicity [total/Solar] from Ma et al 2015
    # for stars, they find [Fe/H] = log(Z_tot/Z_sun) - 0.2. these already include this conversion
    'star.mass': 10
    ** np.array(
        [
            10.446,
            4.615,
            6.359,
            7.075,
            6.119,
            9.374,
            8.174,
            8.401,
            8.337,
            9.611,
            10.3178,
            10.779,
            9.274,
            9.367,
            11.135,
        ]
    ),
    'star.metallicity': 10
    ** np.array(
        [
            0.219,
            -2.859,
            -1.886,
            -1.384,
            -1.829,
            -0.731,
            -1.309,
            -1.025,
            -1.163,
            -0.686,
            -0.157,
            0.114,
            -0.614,
            -0.604,
            0.133,
        ]
    ),
    'gas.metallicity': 10
    ** np.array(
        [
            0.250,
            -3.299,
            -1.157,
            -0.969,
            -1.580,
            -0.370,
            -1.092,
            -0.611,
            -0.800,
            -0.415,
            -0.183,
            0.137,
            -0.183,
            -0.347,
            0.371,
        ]
    ),
}


# --------------------------------------------------------------------------------------------------
# diagnostic
# --------------------------------------------------------------------------------------------------
def test_host_in_catalog_v_tree(hals, halt, host_rank=0):
    '''
    Test differences in primary host assignment between halo catalogs and halo merger trees.
    '''
    host_name = ut.catalog.get_host_name(host_rank)

    for hal in hals:
        if len(hal) > 0 and len(hal['mass']) > 0:
            # get real (non-phantom) halos at this snapshot in trees
            halt_indices = np.where(
                (halt['am.phantom'] == 0) * (halt['snapshot'] == hal.snapshot['index'])
            )[0]
            if halt_indices.size:
                halt_host_index = halt[host_name + 'index'][halt_indices[0]]
                hal_host_index_halt = halt['catalog.index'][halt_host_index]
                hal_host_index = hal[host_name + 'index'][0]
                if hal_host_index_halt != hal_host_index:
                    print(
                        'snapshot {}: {} has {:.3e}, {} has {:.3e}'.format(
                            hal.snapshot['index'],
                            halt_host_index,
                            halt['mass'][halt_host_index],
                            hal_host_index,
                            hal['mass'][hal_host_index],
                        )
                    )


def test_halo_jump(
    halt,
    jump_prop_name='position',
    jump_prop_value=100,
    select_prop_name='vel.circ.max',
    select_prop_limits=None,
):
    '''
    Test jumps in halo properties across adjacent snapshots in halo merger trees.
    '''
    Say = ut.io.SayClass(test_halo_jump)

    snapshot_index_max = halt['snapshot'].max()
    snapshot_index_min = halt['snapshot'].min()
    snapshot_indices = np.arange(snapshot_index_min + 1, snapshot_index_max + 1)

    Say.say(f'halo tree progenitor -> child {jump_prop_name} jump > {jump_prop_value}')

    jump_number = 0
    total_number = 0

    for snapshot_index in snapshot_indices:
        hindices = np.where(halt['snapshot'] == snapshot_index)[0]
        if select_prop_name and select_prop_limits is not None and len(select_prop_limits) > 0:
            hindices = ut.array.get_indices(halt[select_prop_name], select_prop_limits, hindices)
        desc_hindices = hindices[np.where(halt['progenitor.main.index'][hindices] >= 0)[0]]
        prog_hindices = halt['progenitor.main.index'][desc_hindices]

        if jump_prop_name == 'position':
            # position difference [kpc comoving]
            position_difs = ut.coordinate.get_distances(
                halt['position'][prog_hindices],
                halt['position'][desc_hindices],
                halt.info['box.length'],
                total_distance=True,
            )
            hiis_jump = np.where(position_difs > jump_prop_value)[0]
        elif jump_prop_name in ['vel.circ.max', 'mass']:
            # V_c,max or mass jump
            prop_ratios = halt[jump_prop_name][desc_hindices] / halt[jump_prop_name][prog_hindices]
            hiis_jump = np.where(prop_ratios > jump_prop_value)[0]
            # hiis_jump = np.where(velcircmax_ratios < 1 / jump_value)[0]
            # hiis_jump = np.logical_or(
            #    velcircmax_ratios > jump_value, velcircmax_ratios < (1 / jump_value))

        total_number += prog_hindices.size

        if hiis_jump.size:
            Say.say(
                'snapshot {:3d} to {:3d}:  {} (of {})'.format(
                    snapshot_index, snapshot_index + 1, hiis_jump.size, desc_hindices.size
                )
            )

            jump_number += hiis_jump.size

            # print(desc_hindices[hiis_jump])

            # check how many descendants skip a snapshot
            prog_snapshot_indices = halt['snapshot'][prog_hindices[hiis_jump]]
            hiis_skip_snapshot = np.where(prog_snapshot_indices != snapshot_index - 1)[0]
            if hiis_skip_snapshot.size:
                Say.say(f'  {hiis_skip_snapshot.size} descendants skip a snapshot')

        Say.say(f'across all snapshots:  {jump_number} (of {total_number})')
