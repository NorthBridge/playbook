from datetime import datetime
from pygithub3 import Github
import unittest

from . import common_test
from common_test import Fixtures
from .. import export
from ...utils.configHelper import getConfig
from ...utils.constants import (SELECTED_STATUS, IN_PROGRESS_STATUS,
                                ACCEPT_ISSUE_TITLE, ACCEPT_ISSUE_LABEL,
                                STATIC_LABEL_VALUE)
from ..dao.baseDAO import BaseDAO

class ExportTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(ExportTest, self).__init__(*args, **kwargs)
        token = getConfig("github.token")
        owner = getConfig("github.owner")
        self.__eventId = -1
        self.__backlogId = -1
        self.__accCriteriaId = -1
        self.__bDAO = BaseDAO()
        self.__gh = Github(token=token, user=owner, repo=Fixtures.REPO)
        
    def setUp(self):
        #Set up the environment for the test
        # i.e. create test milestone, related issues in database and
        # also a test repo in github
        self.__backlogId, self.__accCriteriaId, self.__eventId = (
            common_test.environ_setup(self.__bDAO, 
            event_name = Fixtures.EVENT_NAME,
            scheduled_id = Fixtures.SCHEDULE_ID,
            milestone_start_date = Fixtures.MILESTONE_START_DATE,
            milestone_due_on = Fixtures.MILESTONE_DUE_ON,
            milestone_title = Fixtures.MILESTONE_TITLE, 
            milestone_desc = Fixtures.MILESTONE_DESC,
            team_id = Fixtures.TEAM_ID,
            repo = Fixtures.REPO,
            acc_cri_title = Fixtures.ACC_CRI_TITLE,
            acc_cri_desc = Fixtures.ACC_CRI_DESC))
        
        common_test.github_createRepo(self.__gh, 
                                      repo = Fixtures.REPO,
                                      repo_desc = Fixtures.REPO_DESC)
        super(ExportTest, self).setUp()
            
    def tearDown(self):
        #Clean up the environment after the test
        # i.e. remove test milestone and related issues from database
        # then remove the test repo from GitHub
        common_test.environ_cleanup(self.__bDAO, 
                                    acc_criteria_id=self.__accCriteriaId,
                                    backlog_id=self.__backlogId,
                                    event_id=self.__eventId)
        common_test.github_remove(self.__gh)
        super(ExportTest, self).tearDown()
    
    def test(self):
        #invoke the export script
        export.main()
        
        status_id_check = """SELECT status_id_fk FROM backlog WHERE id = %s"""
        cur = self.__bDAO.execute(status_id_check, (self.__backlogId,))
        row = cur.fetchone()
        
        self.assertEqual(row['status_id_fk'], IN_PROGRESS_STATUS)
        
        #check if all aspects of the script were successfully executed
        #retrieve milestone and its issues from github and verify data
        backlog_select_row = """SELECT ac.id, ac.title, ac.descr as dac, b.id, 
                                       b.story_title, b.story_descr, 
                                       b.github_number, b.github_repo, 
                                       e.end_dttm, t.name
                                  FROM acceptance_criteria ac, backlog b, 
                                       team t, event e
                                 WHERE b.id = %s
                                   AND b.sprint_id_fk = e.id
                                   AND ac.backlog_id_fk = b.id
                                   AND b.team_id_fk = t.id;"""
        cur = self.__bDAO.execute(backlog_select_row, (self.__backlogId,))
        rows = cur.fetchall()
        
        for row in rows:
            ghMilestone = self.__gh.issues.milestones.get(row['github_number'])
            
            self.assertEqual(ghMilestone.title, row['story_title'])
            self.assertEqual(ghMilestone.description, row['story_descr'])
            self.assertEqual(ghMilestone.state,'open')
            ghDateStr = datetime.strftime(ghMilestone.due_on, '%Y-%m-%d')
            self.assertEqual(ghDateStr, Fixtures.MILESTONE_DUE_ON)
            
            ghIssues = self.__gh.issues.list_by_repo(milestone=ghMilestone.number)
            
            self.assertEqual(len(ghIssues.all()), 2)
            
            for issue in ghIssues.all():
                #TODO: Check if the accept issue label is the only one???
                if any(label.name == ACCEPT_ISSUE_LABEL 
                       for label in issue.labels):
                    self.assertEqual(issue.title, ACCEPT_ISSUE_TITLE)
                else:
                    self.assertEqual(issue.body, row['dac'])
                    self.assertEqual(str(issue.milestone.number), 
                                     row['github_number'])
                    self.assertTrue(len(issue.labels) == 2)
                    self.assertTrue(any(label.name == STATIC_LABEL_VALUE 
                                            for label in issue.labels))
                    self.assertTrue(any(label.name == row['name'] 
                                            for label in issue.labels))
                                           
if __name__ == '__main__':
    unittest.main()
