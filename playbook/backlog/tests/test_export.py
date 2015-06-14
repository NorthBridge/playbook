from .. import export
import unittest
from ..dao.baseDAO import BaseDAO
from ..dao.milestoneDAO import MilestoneDAO
from ..model.milestone import Milestone
from ..model.issue import Issue
import psycopg2.extras
from pygithub3 import Github
from ...utils.configHelper import getConfig

class ExportTest(unittest.TestCase):

    def environ_setup(self):
        # update database with test data

        # create test row for export in backlog
        backlog_create_row = """INSERT INTO backlog (
            id,
            story_title,
            story_descr,
            status_id_fk) VALUES (
            DEFAULT,
            'TEST',
            'This milestone was created by the test_export module',
            14);"""
        bDAO = BaseDAO()
        cur = bDAO.getConnection().cursor(
                                      cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(backlog_create_row,)
        bDAO.getConnection().commit()
        cur.close()

    def environ_cleanup(self):
        # remove test data from backlog table
        backlog_delete_row = """DELETE FROM backlog WHERE 
                                story_title = 'TEST';"""
        bDAO = BaseDAO()
        cur = bDAO.getConnection().cursor(
                                      cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(backlog_delete_row,)
        bDAO.getConnection().commit()
        cur.close()

    def github_remove(self):
        # in order to remove Milestone, need Milestone number (int)
        token = getConfig("github.token")
        owner = getConfig("github.owner")
        gh = Github(token=token, user=owner, repo='test-community')
        northbridge = gh.users.get('northbridge')
        response = gh.issues.milestones.list(owner, 'test-community')
        print response.all()
    
    def test(self):
        #Set up the environment for the test
        # i.e. create test milestone and related issues in database
        self.environ_setup()
        
        #invoke the export script
        #export.main()
        
        #check if all aspects of the script were successfully executed

        #Clean up the environment after the test
        # i.e. remove test milestone and related issues from database
        # then remove milestone and related issues from GitHub
        self.environ_cleanup()

        # self.github_remove()
        
if __name__ == '__main__':
    unittest.main()
