# This file is part of "playbook".
# Module: Export
# Copyright 2015, Northbridge Technology Alliance.
# This is free software.
# You may use, copy, modify, or distribute under the terms of GPLv3 or newer.
# No warranty.

# Last updated: May 20, 2015 17:08 GMT-6

# Description: Alliance Backlog Export Module
#              Exports data from PostgreSQL database to GitHub

import logging
import sys
import argparse
import time
import json
from restkit import Resource, BasicAuth, Connection, request
from socketpool import ConnectionPool

def log_repos():
    logging.basicConfig(filename='export.log', level='DEBUG',
                        format='%(asctime)s %(message)s')
    logging.debug('log_repos called')
    pool = ConnectionPool(factory=Connection)
    serverurl="https://api.github.com"

    # add your username or password here, or prompt for them
    auth = BasicAuth("""user""","""password""")

    # use your basic auth to request a token
    # this is an example taken from http://developer.github.com/v3/
    authreqdata = { "scopes": [ "public_repo" ], "note": "Export Module" }
    resource = Resource('https://api.github.com/authorizations',
                        pool=pool, filters=[auth])
    response = resource.post(headers={ "Content-Type": "application/json" },
                             payload=json.dumps(authreqdata))
    token = json.loads(response.body_string())['token']
    # TODO: token needs to be cached somehow (in a config file?)
    # presently, this script only works once,
    # then get an error: authorization code already exists
    # personal access token then needs to be deleted from GitHub

    """
    Once you have a token, you can pass that in the Authorization header
    You can store this in a cache and throw away the user/password
    This is just an example query.  See http://developer.github.com/v3/
    for more about the url structure
    """
    resource = Resource('https://api.github.com/orgs/northbridge/repos',
                        pool=pool)
    headers = {'Content-Type' : 'application/json' }
    headers['Authorization'] = 'token %s' % token
    response = resource.get(headers = headers)
    repos = json.loads(response.body_string())

    # TODO: the following just dumps everything about all the repos ugly-like
    print(repos)

def main():
    exit_code = 0
    loglevel = 'ERROR'
    parser = argparse.ArgumentParser(description='Export Module')
    parser.add_argument('--log', action="store", dest="log")
    args = parser.parse_args()
    if sys.argv == 1:
        loglevel = args.log

    #logging.basicConfig(filename='export.log',level=logging.DEBUG)
    #loglevel = 
    # assuming loglevel is bound to the string value obtained from the
    # command line argument. Convert to upper case to allow the user to
    # specify --log=DEBUG or --log=debug
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(filename='export.log', level=numeric_level,
                        format='%(asctime)s %(message)s')

    # START TIME
    logging.critical('EXPORT PROCESS STARTED')

    # DO STUFF
    log_repos()

    # END TIME
    logging.critical('EXPORT PROCESS ENDED WITH EXIT CODE: %i', exit_code)

main()
