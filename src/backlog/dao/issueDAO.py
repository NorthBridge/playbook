from baseDAO import BaseDAO
from ..model.issue import Issue

class IssueDAO(BaseDAO):
    
    STATIC_LABEL_VALUE = 'acceptance criteria'
    
    def getIssuesByMilestone(self, milestone):
        #TODO: Verify if this is the right way to check
        assert milestone.getNumber() is not None
        stmt = ('SELECT ac.id, ac.title, ac.descr, b.github_number,'
                '       b.github_repo, t.name'
                '  FROM acceptance_criteria ac, backlog b, team t'
                ' WHERE b.github_number = %s'
                '   AND ac.backlog_id_fk = b.id'
                '   AND b.team_id_fk = t.id;')
        mNumber = milestone.getNumber()
        cur = super(IssueDAO, self).execute(stmt, (str(mNumber),))
        rows = cur.fetchall()
        cur.close()
        
        issues = [Issue(row['id'], 
                        row['title'], 
                        row['descr'], 
                        None, 
                        row['github_number'], 
                        [ IssueDAO.STATIC_LABEL_VALUE, row['name'] ], 
                        row['github_repo'])
                  for row in rows]
        
        return issues