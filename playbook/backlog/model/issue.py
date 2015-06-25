from pygithub3 import Github
from ...utils.configHelper import getConfig
import logging
from ...utils.constants import ACCEPT_ISSUE_LABEL, ACCEPT_ISSUE_TITLE

logger = logging.getLogger('playbook')

def build_issue_from_gh_payload(payload):
    try:
        title = payload['issue']['title']
        body = payload['issue']['body']
        assignee = payload['issue']['assignee']
        milestoneNumber = payload['issue']['milestone']['number']
        labels = payload['issue']['labels']
        state = payload['issue']['state']
        repo = payload['repository']['name']
        
        return Issue(title=title, 
                     body=body, 
                     assignee=assignee,
                     milestoneNumber=milestoneNumber,
                     labels=labels,
                     state=state,
                     repo=repo)
    except KeyError, error:
        logger.exception("Trying to get value from payload using invalid key:")
        raise
 
def createAcceptIssue(milestoneNumber, milestoneRepo):
        descr = ('The product owner should complete this task after all the '
                 'acceptance criteria are met for this story (milestone).')
        issue = Issue(title=ACCEPT_ISSUE_TITLE, 
                      body=descr, 
                      milestoneNumber=milestoneNumber, 
                      labels=[ ACCEPT_ISSUE_LABEL ], 
                      repo=milestoneRepo)
        logger.info("Creating Accept Issue related to milestone #%s" +
                    " into repository %s", 
                    milestoneNumber, milestoneRepo)
        return (issue, issue.create())
      
class Issue(object):
    
    def __init__(self, **kwargs):
        self.__id = kwargs.get('id', None)
        self.__title = kwargs.get('title', None)
        self.__body = kwargs.get('body', None)
        self.__assignee = kwargs.get('assignee', None)
        self.__milestoneNumber = kwargs.get('milestoneNumber', None)
        self.__labels = kwargs.get('labels', None)
        self.__state = kwargs.get('state', None)
        self.__repo = kwargs.get('repo', None)
        
        token = getConfig("github.token")
        owner = getConfig("github.owner")
        self.__gh = Github(token=token, user=owner, repo=self.getRepo())
        
    def create(self):
        data = self.create_data()            
        try:
            ghIssue = self.__gh.issues.create(data)
            logger.info("Issue exported to GitHub: %s", data)
            return ghIssue.number
        except Exception, error:
            logger.exception("Error exporting issue to GitHub: %s", data)
            raise
    
    def create_data(self):
        if self.__title is None:
            logger.error("Title is a required field. This issue will not" +
                         " be exported to GitHub: %s", self.__dict__)
            raise RuntimeError('\'Title\' is required to create an issue')
        
        data = { 'title': self.__title }
            
        if self.__body is not None:
            data['body'] = self.__body
            
        if self.__assignee is not None:
            data['assignee'] = self.__assignee
        
        if self.__state is not None:
            data['state'] = self.__state
            
        if self.__milestoneNumber is not None:
            data['milestone'] = self.__milestoneNumber
            
        if self.__labels is not None:
            data['labels'] = self.__labels
        
        return data
        
    def getId(self):
        return self.__id
                
    def getTitle(self):
        return self.__title
    
    def getBody(self):
        return self.__body
        
    def getAssignee(self):
        return self.__assignee
        
    def getmilestoneNumber(self):
        return self.__milestoneNumber
        
    def getLabels(self):
        return self.__labels
    
    def getState(self):
        return self.__state

    def getRepo(self):
        return self.__repo

    def getGitHub(self):
        return self.__gh
    
    def setGitHub(self, gitHub):
        self.__gh = gitHub
        
        