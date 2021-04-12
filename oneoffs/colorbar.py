#!/usr/bin/python
# -*- coding: utf-8 -*-
# ====================================================================
# @authors: Joe Del Rocco
# @since: 4/12/2021
# @summary: Script to produce a colorbar given some parameters...
# ====================================================================
import argparse
#import os
#import sys
#import math
import matplotlib.pyplot as plt
import matplotlib as mpl


'''
Entry point
'''
def main():
    # # handle command line args
    # parser = argparse.ArgumentParser(description='Framework for machine learning sky radiance sample datasets.', formatter_class=argparse.RawTextHelpFormatter)
    # parser.add_help = True
    # # required parameters (either as args or config file)
    # parser.add_argument('-p', '--photo', dest='photo', type=str, help='path to fisheye sky photo')
    # parser.add_argument('-m', '--model', dest='model', type=str, help='path to ml model')
    # parser.add_argument('-t', '--timestamp', dest='timestamp', type=str, help='datetime of capture (00/00/0000 00:00)')
    # parser.add_argument('-c', '--cover', dest='cover', type=int, help='sky cover (1=UNK, 2=CLR, 3=SCT, 4=OVC)')
    # # optional parameters
    # parser.add_argument('-s', '--scaler', dest='scaler', type=str, help='path to ml model scaler')
    # parser.add_argument('-y', '--polynomial', dest='polynomial', type=int, help='polynomial feature expansion')
    # parser.add_argument('-g', '--grayscale', dest='grayscale',action='store_true', help='generate grayscale map')
    # parser.add_argument('-v', '--visible', dest='visible', action='store_true', help='generate visible spectrum map')
    # parser.add_argument('-b', '--colorbar', dest='colorbar', action='store_true', help='export colorbar as well')
    # parser.add_argument('-x', '--export', dest='export', action='store_true', help='export predictions to file')
    # parser.add_argument('-l', '--log', dest='log', action='store_true', help='log progress to stdout and file')
    # args = parser.parse_args()

    # configure matplotlib
    params = {'legend.fontsize': 'x-large',
              'axes.labelsize': 'x-large',
              'axes.titlesize': 'xx-large',
              'xtick.labelsize': 'large',
              'ytick.labelsize': 'x-large'}
    plt.rcParams.update(params)

    # colormaps for colors for false color renders
    #cmap = plt.get_cmap("viridis")
    #cmap = plt.cm.cool
    #cmap = plt.get_cmap("Blues_r")
    #cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["blue", "white", "red"])
    #cmap = ReNormColormapAdaptor(mpl.cm.jet, mpl.colors.LogNorm(0, maxrad))
    #cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["mediumblue", "white", "xkcd:fire engine red"])
    cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["black", "#ffff00"])

    # save colorbar to file
    fig = plt.figure(figsize=(1, 3))
    ax1 = fig.add_axes([0, 0, 0.25, 1.0])
    norm = mpl.colors.Normalize(vmin=0, vmax=78.0318) # maxrad
    cb = mpl.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm, orientation='vertical')
    cb.set_label('Irradiance ($W/m^2$)')
    fig.savefig("colorbar.png", dpi=600, bbox_inches='tight')


if __name__ == "__main__":
    main()
