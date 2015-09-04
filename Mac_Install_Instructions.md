Installation on Mac
===================

###1) Install python, version 2.7 or higher

###2) Install project dependencies. There are two ways to do this.

#####First way: Use a virtual environment

a) Install pip using easy_install or homebrew

Using easy_install:
    
    sudo easy_install pip

Using homebrew:

    brew install python

b) Create virtual environment

Install virtualenvwrapper:

    pip install virtualenvwrapper

Add the paths to your ~/.bash_profile:
    
    echo 'export WORKON_HOME=$HOME/.virtualenvs' >> ~/.bash_profile

    echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bash_profile

    source ~/.bash_profile

Go to the project directory:

    cd /HOME/PATH/TO/PLAYBOOK

Make a new virtual environment called "playbook":
    
    mkvirtualenv playbook

Use the virtual environment you just created (if not already):
    
    workon playbook

*NOTE: To get out of the virtual environment, type `deactivate`.

c) Install dependencies (while in the virtual environment)

    sudo pip install -r requirements.txt

*NOTE: Running this installs the following packages to your virtual environment (only in playbook):
    
    django==1.8.2
    ipaddress==1.0.7
    psycopg2==2.6.1
    pygithub3==0.5.1
    requests==2.7.0


#####Second way: Use your global python environment

Install all of the dependencies listed in `requirements.txt` using the easy_install utility
    
Example:

    easy_install django ipaddress psycopg2 pygithub3 requests


###3) Install PostgreSQL

a) Download Postgres.app from http://postgresapp.com/

b) Add the Postgres app path to your ~/.bash_profile.
    
Example:

    echo 'export PATH=$HOME/Applications/Postgres.app/Contents/Versions/9.4/bin:$PATH' >> ~/.bash_profile

    source ~/.bash_profile

c) Create a superuser called 'postgres'
    
    createuser -P -s -e postgres

You will be prompted for a password. Set it as 'postgres'.

###4) Update your database connection settings using your database admin user

The database settings must be updated to represent your local environment. They are located in the `playbook/settings.py` file.

Example:
```python
...

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'northbr6_devwaterwheel',
    'USER': 'postgres', # your Postgres username
    'PASSWORD': 'postgres', # your password
    'HOST': '127.0.0.1',
    'PORT': '5432',
    }
}

...
```
In this guide, we assume that that you are using user 'postgres' with password 'postgres', port '5432' and database 'northbr6_devwaterwheel'. However, you can use whatever you like so long as things match.

a) Enter the Postgres interactive terminal (psql) as the superuser

    psql -U postgres

b) Make a new database, called "northbr6_devwaterwheel". Don't forget the semicolons!
    
    create database northbr6_devwaterwheel;

When finished, press control+d to exit.

*NOTE: You may need to change user permissions if you see `ERROR: permission denied to create database` (see 3c).

Alternatively, if you create the database with a different superuser, you can transfer permissions to 'postgres'. In psql, run

    grant all privileges on database northbr6_devwaterwheel to postgres;

###5) Configure Django

a) Run Django migrate scripts (only AFTER database is setup & configured):

    python manage.py makemigrations
    python manage.py migrate

b) Create a Django superuser, which will also be your playbook admin user login (you will be prompted to type in a username, email, and password):

    python manage.py createsuperuser

c) Open the `db/static_inserts.sql` file. This will be used to populate the database with useful testing data. Update it with your admin user information:

```sql
    \set email '\'' '\<The email you used to create the django account>' '\''
    \set fname '\'' '\<your first name>' '\''
    \set lname '\'' '\<your last name>' '\''
    \set github_repo '\'' '<github test repo>' '\''
```
i) After that, run the following command to import the data (you must be logged as a user that has privileges to access/update the database or provide user/password information to psql):

    psql -U postgres northbr6_devwaterwheel < /HOME/PATH/TO/PLAYBOOK/db/static_inserts.sql

ii) We also must create a trigger that will be responsible for update the backlog.update\_dttm field. This trigger will be fired on a row update event. The Postgres_Update_Trigger.sql script is located under the db folder.

    psql -U postgres northbr6_devwaterwheel_test < /HOME/PATH/TO/PLAYBOOK/db/Postgres_Update_Trigger.sql

d) There are also two other files that must be updated:
* `playbook/email\_settings.py` (information concerning email service) 
* `playbook/backlog/github_settings.py` (information used to interact with the github API).

i) The system can notify users through email when an error on modules import/export occurs. Configuration can be done in the file `email_settings.py`. As an example, to send the emails using gmail service, one could configure the file as shown below:

```python
    # Email configuration
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'exampleName@gmail.com'
    EMAIL_HOST_PASSWORD = 'myPassword'
    EMAIL_PORT = 587
    EMAIL_RECIPIENT_LIST = ['exampleName2@gmail.com']
```    

ii) The main functionality of the system is the integration with the GitHub API. In order to put this integration to work there are some pre-requirements that must be met:

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

install ngrok: https://ngrok.com/download
-first download and then unzip
-you can extract it in your downloads folder and then run it:

    ~/Downloads/ngrok http 8000


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

Now we can configure the `backlog\github_settings.py` file (copy the name of the organization, your token, and your secret):

```python
    GITHUB_OWNER = "\<GitHub Organization\>"
    GITHUB_TOKEN = "\<GitHub generated token\>"
    GITHUB_WEBHOOK_SECRET = "\<The secret you created on GitHub\>"
```

Running
=======

a) From your root project directory, run

    python manage.py runserver [host:port]

Example (use the same host & port you added when creating the webhook):
    
    python manage.py runserver 

b) Now you can go to \<host\>:\<port\>/admin and login using the Django user created above. 

Example (type this into the web url):

    localhost:8000/admin

You can create groups and regular users that will be used to login into the playbook application (\<host\>:\<port\>/playbook).

Example (type this into the web url):

    localhost:8000/playbook


###Let's Get Started!

After logging into the admin interface, create a new user using the same email you specified when running the `static_inserts.sql` file. The email field will be the link between the django auth user and the NorthBridge volunteer. Add the "Volunteers" group to the "Chosen groups" field of the user.

####Creating Users:

1) Go to [localhost:8000/admin](http://127.0.0.1:8000/admin) in a web browser (while still have the runserver running on the terminal).

2) Under the Authentication and Authorization administration tab click on "Users".

3) Add a new user (e.g. 'newuser') and give a password (e.g. 'password'); type it 2x and click save!

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

Congrats! you just created your first user! (well, other than the user you created while in the terminal--that createsuperuser command) So what can this user do?!

You should have been directed to a new page where you can fill out neat stuff about your user. Do whatever you like!

####Remember creating your superuser in the terminal?

While still in the admin page under "Core" click on Volunteers. Recognize someone? There you are!

Now you are ready to logout from admin account and access the application using the regular user you have created above.

####To the Playbook!

Go to [localhost:8000/playbook](http://127.0.0.1:8000/playbook) in a web browser.


Troubleshooting Errors
======================

#### Error: pg_config executable not found

Make sure PostGres is installed (see Step 3).

#### Error: permission denied to create database

Create a new PostGres user with superuser privileges (see Step 3c), or create the database from opening psql in the Postgres app and then transfering privileges (see Step 4b).

#### Error: unable to connect to localhost:8000/playbook

Make sure you still have runserver running on the terminal. From the project root directory, run

    python manage.py runserver
