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
            milestoneNumber = milestone.create()
            logger.info("Milestone created with #%s [Title: \'%s\']" % (milestoneNumber, milestone.getTitle()))
            logger.info("Creating associated issues:")
            for issue in iDao.getIssuesByMilestone(milestone):
                issueNumber = issue.create() 
                logger.info("Issue #%d [Title: \'%s\'] associated to Milestone #%s" % (issueNumber, issue.getTitle(), milestoneNumber))
            issue, issueNumber = createAcceptIssue(milestone.getNumber(), milestone.getRepo())
            logger.info("Accept Issue #%d associated to Milestone #%s" % (issueNumber, milestoneNumber))
    except:
        logger.exception("Exception exporting milestones to github:")
        exit_code = 1

    # END TIME
    logger.info('EXPORT PROCESS ENDED WITH EXIT CODE: %i', exit_code)

if __name__ == "__main__":
    main()