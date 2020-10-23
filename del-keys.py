'''
Iterate to find keys matching a pattern and delete them
CRDB databases cannot perform multi-key operations across hash slots
Use SCAN to get keys and add to a pipeline and UNLINK to delete with a delay between exeuctions
redis-py 3 needed for UNLINK, otherwise use DEL
'''

import argparse
import redis
import time

parser = argparse.ArgumentParser(description='Delete keys matching a pattern')
parser.add_argument("-s", "--server", required=True, help="Redis server host:port")
parser.add_argument("-a", "--auth", default='', help="Redis database password")
parser.add_argument("-p", "--pattern", required=True, help="Pattern for key names to match")
parser.add_argument("-b", "--batch", type=int, default=5000, help="Batch size for each SCAN")
parser.add_argument("-d", "--delay", type=float, default=0.5, help="Delay (in seconds) between calls to throttle")

args = vars(parser.parse_args())

[host, port] = args["server"].split(':')
config = { 'host': host, 'port': port, 'password': args["auth"] }
pattern = args["pattern"]
batch = args["batch"]
delay = args["delay"]

try:
	r = redis.StrictRedis(**config)
	r.ping()
except Exception as e:
	print(e)
	exit()

c = '0'
count = 0
deleted = 0
pipe = r.pipeline(transaction=False)

for k in r.scan_iter(match=pattern, count=batch):
	pipe.unlink(k)
	count += 1
	deleted += 1
	if count == batch:
		pipe.execute()
		count = 0	
		time.sleep(delay)

if count != 0:
	pipe.execute()

print("Deleted {} keys".format(deleted))