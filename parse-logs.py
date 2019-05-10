#!/usr/bin/python
import argparse
import glob
import json
import os

import datetime
import time
from datetime import timedelta

# This is the script to parse the application-logs(input) generated everyday, extract data that you need on elasticserch and save it in json file(output)
# the output json file will be picked by filebeat on this server and shipped to Elasticsearch running on a different server somewhere.
# Run this script like a cronjob , once everyday.
# Also does the job of cleaning up JSON file and applicationlogs after few days. 

parser = argparse.ArgumentParser(
    description='Translate log files from docker container to JSON format for kibana import')

parser.add_argument('--log_dir', help='Log folder (default="/")', type=str)
parser.add_argument('--output_dir', help='Output  (default="/")', type=str)
parser.add_argument('--file_age_limit_days', help='Remove log files older than days (default=14,  < 1 to disable)',
                    type=int)
parser.add_argument('--log_age_days', help='Days old input log must be (default=3)', type=int)
parser.add_argument('--no-delete', help='Do not delete logs, just print (false)', default=False,
                    action='store_true')
parser.add_argument('--server', help='Name of the server to label output files with (appserver1)', type=str)

args = parser.parse_args()

no_delete = False

output_dir = '/xxx/xx'
log_dir = '/xxx/x'
file_age_limit_days = 14
log_age_days = 3
server = 'server1'

if args.log_dir:
    log_dir = args.log_dir

if args.output_dir:
    output_dir = args.output_dir

if args.server:
    server = args.server

if args.file_age_limit_days:
    file_age_limit_days = args.file_age_limit_days

if args.log_age_days:
    log_age_days = args.log_age_days

if args.no_delete:
    no_delete = args.no_delete

date_str = datetime.datetime.now() - timedelta(days=log_age_days)
date_str = date_str.strftime("%Y-%m-%d")


result_file = os.path.join(output_dir, 'results-{server}-{date}.json'.format(server=server, date=date_str))
filename = os.path.join(log_dir, 'app.log.{server}.{date}'.format(server=server, date=date_str))

print('INPUT', filename)
print('OUTPUT', result_file)

if not os.path.isfile(filename):
    print('**ERROR** input log file not found: {}'.format(filename))
    os.exit(1)

if not os.path.isdir(output_dir):
    print('**ERROR** output folder not found: {}'.format(output_dir))
    os.exit(1)

with open(filename, "r") as f:
    with open(result_file, "wb") as fw:
        line_count = 0
        for line in f:
            line_count += 1
            try:
                line.strip('\n')
                line_list = line.split()

                #Write Code below to extract the required content from the application logs
                #store the extracted content in dictionary -->line_dict = {} as key value pairs.
                #All the important data that you need for analysis.

               
               fw.write("\n".encode('utf-8'))
               json.dump(line_dict, fw)
            except Exception as e:
                print('**ERROR** {} parsing log file. Line :{}'.format(str(e), line_count))

# age out files log files
if file_age_limit_days > log_age_days:
    for f in glob.glob(os.path.join(log_dir, '*.log.*')):
        days_old = int((time.time() - os.path.getmtime(f)) / (24 * 60 * 60))
        if days_old >= file_age_limit_days:
            print('Removing days old {} log: {}'.format(days_old, f))
            if not no_delete:
                os.unlink(f)

    for f in glob.glob(os.path.join(output_dir, '*.json')):
        days_old = int((time.time() - os.path.getmtime(f)) / (24 * 60 * 60))
        if days_old >= file_age_limit_days:
            print('Removing days old {} JSON: {}'.format(days_old, f))
            if not no_delete:
                os.unlink(f)
