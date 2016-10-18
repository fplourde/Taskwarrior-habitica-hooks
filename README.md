The project is built with the API version 2 and is no more compatible with the current version of Habitica. I will update the project later this year.

Sorry for the incovenient.

# Taskwarrior Habitica Hook
Add todo task on Habiti.com when task add is fired and complete it on task done

## Install
Download files

	wget ...

Copy files to ~/.task/hooks

	mkdir -p ~/.task/hooks
	cp on-add.habitrpg.01.py ~/.task/hooks
	cp on-modify.habitrpg.01.py ~/.task/hooks

Get your API Key and User Key on [https://habitica.com/#/options/settings/api](https://habitica.com/#/options/settings/api) and edit line 8 and 9 of both files. 	

	API_KEY = 'YOURAPIKEY'
	API_USER = 'YOURAPIUSERKEY'

## Usage
	Nothing specific, task add and task done edit Habitica.

## Un-install
Delete the hook::

    rm ~/.task/hooks/on-add.habitrpg.01.py ~/.task/hooks
    rm ~/.task/hooks/on-modify.habitrpg.01.py ~/.task/hooks
