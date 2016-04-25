import os
import sys

path = sys.argv[1]
for filename in os.listdir(path):
    # ShakoorCamera
    prefix = filename[:13]
    num, rest = filename.split('_')
    num = num.zfill(3)
    new_filename = prefix+"_"+num+rest
    os.rename(os.path.join(path, filename), os.path.join(path, new_filename))
