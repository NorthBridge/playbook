from ...utils.constants import SELECTED_STATUS
from ..dao.issueDAO import IssueDAO
from ..model.issue import Issue 

'''
    To perform the tests using gh organization:
        - change 'github.owner' attribute to the organization name
        - use 'in_org' argument when creating the repository
'''

class Fixtures(object):
    TEAM_ID = 10
    SCHEDULE_ID = 1
    EVENT_NAME = 'Sprint Test Export'
    GH_ORGANIZATION = 'Northbridge-Test-Import'
    REPO = 'Test-Repository-Northbridge'
    REPO_DESC = 'Temporary repository used by automated testing of Export module.'
    MILESTONE_START_DATE = '2015-07-11'
    MILESTONE_DUE_ON = '2016-07-04'
    MILESTONE_TITLE = 'Milestone Test Export Module'
    MILESTONE_DESC = 'This milestone was created by the test_export module'
    ACC_CRI_TITLE = 'Acceptance Criteria Test'
    ACC_CRI_DESC = 'Temporary acceptance criteria used by the test_export module'
    
def github_createRepo(github, **kwargs):
    data = { 
            'name': kwargs.get('repo'),
            'description': kwargs.get('repo_desc') 
    }
    github.repos.create(data, in_org=Fixtures.GH_ORGANIZATION)
        
def environ_setup(baseDao, **kwargs):        
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
    cur = baseDao.execute(event_create_row, (kwargs.get('event_name'),
                                             kwargs.get('schedule_id'),
                                             kwargs.get('milestone_start_date'),
                                             kwargs.get('milestone_due_on')))
    eventId = cur.fetchone()[0]
    #Insert into backlog table
    cur = baseDao.execute(backlog_create_row,(kwargs.get('milestone_title'),
                                              kwargs.get('milestone_desc'), 
                                              eventId,
                                              SELECTED_STATUS,
                                              kwargs.get('team_id'),
                                              kwargs.get('repo')))
    backlogId = cur.fetchone()[0]
    #Insert into acceptance_criteria table
    cur = baseDao.execute(acc_crit_create_row, (backlogId,
                                                kwargs.get('acc_cri_title'),
                                                kwargs.get('acc_cri_desc')))
    accCriteriaId = cur.fetchone()[0]
    #Commit the three inserts
    baseDao.getConnection().commit()
    
    return (backlogId, accCriteriaId, eventId)

def environ_cleanup(baseDao, **kwargs):        
    event_delete_row = """DELETE FROM event 
                                WHERE id = %s;"""
    accCriteria_delete_row = """DELETE FROM acceptance_criteria
                                      WHERE id = %s;"""
    backlog_delete_row = """DELETE FROM backlog 
                                  WHERE id = %s;"""
                                    
    cur = baseDao.execute(accCriteria_delete_row,(kwargs.get('acc_criteria_id'),))
    cur = baseDao.execute(backlog_delete_row,(kwargs.get('backlog_id'),))
    cur = baseDao.execute(event_delete_row,(kwargs.get('event_id'),))
    baseDao.getConnection().commit()

def github_remove(github):
    # In order to remove a repo, if OAuth is used, the delete_repo
    #  scope is required.
    github.repos.delete()