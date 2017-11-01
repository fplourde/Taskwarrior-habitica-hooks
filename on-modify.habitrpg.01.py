#!/usr/bin/env python2

import sys
import json
import requests
import copy
from taskw import TaskWarrior

URL = 'https://habitica.com/api/v3'

if len(sys.argv) == 1:
    print "The Habitica hook does not work with TaskWarrior API v1, please upgrade to Taskwarrior 2.4.3 or higher"
    sys.exit(0)

if not sys.argv[1] == "api:2":
    print "The Habitica hook only supports TaskWarrior API v2 at this time"
    sys.exit(0)

configarg = sys.argv[4]
configfile = configarg[3:]
w = TaskWarrior(config_filename=configfile)
config = w.load_config()
API_KEY = config['habitica']['api_key']
API_USER = config['habitica']['api_user']

headers = {
		'Content-Type' : 'application/json',
		'x-api-user' : API_USER,
		'x-api-key' : API_KEY
	}

def main():
	jsonTaskOriginal = json.loads(sys.stdin.readline())
	jsonTask = json.loads(sys.stdin.readline())

	if 'id_habitica' not in jsonTask or not jsonTask["status"] == "completed":
		print json.dumps(jsonTask)
		print "No task updated on Habitica"
		return

	jsonOutput = copy.deepcopy(jsonTask)

	if pushTask(jsonOutput):
		print "Task completed on Habitica"
	else:
		print "Task was not completed on Habitica"

	print json.dumps(jsonTask)

def pushTask( jsonOutput ):
	try:
		req = requests.post(URL + '/tasks/' + jsonOutput["id_habitica"] + '/score/up', headers=headers, timeout=10)
		jsonHabiticaTask = json.loads(req.text)
		return 1
	except requests.ConnectTimeout:
		print "Timeout while communicating with Habitica server!"
		return 0
	except requests.ConnectionError:
		print "Connection error while communicating with Habitica server!"
		return 0

main()
sys.exit(0)
