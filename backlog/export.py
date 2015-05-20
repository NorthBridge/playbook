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
    time.sleep(5)

    # END TIME
    logging.critical('EXPORT PROCESS ENDED WITH EXIT CODE: %i', exit_code)

main()
