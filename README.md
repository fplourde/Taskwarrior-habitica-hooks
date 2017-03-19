# Taskwarrior Habitica Hook
Add todo task on Habitica.com when task are added and complete task on Habitica.com when task added with taskwarrior are completed

## What it does
- Add task through Taskwarrior in Habitica
- Update task added through Taskwarrior in Habitica

## What it does not do
- Add task in Taskwarrior added through Habitica


## Install
Download and unzip files

	wget https://github.com/fplourde/Taskwarrior-habitica-hooks/archive/master.zip
	unzip master.zip -d .

Copy files to ~/.task/hooks

	mkdir -p ~/.task/hooks
	cd Taskwarrior-habitica-hooks-master/
	cp on-add.habitrpg.01.py ~/.task/hooks
	cp on-modify.habitrpg.01.py ~/.task/hooks

Get your API Key and User Key on [https://habitica.com/#/options/settings/api](https://habitica.com/#/options/settings/api) and edit line 8 and 9 of both files. 	

	API_KEY = 'YOURAPIKEY'
	API_USER = 'YOURAPIUSERKEY'

## Usage
	Nothing specific, use command `task add` and `task done` edit Habitica.

## Un-install
Delete the hooks

    rm ~/.task/hooks/on-add.habitrpg.01.py ~/.task/hooks
    rm ~/.task/hooks/on-modify.habitrpg.01.py ~/.task/hooks
