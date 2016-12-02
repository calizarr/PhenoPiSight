#!/bin/bash
# Close STDOUT file descriptor
exec 1<&-
# Close STDERR FD
exec 2<&-

# Open STDOUT as $LOG_FILE file for read and write.
# exec 1<>$LOG_FILE
exec 1<>vsfm.log

# Redirect STDERR to STDOUT
exec 2>&1

set -x
# Getting the path to the image folder and the prefix name for the files
images="$1"
name="$2"
# Name for the sparse reconstruction
sparse=${name}_sparse.nvm
# Name for the sparse reconstruction with additional points
additional=${name}_sparse_add.nvm
# Name for the dense reconstruction
dense=${name}_dense.nvm
# Name for the gcp coordinates with the dense reconstruction
gcp=${name}_dense_gcp.nvm
# Name for the CMP-MVS output from the dense reconstruction
cmp=${name}_dense_cmp
# Making the directories to place the files in
directory=`date +%Y-%m-%d-%H`
mkdir -p run_dir/$directory
# Moving the gcp file to the input directory
mv_cmd="mv vsfm_cm_dim_1D_km.gcp run_dir/$directory/${dense}.gcp"
echo "Launching $mv_cmd"
$mv_cmd
# Changing into the final directory
cd run_dir/$directory
# Creating the final file
mv ../../vsfm.log .
echo "Loading $images and saving to $sparse"
cmd="../../VisualSFM sfm+add $images $sparse |& tee -a vsfm.log"
echo "Launching $cmd"
$cmd
echo "Loading $sparse and saving to $additional"
cmd="../../VisualSFM sfm+add $sparse $additional |& tee -a vsfm.log"
echo "Launching $cmd"
$cmd
echo "Loading $additional and saving to $dense"
cmd="../../VisualSFM sfm+pmvs+merge $additional $dense |& tee -a vsfm.log"
echo "Launching $cmd"
$cmd
echo "Attempting to add GPS points..."
cmd="../../VisualSFM sfm+loadnvm+gcp $dense $gcp |& tee -a vsfm.log"
echo "Launching $cmd"
$cmd

mv ../../log .
