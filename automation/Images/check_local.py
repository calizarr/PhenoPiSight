#!/env/bin/python
import pdb
import os
import itertools
import shutil

files = [x for x in os.listdir('.') if x.endswith('.tar')]
dates = [x.split('_')[1][:-7] for x in files]
dates = set(dates)

source = os.getcwd()
for k in dates:
    sub_files = [x for x in itertools.compress(files, [k in y for y in files])]
    dest = os.path.join(source, k)
    for f in sub_files:
        print("Moving {0} to folder {1}".format(f, dest))
        shutil.move(f, dest)
    

