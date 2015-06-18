from baseDAO import BaseDAO
from ..model.issue import Issue
from ...utils.constants import STATIC_LABEL_VALUE

class IssueDAO(BaseDAO):
    
    def getIssuesByMilestone(self, milestone):
        #TODO: Verify if this is the right way to check
        assert milestone.getNumber() is not None
        stmt = """SELECT ac.id, ac.title, ac.descr, b.github_number,
                         b.github_repo, t.name
                    FROM acceptance_criteria ac, backlog b, team t
                   WHERE b.id = %s
                     AND b.github_number = %s
                     AND b.github_repo = %s
                     AND ac.backlog_id_fk = b.id
                     AND b.team_id_fk = t.id;"""
        mNumber = milestone.getNumber()
        cur = super(IssueDAO, self).execute(stmt, (milestone.getId(),
                                                   str(mNumber), 
                                                   milestone.getRepo()))
        rows = cur.fetchall()
        cur.close()
        
        issues = [Issue(id=row['id'], 
                        title=row['title'], 
                        body=row['descr'], 
                        milestoneNumber=row['github_number'], 
                        labels=[ STATIC_LABEL_VALUE, row['name'] ], 
                        repo=row['github_repo'])
                  for row in rows]
        
        return issues