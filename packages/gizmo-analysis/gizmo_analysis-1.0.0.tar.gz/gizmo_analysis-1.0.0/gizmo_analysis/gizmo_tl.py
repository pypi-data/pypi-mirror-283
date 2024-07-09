'''
Analysis for m12i_r880 'triple latte' release paper.

@author: Andrew Wetzel <arwetzel@gmail.com>


'''

# import collections
import numpy as np
from numpy import Inf
from matplotlib import pyplot as plt
from matplotlib import ticker
from matplotlib import colors

import utilities as ut


# --------------------------------------------------------------------------------------------------
# visualize
# --------------------------------------------------------------------------------------------------
class ImageClass(ut.io.SayClass):
    '''
    Plot 2-D image[s], save values, write to file.
    '''

    def __init__(self):
        '''
        .
        '''
        self.histogram_valuess = None
        self.histogram_xs = None
        self.histogram_ys = None
        self.plot_file_name = None

    def plot_image_simple(
        self,
        part,
        species_name='star',
        weight_name='mass',
        dimensions_plot=[0, 1, 2],
        distance_max=20,
        distance_bin_width=0.1,
        rotation=True,
        host_index=0,
        part_indices=None,
        image_limits=[None, None],
        plot_file=False,
    ):
        '''
        Plot image of the positions of given partcle species, using either a single panel for
        2 dimensions or 3 panels for all 2-dimensional combinations.

        Parameters
        ----------
        part : dict
            catalog of particles at snapshot
        species_name : str
            name of particle species to plot
        weight_name : str
            property to weight positions by
        dimensions_plot : list
            dimensions to plot - if length 2, plot one v one; if length 3, plot all via 3 panels
        distance_max : float or array
            distance from center to plot [kpc]
        distance_bin_width : float
            size of pixel [kpc]
        rotation : bool or array
            whether to rotate particles
            if True, will rotate to align with principal axes defined by input species
        host_index : int
            index of host halo to get position and rotation of (if not input them)
        part_indices : array
            input selection indices for particles
        image_limits : list
            min and max limits to impose on image dynamic range (exposure)
        plot_file : bool
            whether to write figure to file and its name
        '''
        dimen_label = {0: 'x', 1: 'y', 2: 'z'}

        position_limits = [[-distance_max, distance_max] for _ in range(3)]
        position_limits = np.array(position_limits)

        if part_indices is None or len(part_indices) == 0:
            part_indices = ut.array.get_arange(part[species_name]['position'].shape[0])

        host_name = ut.catalog.get_host_name(host_index)

        if rotation is True:
            # rotate according to principal axes
            positions = part[species_name].prop(f'{host_name}.distance.principal', part_indices)
        else:
            # positions in (arbitrary) Cartesian x,y,z of simulation
            positions = part[species_name].prop(f'{host_name}.distance', part_indices)

        weights = None
        if weight_name:
            weights = part[species_name].prop(weight_name, part_indices)

        # keep only particles within distance limits
        masks = positions[:, dimensions_plot[0]] <= distance_max
        for dimen_i in dimensions_plot:
            masks *= (positions[:, dimen_i] >= -distance_max) * (
                positions[:, dimen_i] <= distance_max
            )

        positions = positions[masks]
        if weights is not None:
            weights = weights[masks]

        position_bin_number = int(np.round(2 * np.max(distance_max) / distance_bin_width))

        # set color map
        if 'dark' in species_name or species_name == 'gas' or species_name == 'star':
            color_map = plt.cm.afmhot  # pylint: disable=no-member

        # set interpolation method
        interpolation = 'bilinear'

        if len(dimensions_plot) == 2:
            fig, subplot = ut.plot.make_figure(
                1,
                left=0.22,
                right=0.98,
                bottom=0.15,
                top=0.98,
                background_color='black',
            )

            subplot.set_xlim(position_limits[dimensions_plot[0]])
            subplot.set_ylim(position_limits[dimensions_plot[1]])

            subplot.set_xlabel(f'{dimen_label[dimensions_plot[0]]} $\\left[ {{\\rm kpc}} \\right]$')
            subplot.set_ylabel(f'{dimen_label[dimensions_plot[1]]} $\\left[ {{\\rm kpc}} \\right]$')

            hist_valuess, _hist_xs, _hist_ys, hist_limits = self.get_histogram(
                'histogram',
                dimensions_plot,
                position_bin_number,
                position_limits,
                positions,
                weights,
            )

            image_limits_use = hist_limits
            if image_limits is not None and len(image_limits) > 0:
                if image_limits[0] is not None:
                    image_limits_use[0] = image_limits[0]
                if image_limits[1] is not None:
                    image_limits_use[1] = image_limits[1]

            _Image = subplot.imshow(
                hist_valuess.transpose(),
                norm=colors.LogNorm(),
                cmap=color_map,
                aspect='auto',
                interpolation=interpolation,
                extent=np.concatenate(position_limits[dimensions_plot]),
                vmin=image_limits[0],
                vmax=image_limits[1],
            )

            fig.colorbar(_Image)

            fig.gca().set_aspect('equal')

        elif len(dimensions_plot) == 3:
            fig, subplots = ut.plot.make_figure(
                1,
                [2, 2],
                left=0.22,
                right=0.97,
                bottom=0.16,
                top=0.97,
                background_color='black',
            )

            plot_dimension_iss = [
                [dimensions_plot[0], dimensions_plot[1]],
                [dimensions_plot[0], dimensions_plot[2]],
                [dimensions_plot[1], dimensions_plot[2]],
            ]

            subplot_iss = [[0, 0], [1, 0], [1, 1]]

            histogram_valuesss = []
            for plot_i, plot_dimension_is in enumerate(plot_dimension_iss):
                subplot_is = subplot_iss[plot_i]
                subplot = subplots[subplot_is[0], subplot_is[1]]

                hist_valuess, _hist_xs, _hist_ys, hist_limits = self.get_histogram(
                    'histogram',
                    plot_dimension_is,
                    position_bin_number,
                    position_limits,
                    positions,
                    weights,
                )

                histogram_valuesss.append(hist_valuess)

                image_limits_use = hist_limits
                if image_limits is not None and len(image_limits) > 0:
                    if image_limits[0] is not None:
                        image_limits_use[0] = image_limits[0]
                    if image_limits[1] is not None:
                        image_limits_use[1] = image_limits[1]

                # ensure that tick labels do not overlap
                subplot.set_xlim(position_limits[plot_dimension_is[0]])
                subplot.set_ylim(position_limits[plot_dimension_is[1]])

                units_label = ' $\\left[ {\\rm kpc} \\right]$'
                if subplot_is == [0, 0]:
                    subplot.set_ylabel(dimen_label[plot_dimension_is[1]] + units_label)
                elif subplot_is == [1, 0]:
                    subplot.set_xlabel(dimen_label[plot_dimension_is[0]] + units_label)
                    subplot.set_ylabel(dimen_label[plot_dimension_is[1]] + units_label)
                elif subplot_is == [1, 1]:
                    subplot.set_xlabel(dimen_label[plot_dimension_is[0]] + units_label)

                _Image = subplot.imshow(
                    hist_valuess.transpose(),
                    norm=colors.LogNorm(),
                    cmap=color_map,
                    # aspect='auto',
                    interpolation=interpolation,
                    extent=np.concatenate(position_limits[plot_dimension_is]),
                    vmin=image_limits[0],
                    vmax=image_limits[1],
                )

            if part.info['simulation.name']:
                ut.plot.make_label_legend(subplots[0, 1], part.info['simulation.name'])

            hist_valuess = np.array(histogram_valuesss)

        if plot_file:
            plt.savefig('image.pdf', format='pdf')
        plt.show(block=False)

    def plot_image(
        self,
        part,
        species_name='star',
        weight_name='mass',
        image_kind='histogram',
        dimensions_plot=[0, 1, 2],
        dimensions_select=[0, 1, 2],
        distances_max=20,
        distance_bin_width=0.1,
        distance_bin_number=None,
        center_position=None,
        rotation=None,
        host_index=0,
        property_select={},
        part_indices=None,
        subsample_factor=None,
        use_column_units=None,
        image_limits=[None, None],
        background_color='black',
        hal=None,
        hal_indices=None,
        hal_position_kind='position',
        hal_radius_kind='radius',
        plot_file_name=False,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        Plot image of the positions of given partcle species, using either a single panel for
        2 dimensions or 3 panels for all axis permutations.

        Parameters
        ----------
        part : dict
            catalog of particles at snapshot
        species_name : str
            name of particle species to plot
        weight_name : str
            property to weight positions by
        image_kind : str
            'histogram', 'histogram.3d', 'points'
        dimensions_plot : list
            dimensions to plot - if length 2, plot one v one; if length 3, plot all via 3 panels
        dimensions_select : list
            dimensions to use to select particles
            use this to set selection 'depth' of an image
        distances_max : float or array
            distance[s] from center to plot and/or cut [kpc]
        distance_bin_width : float
            size of pixel [kpc]
        distance_bin_number : int
            number of pixels from distance = 0 to max (2x this across image)
        center_position : array-like
            position of center
        rotation : bool or array
            whether to rotate particles - two options:
            (a) if input array of eigen-vectors, will define rotation axes
            (b) if True, will rotate to align with principal axes defined by input species
        host_index : int
            index of host halo to get position and rotation of (if not input them)
        property_select : dict
            (other) properties to select on: names as keys and limits as values
        part_indices : array
            input selection indices for particles
        subsample_factor : int
            factor by which periodically to sub-sample particles
        use_column_units : bool
            whether to convert to particle number / cm^2
        image_limits : list
            min and max limits to impose on image dynamic range (exposure)
        background_color : str
            name of color for background: 'white', 'black'
        hal : dict
            catalog of halos at snapshot
        hal_indices : array
            indices of halos to plot
        hal_position_kind : str
            name of position to use for center of halo
        hal_radius_kind : str
            name of radius to use for size of halo
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str
            path + directory where to write file
            if ends in '.pdf', override default file naming convention and use input name
        figure_index : int
            index of figure for matplotlib
        '''
        dimen_label = {0: 'x', 1: 'y', 2: 'z'}

        if dimensions_select is None or len(dimensions_select) == 0:
            dimensions_select = dimensions_plot

        if np.isscalar(distances_max):
            distances_max = [
                distances_max for dimen_i in range(part[species_name]['position'].shape[1])
            ]
        distances_max = np.array(distances_max, dtype=np.float64)

        position_limits = []
        for dimen_i in range(distances_max.shape[0]):
            position_limits.append([-distances_max[dimen_i], distances_max[dimen_i]])
        position_limits = np.array(position_limits)

        if part_indices is None or len(part_indices) == 0:
            part_indices = ut.array.get_arange(part[species_name]['position'].shape[0])

        if property_select:
            part_indices = ut.catalog.get_indices_catalog(
                part[species_name], property_select, part_indices
            )

        if subsample_factor is not None and subsample_factor > 1:
            part_indices = part_indices[::subsample_factor]

        positions = np.array(part[species_name]['position'][part_indices])
        weights = None
        if weight_name:
            weights = part[species_name].prop(weight_name, part_indices)

        center_position = ut.particle.parse_property(part, 'position', center_position, host_index)

        if center_position is not None and len(center_position) > 0:
            # re-orient to input center
            positions -= center_position
            positions *= part.snapshot['scalefactor']

            if rotation is not None:
                # rotate image
                if rotation is True:
                    # rotate according to principal axes
                    rotation_tensor = ut.particle.parse_property(part, 'rotation', None, host_index)
                elif len(rotation) > 0:
                    # use input rotation vectors
                    rotation_tensor = np.asarray(rotation)
                    if (
                        np.ndim(rotation_tensor) != 2
                        or rotation_tensor.shape[0] != positions.shape[1]
                        or rotation_tensor.shape[1] != positions.shape[1]
                    ):
                        raise ValueError(f'wrong shape for rotation = {rotation}')
                else:
                    raise ValueError(f'cannot parse rotation = {rotation}')

                positions = ut.coordinate.get_coordinates_rotated(positions, rotation_tensor)

            # keep only particles within distance limits
            masks = positions[:, dimensions_select[0]] <= distances_max[0]
            for dimen_i in dimensions_select:
                masks *= (positions[:, dimen_i] >= -distances_max[dimen_i]) * (
                    positions[:, dimen_i] <= distances_max[dimen_i]
                )

            positions = positions[masks]
            if weights is not None:
                weights = weights[masks]
        else:
            raise ValueError('need to input center_position')

        if distance_bin_width is not None and distance_bin_width > 0:
            position_bin_number = int(
                np.round(2 * np.max(distances_max[dimensions_plot]) / distance_bin_width)
            )
        elif distance_bin_number is not None and distance_bin_number > 0:
            position_bin_number = 2 * distance_bin_number
        else:
            raise ValueError('need to input either distance bin width or bin number')

        if hal is not None:
            # compile halos
            if hal_indices is None or len(hal_indices) == 0:
                hal_indices = ut.array.get_arange(hal['mass'])

            if 0 not in hal_indices:
                hal_indices = np.append(np.array([0], hal_indices.dtype), hal_indices)

            hal_positions = np.array(hal[hal_position_kind][hal_indices])
            if center_position is not None and len(center_position) > 0:
                hal_positions -= center_position
            hal_positions *= hal.snapshot['scalefactor']
            hal_radiuss = hal[hal_radius_kind][hal_indices]

            # initialize masks
            masks = hal_positions[:, dimensions_select[0]] <= distances_max[0]
            for dimen_i in dimensions_select:
                masks *= (hal_positions[:, dimen_i] >= -distances_max[dimen_i]) * (
                    hal_positions[:, dimen_i] <= distances_max[dimen_i]
                )

            hal_radiuss = hal_radiuss[masks]
            hal_positions = hal_positions[masks]

        # plot ----------
        # BYW = colors.LinearSegmentedColormap('byw', ut.plot.color_map_dict['BlackYellowWhite'])
        # plt.register_cmap(cmap=BYW)
        # BBW = colors.LinearSegmentedColormap('bbw', ut.plot.color_map_dict['BlackBlueWhite'])
        # plt.register_cmap(cmap=BBW)

        # set color map
        if background_color == 'black':
            if 'dark' in species_name:
                # color_map = plt.get_cmap('bbw')
                color_map = plt.cm.afmhot  # pylint: disable=no-member
            elif species_name == 'gas':
                color_map = plt.cm.afmhot  # pylint: disable=no-member
            elif species_name == 'star':
                # color_map = plt.get_cmap('byw')
                color_map = plt.cm.afmhot  # pylint: disable=no-member
        elif background_color == 'white':
            color_map = plt.cm.YlOrBr  # pylint: disable=no-member

        # set interpolation method
        # interpolation='nearest'
        interpolation = 'bilinear'
        # interpolation='bicubic'
        # interpolation='gaussian'

        if len(dimensions_plot) == 2:
            fig, subplot = ut.plot.make_figure(
                figure_index,
                left=0.22,
                right=0.98,
                bottom=0.15,
                top=0.98,
                background_color=background_color,
            )

            subplot.set_xlim(position_limits[dimensions_plot[0]])
            subplot.set_ylim(position_limits[dimensions_plot[1]])

            subplot.set_xlabel(f'{dimen_label[dimensions_plot[0]]} $\\left[ {{\\rm kpc}} \\right]$')
            subplot.set_ylabel(f'{dimen_label[dimensions_plot[1]]} $\\left[ {{\\rm kpc}} \\right]$')

            if 'histogram' in image_kind:
                hist_valuess, hist_xs, hist_ys, hist_limits = self.get_histogram(
                    image_kind,
                    dimensions_plot,
                    position_bin_number,
                    position_limits,
                    positions,
                    weights,
                    use_column_units,
                )

                image_limits_use = hist_limits
                if image_limits is not None and len(image_limits) > 0:
                    if image_limits[0] is not None:
                        image_limits_use[0] = image_limits[0]
                    if image_limits[1] is not None:
                        image_limits_use[1] = image_limits[1]

                _Image = subplot.imshow(
                    hist_valuess.transpose(),
                    norm=colors.LogNorm(),
                    cmap=color_map,
                    aspect='auto',
                    interpolation=interpolation,
                    extent=np.concatenate(position_limits[dimensions_plot]),
                    vmin=image_limits[0],
                    vmax=image_limits[1],
                )

                # standard method
                # hist_valuess, hist_xs, hist_ys, _Image = subplot.hist2d(
                #    positions[:, dimensions_plot[0]], positions[:, dimensions_plot[1]],
                #    weights=weights, range=position_limits, bins=position_bin_number,
                #    norm=colors.LogNorm(),
                #    cmap=color_map,
                #    vmin=image_limits[0], vmax=image_limits[1],
                # )

                # plot average of property
                # hist_valuess = ut.math.Fraction.get_fraction(hist_valuess, grid_number)
                # subplot.imshow(
                #    hist_valuess.transpose(),
                #    #norm=colors.LogNorm(),
                #    cmap=color_map,
                #    aspect='auto',
                #    interpolation=interpolation,
                #    extent=np.concatenate(position_limits),
                #    vmin=np.min(weights), vmax=np.max(weights),
                # )

                fig.colorbar(_Image)

            elif image_kind == 'points':
                subplot.scatter(
                    positions[:, dimensions_plot[0]],
                    positions[:, dimensions_plot[1]],
                    marker='o',
                    c=weights,
                )
                # , markersize=2.0, markeredgecolor='red', markeredgewidth=0,
                # color='red', alpha=0.02)

            fig.gca().set_aspect('equal')

            # plot halos
            if hal is not None:
                for hal_position, hal_radius in zip(hal_positions, hal_radiuss):
                    print(hal_position, hal_radius)
                    circle = plt.Circle(
                        hal_position[dimensions_plot],
                        hal_radius,
                        color='w',
                        linewidth=1,
                        fill=False,
                    )
                    subplot.add_artist(circle)

        elif len(dimensions_plot) == 3:
            fig, subplots = ut.plot.make_figure(
                figure_index,
                [2, 2],
                left=0.22,
                right=0.97,
                bottom=0.16,
                top=0.97,
                background_color=background_color,
            )

            plot_dimension_iss = [
                [dimensions_plot[0], dimensions_plot[1]],
                [dimensions_plot[0], dimensions_plot[2]],
                [dimensions_plot[1], dimensions_plot[2]],
            ]

            subplot_iss = [[0, 0], [1, 0], [1, 1]]

            histogram_valuesss = []
            for plot_i, plot_dimension_is in enumerate(plot_dimension_iss):
                subplot_is = subplot_iss[plot_i]
                subplot = subplots[subplot_is[0], subplot_is[1]]

                hist_valuess, hist_xs, hist_ys, hist_limits = self.get_histogram(
                    image_kind,
                    plot_dimension_is,
                    position_bin_number,
                    position_limits,
                    positions,
                    weights,
                    use_column_units,
                )

                histogram_valuesss.append(hist_valuess)

                image_limits_use = hist_limits
                if image_limits is not None and len(image_limits) > 0:
                    if image_limits[0] is not None:
                        image_limits_use[0] = image_limits[0]
                    if image_limits[1] is not None:
                        image_limits_use[1] = image_limits[1]

                # ensure that tick labels do not overlap
                subplot.set_xlim(position_limits[plot_dimension_is[0]])
                subplot.set_ylim(position_limits[plot_dimension_is[1]])

                units_label = ' $\\left[ {\\rm kpc} \\right]$'
                if subplot_is == [0, 0]:
                    subplot.set_ylabel(dimen_label[plot_dimension_is[1]] + units_label)
                elif subplot_is == [1, 0]:
                    subplot.set_xlabel(dimen_label[plot_dimension_is[0]] + units_label)
                    subplot.set_ylabel(dimen_label[plot_dimension_is[1]] + units_label)
                elif subplot_is == [1, 1]:
                    subplot.set_xlabel(dimen_label[plot_dimension_is[0]] + units_label)

                _Image = subplot.imshow(
                    hist_valuess.transpose(),
                    norm=colors.LogNorm(),
                    cmap=color_map,
                    # aspect='auto',
                    interpolation=interpolation,
                    extent=np.concatenate(position_limits[plot_dimension_is]),
                    vmin=image_limits[0],
                    vmax=image_limits[1],
                )

                # default method
                # hist_valuess, hist_xs, hist_ys, _Image = subplot.hist2d(
                #    positions[:, plot_dimension_is[0]], positions[:, plot_dimension_is[1]],
                #    norm=colors.LogNorm(),
                #    weights=weights,
                #    range=position_limits, bins=position_bin_number,
                #    cmap=color_map
                # )

                # fig.colorbar(_Image)  # , ax=subplot)

                # plot halos
                if hal is not None:
                    for hal_position, hal_radius in zip(hal_positions, hal_radiuss):
                        circle = plt.Circle(
                            hal_position[plot_dimension_is],
                            hal_radius,
                            color='w',
                            linewidth=1,
                            fill=False,
                        )
                        subplot.add_artist(circle)

                    circle = plt.Circle((0, 0), 10, color='w', fill=False)
                    subplot.add_artist(circle)

                # subplot.axis('equal')
                # fig.gca().set_aspect('equal')

            if part.info['simulation.name']:
                ut.plot.make_label_legend(subplots[0, 1], part.info['simulation.name'])

            hist_valuess = np.array(histogram_valuesss)

        # get name and directory to write plot file
        if '.pdf' in plot_directory:
            # use input file name, write in current directory
            plot_file_name = plot_directory
            plot_directory = '.'
        elif plot_file_name is True or plot_file_name == '':
            # generate default file name
            prefix = part.info['simulation.name']

            prop = 'position'
            for dimen_i in dimensions_plot:
                prop += '.' + dimen_label[dimen_i]
            prop += '_d.{:.0f}'.format(np.max(distances_max[dimensions_plot]))

            plot_file_name = ut.plot.get_file_name(
                weight_name, prop, species_name, 'redshift', part.snapshot, prefix=prefix
            )

            # if 'histogram' in image_kind:
            #    plot_file_name += '_i.{:.1f}-{:.1f}'.format(
            #        np.log10(image_limits_use[0]), np.log10(image_limits_use[1])
            #    )
        ut.plot.parse_output(plot_file_name, plot_directory)

        self.histogram_valuess = hist_valuess
        self.histogram_xs = hist_xs
        self.histogram_ys = hist_ys
        self.plot_file_name = plot_file_name

    def get_histogram(
        self,
        image_kind,
        dimension_list,
        position_bin_number,
        position_limits,
        positions,
        weights,
        use_column_units=False,
    ):
        '''
        Get 2-D histogram, either by summing all partiles along 3rd dimension or computing the
        highest density along 3rd dimension.

        Parameters
        ----------
        image_kind : str
            'histogram', 'histogram.3d'
        dimension_list : list
            indices of dimensions to plot
            if length 2, plot one v other, if length 3, plot all via 3 panels
        position_bin_number : int
            number of pixels/bins across image
        position_limits : list or list of lists
            min and max values of position to compute
        positions : array
            3-D positions
        weights : array
            weight for each position
        use_column_units : bool
            whether to convert to [number / cm^2]
        '''
        if '3d' in image_kind:
            # calculate maximum local density along projected dimension
            hist_valuess, (hist_xs, hist_ys, hist_zs) = np.histogramdd(
                positions, position_bin_number, position_limits, weights=weights
            )
            # convert to 3-d density
            hist_valuess /= np.diff(hist_xs)[0] * np.diff(hist_ys)[0] * np.diff(hist_zs)[0]

            dimension_project = np.setdiff1d([0, 1, 2], dimension_list)

            # compute maximum density
            hist_valuess = np.max(hist_valuess, dimension_project)

        else:
            # project along single dimension
            hist_valuess, hist_xs, hist_ys = np.histogram2d(
                positions[:, dimension_list[0]],
                positions[:, dimension_list[1]],
                position_bin_number,
                position_limits[dimension_list],
                weights=weights,
            )

            # convert to surface density
            hist_valuess /= np.diff(hist_xs)[0] * np.diff(hist_ys)[0]

            # convert to number density
            if use_column_units:
                hist_valuess *= ut.constant.hydrogen_per_sun * ut.constant.kpc_per_cm**2
                grid_number = hist_valuess.size
                lls_number = np.sum((hist_valuess > 1e17) * (hist_valuess < 2e20))
                dla_number = np.sum(hist_valuess > 2e20)
                self.say(
                    'covering fraction: LLS = {:.2e}, DLA = {:.2e}'.format(
                        lls_number / grid_number, dla_number / grid_number
                    )
                )

        masks = hist_valuess > 0
        self.say(
            'histogram min, med, max = {:.3e}, {:.3e}, {:.3e}'.format(
                hist_valuess[masks].min(), np.median(hist_valuess[masks]), hist_valuess[masks].max()
            )
        )

        hist_limits = np.array([hist_valuess[masks].min(), hist_valuess[masks].max()])

        return hist_valuess, hist_xs, hist_ys, hist_limits

    def print_values(self):
        '''
        Write 2-D histogram values of image to file.
        '''
        file_name = self.plot_file_name + '.txt'

        with open(file_name, 'w', encoding='utf-8') as file_out:
            Write = ut.io.WriteClass(file_out, print_stdout=False)
            Write.write(
                '# pixel (smoothing) scale is {:.2f} kpc'.format(
                    self.histogram_xs[1] - self.histogram_xs[0]
                )
            )
            for ix in range(self.histogram_xs.size - 1):
                x = self.histogram_xs[ix] + 0.5 * (
                    self.histogram_xs[ix + 1] - self.histogram_xs[ix]
                )
                for iy in range(self.histogram_ys.size - 1):
                    y = self.histogram_ys[iy] + 0.5 * (
                        self.histogram_ys[iy + 1] - self.histogram_ys[iy]
                    )
                    Write.write(
                        '{:.3f} {:.3f} {:.3e} {:.3e} {:.3e}'.format(
                            x,
                            y,
                            self.histogram_valuess[0, ix, iy],
                            self.histogram_valuess[1, ix, iy],
                            self.histogram_valuess[2, ix, iy],
                        )
                    )


Image = ImageClass()


# --------------------------------------------------------------------------------------------------
# property distribution
# --------------------------------------------------------------------------------------------------
def plot_density_distribution(
    parts,
    species_name='gas',
    property_name='number.density',
    property_limits=[0.1, 1e5],
    property_bin_width=0.1,
    property_log_scale=True,
    property_statistic='probability',
    temperature_limitss=[None, [0, 1e4], [0, 100]],
    property_select={
        'host.distance.principal.cylindrical.rad': [0, 15],
        'host.distance.principal.cylindrical.vert': [-3, 3],
    },
    part_indicess=None,
    axis_y_limits=None,
    axis_y_log_scale=True,
    plot_file_name=None,
    plot_directory='.',
    figure_index=1,
):
    '''
    Plot distribution of gas density or size (smoothing length).

    Parameters
    ----------
    part : dict
        catalog of particles at snapshot
    species_name : str
        name of particle species
    property_name : str
        property name
    property_limits : list
        min and max limits of property
    property_bin_width : float
        width of property bin (use this or property_bin_number)
    property_log_scale : bool
        whether to use logarithmic scaling for property bins
    property_statistic : str
        statistic to plot: 'probability', 'probability.cum', 'probability.norm', 'histogram',
        'histogram.cum'
    temperature_limitss : list
        limits[s] of temperature to apply
    property_select : dict
        (other) properties to select on: names as keys and limits as values
    part_indicess : array or list of arrays
        indices of particles from which to select
    axis_y_limits : list
        min and max limits for y axis
    axis_y_log_scale : bool
        whether to use logarithmic scaling for y axis
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory to write plot file
    figure_index : int
        index of figure for matplotlib
    '''
    Say = ut.io.SayClass(plot_density_distribution)

    if isinstance(parts, dict):
        parts = [parts]
    if np.isscalar(temperature_limitss):
        temperature_limitss = [temperature_limitss]
    temperature_number = len(temperature_limitss)

    part_indicess = ut.particle.parse_property(parts, 'indices', part_indicess)

    Stat = ut.math.StatisticClass()

    for part_i, part in enumerate(parts):
        if part_indicess[part_i] is not None and len(part_indicess[part_i]) > 0:
            part_indices = part_indicess[part_i]
        else:
            part_indices = ut.array.get_arange(part[species_name]['position'].shape[0])

        if property_select:
            part_indices = ut.catalog.get_indices_catalog(
                part[species_name], property_select, part_indices
            )

        for temperature_limits in temperature_limitss:
            part_indices_t = ut.array.get_indices(
                part[species_name].prop('temperature'), temperature_limits, part_indices
            )
            prop_values = part[species_name].prop(property_name, part_indices_t)
            weights = part[species_name].prop('mass', part_indices_t)
            Say.say(f'keeping {prop_values.size} {species_name} particles')

            Stat.append_to_dictionary(
                prop_values,
                property_limits,
                property_bin_width,
                None,
                property_log_scale,
                weights,
            )

            # Stat.print_statistics(-1)
            # print()

    color_names = ut.plot.get_colors(len(parts))
    line_styles = ut.plot.get_line_styles(len(temperature_limitss))

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    y_values = np.array(
        [Stat.distr[property_statistic][i] for i in range(len(parts) * temperature_number)]
    )

    ut.plot.set_axes_scaling_limits(
        subplot,
        property_log_scale,
        property_limits,
        prop_values,
        axis_y_log_scale,
        axis_y_limits,
        y_values,
    )

    axis_x_label = ut.plot.Label.get_label(property_name, species_name=species_name, get_words=True)
    subplot.set_xlabel(axis_x_label)
    axis_y_label = ut.plot.Label.get_label(
        property_name, property_statistic, species_name, property_log_scale, get_units=False
    )
    subplot.set_ylabel(axis_y_label)

    for part_i, part in enumerate(parts):
        for temp_i, temperature_limits in enumerate(temperature_limitss):
            i = part_i * temperature_number + temp_i
            label = part.info['simulation.name'].replace('Msun', '${{\\rm M}}_\\odot$')
            subplot.plot(
                Stat.distr['bin.mid'][i],
                Stat.distr[property_statistic][i],
                color=color_names[part_i],
                linestyle=line_styles[temp_i],
                alpha=0.8,
                label=label,
            )

    ut.plot.make_legends(subplot)  # , time_value=parts[0].snapshot['redshift'])

    if plot_file_name is True or plot_file_name == '':
        plot_file_name = ut.plot.get_file_name(
            property_name, 'distribution', species_name, snapshot_dict=part.snapshot
        )
    ut.plot.parse_output(plot_file_name, plot_directory)


def plot_smooth_length_distribution(
    parts,
    species_name='gas',
    property_name='number.density',
    property_limits=[0.1, 1e5],
    property_bin_width=0.1,
    property_log_scale=True,
    property_statistic='probability',
    temperature_limitss=[None, [0, 1e4], [0, 100]],
    property_select={
        'host.distance.principal.cylindrical.rad': [0, 15],
        'host.distance.principal.cylindrical.vert': [-3, 3],
    },
    part_indicess=None,
    axis_y_limits=None,
    axis_y_log_scale=True,
    plot_file_name=None,
    plot_directory='.',
    figure_index=1,
):
    '''
    Plot distribution of gas density.

    Parameters
    ----------
    part : dict
        catalog of particles at snapshot
    species_name : str
        name of particle species
    property_name : str
        property name
    property_limits : list
        min and max limits of property
    property_bin_width : float
        width of property bin (use this or property_bin_number)
    property_log_scale : bool
        whether to use logarithmic scaling for property bins
    property_statistic : str
        statistic to plot: 'probability', 'probability.cum', 'probability.norm', 'histogram',
        'histogram.cum'
    temperature_limitss : list
        limits[s] of temperature to apply
    property_select : dict
        (other) properties to select on: names as keys and limits as values
    part_indicess : array or list of arrays
        indices of particles from which to select
    axis_y_limits : list
        min and max limits for y axis
    axis_y_log_scale : bool
        whether to use logarithmic scaling for y axis
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory to write plot file
    figure_index : int
        index of figure for matplotlib
    '''
    Say = ut.io.SayClass(plot_smooth_length_distribution)

    if isinstance(parts, dict):
        parts = [parts]
    if np.isscalar(temperature_limitss):
        temperature_limitss = [temperature_limitss]
    temperature_number = len(temperature_limitss)

    part_indicess = ut.particle.parse_property(parts, 'indices', part_indicess)

    Stat = ut.math.StatisticClass()

    for part_i, part in enumerate(parts):
        if part_indicess[part_i] is not None and len(part_indicess[part_i]) > 0:
            part_indices = part_indicess[part_i]
        else:
            part_indices = ut.array.get_arange(part[species_name]['position'].shape[0])

        if property_select:
            part_indices = ut.catalog.get_indices_catalog(
                part[species_name], property_select, part_indices
            )

        for temperature_limits in temperature_limitss:
            part_indices_t = ut.array.get_indices(
                part[species_name].prop('temperature'), temperature_limits, part_indices
            )
            prop_values = part[species_name].prop(property_name, part_indices_t)
            weights = part[species_name].prop('mass', part_indices_t)
            Say.say(f'keeping {prop_values.size} {species_name} particles')

            Stat.append_to_dictionary(
                prop_values,
                property_limits,
                property_bin_width,
                None,
                property_log_scale,
                weights,
            )

            # Stat.print_statistics(-1)
            # print()

    color_names = ut.plot.get_colors(len(parts))
    line_styles = ut.plot.get_line_styles(len(temperature_limitss))

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    y_values = np.array(
        [Stat.distr[property_statistic][i] for i in range(len(parts) * temperature_number)]
    )

    ut.plot.set_axes_scaling_limits(
        subplot,
        property_log_scale,
        property_limits,
        prop_values,
        axis_y_log_scale,
        axis_y_limits,
        y_values,
    )

    axis_x_label = ut.plot.Label.get_label(property_name, species_name=species_name, get_words=True)
    subplot.set_xlabel(axis_x_label)
    axis_y_label = ut.plot.Label.get_label(
        property_name, property_statistic, species_name, property_log_scale, get_units=False
    )
    subplot.set_ylabel(axis_y_label)

    for part_i, part in enumerate(parts):
        for temp_i, temperature_limits in enumerate(temperature_limitss):
            i = part_i * temperature_number + temp_i
            label = part.info['simulation.name'].replace('Msun', '${{\\rm M}}_\\odot$')
            subplot.plot(
                Stat.distr['bin.mid'][i],
                Stat.distr[property_statistic][i],
                color=color_names[part_i],
                linestyle=line_styles[temp_i],
                alpha=0.8,
                label=label,
            )

    ut.plot.make_legends(subplot)  # , time_value=parts[0].snapshot['redshift'])

    if plot_file_name is True or plot_file_name == '':
        plot_file_name = ut.plot.get_file_name(
            property_name, 'distribution', species_name, snapshot_dict=part.snapshot
        )
    ut.plot.parse_output(plot_file_name, plot_directory)


def plot_property_v_property(
    part,
    species_name='gas',
    x_property_name='number.density',
    x_property_limits=None,
    x_property_log_scale=True,
    y_property_name='temperature',
    y_property_limits=None,
    y_property_log_scale=True,
    property_bin_number=150,
    weight_property='mass',
    cut_percent=0,
    host_distance_limits=[0, 300],
    center_position=None,
    host_index=0,
    property_select={},
    part_indices=None,
    draw_statistics=False,
    plot_file_name=False,
    plot_directory='.',
    add_simulation_name=False,
    figure_index=1,
):
    '''
    Plot property v property.

    Parameters
    ----------
    part : dict
        catalog of particles at snapshot
    species_name : str
        name of particle species
    x_property_name : str
        property name for x-axis
    x_property_limits : list
        min and max limits to impose on x_property_name
    x_property_log_scale : bool
        whether to use logarithmic scaling for x axis
    y_property_name : str
        property name for y-axis
    y_property_limits : list
        min and max limits to impose on y_property_name
    y_property_log_scale : bool
        whether to use logarithmic scaling for y axis
    property_bin_number : int
        number of bins for histogram along each axis
    weight_property : str
        property to weight each particle by
    host_distance_limits : list
        min and max limits for distance from galaxy
    center_position : array
        position of galaxy center
    host_index : int
        index of host galaxy/halo to get position of (if not input)
    property_select : dict
        (other) properties to select on: names as keys and limits as values
    part_indices : array
        indices of particles from which to select
    draw_statistics : bool
        whether to draw statistics (such as median) on figure
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory to write figure file
    add_simulation_name : bool
        whether to add name of simulation to figure name
    figure_index : int
        index of figure for matplotlib
    '''
    Say = ut.io.SayClass(plot_property_v_property)

    center_position = ut.particle.parse_property(part, 'position', center_position, host_index)

    if part_indices is None or len(part_indices) == 0:
        part_indices = ut.array.get_arange(part[species_name].prop(x_property_name))

    if property_select:
        part_indices = ut.catalog.get_indices_catalog(
            part[species_name], property_select, part_indices
        )

    if (
        len(center_position) > 0
        and host_distance_limits is not None
        and len(host_distance_limits) > 0
    ):
        distances = ut.coordinate.get_distances(
            part[species_name]['position'][part_indices],
            center_position,
            part.info['box.length'],
            part.snapshot['scalefactor'],
            total_distance=True,
        )  # [kpc phy]
        part_indices = part_indices[ut.array.get_indices(distances, host_distance_limits)]

    x_prop_values = part[species_name].prop(x_property_name, part_indices)
    y_prop_values = part[species_name].prop(y_property_name, part_indices)
    weights = None
    if weight_property is not None and len(weight_property) > 0:
        weights = part[species_name].prop(weight_property, part_indices)

    part_indices = ut.array.get_arange(part_indices)

    if x_property_limits:
        part_indices = ut.array.get_indices(x_prop_values, x_property_limits, part_indices)

    if y_property_limits:
        part_indices = ut.array.get_indices(y_prop_values, y_property_limits, part_indices)

    if cut_percent > 0:
        x_limits = ut.array.get_limits(x_prop_values[part_indices], cut_percent=cut_percent)
        y_limits = ut.array.get_limits(y_prop_values[part_indices], cut_percent=cut_percent)
        part_indices = ut.array.get_indices(x_prop_values, x_limits, part_indices)
        part_indices = ut.array.get_indices(y_prop_values, y_limits, part_indices)

    x_prop_values = x_prop_values[part_indices]
    y_prop_values = y_prop_values[part_indices]
    if weight_property is not None and len(weight_property) > 0:
        weights = weights[part_indices]

    Say.say(f'keeping {x_prop_values.size} particles')

    if draw_statistics:
        stat_bin_number = int(np.round(property_bin_number / 10))
        Bin = ut.binning.BinClass(
            x_property_limits, None, stat_bin_number, False, x_property_log_scale
        )
        stat = Bin.get_statistics_of_array(x_prop_values, y_prop_values)

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    axis_x_limits, axis_y_limits = ut.plot.set_axes_scaling_limits(
        subplot,
        x_property_log_scale,
        x_property_limits,
        x_prop_values,
        y_property_log_scale,
        y_property_limits,
        y_prop_values,
    )

    axis_x_label = ut.plot.Label.get_label(
        x_property_name, species_name=species_name, get_words=True
    )
    subplot.set_xlabel(axis_x_label)

    axis_y_label = ut.plot.Label.get_label(
        y_property_name, species_name=species_name, get_words=True
    )
    subplot.set_ylabel(axis_y_label)

    if x_property_log_scale:
        axis_x_log_limits = ut.math.get_log(axis_x_limits)
        axis_x_bins = np.logspace(axis_x_log_limits[0], axis_x_log_limits[1], property_bin_number)
    else:
        axis_x_bins = np.linspace(axis_x_limits[0], axis_x_limits[1], property_bin_number)
    if y_property_log_scale:
        axis_y_log_limits = ut.math.get_log(axis_y_limits)
        axis_y_bins = np.logspace(axis_y_log_limits[0], axis_y_log_limits[1], property_bin_number)
    else:
        axis_y_bins = np.linspace(axis_y_limits[0], axis_y_limits[1], property_bin_number)

    color_map = plt.cm.inferno_r  # pylint: disable=no-member
    # color_map = plt.cm.gist_heat_r  # pylint: disable=no-member
    # color_map = plt.cm.afmhot_r  # pylint: disable=no-member

    _valuess, _xs, _ys, _Image = plt.hist2d(
        x_prop_values,
        y_prop_values,
        # property_bin_number,
        [axis_x_bins, axis_y_bins],
        [axis_x_limits, axis_y_limits],
        norm=colors.LogNorm(),
        weights=weights,
        cmin=None,
        cmax=None,
        cmap=color_map,
    )

    """
    valuess, _xs, _ys = np.histogram2d(
        x_prop_values, y_prop_values, property_bin_number, [axis_x_limits, axis_y_limits],
        weights=weights)

    subplot.imshow(
        valuess.transpose(),
        norm=colors.LogNorm(),
        cmap=color_map,
        aspect='auto',
        interpolation='nearest',
        #interpolation='none',
        extent=(axis_x_limits[0], axis_x_limits[1], axis_y_limits[0], axis_y_limits[1]),
        #vmin=valuess.min(), vmax=valuess.max(),
        #label=label,
    )
    plt.colorbar()
    """

    if draw_statistics:
        print(stat['bin.mid'])
        subplot.plot(stat['bin.mid'], stat['median'], color='black', linestyle='-', alpha=0.4)
        subplot.plot(stat['bin.mid'], stat['percent.16'], color='black', linestyle='--', alpha=0.3)
        subplot.plot(stat['bin.mid'], stat['percent.84'], color='black', linestyle='--', alpha=0.3)

    # distance legend
    if host_distance_limits is not None and len(host_distance_limits) > 0:
        label = ut.plot.Label.get_label('radius', property_limits=host_distance_limits)
        ut.plot.make_label_legend(subplot, label, 'best')

    if plot_file_name is True or plot_file_name == '':
        if add_simulation_name:
            prefix = part.info['simulation.name']
        else:
            prefix = ''

        plot_file_name = ut.plot.get_file_name(
            y_property_name,
            x_property_name,
            species_name,
            snapshot_dict=part.snapshot,
            host_distance_limits=host_distance_limits,
            prefix=prefix,
        )
    ut.plot.parse_output(plot_file_name, plot_directory)


def plot_property_v_distance(
    parts,
    species_name='dark',
    property_name='mass',
    property_statistic='sum',
    property_log_scale=True,
    property_limits=None,
    weight_property='mass',
    distance_limits=[0.1, 300],
    distance_bin_width=0.02,
    distance_log_scale=True,
    dimension_number=3,
    rotation=None,
    other_axis_distance_limits=None,
    center_positions=None,
    center_velocities=None,
    host_index=0,
    property_select={},
    part_indicess=None,
    distance_reference=None,
    plot_nfw=False,
    plot_fit=False,
    fit_distance_limits=None,
    print_values=False,
    get_values=False,
    plot_file_name=False,
    plot_directory='.',
    figure_index=1,
):
    '''
    parts : dict or list
        catalog[s] of particles (can be different simulations or snapshots)
    species_name : str
        name of particle species to compute mass from: 'dark', 'star', 'gas', 'baryon', 'total'
    property_name : str
        property to get profile of
    property_statistic : str
        statistic/type to plot: sum, sum.cum, density, density.cum, vel.circ, sum.fraction,
        sum.cum.fraction, median, average
    property_log_scale : bool
        whether to use logarithmic scaling for property bins
    weight_property : str
        property to weight each particle by
    property_limits : list
        limits to impose on y-axis
    distance_limits : list
        min and max distance for binning
    distance_bin_width : float
        width of distance bin
    distance_log_scale : bool
        whether to use logarithmic scaling for distance bins
    dimension_number : int
        number of spatial dimensions for profile. if 1, get profile along minor axis.
        if 2, get profile along 2 major axes
    rotation : bool or array
        whether to rotate particles - two options:
        (a) if input array of eigen-vectors, will define rotation axes
        (b) if True, will rotate to align with principal axes stored in species dictionary
    other_axis_distance_limits : float
        min and max distances along other axis[s] to keep particles [kpc physical]
    center_positions : array or list of arrays
        position of center for each particle catalog
    center_velocities : array or list of arrays
        velocity of center for each particle catalog
    host_index : int
        index of host halo to get position and/or velocity of (if not input them)
    property_select : dict
        (other) properties to select on: names as keys and limits as values
    part_indicess : array or list of arrays
        indices of particles from which to select
    distance_reference : float
        reference distance at which to draw vertical line
    plot_nfw : bool
        whether to overplot NFW profile: density ~ 1 / r
    plot_fit : bool
        whether to overplot linear fit
    fit_distance_limits : list
        min and max distance for fit
    print_values : bool
        whether to print values plotted
    get_values : bool
        whether to return values plotted
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory to write figure file
    figure_index : int
        index of figure for matplotlib
    '''
    if isinstance(parts, dict):
        parts = [parts]

    center_positions = ut.particle.parse_property(parts, 'position', center_positions, host_index)
    if 'velocity' in property_name:
        center_velocities = ut.particle.parse_property(
            parts, 'velocity', center_velocities, host_index
        )
    else:
        center_velocities = [center_velocities for _ in center_positions]
    part_indicess = ut.particle.parse_property(parts, 'indices', part_indicess)

    SpeciesProfile = ut.particle.SpeciesProfileClass(
        distance_limits,
        width=distance_bin_width,
        log_scale=distance_log_scale,
        dimension_number=dimension_number,
    )

    pros = []

    for part_i, part in enumerate(parts):
        pros_part = SpeciesProfile.get_profiles(
            part,
            species_name,
            property_name,
            property_statistic,
            weight_property,
            host_index,
            center_positions[part_i],
            center_velocities[part_i],
            rotation,
            other_axis_distance_limits,
            property_select,
            part_indicess[part_i],
        )

        pros.append(pros_part)

    if print_values:
        # print results
        print(pros[0][species_name]['distance'])
        for part_i, pro in enumerate(pros):
            print(pro[species_name][property_statistic])

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    y_values = [pro[species_name][property_statistic] for pro in pros]
    _axis_x_limits, axis_y_limits = ut.plot.set_axes_scaling_limits(
        subplot,
        distance_log_scale,
        distance_limits,
        None,
        property_log_scale,
        property_limits,
        y_values,
    )

    if dimension_number in [2, 3]:
        axis_x_label = 'radius'
    elif dimension_number == 1:
        axis_x_label = 'height'
    axis_x_label = ut.plot.Label.get_label(axis_x_label, get_words=True)
    subplot.set_xlabel(axis_x_label)

    if property_statistic == 'vel.circ':
        label_property_name = 'vel.circ'
    else:
        label_property_name = property_name
    axis_y_label = ut.plot.Label.get_label(
        label_property_name, property_statistic, species_name, dimension_number=dimension_number
    )
    subplot.set_ylabel(axis_y_label)

    color_names = ut.plot.get_colors(len(parts))

    if (
        'fraction' in property_statistic
        or 'beta' in property_name
        or 'velocity.rad' in property_name
    ):
        if 'fraction' in property_statistic:
            y_values = [1, 1]
        elif 'beta' in property_name:
            y_values = [0, 0]
        elif 'velocity.rad' in property_name:
            y_values = [0, 0]
        subplot.plot(distance_limits, y_values, color='black', linestyle=':', alpha=0.3)

    if distance_reference is not None:
        subplot.plot(
            [distance_reference, distance_reference],
            axis_y_limits,
            color='black',
            linestyle=':',
            alpha=0.6,
        )

    if plot_nfw:
        pro = pros[0]
        distances_nfw = pro[species_name]['distance']
        # normalize to outermost distance bin
        densities_nfw = (
            np.ones(pro[species_name]['distance'].size) * pro[species_name][property_statistic][-1]
        )
        densities_nfw *= pro[species_name]['distance'][-1] / pro[species_name]['distance']
        subplot.plot(distances_nfw, densities_nfw, color='black', linestyle=':', alpha=0.6)

    # plot profiles
    if len(pros) == 1:
        alpha = None
        linewidth = 3.5
    else:
        alpha = 0.7
        linewidth = None

    for part_i, pro in enumerate(pros):
        color = color_names[part_i]

        label = parts[part_i].info['simulation.name']
        if len(pros) > 1 and parts[0].info['simulation.name'] == parts[1].info['simulation.name']:
            label = '$z={:.1f}$'.format(parts[part_i].snapshot['redshift'])

        masks = pro[species_name][property_statistic] != 0  # plot only non-zero values
        subplot.plot(
            pro[species_name]['distance'][masks],
            pro[species_name][property_statistic][masks],
            color=color,
            alpha=alpha,
            linewidth=linewidth,
            label=label,
        )

    ut.plot.make_legends(subplot, time_value=parts[0].snapshot['redshift'])

    if plot_fit:
        xs = pro[species_name]['distance']
        ys = pro[species_name][property_statistic]

        masks = np.isfinite(xs)
        if fit_distance_limits is not None and len(fit_distance_limits) > 0:
            masks = (xs >= min(fit_distance_limits)) * (xs < max(fit_distance_limits))

        fit_kind = 'exponential'
        # fit_kind = 'sech2.single'
        # fit_kind = 'sech2.double'

        from scipy.optimize import curve_fit
        from scipy import stats

        if fit_kind == 'exponential':
            if distance_log_scale:
                xs = np.log10(xs)
            if property_log_scale:
                ys = np.log10(ys)

            slope, intercept, _r_value, _p_value, _std_err = stats.linregress(xs[masks], ys[masks])

            print('# raw fit: slope = {:.3f}, intercept = {:.3f}'.format(slope, intercept))
            if property_log_scale and not distance_log_scale:
                print('# exponential fit:')
                print('  scale length = {:.3f} kpc'.format(-1 * np.log10(np.e) / slope))
                print('  normalization = 10^{:.2f} Msun / kpc^2'.format(intercept))

            ys_fit = intercept + slope * xs

            if distance_log_scale:
                xs = 10**xs
            if property_log_scale:
                ys_fit = 10**ys_fit

        elif fit_kind == 'sech2.single':

            def disk_height_single(xs, a, b):
                return a / np.cosh(xs / (2 * b)) ** 2

            params, _ = curve_fit(
                disk_height_single, xs[masks], ys[masks], [1e7, 0.5], bounds=[[0, 0], [1e14, 10]]
            )
            print('# single sech^2 fit:')
            print('  scale height = {:.2f} kpc'.format(params[1]))
            print('  normalization = {:.2e} Msun / kpc'.format(params[0] / 2))

            ys_fit = disk_height_single(xs, *params)

        elif fit_kind == 'sech2.double':

            def disk_height_double(xs, a, b, c, d):
                return a / np.cosh(xs / (2 * b)) ** 2 + c / np.cosh(xs / (2 * d)) ** 2

            params, _ = curve_fit(
                disk_height_double,
                xs[masks],
                ys[masks],
                [1e8, 0.1, 1e8, 2],
                bounds=[[10, 0.01, 10, 0.2], [1e14, 3, 1e14, 5]],
            )

            print('# double sech^2 fit:')
            print('* thin scale height = {:.3f} kpc'.format(params[1]))
            print('  normalization = {:.2e} Msun / kpc'.format(params[0] / 2))
            print('* thick scale height = {:.3f} kpc'.format(params[3]))
            print('  normalization = {:.2e} Msun / kpc'.format(params[2] / 2))

            ys_fit = disk_height_double(xs, *params)

        subplot.plot(xs, ys_fit, color='black', alpha=0.5, linewidth=3.5)

    distance_name = 'dist'
    if dimension_number == 2:
        distance_name += '.2d'
    elif dimension_number == 1:
        distance_name = 'height'

    if plot_file_name is True or plot_file_name == '':
        plot_file_name = ut.plot.get_file_name(
            property_name + '.' + property_statistic,
            distance_name,
            species_name,
            snapshot_dict=parts[0].snapshot,
        )
        plot_file_name = plot_file_name.replace('.sum', '')
        plot_file_name = plot_file_name.replace('mass.vel.circ', 'vel.circ')
        plot_file_name = plot_file_name.replace('mass.density', 'density')
    ut.plot.parse_output(plot_file_name, plot_directory)

    if get_values:
        if len(parts) == 1:
            pros = pros[0]
        return pros


def plot_velocity_distribution(
    parts,
    species_name='star',
    property_name='velocity.tan',
    property_limits=None,
    property_bin_width=None,
    property_bin_number=100,
    property_log_scale=False,
    property_statistic='probability',
    distance_limits=[70, 90],
    center_positions=None,
    center_velocities=None,
    host_index=0,
    property_select={},
    part_indicess=None,
    axis_y_limits=None,
    axis_y_log_scale=False,
    plot_file_name=False,
    plot_directory='.',
    figure_index=1,
):
    '''
    Plot distribution of velocities.

    Parameters
    ----------
    part : dict
        catalog of particles at snapshot
    species_name : str
        name of particle species
    property_name : str
        property name
    property_limits : list
        min and max limits of property
    property_bin_width : float
        width of property bin (use this or property_bin_number)
    property_bin_number : int
        number of bins within limits (use this or property_bin_width)
    property_log_scale : bool
        whether to use logarithmic scaling for property bins
    property_statistic : str :
        statistic to plot: 'probability', 'probability.cum', 'histogram', 'histogram.cum'
    distance_limits : list
        min and max limits for distance from galaxy
    center_positions : array or list of arrays
        position[s] of galaxy center[s]
    center_velocities : array or list of arrays
        velocity[s] of galaxy center[s]
    host_index : int
        index of host galaxy/halo to get position and/or velocity of (if not input them)
    property_select : dict
        (other) properties to select on: names as keys and limits as values
    part_indicess : array or list of arrays
        indices of particles from which to select
    axis_y_limits : list
        min and max limits for y axis
    axis_y_log_scale : bool
        whether to use logarithmic scaling for y axis
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory to write figure file
    figure_index : int
        index of figure for matplotlib
    '''
    Say = ut.io.SayClass(plot_velocity_distribution)

    if isinstance(parts, dict):
        parts = [parts]

    center_positions = ut.particle.parse_property(parts, 'position', center_positions, host_index)
    part_indicess = ut.particle.parse_property(parts, 'indices', part_indicess)
    if 'velocity' in property_name:
        center_velocities = ut.particle.parse_property(
            parts, 'velocity', center_velocities, host_index
        )

    Stat = ut.math.StatisticClass()

    for part_i, part in enumerate(parts):
        if part_indicess[part_i] is not None and len(part_indicess[part_i]) > 0:
            part_indices = part_indicess[part_i]
        else:
            part_indices = ut.array.get_arange(part[species_name]['position'].shape[0])

        if property_select:
            part_indices = ut.catalog.get_indices_catalog(
                part[species_name], property_select, part_indices
            )

        if distance_limits:
            # [kpc physical]
            distances = ut.coordinate.get_distances(
                part[species_name]['position'][part_indices],
                center_positions[part_i],
                part.info['box.length'],
                part.snapshot['scalefactor'],
                total_distance=True,
            )
            part_indices = part_indices[ut.array.get_indices(distances, distance_limits)]

        if 'velocity' in property_name:
            orb = ut.particle.get_orbit_dictionary(
                part,
                species_name,
                part_indices,
                center_positions[part_i],
                center_velocities[part_i],
                host_index,
            )
            prop_values = orb[property_name]
        else:
            prop_values = part[species_name].prop(property_name, part_indices)

        Say.say(f'keeping {prop_values.size} {species_name} particles')

        Stat.append_to_dictionary(
            prop_values,
            property_limits,
            property_bin_width,
            property_bin_number,
            property_log_scale,
        )

        # Stat.print_statistics(-1)
        # print()

    color_names = ut.plot.get_colors(len(parts))

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    y_values = np.array([Stat.distr[property_statistic][part_i] for part_i in range(len(parts))])

    ut.plot.set_axes_scaling_limits(subplot, property_log_scale, property_limits, prop_values)
    ut.plot.set_axes_scaling_limits(
        subplot, None, None, None, axis_y_log_scale, axis_y_limits, y_values
    )

    axis_x_label = ut.plot.Label.get_label(property_name, species_name=species_name, get_words=True)
    subplot.set_xlabel(axis_x_label)
    axis_y_label = ut.plot.Label.get_label(
        property_name, property_statistic, species_name, get_units=False
    )
    subplot.set_ylabel(axis_y_label)

    for part_i, part in enumerate(parts):
        subplot.plot(
            Stat.distr['bin.mid'][part_i],
            Stat.distr[property_statistic][part_i],
            color=color_names[part_i],
            alpha=0.8,
            label=part.info['simulation.name'],
        )

    ut.plot.make_legends(subplot, time_value=parts[0].snapshot['redshift'])

    if plot_file_name is True or plot_file_name == '':
        plot_file_name = ut.plot.get_file_name(
            property_name, 'distribution', species_name, snapshot_dict=part.snapshot
        )
    ut.plot.parse_output(plot_file_name, plot_directory)


# --------------------------------------------------------------------------------------------------
# ISM
# --------------------------------------------------------------------------------------------------
class ISMClass(ut.io.SayClass):
    '''
    .
    '''

    def get_positions_sampled(
        self,
        parts,
        species_name='gas',
        property_select={},
        part_indicess=None,
        radius_limits=[3, 12],
        height_limits=[-0.1, 0.1],
        coordinate_modifier='principal',
        host_index=0,
        dimension_number=3,
        sample_number=100,
    ):
        '''
        .
        '''
        if isinstance(parts, dict):
            parts = [parts]

        positionss = []

        for part_i, part in enumerate(parts):
            part_spec = part[species_name]

            part_indices = None
            if part_indicess is not None:
                part_indices = part_indicess[part_i]

            position_name, _velocity_name = ut.particle.parse_coordinate_names(
                host_index, coordinate_modifier
            )

            if property_select:
                part_indices = ut.catalog.get_indices_catalog(
                    part_spec, property_select, part_indices
                )

            positions_cyl = None

            if radius_limits is not None and len(radius_limits) > 0:
                if positions_cyl is None:
                    positions_cyl = part_spec.prop(f'{position_name}.cylindrical')
                part_indices = ut.array.get_indices(
                    positions_cyl[:, 0], radius_limits, part_indices
                )

            if height_limits is not None and len(height_limits) > 0:
                if positions_cyl is None:
                    positions_cyl = part_spec.prop(f'{position_name}.cylindrical')
                part_indices = ut.array.get_indices(
                    positions_cyl[:, 2], height_limits, part_indices
                )

            part_indices = np.random.choice(part_indices, sample_number)

            if positions_cyl is not None:
                R_med = np.median(positions_cyl[part_indices, 0])
                Z_med = np.median(np.abs(positions_cyl[part_indices, 2]))
                self.say('  R median = {:.2f} kpc'.format(R_med))
                self.say('|Z| median = {:.2f} kpc'.format(Z_med))

            positions = part_spec.prop(position_name, part_indices)

            if dimension_number == 2:
                positions = positions[:, [0, 1]]

            positionss.append(positions)

        return np.array(positionss)

    def get_velocity_dispersion_v_distance(
        self,
        center_positionss,
        parts,
        species_name='gas',
        property_select={},
        part_indicess=None,
        weight_by_mass=True,
        neig_number_max=300000,
        distance_limits=[0.001, 2],
        distance_bin_width=0.01,
        distance_log_scale=True,
        coordinate_modifier='principal',
        host_index=0,
        periodic=False,
    ):
        '''
        .
        '''
        if np.ndim(center_positionss) == 1:
            center_positionss = [center_positionss]

        if isinstance(parts, dict):
            parts = [parts]

        assert len(center_positionss) == len(parts)

        veldisp = {}
        for part_i, part in enumerate(parts):
            center_positions = center_positionss[part_i]

            part_indices = None
            if part_indicess is not None:
                part_indices = part_indicess[part_i]

            veldisp_p = ut.particle.get_velocity_dispersion_v_distance(
                center_positions,
                part,
                species_name,
                property_select,
                part_indices,
                weight_by_mass,
                neig_number_max,
                distance_limits,
                distance_bin_width,
                distance_log_scale,
                coordinate_modifier,
                host_index,
                periodic,
            )
            veldisp_p['simulation.name'] = part.info['simulation.name']

            ut.array.append_dictionary(veldisp, veldisp_p)

        return veldisp

        # self.plot_velocity_dispersion_v_distance(
        #    veldisp, species_name, distance_limits, distance_log_scale,
        # )

    def plot_velocity_dispersion_v_distance(
        self,
        veldisp,
        veldisp_2=None,
        veldisp_3=None,
        species_name='gas',
        distance_limits=[0.003, 2],
        distance_log_scale=True,
        veldisp_limits=[1, 100],
        veldisp_log_scale=True,
        veldisp_dimen_number=3,
        plot_file_name=False,
        plot_directory='.',
    ):
        '''
        .
        '''
        part_number = len(veldisp['distance'])
        selection_number = 1
        if veldisp_2 is not None:
            selection_number = 2
            if veldisp_3 is not None:
                selection_number = 3
            part_number = 1
        distance_limits = np.array(distance_limits) * ut.constant.kilo

        dimen_factor = 1.0
        if veldisp_dimen_number == 1:
            dimen_factor /= np.sqrt(3)

        # plot ----------
        _fig, subplot = ut.plot.make_figure(right=0.94)

        _axis_x_limits, _axis_y_limits = ut.plot.set_axes_scaling_limits(
            subplot,
            distance_log_scale,
            distance_limits,
            None,
            veldisp_log_scale,
            veldisp_limits,
        )

        # subplot.yaxis.set_minor_locator(ticker.AutoMinorLocator(10))

        subplot.set_xlabel('radius of sphere $r$ $\\left[ {{\\rm pc}} \\right]$')
        axis_y_label = '$\\sigma_{\\rm vel,3D}(< r)$ $\\left[ {{\\rm km/s}} \\right]$'
        if veldisp_dimen_number == 1:
            axis_y_label = axis_y_label.replace('3D', '1D')
        subplot.set_ylabel(axis_y_label)

        color_names = ut.plot.get_colors(max(part_number, selection_number))

        for pi in range(part_number):
            color = color_names[pi]

            if selection_number == 1:
                label = veldisp['simulation.name'][pi]
                label = label.replace('Msun', '${\\rm M}_\\odot$')
            else:
                label = 'all'

            subplot.fill_between(
                veldisp['distance'][0] * ut.constant.kilo,
                veldisp['cum.median.16'][pi] * dimen_factor,
                veldisp['cum.median.84'][pi] * dimen_factor,
                color=color,
                alpha=0.25,
                edgecolor=None,
            )
            subplot.plot(
                veldisp['distance'][0] * ut.constant.kilo,
                veldisp['cum.median.50'][pi] * dimen_factor,
                color=color,
                alpha=0.8,
                linestyle='-',
                label=label,
            )

            """
            label = veldisp['simulation.name'][pi] + ' average'
            subplot.fill_between(
                distances,
                veldisp['cum.average.16'][pi] * dimen_factor,
                veldisp['cum.average.84'][pi] * dimen_factor,
                color=color,
                alpha=0.4,
            )
            subplot.plot(
                distances,
                veldisp['cum.average.50'][pi] * dimen_factor,
                color=color,
                alpha=0.8,
                label=label,
                linestyle='--',
            )
            """

        if veldisp_2 is not None:
            pi = 0
            color = color_names[1]
            label = 'cold (T < 100 K)'
            subplot.fill_between(
                veldisp_2['distance'][0] * ut.constant.kilo,
                veldisp_2['cum.median.16'][pi] * dimen_factor,
                veldisp_2['cum.median.84'][pi] * dimen_factor,
                color=color,
                alpha=0.25,
                edgecolor=None,
            )
            subplot.plot(
                veldisp_2['distance'][0] * ut.constant.kilo,
                veldisp_2['cum.median.50'][pi] * dimen_factor,
                color=color,
                alpha=0.8,
                linestyle='-',
                label=label,
            )

        if veldisp_3 is not None:
            pi = 0
            color = color_names[2]
            label = 'star forming'
            subplot.fill_between(
                veldisp_3['distance'][0] * ut.constant.kilo,
                veldisp_3['cum.median.16'][pi] * dimen_factor,
                veldisp_3['cum.median.84'][pi] * dimen_factor,
                color=color,
                alpha=0.25,
                edgecolor=None,
            )
            subplot.plot(
                veldisp_3['distance'][0] * ut.constant.kilo,
                veldisp_3['cum.median.50'][pi] * dimen_factor,
                color=color,
                alpha=0.8,
                linestyle='-',
                label=label,
            )

        # power law relation
        ds = np.array([50, 1000])
        sigs = 5 * dimen_factor * np.ones(ds.size)
        sigs[1] = sigs[0] * (ds[1] / ds[0]) ** (1 / 2)
        subplot.plot(
            ds,
            sigs,
            color='black',
            alpha=0.6,
            linestyle=':',
            label='$\\sigma \\propto r^{1/2}$',
        )

        ut.plot.make_legends(subplot)

        if plot_file_name is True or plot_file_name == '':
            # property_y = 'disk.orientation'
            # plot_file_name = ut.plot.get_file_name(
            #    property_y, property_name, snapshot_dict=part.snapshot
            # )
            plot_file_name = f'{species_name}_veldisp_v_rad'
        ut.plot.parse_output(plot_file_name, plot_directory)


ISM = ISMClass()


# --------------------------------------------------------------------------------------------------
# star formation history
# --------------------------------------------------------------------------------------------------
class StarFormHistoryClass(ut.io.SayClass):
    '''
    .
    '''

    def plot_star_form_history(
        self,
        parts=None,
        sfh_name='form.rate',
        time_name='time.lookback',
        time_limits=[0, 13],
        time_width=0.2,
        time_log_scale=False,
        distance_limits=[0, 15],
        center_positions=None,
        host_index=0,
        property_select={},
        part_indicess=None,
        sfh_limits=None,
        sfh_log_scale=True,
        verbose=False,
        plot_file_name=False,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        Plot star-formation history v time_name.

        Parameters
        ----------
        parts : dict or list
            catalog[s] of particles
        sfh_name : str
            star form kind to plot: 'form.rate', 'form.rate.specific', 'mass', 'mass.normalized'
        time_name : str
            time kind to use: 'time', 'time.lookback', 'age', 'redshift', 'scalefactor'
        time_limits : list
            min and max limits of time_name to impose
        time_width : float
            width of time_name bin
        time_log_scale : bool
            whether to use logarithmic scaling for time bins
        distance_limits : list
            min and max limits of distance to select star particles
        center_positions : list or list of lists
            position[s] of galaxy centers [kpc comoving]
        host_index : int
            index of host galaxy/halo to get position of (if not input center_position)
        property_select : dict
            properties to select on: names as keys and limits as values
        part_indicess : array
            indices of particles from which to select
        sfh_limits : list
            min and max limits for y-axis
        sfh_log_scale : bool
            whether to use logarithmic scaling for SFH bins
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str
            directory to write figure file
        figure_index : int
            index of figure for matplotlib
        '''
        if isinstance(parts, dict):
            parts = [parts]

        center_positions = ut.particle.parse_property(
            parts, 'position', center_positions, host_index
        )
        part_indicess = ut.particle.parse_property(parts, 'indices', part_indicess)

        time_limits = np.array(time_limits)
        if None in time_limits:
            if time_name == 'redshift':
                if time_limits[0] is None:
                    time_limits[0] = np.floor(parts[0].snapshot[time_name])
                if time_limits[1] is None:
                    time_limits[1] = 7
            elif time_name == 'time':
                if time_limits[0] is None:
                    time_limits[0] = 0
                elif time_limits[1] is None:
                    time_limits[1] = parts[0].snapshot[time_name]
            elif time_name == 'time.lookback':
                if time_limits[0] is None:
                    time_limits[0] = 0
                elif time_limits[1] is None:
                    # time_limits[1] = 13.6  # [Gyr]
                    time_limits[1] = parts[0]['star'].prop('age').max()  # [Gyr]

        sfh = {}

        for part_i, part in enumerate(parts):
            sfh_p = self._get_star_form_history(
                part,
                time_name,
                time_limits,
                time_width,
                time_log_scale,
                distance_limits,
                center_positions[part_i],
                host_index,
                property_select,
                part_indicess[part_i],
            )

            if part_i == 0:
                for k in sfh_p:
                    sfh[k] = []  # initialize

            for k, s in sfh_p.items():
                sfh[k].append(s)

            if verbose:
                self.say(
                    'M_star max = {}'.format(
                        ut.io.get_string_from_numbers(sfh_p['mass'].max(), 2, exponential=True)
                    )
                )

        if time_name == 'redshift' and time_log_scale:
            time_limits += 1  # convert to z + 1 so log is well-defined

        # plot ----------
        left = None
        if 'specific' in sfh_name:
            left = 0.215
        _fig, subplot = ut.plot.make_figure(figure_index, left=left, axis_secondary='x')

        y_values = None
        if sfh is not None:
            y_values = sfh[sfh_name]

        ut.plot.set_axes_scaling_limits(
            subplot, time_log_scale, time_limits, None, sfh_log_scale, sfh_limits, y_values
        )

        axis_x_label = ut.plot.Label.get_label(time_name, get_words=True)
        subplot.set_xlabel(axis_x_label)

        if sfh_name == 'mass.normalized':
            axis_y_label = '$M_{\\rm star}(z) \\, / \\, M_{\\rm star}(z=0)$'
        else:
            axis_y_label = ut.plot.Label.get_label('star.' + sfh_name)
        subplot.set_ylabel(axis_y_label)

        ut.plot.make_axis_secondary_time(subplot, time_name, time_limits, parts[0].Cosmology)

        color_names = ut.plot.get_colors(len(parts))

        for part_i, part in enumerate(parts):
            tis = sfh[sfh_name][part_i] > 0
            if time_name in ['redshift', 'time.lookback', 'age']:
                tis *= sfh[time_name][part_i] >= parts[0].snapshot[time_name] * 0.99
            else:
                tis *= sfh[time_name][part_i] <= parts[0].snapshot[time_name] * 1.01
            subplot.plot(
                sfh[time_name][part_i][tis],
                sfh[sfh_name][part_i][tis],
                color=color_names[part_i],
                alpha=0.8,
                label=part.info['simulation.name'],
            )

        ut.plot.make_legends(subplot, time_value=parts[0].snapshot['redshift'])

        if plot_file_name is True or plot_file_name == '':
            time_value = None
            if time_name == 'redshift' and min(time_limits) > 1.1 * parts[0].snapshot['redshift']:
                time_value = min(time_limits)
            plot_file_name = ut.plot.get_file_name(
                sfh_name + '.history',
                time_name,
                'star',
                'redshift',
                parts[0].snapshot,
                time_value,
            )
        ut.plot.parse_output(plot_file_name, plot_directory)

    def plot_star_form_history_galaxies(
        self,
        part=None,
        hal=None,
        gal=None,
        mass_name='star.mass',
        mass_limits=[1e5, 1e9],
        property_select={},
        hal_indices=None,
        sfh_name='mass.normalized',
        sfh_limits=None,
        sfh_log_scale=False,
        time_name='time.lookback',
        time_limits=[13.7, 0],
        time_width=0.2,
        time_log_scale=False,
        plot_file_name=False,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        Plot star-formation history v time_name for multiple galaxies in a halo catalog.

        Parameters
        ----------
        part : dict
            catalog of particles
        hal : dict
            catalog of halos at snapshot
        gal : dict
            catalog of galaxies in the Local Group with SFHs
        mass_name : str
            mass kind by which to select halos
        mass_limits : list
            min and max limits to impose on mass_name
        property_select : dict
            properties to select on: names as keys and limits as values
        hal_indices : index or array
            index[s] of halo[s] whose particles to plot
        sfh_name : str
            star form kind to plot: 'rate', 'rate.specific', 'mass', 'mass.normalized'
        sfh_limits : list
            min and max limits for y axis
        sfh_log_scale : bool
            whether to use logarithmic scaling for y axis
        time_name : str
            time kind to plot: 'time', 'time.lookback', 'age', 'redshift'
        time_limits : list
            min and max limits of time_name to plot
        time_width : float
            width of time_name bin
        time_log_scale : bool
            whether to use logarithmic scaling for time bins
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str
            directory to write figure file
        figure_index : int
            index of figure for matplotlib
        '''
        time_limits = np.array(time_limits)
        if part is not None:
            if time_limits[0] is None:
                time_limits[0] = part.snapshot[time_name]
            if time_limits[1] is None:
                time_limits[1] = part.snapshot[time_name]

        sfh = None
        if hal is not None:
            if hal_indices is None or not len(hal_indices) > 0:
                hal_indices = ut.array.get_indices(hal.prop('star.number'), [2, Inf])

            if mass_limits is not None and len(mass_limits) > 0:
                hal_indices = ut.array.get_indices(hal.prop(mass_name), mass_limits, hal_indices)

            if property_select:
                hal_indices = ut.catalog.get_indices_catalog(hal, property_select, hal_indices)

            hal_indices = hal_indices[np.argsort(hal.prop(mass_name, hal_indices))]

            print(f'halo number = {hal_indices.size}')

            sfh = {}

            for hal_ii, hal_i in enumerate(hal_indices):
                part_indices = hal.prop('star.indices', hal_i)
                sfh_h = self._get_star_form_history(
                    part,
                    time_name,
                    time_limits,
                    time_width,
                    time_log_scale,
                    part_indices=part_indices,
                )

                if hal_ii == 0:
                    for k in sfh_h:
                        sfh[k] = []  # initialize

                for k, s in sfh_h.items():
                    sfh[k].append(s)

                string = 'id = {:8d}, star.mass = {:.3e}, particle.number = {}, distance = {:.0f}'
                self.say(
                    string.format(
                        hal_i,
                        sfh_h['mass'].max(),
                        part_indices.size,
                        hal.prop('host.distance', hal_i),
                    )
                )
                # print(hal.prop('position', hal_i))

            for k in sfh:
                sfh[k] = np.array(sfh[k])

            sfh['mass.normalized.median'] = np.median(sfh['mass.normalized'], 0)

        if time_name == 'redshift' and time_log_scale:
            time_limits += 1  # convert to z + 1 so log is well-defined

        # plot ----------
        _fig, subplot = ut.plot.make_figure(figure_index, axis_secondary='x')

        y_values = None
        if sfh is not None:
            y_values = sfh[sfh_name]

        ut.plot.set_axes_scaling_limits(
            subplot, time_log_scale, time_limits, None, sfh_log_scale, sfh_limits, y_values
        )

        subplot.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))

        axis_x_label = ut.plot.Label.get_label(time_name, get_words=True)
        subplot.set_xlabel(axis_x_label)

        if sfh_name == 'mass.normalized':
            axis_y_label = '$M_{\\rm star}(z) \\, / \\, M_{\\rm star}(z=0)$'
        else:
            axis_y_label = ut.plot.Label.get_label('star.' + sfh_name)
        subplot.set_ylabel(axis_y_label)

        ut.plot.make_axis_secondary_time(subplot, time_name, time_limits, part.Cosmology)

        if hal is not None:
            color_names = ut.plot.get_colors(len(hal_indices))
        elif gal is not None:
            color_names = ut.plot.get_colors(len(gal.sfh))

        label = None

        # draw observed galaxies
        if gal is not None:
            import string

            gal_names = np.array(list(gal.sfh.keys()))
            gal_indices = [gal['name.to.index'][gal_name] for gal_name in gal_names]
            gal_names_sort = gal_names[np.argsort(gal['star.mass'][gal_indices])]

            for gal_i, gal_name in enumerate(gal_names_sort):
                linestyle = '-'
                if hal is not None:
                    color = 'black'
                    linewidth = 1.0 + 0.25 * gal_i
                    alpha = 0.2
                    label = None
                else:
                    color = color_names[gal_i]
                    linewidth = 1.25 + 0.25 * gal_i
                    alpha = 0.45
                    label = string.capwords(gal_name)
                    label = label.replace('Canes Venatici I', 'CVn I').replace('Ii', 'II')

                    print(label)
                subplot.plot(
                    gal.sfh[gal_name][time_name],
                    gal.sfh[gal_name][sfh_name],
                    linewidth=linewidth,
                    linestyle=linestyle,
                    alpha=alpha,
                    color=color,
                    label=label,
                )

        # draw simulated galaxies
        if hal is not None:
            label = '$M_{{\\rm star}}=$'
            subplot.plot(-1, -1, label=label)
            for hal_ii, hal_i in enumerate(hal_indices):
                linewidth = 2.5 + 0.1 * hal_ii
                # linewidth = 3.0
                mass = ut.io.get_string_from_numbers(sfh['mass'][hal_ii][-1], 1, exponential=True)
                label = f'${mass}\,{{\\rm M}}_\\odot$'
                subplot.plot(
                    sfh[time_name][hal_ii],
                    sfh[sfh_name][hal_ii],
                    linewidth=linewidth,
                    color=color_names[hal_ii],
                    alpha=0.55,
                    label=label,
                )

        # subplot.plot(sfh['time'][0], sfh['mass.normalized.median'],
        #             linewidth=4.0, color='black', alpha=0.5)

        ut.plot.make_legends(subplot, time_value=part.snapshot['redshift'])

        if plot_file_name is True or plot_file_name == '':
            snapshot_dict = None
            if part is not None:
                snapshot_dict = part.snapshot
            time_name_file_name = 'redshift'
            if hal is None:
                time_name_file_name = None
            host_distance_limits = None
            if 'host.distance' in property_select:
                host_distance_limits = property_select['host.distance']

            plot_file_name = ut.plot.get_file_name(
                sfh_name,
                time_name,
                'star',
                time_name_file_name,
                snapshot_dict,
                host_distance_limits=host_distance_limits,
            )
            if gal is not None:
                plot_file_name += '_lg'
        ut.plot.parse_output(plot_file_name, plot_directory)

    def _get_star_form_history(
        self,
        part,
        time_name='redshift',
        time_limits=[0, 8],
        time_width=0.1,
        time_log_scale=False,
        distance_limits=None,
        center_position=None,
        host_index=0,
        property_select={},
        part_indices=None,
    ):
        '''
        Get array of times and star-formation rate at each time.

        Parameters
        ----------
        part : dict
            catalog of particles
        time_name : str
            time metric to use: 'time', 'time.lookback', 'age', 'redshift', 'scalefactor'
        time_limits : list
            min and max limits of time_name to impose
        time_width : float
            width of time_name bin (in units set by time_scaling)
        time_log_scale : bool
            whether to use logarithmic scaling for time bins
        distance_limits : list
            min and max limits of galaxy distance to select star particles
        center_position : list
            position of galaxy centers [kpc comoving]
        host_index : int
            index of host galaxy/halo to get position of (if not input it)
        property_select : dict
            dictionary with property names as keys and limits as values
        part_indices : array
            indices of star particles to select

        Returns
        -------
        sfh : dictionary
            arrays of SFH properties
        '''
        species = 'star'

        if part_indices is None:
            part_indices = ut.array.get_arange(part[species]['mass'])

        if property_select:
            part_indices = ut.catalog.get_indices_catalog(
                part['star'], property_select, part_indices
            )

        center_position = ut.particle.parse_property(part, 'position', center_position, host_index)

        if (
            center_position is not None
            and len(center_position) > 0
            and distance_limits is not None
            and len(distance_limits) > 0
            and (min(distance_limits) > 0 or max(distance_limits) < np.inf)
        ):
            distances = ut.coordinate.get_distances(
                part['star']['position'][part_indices],
                center_position,
                part.info['box.length'],
                part.snapshot['scalefactor'],
                total_distance=True,
            )  # [kpc physical]
            part_indices = part_indices[ut.array.get_indices(distances, distance_limits)]

        # get formation times of star particles, sorted from earliest
        part_indices_sort = part_indices[np.argsort(part[species].prop('form.time', part_indices))]
        form_times = part[species].prop('form.time', part_indices_sort)
        # avoid precision error with cumsum below
        form_masses = part[species].prop('form.mass', part_indices_sort).astype(np.float64)
        current_masses = part[species]['mass'][part_indices_sort].astype(np.float64)

        # get time bins, ensure are ordered from earliest
        time_dict = part.Cosmology.get_time_bins(time_name, time_limits, time_width, time_log_scale)
        time_bins = np.sort(time_dict['time'])
        time_difs = np.diff(time_bins)

        form_mass_cum_bins = np.interp(time_bins, form_times, np.cumsum(form_masses))
        form_mass_difs = np.diff(form_mass_cum_bins)
        form_rate_bins = form_mass_difs / time_difs / ut.constant.giga  # convert to [M_sun / yr]

        current_mass_cum_bins = np.interp(time_bins, form_times, np.cumsum(current_masses))
        current_mass_difs = np.diff(current_mass_cum_bins)

        # convert to midpoints of bins
        current_mass_cum_bins = (
            current_mass_cum_bins[: current_mass_cum_bins.size - 1] + 0.5 * current_mass_difs
        )
        form_mass_cum_bins = (
            form_mass_cum_bins[: form_mass_cum_bins.size - 1] + 0.5 * form_mass_difs
        )

        for k in time_dict:
            time_dict[k] = time_dict[k][: time_dict[k].size - 1] + 0.5 * np.diff(time_dict[k])

        # ensure that ordering jives with ordering of input limits
        if time_dict['time'][0] > time_dict['time'][1]:
            form_rate_bins = form_rate_bins[::-1]
            current_mass_cum_bins = current_mass_cum_bins[::-1]
            form_mass_cum_bins = form_mass_cum_bins[::-1]

        sfh = {}
        for k in time_dict:
            sfh[k] = time_dict[k]
        sfh['form.rate'] = form_rate_bins
        sfh['form.rate.specific'] = form_rate_bins / form_mass_cum_bins
        sfh['mass'] = current_mass_cum_bins
        sfh['mass.normalized'] = current_mass_cum_bins / current_mass_cum_bins.max()
        sfh['particle.number'] = form_times.size

        return sfh


StarFormHistory = StarFormHistoryClass()


# --------------------------------------------------------------------------------------------------
# analysis across time
# --------------------------------------------------------------------------------------------------
def plot_galaxy_property_v_time(
    gals=None,
    sfhs=None,
    Cosmology=None,
    property_name='star.mass',
    time_name='redshift',
    time_limits=[0, 8],
    time_log_scale=False,
    snapshot_subsample_factor=1,
    axis_y_limits=None,
    axis_y_log_scale=True,
    plot_file_name=False,
    plot_directory='.',
    figure_index=1,
):
    '''
    Plot host galaxy property v time_name, using tabulated dictionary of properties of progenitor
    across snapshots.

    Parameters
    ----------
    gals : dict
        tabulated dictionary of host galaxy properties
    sfhs : dict
        tabulated dictinnary of star-formation histories (computed at single snapshot)
    property_name : str
        name of star formation history property to plot:
            'rate', 'rate.specific', 'mass', 'mass.normalized'
    time_name : str
        time kind to use: 'time', 'time.lookback', 'redshift'
    time_limits : list
        min and max limits of time_name to get
    time_log_scale : bool
        whether to use logarithmic scaling for time bins
    snapshot_subsample_factor : int
        factor by which to sub-sample snapshots from gals
    axis_y_limits : list
        min and max limits for y axis
    axis_y_log_scale : bool
        whether to use logarithmic scaling for y axis
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory to write figure file
    figure_index : int
        index of figure for matplotlib
    '''
    # Say = ut.io.SayClass(plot_galaxy_property_v_time)

    if gals is not None and isinstance(gals, dict):
        gals = [gals]

    if sfhs is not None and isinstance(sfhs, dict):
        sfhs = [sfhs]

    time_limits = np.array(time_limits)
    if time_limits[0] is None:
        time_limits[0] = gals[0][time_name].min()
    if time_limits[1] is None:
        time_limits[1] = gals[0][time_name].max()

    if time_name == 'redshift' and time_log_scale:
        time_limits += 1  # convert to z + 1 so log is well-defined

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    y_values = []
    if gals is not None:
        y_values.append(gals[0][property_name])
    if sfhs is not None:
        y_values.append(sfhs[0][time_name])
    subplot.set_ylim(ut.plot.get_axis_limits(y_values, axis_y_log_scale, axis_y_limits))

    axis_y_label = ut.plot.Label.get_label('star.mass')
    subplot.set_ylabel(axis_y_label)

    ut.plot.make_axis_secondary_time(subplot, time_name, time_limits, Cosmology)

    # colors = ut.plot.get_colors(len(gals))

    if gals is not None:
        for _gal_i, gal in enumerate(gals):
            subplot.plot(
                gal[time_name][::snapshot_subsample_factor],
                gal[property_name][::snapshot_subsample_factor],
                linewidth=3.0,
                alpha=0.9,
                # color=colors[gal_i],
                color=ut.plot.get_color('blue.mid'),
                label='main progenitor',
            )

    if sfhs is not None:
        for _sfh_i, sfh in enumerate(sfhs):
            subplot.plot(
                sfh[time_name],
                sfh['mass'],
                '--',
                linewidth=3.0,
                alpha=0.9,
                # color=colors[sfh_i],
                color=ut.plot.get_color('orange.mid'),
                label='SFH computed at $z=0$',
            )

    ut.plot.make_legends(subplot)

    if plot_file_name is True or plot_file_name == '':
        plot_file_name = f'galaxy_{property_name}_v_{time_name}'
    ut.plot.parse_output(plot_file_name, plot_directory)
