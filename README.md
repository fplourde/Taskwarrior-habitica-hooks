# Taskwarrior Habitica Hook
Add todo task on Habitica.com when task are added and complete task on Habitica.com when task added with taskwarrior are completed

## What it does
- Add task through Taskwarrior in Habitica
- Update task added through Taskwarrior in Habitica

## What it does not do
- Add task in Taskwarrior added through Habitica

## Install taskw
This updated version of the hooks require the taskw [https://github.com/ralphbean/taskw](https://github.com/ralphbean/taskw) python package. It can be installed with pip:
      pip install taskw

Or using your system package manager. For example, on Ubuntu (and Ubuntu-ish) Linux:
      sudo apt install python-taskw

## Install these hooks
Download and unzip files

	wget https://git.shadow53.com/Shadow53/taskwarrior-habitica-hooks/archive/master.zip
	unzip master.zip -d .

Copy files to ~/.task/hooks

	mkdir -p ~/.task/hooks
	cp -r taskwarrior-habitica-hooks-master ~/.task/hooks/habitica
	ln -sf ~/.task/hooks/habitica/habitica.py ~/.task/hooks/on-add.05.habitica.py
	ln -sf ~/.task/hooks/habitica/habitica.py ~/.task/hooks/on-modify.05.habitica.py

Get your API Key and User Key on [https://habitica.com/user/settings/api](https://habitica.com/user/settings/api) and add them to your taskwarrior config file (usually ~/.taskrc)

	habitica.api_key = 'YOURAPIKEY'
	habitica.api_user = 'YOURAPIUSERKEY'

## Usage
	Nothing specific, use command `task add` and `task done` edit Habitica.

## Un-install
Delete the hooks

    rm ~/.task/hooks/on-add.05.habitrpg.py ~/.task/hooks/on-modify.05.habitrpg.py ~/.task/hooks/habitica
