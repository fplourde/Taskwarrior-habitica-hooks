#!/usr/bin/env python3

from datetime import datetime
import sys
import json
import requests
from taskw import TaskWarrior

URL = 'https://habitica.com/api/v3'

if len(sys.argv) == 1:
    print("The Habitica hook does not work with TaskWarrior API v1, please upgrade to Taskwarrior 2.4.3 or higher")
    sys.exit(1)

if not sys.argv[1] == "api:2":
    print("The Habitica hook only supports TaskWarrior API v2 at this time")
    sys.exit(1)

configfile = sys.argv[4][3:]
command = sys.argv[3][8:]

# Define constants to avoid magic values
COMMAND_ADD = 'add'

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

HABITICA_DATA = 'data'
HABITICA_DATE = 'date'
HABITICA_DIFFICULTY = 'difficulty'
HABITICA_ERROR = 'err'
HABITICA_ID = 'id'

TASK_HABITICA_ID = 'id_habitica'
TASK_KEY_DESCRIPTION = 'description'
TASK_KEY_DIFFICULTY = 'difficulty'
TASK_KEY_DUE = 'due'
TASK_CONFIG_HABITICA = 'habitica'
TASK_CONFIG_HABITICA_KEY = 'api_key'
TASK_CONFIG_HABITICA_USER = 'api_user'
TASK_KEY_STATUS = 'status'
TASK_STATUS_COMPLETED = 'completed'

w = TaskWarrior(config_filename=configfile)
config = w.load_config()
API_KEY = config[TASK_CONFIG_HABITICA][TASK_CONFIG_HABITICA_KEY]
API_USER = config[TASK_CONFIG_HABITICA][TASK_CONFIG_HABITICA_USER]

headers = {
    'Content-Type': 'application/json',
    'x-api-user': API_USER,
    'x-api-key': API_KEY
}

priorityMap = {
    "trivial": "0.1",
    "easy": "1",
    "medium": "1.5",
    "hard": "2"
}


class TaskException(Exception):
    ERROR_TIMEOUT = "Timeout while communicating with Habitica server"
    ERROR_CONNECTION = "Connection error while communicating with Habitica server"

    def __init__(self, timeout=False, connection=False, habitica_error=""):
        if not (timeout or connection or habitica_error):
            raise ValueError("At least one argument must be true")
        self.timeout = timeout
        self.connection = connection
        self.habitica_error = habitica_error

    def __str__(self):
        msg = ""
        if self.timeout:
            msg = self.ERROR_TIMEOUT
        elif self.connection:
            msg = self.ERROR_CONNECTION
        elif self.habitica_error:
            msg = self.habitica_error

        return "Error: {}".format(msg)


def pushTask(task):
    values = {
        "type": "todo",
        "text": task[TASK_KEY_DESCRIPTION],
        "notes": "Created from Taskwarrior"
    }

    # If task has due date, add to Habitica request
    if TASK_KEY_DUE in task:
        values[HABITICA_DATE] = datetime.strptime(task[TASK_KEY_DUE],
                                                  "%Y%m%dT%H%M%SZ").isoformat()

    # If task has difficulty, map to Habitica difficulty
    if TASK_KEY_DIFFICULTY in task and task[TASK_KEY_DIFFICULTY] in priorityMap:
        values[HABITICA_DIFFICULTY] = priorityMap[task[TASK_KEY_DIFFICULTY]]

    try:
        req = requests.post(URL + '/tasks/user', data=json.dumps(values),
                            headers=headers, timeout=10)
        todo = req.json()
        if req.status_code >= 400:
            error = "Received HTTP error {} from Habitica API: {}".format(req.status_code, req.text)
            if HABITICA_ERROR in todo:
                error = todo[HABITICA_ERROR]
            raise TaskException(habitica_error=error)
        elif HABITICA_DATA not in todo:
            error = "Data object not found in Habitica response"
            raise TaskException(habitica_error=error)
        elif HABITICA_ID not in todo[HABITICA_DATA]:
            error = "Task ID not found in Habitica response"
            raise TaskException(habitica_error=error)
        else:
            return todo[HABITICA_DATA][HABITICA_ID]
    except requests.ConnectTimeout:
        raise TaskException(timeout=True)
    except requests.ConnectionError:
        raise TaskException(connection=True)


def add_task(task):
    id = pushTask(task)
    if id:
        task[TASK_HABITICA_ID] = id


def main():
    task = None
    if command == COMMAND_ADD:
        task = json.loads(sys.stdin.readline())
        add_task(task)
        print(json.dumps(task))
        if TASK_HABITICA_ID in task:
            print("Added task to Habitica")
        else:
            print("Failed to add task to Habitica, yet without error")
    else:
        # Assumed anything not add is modification
        # Skip original task first
        sys.stdin.readline()
        task = json.loads(sys.stdin.readline())

        if TASK_HABITICA_ID not in task:
            print(json.dumps(task))
            print("Task not present on Habitica. Ignoring.")
            return
        elif not task[TASK_KEY_STATUS] == TASK_STATUS_COMPLETED:
            print(json.dumps(task))
            print("Task not marked as completed. Ignoring.")
            return

        complete_task(task)
        print(json.dumps(task))
        print("Task completed on Habitica")


def complete_task(task):
    try:
        url = "{}/tasks/{}/score/up".format(URL, task[TASK_HABITICA_ID])
        requests.post(url, headers=headers, timeout=10)
    except requests.ConnectTimeout:
        raise TaskException(timeout=True)
    except requests.ConnectionError:
        raise TaskException(connection=True)


if __name__ == '__main__':
    try:
        main()
        sys.exit(EXIT_SUCCESS)
    except TaskException as e:
        print(e)
        sys.exit(EXIT_FAILURE)
