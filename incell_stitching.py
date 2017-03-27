from __future__ import division

import os
import argparse

#bf_dir = '/Users/daniellefever/Desktop/Lans_Taylor_Lab/projects/NAFLD_MPS/wet_lab/experiments/170306_experiment/170309_images/incell_images/VPR_BiosAcq_apoptosis_mKate_160810/VPR_BiosAcq_apoptosis_mKate_160810_day6dev1_2017.03.13.15.58.20/renamed_pics/brightfield'
#fitc_dir = '/Users/daniellefever/Desktop/Lans_Taylor_Lab/projects/NAFLD_MPS/wet_lab/experiments/170306_experiment/170309_images/incell_images/VPR_BiosAcq_apoptosis_mKate_160810/VPR_BiosAcq_apoptosis_mKate_160810_day6dev1_2017.03.13.15.58.20/renamed_pics/fitc'
#dsred_dir = '/Users/daniellefever/Desktop/Lans_Taylor_Lab/projects/NAFLD_MPS/wet_lab/experiments/170306_experiment/170309_images/incell_images/VPR_BiosAcq_apoptosis_mKate_160810/VPR_BiosAcq_apoptosis_mKate_160810_day6dev1_2017.03.13.15.58.20/renamed_pics/dsred'

#bf_string = 'run(\"Grid/Collection stitching\", \"type=[Grid: row-by-row] order=[Right & Down                ] grid_size_x=8 grid_size_y=3 tile_overlap=1 first_file_index_i=1 directory=%s file_names=field_{ii}_wv_TL-Brightfield_-_dsRed.tif output_textfile_name=TileConfiguration.txt fusion_method=[Linear Blending] regression_threshold=0.30 max/avg_displacement_threshold=2.50 absolute_displacement_threshold=3.50 computation_parameters=[Save computation time (but use more RAM)] image_output=[Fuse and display]\");' % (bf_dir)

#fitc_string = 'run(\"Grid/Collection stitching\", \"type=[Grid: row-by-row] order=[Right & Down                ] grid_size_x=8 grid_size_y=3 tile_overlap=1 first_file_index_i=1 directory=%s file_names=field_{ii}_wv_Blue_-_FITC.tif output_textfile_name=TileConfiguration.txt fusion_method=[Linear Blending] regression_threshold=0.30 max/avg_displacement_threshold=2.50 absolute_displacement_threshold=3.50 computation_parameters=[Save computation time (but use more RAM)] image_output=[Fuse and display]\");' % (fitc_dir)

#fitc_string_z_stack = 'run(\"Grid/Collection stitching\", \"type=[Grid: row-by-row] order=[Right & Down                ] grid_size_x=8 grid_size_y=3 tile_overlap=1 first_file_index_i=1 directory=%s file_names=field_{ii}_wv_Blue_-_FITC_z_%i.tif output_textfile_name=TileConfiguration.txt fusion_method=[Linear Blending] regression_threshold=0.30 max/avg_displacement_threshold=2.50 absolute_displacement_threshold=3.50 computation_parameters=[Save computation time (but use more RAM)] image_output=[Fuse and display]\");' % (fitc_dir, ind_num)

#save_fitc_image = 'saveAs("Tiff", %s);' % (image_name)


#dsred_string = 'run(\"Grid/Collection stitching\", \"type=[Grid: row-by-row] order=[Right & Down                ] grid_size_x=8 grid_size_y=3 tile_overlap=1 first_file_index_i=1 directory=%s file_names=field_{ii}_wv_Green_-_dsRed.tif output_textfile_name=TileConfiguration.txt fusion_method=[Linear Blending] regression_threshold=0.30 max/avg_displacement_threshold=2.50 absolute_displacement_threshold=3.50 computation_parameters=[Save computation time (but use more RAM)] image_output=[Fuse and display]\");' % (dsred_dir)

def fiji_formatted_filenames(outpath, stack_size=11):

        file_list = []
        for stack_num in range(stack_size +1)[1:]:


            #fitc_form = os.path.join(inpath, 'field_{ii}_wv_Blue_-_FITC_z_%02d.tif' % (stack_num)) #sloppy but works
            fitc_form = 'field_{ii}_wv_Blue_-_FITC_z_%02d.tif' % (stack_num)
            fitc_stitched_filename = os.path.join(outpath,
                                                  'fitc_stiched_z_%02d.tif' % (stack_num))
            #dsred_form = os.path.join(inpath, 'field_{ii}_wv_Green_-_dsRed_z_%02d.tif' % (stack_num))
            dsred_form = 'field_{ii}_wv_Green_-_dsRed_z_%02d.tif' % (stack_num)
            dsred_stitched_filename = os.path.join(outpath,
                                                   'dsred_stiched_z_%02d.tif' % (stack_num))
            file_list.append((fitc_form, fitc_stitched_filename))
            file_list.append((dsred_form, dsred_stitched_filename))

        return file_list

def macro_generator(inpath, fff_list, fiji_ijm='fiji_commands.ijm'):
    with open(fiji_ijm, 'w+') as f:

        for fiji_file_string, out_file_string in fff_list:
            stitching_string = 'run(\"Grid/Collection stitching\", \"type=[Grid: row-by-row] order=[Right & Down                ] grid_size_x=3 grid_size_y=6 tile_overlap=0 first_file_index_i=1 directory=%s file_names=%s output_textfile_name=TileConfiguration.txt fusion_method=[Linear Blending] regression_threshold=0.30 max/avg_displacement_threshold=2.50 absolute_displacement_threshold=3.50 computation_parameters=[Save computation time (but use more RAM)] image_output=[Fuse and display]\");' % (inpath, fiji_file_string)

            save_fitc_image = 'saveAs("Tiff", \"%s\");' % (out_file_string) # kludge to get shit to work

            f.write(stitching_string + '\n' +  save_fitc_image + '\n' + 'close();' + '\n')


        #fused_image_name = os.path.join(outpath, ('dsred_stiched_z_%02d.tif') % (i))



def main():
    parser = argparse.ArgumentParser()
    req = parser.add_argument_group('required arguments')
    opt = parser.add_argument_group('optional arguments')

    req.add_argument('-i',
        help = 'input dir of renamed_files',
        metavar = '',
        required=True)
    opt.add_argument('-o',
        default = 'processed_images',
        help='output directory (Default: processed_images)',
        metavar='')
    args = parser.parse_args()

    inpath = os.path.abspath(args.i)

    if not os.path.exists(args.o):
        os.makedirs(args.o)

    outpath = os.path.abspath(args.o)
        


    fff_list = fiji_formatted_filenames(outpath)
    macro_generator(inpath, fff_list)
if __name__ == '__main__':
    main()