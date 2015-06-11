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
import logging.config
from pygithub3 import Github
from milestoneDAO import MilestoneDAO
from issueDAO import IssueDAO
from issue import Issue, createAcceptIssue

def main():
    logging.config.fileConfig('logging.ini')
    logger = logging.getLogger("playbook")

    # START TIME
    logger.info('EXPORT PROCESS STARTED')
    
    exit_code = 0
    
    mDao = MilestoneDAO()
    iDao = IssueDAO()
    for milestone in mDao.getMilestones():
        milestoneNumber = milestone.create()
        if milestoneNumber is None:
            logger.error("Error when trying to create milestone.")
        else:
            logger.info("Milestone created with #%d [Title: \'%s\']" % (milestoneNumber, milestone.getTitle()))
            logger.info("Creating associated issues:")
            for issue in iDao.getIssuesByMilestone(milestone):
                issueNumber = issue.create() 
                if issueNumber is None:
                    logger.error("\tError creating Issue associated with milestone #%d" % milestoneNumber)
                else:
                    logger.info("\tIssue #%d [Title: \'%s\'] associated to Milestone #%d" % (issueNumber, issue.getTitle(), milestoneNumber))
            issue, issueNumber = createAcceptIssue(milestone.getNumber(), milestone.getRepo())
            if issueNumber is None:
                logger.error("\tError creating Accept Issue associated with milestone #%d" % milestoneNumber)
            else:
                logger.info("\tAccept Issue #%d associated to Milestone #%d" % (issueNumber, milestoneNumber))

    # END TIME
    logger.info('EXPORT PROCESS ENDED WITH EXIT CODE: %i', exit_code)

if __name__ == "__main__":
    main()