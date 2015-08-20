# The Problem 

GitHub provides lots of essential things that are needed in order to collaborate productively in an open-source, decentralized way: self managed user accounts, teams, messaging, task management, and even simple burndown charting. There is one component that Northbridge Technology Alliance needs in order to make GitHub hit the sweet spot of our agile development methodology, and that is backlog management.

This project provides a web-based backlog that Northbridge uses to prioritize all of our volunteer work across several projects. When a team selects a user story to accomplish, a button push exports the story into GitHub as a milestone and the associated acceptance criteria as tasks associated to that milestone.

Upon completion of the milestone, a GitHub API web hook is used to signal that the story is complete, and our backlog is udated accordingly.

We have researched lots of task management tools, and there are some very nice ones available. However they generally required the construction of a rather siloed user base. Northbridge wants to leverage the user infrastructure of GitHub, and all the other GitHub goodness. So this project give us the backlog we need in order to do that seamlessly.

# Overview

This repository wiki describes Northbridge agile team processes.

This repository code supports the Alliance project, which is responsible
for the interactions between Northbridge agile team processes and GitHub
issues tracking.

There are three major components to Alliance: **web interface**,
**export**, and **import**. These are represented as the yellow
components of this diagram.

- **Web Interface**: Allows Northbridge volunteers to estimate and
  select user stories from a prioritized backlog of work.

- **Export**: When invoked, export all Backlog User Stories in state
  "Selected" from the database to a GitHub Issues list using the GitHub
API.

- **Import**: When invoked, update a Backlog User Story to Accepted.
  This process will respond to a GitHub Issues Webhook.

