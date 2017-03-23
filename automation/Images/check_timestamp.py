#!/env/python
from __future__ import print_function
import argparse
import subprocess
import sys
import os

parser = argparse.ArgumentParser(description="Check that all images are existent")
parser.add_argument('timestamp', help = "Timestamp to check for Year-Month-Day-Hour (2017-03-21-14)")

args = parser.parse_args()

ymd = "-".join(args.timestamp.split('-')[:3])
files = [f for f in os.listdir(os.path.join(os.getcwd(), ymd)) if f.endswith(args.timestamp + ".tar")]

# sed 's/2017-03-21\/ShakoorCamera\([0-1][0-9][0-9]\)_2017-03-21-14.tar/\1/'
stripped = set(sorted([int(x.replace("ShakoorCamera", "").replace("_" + args.timestamp + ".tar", "")) for x in files]))
all_files = set(range(11,191))
print("Missing RPIs images: {0}".format(stripped.symmetric_difference(all_files)))


