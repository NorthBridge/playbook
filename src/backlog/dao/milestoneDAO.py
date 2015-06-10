from baseDAO import BaseDAO
from milestone import Milestone

class MilestoneDAO(BaseDAO):
    
    SELECTED_STATUS = 14
    IN_PROGRESS_STATUS = 15
    
    def __init__(self):
        super(MilestoneDAO, self).__init__()
    
    def getMilestones(self):
        stmt=('SELECT b.id, b.story_title, b.story_descr, e.end_dttm, b.github_repo'
              '  FROM event e, backlog b'
              ' WHERE b.sprint_id_fk = e.id'
              '   AND b.status_id_fk = %s;')
        cur = super(MilestoneDAO, self).execute(stmt, (MilestoneDAO.SELECTED_STATUS,))
        rows = cur.fetchall()
        cur.close()
        
        milestones = [Milestone(row['id'],
                                row['story_title'], 
                                'open', 
                                row['story_descr'], 
                                str(row['end_dttm']), 
                                row['github_repo']) 
                      for row in rows]
        
        return milestones
    
    def updateMilestoneNumber(self, milestone):
        stmt = ('UPDATE backlog SET github_number = %s, status_id_fk = %s where id = %s;')
        try:
            cur = super(MilestoneDAO, self).execute(stmt, (milestone.getNumber(), 
                                                           MilestoneDAO.IN_PROGRESS_STATUS, 
                                                           milestone.getId()))
            super(MilestoneDAO, self).getConnection().commit()
        except Exception:
            super(MilestoneDAO, self).getConnection().rollback()
        finally:
            cur.close()
    