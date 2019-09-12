#! /bin/bash

: '''
This script converts all Planet *Analytic.tif radiance files located with the XML files to SCALED TOA reflectance - these will need to be divided by 10,000 to obtain proper reflectance values (currently stored as UINT16 from Planet docs).

    Usage: bash ~/ghw2019_planetpieces/scripts/convert_refl.sh path_to_output_directory

'''

set -e

out_directory=$1

for f in $(find ${out_directory} -iname "*Analytic.tif") ; do python toa_calc.py $f ; done
