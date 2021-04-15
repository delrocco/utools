#!/usr/bin/python
# -*- coding: utf-8 -*-
# ====================================================================
# @authors: Joe Del Rocco
# @since: 4/12/2021
# @summary: Script to produce a colorbar given some parameters...
# ====================================================================
import argparse
import matplotlib.pyplot as plt
import matplotlib as mpl


def main():
    # handle command line args
    parser = argparse.ArgumentParser(description='Script to produce a colorbar only figure.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_help = True
    parser.add_argument('-v', '--vertical', dest='vertical', action='store_true', default=False, help='vertical?')
    parser.add_argument('-l', '--label', dest='label', type=str, default='', help='text string label')
    parser.add_argument('-b', '--bounds', dest='bounds', type=float, nargs='*', default=[0, 100], help='bounds [min, max]')
    parser.add_argument('-c', '--colors', dest='colors', type=str, nargs='*', default=['#000000', '#00ff00'], help='list of colors')
    parser.add_argument('-f', '--filename', dest='filename', type=str, default='colorbar', help='saved as this name')
    parser.add_argument('-x', '--extension', dest='extension', type=str, default='pdf', help='saved w/ this extension')
    args = parser.parse_args()

    # configure matplotlib
    params = {'legend.fontsize': 'large',
              'axes.labelsize': 'large',
              'axes.titlesize': 'x-large',
              'xtick.labelsize': 'medium',
              'ytick.labelsize': 'large'}
    plt.rcParams.update(params)
    # plt.locator_params(axis="x", integer=True)

    # colormaps for colors for false color renders
    #cmap = plt.get_cmap("viridis")
    #cmap = plt.cm.cool
    #cmap = plt.get_cmap("Blues_r")
    #cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["blue", "white", "red"])
    #cmap = ReNormColormapAdaptor(mpl.cm.jet, mpl.colors.LogNorm(0, maxrad))
    #cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["mediumblue", "white", "xkcd:fire engine red"])

    # check orientation
    if args.vertical:
        args.orientation = 'vertical'
        args.rotation = 'horizontal'
        args.szfig = (1, 3)
        args.szaxis = [0, 0, 0.25, 1.0]
    else:
        args.orientation = 'horizontal'
        args.rotation = 'vertical'
        args.szfig = (3, 1)
        args.szaxis = [0, 0, 1, 0.25]

    # do it!
    cmap = mpl.colors.LinearSegmentedColormap.from_list("", args.colors)
    fig = plt.figure(figsize=args.szfig)
    ax1 = fig.add_axes(args.szaxis)
    norm = mpl.colors.Normalize(vmin=args.bounds[0], vmax=args.bounds[1])
    cb = mpl.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm, orientation=args.orientation)
    cb.ax.set_yticklabels(cb.ax.get_yticklabels(), rotation=args.rotation)
    cb.set_label(args.label)
    fig.savefig(args.filename + '.' + args.extension, dpi=600, bbox_inches='tight', pad_inches=0)


if __name__ == "__main__":
    main()
