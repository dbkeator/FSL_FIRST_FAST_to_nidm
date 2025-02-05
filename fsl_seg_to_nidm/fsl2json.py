#!/usr/bin/env python3
#
# Export FSL FIRST/FAST statistics to JSON
#
# FIRST and FAST were run in the same directory per subject
#   with default settings
# Expecting derivaties\fsl\sub-0x\*_firstseg.nii.gz
#   derivaties\fsl\sub-0x\*pve*.nii.gz
# Creating derivaties\fsl\sub-0x\segstats.json
# Run the script from top of FSL derivative folder
# Assumption that FIRST was run with a brain-stripped
#   image and a "_brain" suffix e.g. sub-001_T1W_brain.nii.gz
# Version: 15 Jan 2025

import json, os, argparse, glob
from nipype.interfaces.fsl import ImageStats

#%% Parser
parser_features = argparse.ArgumentParser(
    description='Export FSL FIRST/FAST statistics to json',
    epilog='''
        Example usage: python fsl2json.py /path/to/fsl_derivatives
        ''')
parser_features.add_argument('indir',
                    metavar='o',
                    type=str,
                    help='the path to the FSL derivatives folder')
args_features = parser_features.parse_args()

def fast_stats(roi, infile):
    stats = ImageStats()
    stats.inputs.in_file = infile
    stats.inputs.op_string = '-V'
    result = stats.run()
    voxels = round(result.outputs.out_stat[0])
    volume = round(result.outputs.out_stat[1], 1)
    return voxels, volume

FIRST_dict = {'Background': 0,
                'Left-Thalamus-Proper': 10,
                'Left-Caudate': 11,
                'Left-Putamen': 12,
                'Left-Pallidum': 13,
                'Left-Hippocampus': 17,
                'Left-Amygdala': 18,
                'Left-Accumbens-area': 26,
                'Right-Thalamus-Proper': 49,
                'Right-Caudate': 50,
                'Right-Putamen': 51,
                'Right-Pallidum': 52,
                'Right-Hippocampus': 53,
                'Right-Amygdala': 54,
                'Right-Accumbens-area': 58}
FAST_dict = {'csf': 0,
             'gray': 1,
             'white': 2}

wkdir = args_features.indir
os.chdir(wkdir)
subj_list = (glob.glob('sub-*'))

for subj in subj_list:
    print('##### Processing ' + subj + '#####')
    infile = wkdir + '/' + subj + '/' + subj + '_T1w_brain_all_fast_firstseg.nii.gz'
    outfile = wkdir + '/' + subj + '/segstats.json'
    stats = ImageStats()
    stats.inputs.in_file = infile
    results_dict = {}

    ## FIRST results
    for roi,thresh in FIRST_dict.items():
        print('The ' + roi + ' ROI has a threshold of ' + str(thresh))
        if thresh == 0:
            l_thresh = 0
        else:
            l_thresh = thresh - 0.5
        u_thresh = thresh + 0.5
        stats.inputs.op_string = '-l ' + str(l_thresh) + ' -u ' + str(u_thresh) + ' -V'
        result = stats.run()
        voxels = round(result.outputs.out_stat[0])
        volume = round(result.outputs.out_stat[1], 1)
        results_dict[roi] = voxels, volume
    ## FAST results
    for roi,pve in FAST_dict.items():
        print('Partial volume estimation for ' + roi)
        infile = wkdir + '/' + subj + '/' + subj + '_T1w_brain_pve_' + str(pve) + '.nii.gz'
        results_dict[roi] = fast_stats(roi,infile)
    ## Dump to JSON
    with open(outfile, 'w') as convert_file: 
        convert_file.write(json.dumps(results_dict, indent = 4))

print('Complete!')
