#! /bin/bash

: '''
Move planet files to flat system in specified output directory.  Make sure you have unzipped the .zip file and are in the same directory where unzipped outputs go.

    Usage: bash ~/ghw2019_planetpieces/scripts/collapse_files.sh path_to_output_directory

'''

set -e

# This is the output directory where the tifs and xmls will be sent
out_directory=$1

for img in $(find . -iname '*.tif') ; do mv $img $out_directory/ ; done
for img in $(find . -iname '*.xml') ; do mv $img $out_directory/ ; done