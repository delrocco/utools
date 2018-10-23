#!/usr/bin/python
# -*- coding: utf-8 -*-
# ====================================================================
# @author: Joe Del Rocco
# @since: 10/17/2018
# @summary: Script to fit poly to points and find inverse fit.
# ====================================================================
import numpy as np


def main():
    # fit polynomial to the specified points
    x = np.array([0, 0.25, 0.5, 0.75, 1, 1.25, 1.5])
    #y = np.array([0, 0.17931912, 0.35597335, 0.5271127, 0.68979342, 0.840978, 0.97753519])
    y = np.array([0, 0.18567305, 0.36590625, 0.53705742, 0.6963, 0.84162305, 0.97183125])
    z = np.polyfit(x, y, 4)
    print(z)

    # find inverse fit
    t = x
    x = y
    y = t
    z = np.polyfit(x, y, 4)
    print(z)

if __name__ == "__main__":
    main()