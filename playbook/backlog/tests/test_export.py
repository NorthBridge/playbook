from .. import export
import unittest
from ..dao.baseDAO import BaseDAO
from ..dao.milestoneDAO import MilestoneDAO
from ..model.milestone import Milestone
from ..model.issue import Issue
import psycopg2.extras

class ExportTest(unittest.TestCase):

    def environ_setup(self):
        #update database with test data

        backlog_stmt = """INSERT INTO backlog (
            id,
            story_title,
            story_descr,
            status_id_fk) VALUES (
            DEFAULT,
            'TEST',
            'This milestone was created by the test_export module',
            14);"""
        bDAO = BaseDAO()
        cur = bDAO.getConnection().cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(backlog_stmt,)
        bDAO.getConnection().commit()
        cur.close()

    def environ_cleanup(self):
        pass
    
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
        pass

if __name__ == '__main__':
    unittest.main()
