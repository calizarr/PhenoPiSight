#!/bin/bash
date_hour=$1
date=$(echo $date_hour | cut -d'-' -f1-3)
vsfm=VisualSFM_${date_hour}
mkdir $vsfm
cp VisualSFM_Stub/* ${vsfm}/
cd ${vsfm}
mkdir run_dir
sed -i "s/1970-01-01-00/${date_hour}/" visual_sfm_full_1970-01-01.condor
sed -i "s/1970-01-01/${date}/" visual_sfm_full_1970-01-01.condor
mv visual_sfm_full_1970-01-01.condor visual_sfm_full_${date_hour}.condor
