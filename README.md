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

###1) Install python (2.7 or higher)

TODO: add Windows instructions

Installation on OSX: go to https://www.python.org/downloads/mac-osx/

###2) Install project dependencies. There are two ways to do this:

####1. First way: Use a virtual environment (Ubuntu):

Install pip

	sudo apt-get install python-pip
Install virtualenv using pip

	pip install virtualenvwrapper
Add the following two lines to your ~/.bashrc script:

    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh
Close the file and source it:

	source ~/.bashrc
Go to the project directory: Make sure you are in the directory playbook (if you do "ls" in your command line you will find there is another folder called playbook. Don't go in there. Stay here.)

	mkvirtualenv playbook
The next command is only necessary if you are not already using the created virtualenv

	workon playbook
	
* If it says "command not found", try typing: virtualenv virtualenv
* ls to confirm that "venv" is amongst your files.
* type: source venv/bin/activate to activate your virtual environment.
You should see (venv) before your project directory

##### Ubuntu and Mac
	pip install -r requirements.txt

##### Windows
	python -m pip install

####2. Second way: Use your global python environment

Directly install the dependencies listed in requirements.txt using pip or the easy_install utility. If you are using Mac you will have to configure psycopg2 setting up the file path for postgresql and then restart the terminal to avoid errors.

###3) Install PostgreSQL

###### Ubuntu

helpful link: https://help.ubuntu.com/community/PostgreSQL

###### Mac

a) Download Postgres.app from http://postgresapp.com/

b) Add the path to ~/.profile

	echo 'export PATH="/Applications/Postgres.app/Contents/Versions/9.4/bin:$PATH"' >> ~/.profile
	source ~/.profile

###4) Update your database connection settings using your database admin user

The database settings are located in the playbook/settings.py file and must be updated to represent your local environment. Create the database north6_devwaterwheel by running the following SQL command (you can use psql or any client of your choice):

	create database northbr6_devwaterwheel;

Do not forget to use the correct database user and password in the settings.py file. Here is how you could change your database password, supposing the user is 'postgres'.

In your linux terminal, considering your database user is postgres, type:

	sudo -u postgres psql postgres

Now that you are connected to the psql:

	\password postgres

###5) Configure Django

Run Django migration scripts

	python manage.py makemigrations
	python manage.py migrate

Create a superuser (you will be prompted to type in a username, email and password)

	python manage.py createsuperuser

Use the db/static_inserts.sql file to populate the database with usefull testing information:

Open the file and update the lines below with your information:

	\set email '\'' '\<The email you used to create the django account>' '\''
	\set fname '\'' '\<your first name>' '\''
	\set lname '\'' '\<your last name>' '\''
	
For example:

	\set email '\'' 'johndoe@gmail.com' '\''
	\set fname '\'' 'John' '\''
	\set lname '\'' 'Doe' '\''

After that, run the following command to import the data (you must be logged as a user that has privileges to access/update the database or provide user/password information to psql):

	psql northbr6_devwaterwheel < static_inserts.sql
	
We also must create a trigger that will be responsible for update the backlog.update_dttm field. This trigger will be fired on a row update event. The Postgres_Update_Trigger.sql script is located under the db folder.

	psql northbr6_devwaterwheel_test < Postgres_Update_Trigger.sql

There is also two other files that must be updated: playbook/email_settings.py (information concerning email service) and playbook/backlog/github_settings.py (information used to interact with the github API)

Running
=======

	python manage.py runserver [host:port]

Now you can go to \<host\>:\<port\>/admin and login using the user created above. You can create groups and regular users that will be used to login into the playbook application (\<host\>:\<port\>/playbook).

After logging into the admin interface, create a new user, using the same email you specified when running the static_inserts.sql file. The email field will be the link between the django auth user and the NorthBridge volunteer. Add the "Volunteers" group to the "Chosen groups" field of the user.

Now you are ready to logout from admin account and access the application using the regular user you have created above.

A main restriction is that the user's email must match the volunteer's email. It is through this relation that we can link a django user and the volunteer's informations. For now there is no database constraint ensuring this.
