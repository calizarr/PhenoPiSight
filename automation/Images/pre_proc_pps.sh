#!/bin/bash
date_hour=$1
date=$(echo $date_hour | cut -d'-' -f1-3)
find ${date}/ -name "*${date_hour}*" -exec tar xf {} \;
folder=$(find ${date}/ -type d -name "${date_hour}")
python zeropad.py ${folder}/
cd ../Reconstructions
bash process_stub_to_folder.sh ${date_hour}
