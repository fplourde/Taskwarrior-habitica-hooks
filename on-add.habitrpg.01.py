#!/usr/bin/env python2

import sys
import json
import requests
import argparse
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
	jsonTask = json.loads(sys.stdin.readline())

	id = pushTask(jsonTask)
	if not id == "":
		jsonTask["id_habitica"] = id
		print "Task added on Habitica"
	else:
		print "Task was not added on Habitica"

	print(json.dumps(jsonTask))

def pushTask( jsonTask ):
	values = {
		"type" : "todo",
		"text" : jsonTask["description"],
		"notes" : "Created from Taskwarrior"
		}

	priorityMap = {
		"trivial": .1,
		"easy": 1,
		"medium": 1.5,
		"hard": 2
	}

	if 'due' in jsonTask:
		values["date"] = jsonTask["due"]

	if 'difficulty' in jsonTask and jsonTask["difficulty"] in priorityMap:
		values["difficulty"] = priorityMap[jsonTask["difficulty"]]

	try:
		req = requests.post(URL + '/tasks/user', data=json.dumps(values), headers=headers, timeout=10)
		jsonHabiticaTask = json.loads(req.text)
		value = '';
	except requests.ConnectTimeout:
		print "Timeout while communicating with Habitica server!"
	except requests.ConnectionError:
		print "Connection error while communicating with Habitica server!"

	try:
		vError = jsonHabiticaTask["err"]
		print "Error while pushing task to Habitica : " + vError
	except:
		try:
			value = jsonHabiticaTask["data"]["id"]
		except:
			value = ""

	return value

try:
	main()
except:
	print "Error! Unable to add task to Habitica"
sys.exit(0)
