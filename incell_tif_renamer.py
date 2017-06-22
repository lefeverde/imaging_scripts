#!/Users/daniellefever/anaconda/bin/python
# -*- coding: utf-8 -*-


from __future__ import division

import os
import subprocess
import argparse
import re


def incell_tif_renamer(tif_dir, out_dir='renamed_images'):
    '''
    This function takes a dir of tifs produced by the incell
    and removes whitespace from the file names and puts them
    into a new dir.

    Right now, whitespace is simply removed and
    other formatting is done.
    '''
    cur_files = os.listdir(tif_dir)
    cur_dir_path = os.path.abspath(tif_dir)
    for i in cur_files:

        cur_file_path = os.path.join(cur_dir_path, i)
        if i.split('.')[-1] == 'tif':
            space_sep_tit = i.split('.')[0].split()
            new_tit = re.sub('\(|\)' ,'_',''.join(space_sep_tit) + '.tif')
            out_path = os.path.join(cur_dir_path, out_dir)
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            out_handle = os.path.join(out_path, new_tit)
            out_str = 'cp ' + '\"' + cur_file_path +'\"' + ' ' + out_handle
            subprocess.check_call((out_str), shell=True)

def auto_folders_namer(inpath, out_str):
    # TODO use os.walk to automagically go Down
    # a dir tree
    '''
    Function to automatically name folders by
    getting the important info from the input
    dir(s)
    '''
    device_name, image_date = os.path.abspath(inpath).split('_')[-2:]
    fixed_image_date = '_'.join(image_date.split('.')[0:3])
    out_dir_handle = device_name + '_' + fixed_image_date + '_' + out_str
    outpath = os.path.join(inpath, out_dir_handle)
    return(outpath)


def main():

    parser = argparse.ArgumentParser()
    req = parser.add_argument_group('required arguments')
    opt = parser.add_argument_group('optional arguments')


    req.add_argument('-i',
                     help = 'input dir of incell tif files',
                     metavar = '',
                     required=True)
    opt.add_argument('-o',
                     default = 'renamed_tif_files',
                     help='output directory (Default: renamed_tif_files)',
                     metavar='')

    opt.add_argument('-dir',
                     action='store_true',
                     help='parameter which changes input to a dir of dirs')
    args = parser.parse_args()

    #inpath = args.i
    full_inpath = [os.path.join(os.path.abspath(args.i), i) for i in os.listdir(args.i)]
    #device_name, image_date = os.path.abspath(args.i).split('_')[-2:]
    #fixed_image_date = '_'.join(image_date.split('.')[0:3])
    #out_dir_handle = device_name + '_' + fixed_image_date + '_' + args.o
    print(full_inpath)
    for cur_dir in full_inpath:
        try:
            out_dir_handle = auto_folders_namer(cur_dir, args.o)
            if not os.path.exists(out_dir_handle):
                os.makedirs(out_dir_handle)

            outpath = os.path.abspath(out_dir_handle)

            incell_tif_renamer(cur_dir, outpath)
        except:
            continue

if __name__ == '__main__':
    main()
