Overview
========

This repository wiki describes Northbridge agile team processes.

This repository code supports the Alliance project, which is responsible for the interactions between Northbridge agile team processes and GitHub issues tracking.

There are three major components to Alliance: web interface, export, and import. These are represented as the yellow components of this diagram.

Web Interface: Allows Northbridge volunteers to estimate and select user stories from a prioritized backlog of work.

Export: When invoked, export all Backlog User Stories in state "Selected" from the database to a GitHub Issues list using the GitHub API.

Import: When invoked, update a Backlog User Story to Accepted. This process will respond to a GitHub Issues Webhook.

![Project Diagram](http://northbridgetech.org/images/alliance2.jpg)

Setup
=====

In order to work on these files, search for "NorthBridge Playbook" in Github and
click on "fork" to have a copy in your own repository section in your profile.

Click on "Clone in Desktop" in order to have a copy of all of the files on your
Desktop (or wherever you choose to save and access the files)

Open the files in your favorite text editor (I like to use Atom) and cd into the
project in your terminal.

Now you should be ready to work on the project!



Installation
============
1. Install python, v 2.7 or higher

        Installation on OSX:

            Install python (2.7 or higher) go to https://www.python.org/downloads/mac-osx/


2. Install project dependencies. There are two ways to do this.

First way: Use a virtual environment:

	sudo apt-get install python-pip

If you want to use a virtual environment you must do something like (Ubuntu):

	pip install virtualenvwrapper
	# Go to the project directory

	#make sure you are in the directory playbook (if you do "ls" in your command line you will find there is another folder called playbook--don't go in there. stay here.)

	export WORKON_HOME=$HOME/.virtualenvs
	source /usr/local/bin/virtualenvwrapper.sh

	mkvirtualenv playbook

	# The next command is only necessary if you are not already using the created virtualenv
	workon playbook

To install the dependencies you could do something like this (Ubuntu):

	pip install -r requirements.txt

Second way: Use your global python environment

	install the dependencies listed in requirements.txt using the easy_install utility
	
	example: easy_install psycopg2

3. install postresql 

4. update your database connection settings using your database admin user

helpful link: https://help.ubuntu.com/community/PostgreSQL

The database settings are located in the playbook/settings.py file and must be updated to represent your local environment. 

create the database north6_devwaterwheel by running the following in the command line:
create database northbr6_devwaterwheel

You can change credencials to fit file (aka user: postgres with password:postgres like specified in settings.py under "DATABASES") which can be done like so:

In a terminal, type:

sudo -u postgres psql postgres
Set a password for the "postgres" database role using the command:

\password postgres

OR configure to have your username and password in settings.py

5. install django

6. install the project

Run django migrate scripts:

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


There is also two other files that must be updated: playbook/email_settings.py (information concerning email service) and playbook/backlog/github_settings.py (information used to interact with the github API)
