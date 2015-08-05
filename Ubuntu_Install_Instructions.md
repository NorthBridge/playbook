
Installation
============

###1) Install python (2.7 or higher)

###2) Install project dependencies. There are two ways to do this:

Use a virtual environment (Ubuntu):

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

Install python dependencies

	pip install -r requirements.txt

*Running this installs the following packages to your virtual environment (only in playbook):
	
	Django==1.8.2
	ipaddress==1.0.7
	psycopg2==2.6.1
	pygithub3==0.5.1
	requests==2.7.0

###3) Install PostgreSQL

Currently 9.4 is the most current release of postgres:

	sudo apt-get install postgresql-9.4

helpful link: https://help.ubuntu.com/community/PostgreSQL

###4) Update your database connection settings using your database admin user

The database settings are located in the playbook/settings.py file and must be updated to represent your local environment. 

*This means go into playbook/settings.py and look for the DATABASE section. should look something like:
	
	DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'northbr6_devwaterwheel',
    'USER': 'postgres',
    'PASSWORD': 'postgres',
    'HOST': '127.0.0.1',
    'PORT': '5432',
    	}
	}

*Make sure that your user, password, host, and port match how everything is set up on postgres on your local machine. Name corresponds to the name of the database which we create below in the next section:

Create the database north6_devwaterwheel by running the following SQL command (you can use psql or any client of your choice). First you must sign into the postgres user (if prompt for a password when getting into the postgres superuser type in your computer password:

	sudo su - postgres
	psql
	create database northbr6_devwaterwheel;

After you are done with setting up the database you can log out by Ctrl+D twice OR until you see that your back in your virtual environment, you see (playbook). You should always see (playbook) unless in postgres. 

*In case you need to change your password for user posgres:

	sudo -u postgres psql postgres

Now that you are connected to psql you can change your password to 'postgres':

	\password postgres


###5) Configure Django

Run Django migration scripts (only AFTER database is setup/configured):

	python manage.py makemigrations
	python manage.py migrate

Create a superuser (you will be prompted to type in a username, email and password):

	python manage.py createsuperuser

Use the db/static_inserts.sql file to populate the database with useful testing information:

Open the file (db/static_inserts.sql) and update the lines below with your information:

	\set email '\'' '\<The email you used to create the django account>' '\''
	\set fname '\'' '\<your first name>' '\''
	\set lname '\'' '\<your last name>' '\''
	
For example:

	\set email '\'' 'johndoe@gmail.com' '\''
	\set fname '\'' 'John' '\''
	\set lname '\'' 'Doe' '\''

After that, run the following command to import the data (you must be logged as a user that has privileges to access/update the database or provide user/password information to psql):

	sudo su - postgres
    psql northbr6_devwaterwheel < /home/path/to/playbook/db/static_inserts.sql

	
We also must create a trigger that will be responsible for update the backlog.update_dttm field. This trigger will be fired on a row update event. The Postgres_Update_Trigger.sql script is located under the db folder.

	psql northbr6_devwaterwheel_test < /home/path/to/playbook/db/Postgres_Update_Trigger.sql


-------TO EDIT FURTHER -----


There is also two other files that must be updated: playbook/email_settings.py (information concerning email service) and playbook/backlog/github_settings.py (information used to interact with the github API).

The system can notify users through email when an error on modules import/export occurs. Configuration can be done in the file email_settings.py. As an example, to send the emails using gmail service, one could configure the file as shown below:

	# Email configuration
	EMAIL_USE_TLS = True
	EMAIL_HOST = 'smtp.gmail.com'
	EMAIL_HOST_USER = 'exampleName@gmail.com'
	EMAIL_HOST_PASSWORD = 'myPassword'
	EMAIL_PORT = 587
	EMAIL_RECIPIENT_LIST = ['exampleName2@gmail.com', 'exampleName3@yahoo.com']
	
The main functionality of the system is the integration with the GitHub API. In order to put this integration to work there are some pre-requirements that must be met:

  - You must have a GitHub Organization
  - The GitHub repositories must be inside this organization. Of course, a repository must exist before the system can interact with it.
  - You must create a "Personal access token":
    - Click on your GitHub profile picture and select "Settings"
    - Chose "Personal access tokens" on the left menu
    - Chose a description for the token
    - Select the scopes: repo, public_repo, user, gist
    - Click "Generate token"
    - Copy the generated token as we will use it later (warning: You cannot access the generated token after leaving the page so be careful to store it elsewhere)
  - You must configure a GitHub webhook inside the Organization:
    - The Payload URL must point to: 
      - If you are running over HTTP (for example, through manage.py script):
        - http://\<host\>:\<port\>/playbook/backlog/githubimport
      - If you want to use HTTPS (the HTTP server must be configured):
        - https://\<host\>:\<port\>/playbook/backlog/githubimport
        - Remember to "Disable SSL verification" if you have a self signed certificate
    - Content type: application/json
    - Secret: chose a strong secret
    - Which events would you like to trigger this webhook?
      - Choose "Let me select individual events" and check the "Issues" event.

Now we can configure the github_settings.py file:

	GITHUB_OWNER = "\<GitHub Organization\>"
	GITHUB_TOKEN = "\<GitHub generated token\>"
	GITHUB_WEBHOOK_SECRET = "\<The secret you created on GitHub\>"

Running
=======

	python manage.py runserver [host:port]

Now you can go to \<host\>:\<port\>/admin and login using the user created above. You can create groups and regular users that will be used to login into the playbook application (\<host\>:\<port\>/playbook).

After logging into the admin interface, create a new user, using the same email you specified when running the static_inserts.sql file. The email field will be the link between the django auth user and the NorthBridge volunteer. Add the "Volunteers" group to the "Chosen groups" field of the user.

Now you are ready to logout from admin account and access the application using the regular user you have created above.

A main restriction is that the user's email must match the volunteer's email. It is through this relation that we can link a django user and the volunteer's informations. For now there is no database constraint ensuring this.