![Project Diagram](http://northbridgetech.org/images/alliance2.jpg)

# Setup

In order to work on these files, search for "NorthBridge Playbook" in
Github and click on "fork" to have a copy in your own repository section
in your profile.

Click on "Clone in Desktop" in order to have a copy of all of the files
on your Desktop (or wherever you choose to save and access the files)

Open the files in your favorite text editor (I like to use Atom) and cd
into the project in your terminal.

Now you should be ready to work on the project!

# Installation

This guide will explain how to install the following:

- Python 2.7+ (not Python 3)
- Pip
- VirtualEnvWrapper
- PostgreSQL 9.4
- Django

## Install Python 2 (2.7 or higher)

### Installing on Windows

You'll need to know if you have 32 or 64 bit Windows. You can find out
by [following the instructions
here](https://support.microsoft.com/en-us/kb/827218). To install on
Windows, download the Python installer [found
here](https://www.python.org/downloads/windows/) for Windows. If you
have a 32-bit operating system, download the `Windows x86 MSI
installer`. If you have a 64-bit operating system, download the `Windows
x86-64 MSI Installer`.

Alternatively, you can install [Chocolatey](https://chocolatey.org/) and
install Python from the command line by opening up `Powershell` and
executing the following command: `choco install python2`.

### Installing on Mac OS X

To install on OS X, download the Python installer [found
here](https://www.python.org/downloads/mac-osx/).

Alternatively, you can install [Homebrew](http://brew.sh/) and install
Python from the command line by opening up a `Terminal` and executing
the following command: `brew install python`.

### Installing on Linux Ubuntu (and other `apt` distributions)

TODO (ensure to include python-dev)

## Installing project dependencies

There are two ways to do this:

### Use a virtual environment (Ubuntu):

Install pip

    sudo apt-get install python-pip

Install virtualenv using pip

    pip install virtualenvwrapper

Add the following two lines to your ~/.bashrc script:

    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh

Close the file and source it:

    source ~/.bashrc

Go to the project directory: Make sure you are in the directory playbook
(if you do "ls" in your command line you will find there is another
folder called playbook. Don't go in there. Stay here.)

    mkvirtualenv playbook

The next command is only necessary if you are not already using the
created virtualenv.

    workon playbook

You should see `(playbook)` before your project directory

Finally, install any python dependencies:

    pip install -r requirements.txt

If you encounter errors, setup PostgreSQL and come back to this step.

### Use your global python environment

Directly install the dependencies listed in `requirements.txt` using
`pip` or the `easy_install` utility. If you are using Mac you will have
to configure psycopg2 setting up the file path for postgresql and then
restart the terminal to avoid errors.

## Install PostgreSQL

### Ubuntu

Helpful link: https://help.ubuntu.com/community/PostgreSQL

### Mac

a) Download Postgres.app from http://postgresapp.com/

b) Add the path to ~/.profile

	echo 'export PATH="/Applications/Postgres.app/Contents/Versions/9.4/bin:$PATH"' >> ~/.profile
	source ~/.profile

## Update your database connection settings using your database admin user

The database settings are located in the playbook/settings.py file and
must be updated to represent your local environment. You can name your
database whatever you like. In this guide, we assume that the name is
`devwaterwheel`.

Create the database `devwaterwheel` by running the following SQL command
(you can use psql or any client of your choice):

    create database devwaterwheel;

Do not forget to use the correct database user and password in the
settings.py file. Here is how you could change your database password,
assuming the user is 'postgres'.

In your linux terminal, considering your database user is postgres,
type:

    sudo -u postgres psql postgres

Alternatively, you can also use the following command:

    sudo su - postgres
    psql

Now that you are connected to the psql:

  \password postgres

### Configure Django

Run Django migration scripts:

    python manage.py makemigrations
    python manage.py migrate

Create a superuser (you will be prompted to type in a username, email
and password):

    python manage.py createsuperuser

Use the `db/static_inserts.sql` file to populate the database with
useful testing information:

Open the file and update the lines below with your information:

    \set email '\'' '\<The email you used to create the django account>' '\''
    \set fname '\'' '\<your first name>' '\''
    \set lname '\'' '\<your last name>' '\''

For example:

    \set email '\'' 'johndoe@gmail.com' '\''
    \set fname '\'' 'John' '\''
    \set lname '\'' 'Doe' '\''

After that, run the following command to import the data (you must be
logged as a user that has privileges to access/update the database or
provide user/password information to psql):

    psql devwaterwheel < /path/to/your/static_inserts.sql

We also must create a trigger that will be responsible for update the
`backlog.update_dttm` field. This trigger will be fired on a row update
event. The `Postgres_Update_Trigger.sql` script is located under the db
folder. If you have a test database, run the following command:

    psql devwaterwheel_test < Postgres_Update_Trigger.sql

There is also two other files that must be updated:
`playbook/email_settings.py` (information concerning email service) and
`playbook/backlog/github_settings.py` (information used to interact with
the github API).

The system can notify users through email when an error on modules
import/export occurs. Configuration can be done in the file
`email_settings.py`. As an example, to send the emails using gmail
service, one could configure the file as shown below:

    # Email configuration
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'exampleName@gmail.com'
    EMAIL_HOST_PASSWORD = 'myPassword'
    EMAIL_PORT = 587
    EMAIL_RECIPIENT_LIST = ['exampleName2@gmail.com', 'exampleName3@yahoo.com']

The main functionality of the system is the integration with the GitHub
API. In order to put this integration to work there are some
pre-requirements that must be met:

  - You must have a GitHub Organization
  - The GitHub repositories must be inside this organization. Of course,
    a repository must exist before the system can interact with it.
  - You must create a "Personal access token":
    - Click on your GitHub profile picture and select "Settings"
    - Chose "Personal access tokens" on the left menu
    - Chose a description for the token
    - Select the scopes: `repo`, `public_repo`, `user`, `gist`
    - Click "Generate token"
    - Copy the generated token as we will use it later (warning: You
      cannot access the generated token after leaving the page so be
      careful to store it elsewhere)
  - You must configure a GitHub webhook inside the Organization:
    - The Payload URL must point to:
      - If you are running over HTTP (for example, through manage.py
        script):
        - `http://\<host\>:\<port\>/playbook/backlog/githubimport`
      - If you want to use HTTPS (the HTTP server must be configured):
        - `https://\<host\>:\<port\>/playbook/backlog/githubimport`
        - Remember to "Disable SSL verification" if you have a
          self-signed certificate
    - Content type: `application/json`
    - Secret: chose a strong secret
    - Which events would you like to trigger this webhook?
      - Choose "Let me select individual events" and check the "Issues"
        event.

Now we can configure the `github_settings.py` file:

    GITHUB_OWNER = "\<GitHub Organization\>"
    GITHUB_TOKEN = "\<GitHub generated token\>"
    GITHUB_WEBHOOK_SECRET = "\<The secret you created on GitHub\>"

## Running

    python manage.py runserver [host:port]

Now you can go to `\<host\>:\<port\>/admin` and login using the user
created above. You can create groups and regular users that will be used
to login into the playbook application (`\<host\>:\<port\>/playbook`).

After logging into the admin interface, create a new user, using the
same email you specified when running the `static_inserts.sql` file. The
email field will be the link between the django auth user and the
NorthBridge volunteer. Add the "Volunteers" group to the "Chosen groups"
field of the user.

Now you are ready to logout from admin account and access the
application using the regular user you have created above.

A main restriction is that the user's email must match the volunteer's
email. It is through this relation that we can link a django user and
the volunteer's informations. For now there is no database constraint
ensuring this.

