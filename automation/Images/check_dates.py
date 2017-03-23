#!/env/python
from __future__ import print_function
import argparse
import subprocess
import sys
import os
import glob

parser = argparse.ArgumentParser(description="Checking if files are not in the proper section")
parser.add_argument('conflict_file', help = "File containing '/' separated YMD stamp (Year-Month-Day) to check")

args = parser.parse_args()

if args.conflict_file == "":
    subprocess.call("find . -maxdepth 1 -type d -exec find {} -maxdepth 1 -type f -name \"ShakoorCamera*\" \\; | xargs -I {} printf \"%s\\n\" {} | sed 's/\\(\\.\\/201[0-9]-[0-9][0-9]-[0-9][0-9]\\/\\)ShakoorCamera[0-1][0-9][0-9]_\\(201[0-9]-[0-9][0-9]-[0-9][0-9]\\)-[0-9][0-9]\\.tar/\\1\\2/' | uniq > diag", shell = True)
    diagnostics = os.path.join(os.getcwd(), "diag")
else:
    diagnostics = args.conflict_file


final_dict = {}
    
with open(diagnostics, "r") as diag:
    for line in diag:
        line = line.replace("./", "").strip()
        line = line.split("/")
        if line[0] != line[1]:
            if line[0] in final_dict:
                final_dict[line[0]].add(line[1])
            else:
                final_dict[line[0]] = set([line[1]])
            # print(' != '.join(line))


for k in final_dict.keys():
    folder = k
    for to in final_dict[k]:
        cmd = "mv {folder}/ShakoorCamera[0-9][0-9][0-9]_{to}-[0-9][0-9].tar {to}".format(**dict(folder = k, to = to))
        print("Running cmd: {0}".format(cmd))
        subprocess.call(cmd, shell = True)
    

# dirs = [x for x in os.listdir(os.getcwd()) if os.path.isdir(x)]
# files = [os.listdir(x) for x in dirs]
# print(files)

# find . -maxdepth 1 -type d -exec find {} -maxdepth 1 -type f -name "ShakoorCamera011*" \; | xargs -I {} printf "%s\n" {} | sed 's/\(\.\/201[67]-[0-9][0-9]-[0-9][0-9]\/\)ShakoorCamera[0-1][0-9][0-9]_\(201[67]-[0-9][0-9]-[0-9][0-9]\)-[0-9][0-9]\.tar/\1\2/' | uniq > diag
