import logging
import random as rand
import os
from datetime import datetime, timedelta
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--count', type=int, default=100, help='Number of jobs to simulate')

args = parser.parse_args()
count = args.count

# create path that is portable and configurable
two_up = os.path.dirname(os.path.dirname(__file__))
path = os.path.join(two_up, 'logs', 'service.logs')

logging.basicConfig(level=logging.INFO, filename=path, filemode='w',
                    format='%(message)s')

timestamp = datetime.now()

for id in range(count):
    job_id = id
    latency = rand.randint(50, 600)
    status = rand.choice(['success', 'failure'])
   
    offset = timedelta(seconds=rand.randint(1, 5))
    timestamp += offset
    time_str = timestamp.strftime('%Y-%m-%dT%H:%M:%S')
    
    if status == 'failure':
        reason = rand.choice(['Internal Server Error', 'Bad Request', 'Unprocessable Content'])
        logging.info(f'{time_str} | job_id={job_id} | status={status} | reason={reason} | latency={latency}ms')
    else:
        logging.info(f'{time_str} | job_id={job_id} | status={status} | latency={latency}ms')