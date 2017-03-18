#!/usr/bin/env python

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
	
	pushTask(jsonOutput)
	
	print(json.dumps(jsonTask))
		
	print "Task completed on Habitica"

def pushTask( jsonOutput ):
	req = requests.post(URL + '/tasks/' + jsonOutput["id_habitica"] + '/score/up', headers=headers)
		
	jsonHabiticaTask = json.loads(req.text)
	
main()
sys.exit(0)
