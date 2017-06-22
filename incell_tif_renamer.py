#!/Users/daniellefever/anaconda/bin/python
# -*- coding: utf-8 -*-


from __future__ import division

import os
import subprocess
import argparse


def incell_tif_renamer(tif_dir, out_dir):
    #cur_files = os.listdir(tif_dir)
    cur_files = [os.path.join(os.path.abspath(tif_dir), i) for i in os.listdir(tif_dir)]
    for i in cur_files:
        '''
        This function renames the incell image names to
        remove whitespace and weird parens.
        '''
        if i.split('.')[-1] == 'tif':
            space_sep_tit = i.split('.')[0].split()
            new_tit = 'field'
            for word in space_sep_tit[3:]:
                new_tit = new_tit + '_' + word
            new_tit = new_tit.strip('\)')
            new_tit = new_tit.strip('_') + '.tif'
            final_tit = out_dir + '/' + new_tit
            #out_str = 'cp ' + '\"' + i +'\"' + ' ' + final_tit + '; rm \"' + i +'\"'
            out_str = 'cp ' + '\"' + i +'\"' + ' ' + final_tit
            subprocess.check_call((out_str), shell=True)

def auto_folders_namer(inpath, out_str):
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
