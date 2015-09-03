Installation on Mac
===================

####1. Install python, version 2.7 or higher

####2. Install project dependencies. There are two ways to do this.

#####First way: Use a virtual environment:

a) Install pip

Using easy_install:
    
    sudo easy_install pip

Using homebrew:

    brew install python
    
b) Create virtual environment

Install virtualenvwrapper:

    pip install virtualenvwrapper

Go to the project directory:

    cd PATH/TO/PROJECT

Make new virtualenv
    
    mkvirtualenv playbook

Use the virtualenv
    
    workon playbook

c) Install dependencies

    sudo pip install -r requirements.txt

#####Second way: Use your global python environment

Install all of the dependencies listed in requirements.txt using the easy_install utility
    
Example:

    easy_install psycopg2


###3) Install PostgreSQL

a) Download Postgres.app from http://postgresapp.com/

b) Add the Postgres app path to your ~/.profile.
    
Example:

    echo 'export PATH="/Applications/Postgres.app/Contents/Versions/9.4/bin:$PATH"' >> ~/.bash_profile

    source ~/.bash_profile

c) Create a superuser called postgres
    
    createuser -P -s -e postgres

You will be prompted for a password. Set it as 'postgres' or update the database settings located in the playbook/settings.py file.

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

d) Enter the Postgres interactive terminal (psql) as the superuser

    psql -U postgres

create database northbr6_devwaterwheel;

Note: You may need to change permissions if you get the following error

    ERROR: permission denied to create database

To do so, in psql run

    grant all privileges on database northbr6_devwaterwheel to postgres

###5) Install Django

###6) Install the project

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


Troubleshooting Errors
======================

#### Error: pg_config executable not found.
    
Make sure PostGres is installed (see Step 3) Install PostgreSQL).
