from __future__ import division

import os
import subprocess
import argparse


def incell_tif_renamer(tif_dir, out_dir):
    cur_files = os.listdir(tif_dir)
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
            out_str = 'cp ' + '\"' + i +'\"' + ' ' + final_tit
            subprocess.check_call((out_str), shell=True)

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
    args = parser.parse_args()

    inpath = args.i
    if not os.path.exists(args.o):
        os.makedirs(args.o)
    incell_tif_renamer(args.i, args.o)

if __name__ == '__main__':
    main()
