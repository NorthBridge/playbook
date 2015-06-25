import unittest
import common_test
from .. import export
from common_test import Fixtures 
from ..dao.baseDAO import BaseDAO
from ..dao.issueDAO import IssueDAO 
from ..dao.milestoneDAO import MilestoneDAO
from pygithub3 import Github
from ...utils.configHelper import getConfig
from ...utils.constants import ACCEPT_ISSUE_LABEL, GH_CLOSED_STATE, GH_OPEN_STATE
import time

'''
    When any issue of a specific github organization is updated the trigger is 
     fired (webhook). The first thing to verify is if the issue has a special 
     label: "owner acceptance". Also, only two special actions are treated: 
     "close" and "reopen".
    
    Test planning:
        0- Run ngrok on port 5000 and update the webhook URL to the "Forwarding"
            URL that ngrok shows
        1- Run the ghimport.py script to accept connections (manually?)
        2- Create a test repository on github
        3- Create some data test and export issues to the repository
        4- Close a github issue that do not have the specific label.
            - Assert that nothing has changed: No database or github updates
        5- Close a github issue that contains the specific label.
            - Asser that:
                - The backlog record relative to the issue is updated with
                  status_id_fk = 16
                - The github milestone linked to the issue is updated with 
                  state = 'closed'
        6- Reopen the issue previously closed.
            - Assert that:
                - The backlog record relative to the issue is updated with
                  status_id_fk = 15
                - The github milestone linked to the issue is updated with
                  state = 'open'
        7- Remove data test from database and from github
        5- Kill the ghimport.py process
'''
class GHImportTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(GHImportTest, self).__init__(*args, **kwargs)
        token = getConfig("github.token")
        owner = getConfig("github.owner")
        self.__eventId = -1
        self.__backlogId = -1
        self.__accCriteriaId = -1
        self.__bDAO = BaseDAO()
        self.__gh = Github(token=token, user=owner, repo=Fixtures.REPO)
     
    def setUp(self):
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
        super(GHImportTest, self).setUp()
     
    def tearDown(self):
        common_test.environ_cleanup(self.__bDAO, 
                                    acc_criteria_id=self.__accCriteriaId,
                                    backlog_id=self.__backlogId,
                                    event_id=self.__eventId)
        common_test.github_remove(self.__gh)
        super(GHImportTest, self).tearDown()
     
    def test(self):
        #Last part of step #3
        export.main()
        
        #Getting all the entities that were created through the export 
        # process to later compare them
        milestone = MilestoneDAO().find_by_id(self.__backlogId)
        new_issues_from_db = IssueDAO().getIssuesByMilestone(milestone)
        owner_acc_issue, common_issue = self.retrieve_new_issues_from_gh(milestone)

        #Step #4
        self.__gh.issues.update(common_issue.number, 
                                self.create_data(common_issue, 'closed'))
        self.assert_step_4(milestone, owner_acc_issue, common_issue)
        
        #step #5
        self.__gh.issues.update(owner_acc_issue.number, 
                                  self.create_data(owner_acc_issue, 'closed'))
        print "Waiting 5 seconds for the webhook request..."
        time.sleep(5)
        self.assert_step_5(milestone, owner_acc_issue)
        
        #step #6
        self.__gh.issues.update(owner_acc_issue.number, 
                                  self.create_data(owner_acc_issue, 'open'))
        print "Waiting 5 seconds for the webhook request..."
        time.sleep(5)
        self.assert_step_6( milestone, owner_acc_issue)
        
        print "Waiting 5 seconds for the webhook request..."
        time.sleep(5)
        
        
    def assert_step_4(self, milestone, owner_acc_issue, common_issue):
        new_milestone = MilestoneDAO().find_by_id(self.__backlogId)
        self.assertEqual(new_milestone.getState(), milestone.getState())
        
        after_owner_acc_issue, after_common_issue = self.retrieve_new_issues_from_gh(milestone)
        self.assertEqual(owner_acc_issue.state, after_owner_acc_issue.state)
        self.assertNotEqual(after_common_issue.state, common_issue.state)
        self.assertEqual(after_common_issue.state, GH_CLOSED_STATE)
    
    def assert_step_5(self, milestone, owner_acc_issue):
        #Assert that milestone was closed
        new_milestone = MilestoneDAO().find_by_id(self.__backlogId)
        self.assertNotEqual(new_milestone.getState(), milestone.getState())
        self.assertEqual(new_milestone.getState(), GH_CLOSED_STATE)
        
        #Assert that the issue was closed
        after_owner_acc_issue, after_common_issue = self.retrieve_new_issues_from_gh(milestone)
        self.assertNotEqual(owner_acc_issue.state, after_owner_acc_issue.state)
        self.assertEqual(after_owner_acc_issue.state, GH_CLOSED_STATE)
    
    def assert_step_6(self, milestone, owner_acc_issue):
        #Assert that the acceptance issue was reopened
        after_owner_acc_issue, after_common_issue = self.retrieve_new_issues_from_gh(milestone)
        self.assertEqual(owner_acc_issue.state, after_owner_acc_issue.state)
        self.assertEqual(after_owner_acc_issue.state, GH_OPEN_STATE)
        
        #Assert that, after the acceptance issue was reopened, 
        # the milestone was also reopened
        new_milestone = MilestoneDAO().find_by_id(self.__backlogId)
        self.assertEqual(new_milestone.getState(), milestone.getState())
        self.assertEqual(new_milestone.getState(), GH_OPEN_STATE)
        
    
    def create_data(self, issue, state):
        data = { 'title': issue.title,
                 'body' : issue.body,
                 'assignee': issue.assignee,
                 'state': state,
                 'milestone': issue.milestone.number,
                 'labels': issue.labels
        }
        return data
    
    def retrieve_new_issues_from_gh(self, milestone):
        ghIssues = self.__gh.issues.list_by_repo(milestone=
                                                 milestone.getNumber(),
                                                 state='all')

        owner_acc_issue = None
        common_issue = None
        
        for issue in ghIssues.all():
            if any(label.name == ACCEPT_ISSUE_LABEL 
                       for label in issue.labels):
                owner_acc_issue = issue
            else:
                common_issue = issue
                
        return (owner_acc_issue, common_issue)
                
if __name__ == '__main__':
    unittest.main()