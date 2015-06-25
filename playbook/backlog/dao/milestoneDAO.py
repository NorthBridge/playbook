from baseDAO import BaseDAO
from ..model.milestone import Milestone, map_db_status_to_gh_state
from ...utils.constants import (IN_PROGRESS_STATUS, ACCEPTED_STATUS, 
                                SELECTED_STATUS, GH_ACTION)
import logging

logger = logging.getLogger('playbook')

class MilestoneDAO(BaseDAO):
    
    def __init__(self):
        super(MilestoneDAO, self).__init__()
        
    def find_by_id(self, id):
        stmt = """SELECT b.id, b.story_title, b.story_descr, e.end_dttm,
                         b.github_repo, b.github_number, b.status_id_fk
                    FROM backlog b, event e
                   WHERE b.id = %s
                     AND b.sprint_id_fk = e.id;"""
        cur = super(MilestoneDAO, self).execute(stmt, 
                                                (id,))
        row = cur.fetchone()
        cur.close()
        
        state=map_db_status_to_gh_state(row['status_id_fk'])
        
        milestone = Milestone(id=row['id'],
                              title=row['story_title'],
                              state=state, 
                              desc=row['story_descr'], 
                              due_on=str(row['end_dttm']), 
                              repo=row['github_repo'],
                              number=row['github_number'])
        return milestone 

    def getMilestones(self):
        stmt="""SELECT b.id, b.story_title, b.story_descr, e.end_dttm,
                       b.github_repo
                  FROM event e, backlog b
                 WHERE b.sprint_id_fk = e.id
                   AND b.status_id_fk = %s;"""
        cur = super(MilestoneDAO, self).execute(stmt, 
                                                (SELECTED_STATUS,))
        rows = cur.fetchall()
        cur.close()
        
        milestones = [Milestone(id=row['id'],
                                title=row['story_title'], 
                                state='open', 
                                desc=row['story_descr'], 
                                due_on=str(row['end_dttm']), 
                                repo=row['github_repo']) 
                      for row in rows]
        
        return milestones
    
    def updateMilestoneNumber(self, milestone):
        stmt = ('UPDATE backlog SET github_number = %s, status_id_fk = %s'
                ' WHERE id = %s;')
        cur = None
        try:
            cur = super(MilestoneDAO, self).execute(stmt, (milestone.getNumber(), 
                                                           IN_PROGRESS_STATUS, 
                                                           milestone.getId()))
            super(MilestoneDAO, self).getConnection().commit()
        except:
            super(MilestoneDAO, self).getConnection().rollback()
            raise
        finally:
            if cur is not None:
                cur.close()
            
    def updateMilestoneStatus(self, milestone, new_status):
        stmt = """UPDATE backlog SET status_id_fk = %s
                   WHERE github_repo = %s
                     AND github_number = %s;"""
        cur = None
        try:
            cur = super(MilestoneDAO, self).execute(stmt, (new_status,
                                                           milestone.getRepo(), 
                                                           milestone.getNumber()))
            super(MilestoneDAO, self).getConnection().commit()
        except:
            super(MilestoneDAO, self).getConnection().rollback()
            raise
        finally:
            if cur is not None:
                cur.close()
    