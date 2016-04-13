#!/usr/bin/env python

import sys
import json
import requests
import datetime

URL = 'https://habitica.com/api/v2'
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
	print json.dumps(jsonTask,sort_keys=True,indent=4, separators=(',', ': '))
	if jsonTask["id_habitica"] is 'null' or not jsonTask["status"] == "completed":
		print json.dumps(jsonTask)
		print "No task updated on Habitica"
		return
		
	pushTask(jsonTask)
	
	print(json.dumps(jsonTask))
	
	print "Task completed on Habitica"

def pushTask( jsonTask ):
	req = requests.post(URL + '/user/tasks/' + jsonTask["id_habitica"] + '/up', headers=headers)
	jsonHabiticaTask = json.loads(req.text)
	
main()
sys.exit(0)
	