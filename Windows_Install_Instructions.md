
Installation
============

###1) Install python 2.7.x (Currently 2.7.10 is the latest version). Install the appropriate python according to how many bits your computer has. Link below:

	https://www.python.org/downloads/release/python-2710/

###2) Install project dependencies. There are two ways to do this:



Install pip. Download get-pip.py and save (this will probably go into your Downloads Folder)

	https://bootstrap.pypa.io/get-pip.py

Once downloaded go into cmd:

	cd ~/Downloads
	python get-pip.py

Go to the Environment variables and make variable "PYTHON_HOME" in systems variables with path "C:\Python27"

cmd:
	pip install virtualenvwrapper-win

	
Go to the project directory: Make sure you are in the directory playbook (if you do "ls" in your command line you will find there is another folder called playbook. Don't go in there. Stay here.)

	mkvirtualenv playbook

The next command is only necessary if you are not already using the created virtualenv

	workon playbook

*to get out of the virtual environment type in:
	
	deactivate

Install python dependencies (while in virtual environment aka (playbook)):

	pip install -r requirements.txt

*Running this installs the following packages to your virtual environment (only in playbook):
	
	Django==1.8.2
	ipaddress==1.0.7
	psycopg2==2.6.1
	pygithub3==0.5.1
	requests==2.7.0


**If you get an error about psycopg2, go to: http://aka.ms/vcpython27 & download. Run the following command and retry to install the requirements again.

	msiexec/i C:\Users\\Downloads\VCForPython27.msi ALLUSERS=1

###3) Install PostgreSQL: http://www.postgresql.org/download/windows/
Go to your environment variables and add postgres to the PATH. (Should look something like C:\Program Files\PostgreSQL\9.x\bin;)

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

	psql -U postgres
	create database northbr6_devwaterwheel;

After you are done with setting up the database you can log out by running exit() & you see that your back in your virtual environment, you see (playbook). You should always see (playbook) unless in postgres. 


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
	\set github_repo '\'' '<github test repo>' '\''
	
For example:

	\set email '\'' 'johndoe@gmail.com' '\''
	\set fname '\'' 'John' '\''
	\set lname '\'' 'Doe' '\''
	\set github_repo '\'' 'https://github.com/myorg/githubtest' '\''

After that, run the following command to import the data (you must be logged as a user that has privileges to access/update the database or provide user/password information to psql):

	
    psql -U postgres -f db/static_inserts.sql northbr6_devwaterwheel

	
We also must create a trigger that will be responsible for update the backlog.update_dttm field. This trigger will be fired on a row update event. The Postgres_Update_Trigger.sql script is located under the db folder.

	psql -U postgres db/Postgres_Update_Trigger.sql northbr6_devwaterwheel


There is also two other files that must be updated: playbook/email_settings.py (information concerning email service) and playbook/backlog/github_settings.py (information used to interact with the github API).



The system can notify users through email when an error on modules import/export occurs. Configuration can be done in the file email_settings.py. As an example, to send the emails using gmail service, one could configure the file as shown below:

	# Email configuration
	EMAIL_USE_TLS = True
	EMAIL_HOST = 'smtp.gmail.com'
	EMAIL_HOST_USER = 'exampleName@gmail.com'
	EMAIL_HOST_PASSWORD = 'myPassword'
	EMAIL_PORT = 587
	EMAIL_RECIPIENT_LIST = ['exampleName2@gmail.com']
	
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

*Helpful link: https://developer.github.com/webhooks/creating/

To set up a repository webhook on GitHub, head over to the Settings page of your repository, and click on Webhooks & services. After that, click on Add webhook.

Payload URL = the server endpoint that will receive the webhook payload.

The Payload URL must point to: 
-If you are running over HTTP (for example, through manage.py script):
  	
  	http://\<host\>:\<port\>/playbook/backlog/githubimport

Install ngrok: https://ngrok.com/download
-first download and then unzip
-you can extract it in your downloads folder and then run it by double clicking on ngrok.exe. Run the following in the ngrok terminal:

	ngrok http 8000 


Something like this will pop up:
	
	ngrok by @inconshreveable                                       (Ctrl+C to quit)
	                                                                                
	Tunnel Status                 online                                            
	Version                       2.0.19/2.0.19                                     
	Web Interface                 http://127.0.0.1:4040                             
	Forwarding                    http://389c1340.ngrok.io -> localhost:8000        
	Forwarding                    https://389c1340.ngrok.io -> localhost:8000       
	                                                                                
	Connections                   ttl     opn     rt1     rt5     p50     p90       
	                              0       0       0.00    0.00    0.00    0.00  
	
	http://389c1340.ngrok.io/playbook/backlog/githubimport
	
^This become the payload url. note that http://389c1340.ngrok.io/ points to localhost:8000 (the default)

- If you want to use HTTPS (the HTTP server must be configured):
    - https://\<host\>:\<port\>/playbook/backlog/githubimport
    - Remember to "Disable SSL verification" if you have a self signed certificate
- Content type: application/json
- Secret: chose a strong secret
- Which events would you like to trigger this webhook?
  - Choose "Let me select individual events" and check the "Issues" event.

Now we can configure the playbook\backlog\github_settings.py file (copy the name of the organization, your token, and your secret):

	GITHUB_OWNER = "\<GitHub Organization\>"
	GITHUB_TOKEN = "\<GitHub generated token\>"
	GITHUB_WEBHOOK_SECRET = "\<The secret you created on GitHub\>"

Running
=======

	python manage.py runserver [host:port]


example (add the same info you added when creating the webhook aka the same host and port):
	
	python manage.py runserver 


Now you can go to \<host\>:\<port\>/admin and login using the user created above. 

example--type this into the web url: 

	localhost:8000/admin


You can create groups and regular users that will be used to login into the playbook application (\<host\>:\<port\>/playbook).

example--type this into the web url: 

	localhost:8000/playbook


###Let's Get Started!

After logging into the admin interface, create a new user, using the same email you specified when running the static_inserts.sql file. The email field will be the link between the django auth user and the NorthBridge volunteer. Add the "Volunteers" group to the "Chosen groups" field of the user.

Creating User:

go to localhost:8000/admin (still have the runserver running on the terminal).
Under the Authentication and Authorization administration tab click on "Users". Add a new user example: newuser and give a password (i.e. password); type it 2x and click save!

Congrats! you just created your first user! (well other than the user you created while in the terminal--that createsuperuser command) So what can this user do?!

You should have been directed to a new page where you can fill out neat stuff about your user. Do whatever you like!

Example:
	
	Personal Info:
	first name: new
	last name: user
	email: newuser@newuser.gq
	
	Permissions: Active
	Groups: Volunteer (add-- click the arrow)
	User Permissions: admin | log entry | can change log entry (add-- click the arrow)
	Date joined: today & now
	click SAVE!

####Remember creating your superuser in the terminal?
while still in the admin page under "Core" click on Volunteers. Recognize someone? there you are!

Now you are ready to logout from admin account and access the application using the regular user you have created above.

####To the Playbook!

Go to localhost:8000/playbook

A main restriction is that the user's email must match the volunteer's email. It is through this relation that we can link a django user and the volunteer's informations. For now there is no database constraint ensuring this.
