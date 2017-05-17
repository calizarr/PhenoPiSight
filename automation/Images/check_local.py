#!/env/bin/python
import pdb
import os
import itertools
import shutil

files = [x for x in os.listdir('.') if x.endswith('.tar')]
dates = [x.split('_')[1][:-7] for x in files]
dates = set(dates)

source = os.getcwd()
parent = os.path.dirname(source)

for k in dates:
    sub_files = [x for x in itertools.compress(files, [k in y for y in files])]
    destination = os.path.join(parent, k)
    print("The destination path is: {0}".format(destination))
    if not os.path.isdir(destination):
        os.mkdir(destination)
    dest = destination
    for f in sub_files:
        print("Moving {0} to folder {1}".format(f, dest))
        try:
            shutil.move(f, dest)
        except shutil.Error:
            src = os.stat(f).st_size
            dst = os.stat(os.path.join(dest, f)).st_size
            if src > dst:
                shutil.copy(f, dest)
            else:
                os.remove(f)

