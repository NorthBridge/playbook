Overview
========

This repository wiki describes Northbridge agile team processes.

This repository code supports the Alliance project, which is responsible for the interactions between Northbridge agile team processes and GitHub issues tracking.

There are three major components to Alliance: web interface, export, and import. These are represented as the yellow components of this diagram.

Web Interface: Allows Northbridge volunteers to estimate and select user stories from a prioritized backlog of work.

Export: When invoked, export all Backlog User Stories in state "Selected" from the database to a GitHub Issues list using the GitHub API.

Import: When invoked, update a Backlog User Story to Accepted. This process will respond to a GitHub Issues Webhook.

![Project Diagram](http://northbridgetech.org/images/alliance2.jpg)

Installation
============
TODO: add Windows instructions

####1) Install pip

##### Ubuntu
	
	sudo apt-get install python-pip
	
##### Mac

Install pip with either easy_install or homebrew:
	
	sudo easy_install pip

	brew install python
	
####2) Create virtual environment (optional)

##### Ubuntu and Mac
	pip install virtualenvwrapper
	# Go to the project directory
	mkvirtualenv playbook
	# The next command is only necessary if you are not already using the created virtualenv
	workon playbook
	
####3) Install dependencies

##### Ubuntu and Mac

	sudo pip install -r requirements.txt


The database settings are located in the playbook/settings.py file and must be updated to represent your local environment. There is also two other files that must be updated: playbook/email_settings.py (information concerning email service) and playbook/backlog/github_settings.py (information used to interact with the github API)

If you do not already have the database structure you must run django migrate scripts:

	# Note that running the following commands will create an empty
	#  database (No projects, teams, backlogs, volunteers etc)
	python manage.py makemigrations
	python manage.py migrate

Create a superuser

	python manage.py createsuperuser

Running
=======

	python manage.py runserver [host:port]


Now you can go to \<host\>:\<port\>/admin and login using the user created above. You can create groups and regular users that will be used to login into the playbook application (\<host\>:\<port\>/playbook).

A main restriction is that the user's email must match the volunteer's email. It is through this relation that we can link a django user and the volunteer's informations. For now there is no database constraint ensuring this.


Troubleshoot
============
### Error: pg_config executable not found.
	
Make sure PostGres is installed on your machine.

#### Mac

Go to http://postgresapp.com/ and follow the instructions to add the application.

Add the path to ~/.profile
	
	echo PATH="/Applications/Postgres.app/Contents/Versions/9.4/bin:$PATH" >> ~/.profile
	source ~/.profile
