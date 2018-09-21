#!/usr/bin/env python
# ====================================================================
# Copyright (c) 2018 Joe Del Rocco
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ====================================================================
# @author: Joe Del Rocco
# @since: 09/17/2018
# @summary: Script to resize dir of images.
# ====================================================================
import os, sys
import argparse
from PIL import Image


def resizeImages(args):
    for fname in os.listdir(args.dir):
        r,ext = os.path.splitext(fname)
        if ext.lower() != ".jpg":
            continue

        filein = os.path.join(args.dir, fname)
        fileout = os.path.join(args.dirout, fname)

        try:
            img = Image.open(filein)
            if img.width > img.height:
                img = img.resize(args.dim, Image.ANTIALIAS)
            else:
                img = img.resize(args.dimrot, Image.ANTIALIAS)
            img.save(fileout, 'JPEG', quality=args.quality)
        except IOError:
            print("Error: could not resize: " + filein)

def main():
    # handle command line args
    parser = argparse.ArgumentParser(description='Script to resize a directory of images (respecting dimensions with rotation).', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_help = True
    parser.add_argument('dir', help='a directory of images')
    parser.add_argument('-d', '--dim', dest='dim', type=int, nargs=2, default=(1024,768), help='dimensions as ints (def 1024 768)')
    parser.add_argument('-q', '--quality', dest='quality', type=int, default=90, help='quality 1-95 (def 90)')
    args = parser.parse_args()

    # dir not found
    if not os.path.exists(args.dir):
        print("Error: no directory found: '" + args.dir + "'")
        sys.exit(2)

    # ensure dimensions are tuple
    if isinstance(args.dim, list):
        args.dim = tuple(args.dim)
    args.dimrot = (args.dim[1], args.dim[0])

    # create output dir if necessary
    args.dirout = os.path.join(args.dir, "resized")
    if not os.path.exists(args.dirout):
        os.makedirs(args.dirout)

    # do it
    resizeImages(args)

if __name__ == "__main__":
    main()
