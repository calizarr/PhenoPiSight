#!/env/bin/python
from __future__ import print_function
import argparse
import subprocess
import sys
import os

parser = argparse.ArgumentParser(description="Make DAG stub into dag")
parser.add_argument('timestamp', help = "Timestamp to launch dag for Year-Month-Day-Hour (2017-03-21-14)")

args = parser.parse_args()

cmd = "sed 's/date_var/{0}/g' PhenoPiSight_dag.stub > PhenoPiSight_{0}.dag".format(args.timestamp)
subprocess.call(cmd, shell = True)

dagfile = "PhenoPiSight_{0}.dag".format(args.timestamp)
cmd = "condor_submit_dag {0}".format(dagfile)
subprocess.call(cmd, shell = True)
