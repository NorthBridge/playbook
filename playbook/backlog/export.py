# This file is part of "playbook".
# Module: Export
# Copyright 2015, Northbridge Technology Alliance.
# This is free software.
# You may use, copy, modify, or distribute under the terms of GPLv3 or newer.
# No warranty.

# Last updated: Jun 12, 2015 10:00 GMT-6

# Description: Alliance Backlog Export Module
#              Exports data from PostgreSQL database to GitHub

import logging.config
from .dao.milestoneDAO import MilestoneDAO
from .dao.issueDAO import IssueDAO
from .model.issue import createAcceptIssue

def main():
    logging.config.fileConfig('logging.ini')
    logger = logging.getLogger("playbook")

    # START TIME
    logger.info('EXPORT PROCESS STARTED')
    
    exit_code = 0
    
    mDao = MilestoneDAO()
    iDao = IssueDAO()
    try:
        for milestone in mDao.getMilestones():
            try:
                milestoneNumber = milestone.create()
                logger.info("Creating associated issues:")
            except:
                #If something wrong happened, it is already logged and we do not
                # continue exporting issues related to this milestone. But we
                # try to export following milestones/issues if they exists.
                exit_code = 1
            else:
                for issue in iDao.getIssuesByMilestone(milestone):
                    try:
                        issueNumber = issue.create() 
                    except:
                        #Same thing here, if something goes wrong when exporting
                        # the current issue, it is already logged and we continue
                        # with the next one.
                        exit_code = 1
                try:
                    issue, issueNumber = createAcceptIssue(milestone.getNumber(), 
                                                           milestone.getRepo())
                except:
                    exit_code = 1
    except:
        logger.exception("Exception exporting milestones to github:")
        exit_code = 1

    # END TIME
    logger.info('EXPORT PROCESS ENDED WITH EXIT CODE: %i', exit_code)

if __name__ == "__main__":
    main()