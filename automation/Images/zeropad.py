import os
import sys
import pdb
import shutil

path = sys.argv[1]
# choice = sys.argv[2]
for filename in os.listdir(path):
    # ShakoorCamera
    prefix = filename[:13]
    postfix = filename[13:].split('_')
    num = postfix[0]
    num = num.zfill(3)
    rest = '_'.join(postfix[1:-1])
    ext = postfix[-1].split('.')[-1]
    # if choice == "number":
    #     new_filename = prefix+"_"+num+"_"+ext
    #     new_path = os.path.join(path, "number")
    # else:
    #     new_filename = prefix+"_"+rest+"."+ext
    #     new_path = os.path.join(path, "coord")
    number_filename = prefix+"_"+num+"."+ext
    number_path = os.path.join(path, "number")
    coord_filename = prefix+"_"+rest+"."+ext
    coord_path = os.path.join(path, "coord")
    if not os.path.exists(number_path):
        os.makedirs(number_path)
    if not os.path.exists(coord_path):
        os.makedirs(coord_path)
    shutil.copy(os.path.join(path, filename), os.path.join(number_path, number_filename))
    shutil.copy(os.path.join(path, filename), os.path.join(coord_path, coord_filename))
    # shutil.copy(os.path.join(path, filename), os.path.join(path, new_filename))
    # os.rename(os.path.join(path, filename), os.path.join(path, new_filename))
