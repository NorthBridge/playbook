from .. import export
import unittest
from ..dao.baseDAO import BaseDAO
from ..dao.issueDAO import IssueDAO
from ...utils.constants import (SELECTED_STATUS, IN_PROGRESS_STATUS, 
                                ACCEPT_ISSUE_TITLE, ACCEPT_ISSUE_LABEL, 
                                STATIC_LABEL_VALUE)
from ..model.issue import Issue 
from pygithub3 import Github
from ...utils.configHelper import getConfig
from datetime import datetime

class ExportTest(unittest.TestCase):
    
    TEAM_ID = 10
    SCHEDULE_ID = 1
    EVENT_NAME = 'Sprint Test Export'
    REPO = 'Export-Test-Repository-Northbridge'
    REPO_DESC = 'Temporary repository used by automated testing of Export module.'
    MILESTONE_START_DATE = '2015-07-11'
    MILESTONE_DUE_ON = '2015-07-04'
    MILESTONE_TITLE = 'Milestone Test Export Module'
    MILESTONE_DESC = 'This milestone was created by the test_export module'
    ACC_CRI_TITLE = 'Acceptance Criteria Test'
    ACC_CRI_DESC = 'Temporary acceptance criteria used by the test_export module'
    
    def __init__(self, *args, **kwargs):
        super(ExportTest, self).__init__(*args, **kwargs)
        token = getConfig("github.token")
        owner = getConfig("github.owner")
        self.__eventId = -1
        self.__backlogId = -1
        self.__accCriteriaId = -1
        self.__bDAO = BaseDAO()
        self.__gh = Github(token=token, user=owner, repo=ExportTest.REPO)
        
    def setUp(self):
        #Set up the environment for the test
        # i.e. create test milestone, related issues in database and
        # also a test repo in github
        self.environ_setup()
        self.github_createRepo() 
        super(ExportTest, self).setUp()
            
    def tearDown(self):
        #Clean up the environment after the test
        # i.e. remove test milestone and related issues from database
        # then remove the test repo from GitHub
        self.environ_cleanup()
        self.github_remove()
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
            self.assertEqual(ghDateStr, ExportTest.MILESTONE_DUE_ON)
            
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
                                           
    def github_createRepo(self):
        data = { 'name': ExportTest.REPO,
                 'description': ExportTest.REPO_DESC}
        self.__gh.repos.create(data)
        
    def environ_setup(self):        
        event_create_row = """INSERT INTO event (
            name,
            schedule_id_fk,
            start_dttm,
            end_dttm) VALUES (
            %s,
            %s,
            %s,
            %s) RETURNING id;"""
            
        backlog_create_row = """INSERT INTO backlog (
            id,
            story_title,
            story_descr,
            sprint_id_fk,
            status_id_fk,
            team_id_fk,
            github_repo) VALUES (
            DEFAULT,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s) RETURNING id;"""
            
        acc_crit_create_row = """INSERT INTO acceptance_criteria (
            backlog_id_fk,
            title,
            descr) VALUES (
            %s,
            %s,
            %s) RETURNING id;"""

        #Insert into event table            
        cur = self.__bDAO.execute(event_create_row, (ExportTest.EVENT_NAME,
                                                     ExportTest.SCHEDULE_ID,
                                                     ExportTest.MILESTONE_START_DATE,
                                                     ExportTest.MILESTONE_DUE_ON))
        self.__eventId = cur.fetchone()[0]
        #Insert into backlog table
        cur = self.__bDAO.execute(backlog_create_row,(ExportTest.MILESTONE_TITLE,
                                                      ExportTest.MILESTONE_DESC, 
                                                      self.__eventId,
                                                      SELECTED_STATUS,
                                                      ExportTest.TEAM_ID,
                                                      ExportTest.REPO))
        self.__backlogId = cur.fetchone()[0]
        #Insert into acceptance_criteria table
        cur = self.__bDAO.execute(acc_crit_create_row, (self.__backlogId,
                                                        ExportTest.ACC_CRI_TITLE,
                                                        ExportTest.ACC_CRI_DESC))
        self.__accCriteriaId = cur.fetchone()[0]
        #Commit the three inserts
        self.__bDAO.getConnection().commit()

    def environ_cleanup(self):        
        event_delete_row = """DELETE FROM event 
                                    WHERE id = %s;"""
        accCriteria_delete_row = """DELETE FROM acceptance_criteria
                                          WHERE id = %s;"""
        backlog_delete_row = """DELETE FROM backlog 
                                      WHERE id = %s;"""
                                        
        cur = self.__bDAO.execute(accCriteria_delete_row,(self.__accCriteriaId,))
        cur = self.__bDAO.execute(backlog_delete_row,(self.__backlogId,))
        cur = self.__bDAO.execute(event_delete_row,(self.__eventId,))
        self.__bDAO.getConnection().commit()

    def github_remove(self):
        # In order to remove a repo, if OAuth is used, the delete_repo
        #  scope is required.
        self.__gh.repos.delete()
        
if __name__ == '__main__':
    unittest.main()
