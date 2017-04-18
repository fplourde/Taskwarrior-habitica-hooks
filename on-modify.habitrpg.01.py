#!/usr/bin/env python2

import sys
import json
import requests
import copy

URL = 'https://habitica.com/api/v3'
API_KEY = ''
API_USER = ''

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
		print(json.dumps(jsonTask))
		print "Task completed on Habitica"
	else:
		print(json.dumps(jsonTaskOriginal))
		print "Task was not completed on Habitica"

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
