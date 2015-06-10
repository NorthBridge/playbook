from pygithub3 import Github
from pygithub3.exceptions import UnprocessableEntity
from configHelper import getConfig

def createAcceptIssue(milestoneNumber, milestoneRepo):
        title = 'Accept the story (milestone)'
        descr = ('The product owner should complete this task after all the '
                 'acceptance criteria are met for this story (milestone).')
        issue = Issue(None, 
                      title, 
                      descr, 
                      None, 
                      milestoneNumber, 
                      None, 
                      milestoneRepo)
        return (issue, issue.create())
        
class Issue(object):
    
    def __init__(self, id, title, body, assignee, milestoneNumber, labels, repo):
        
        token = getConfig("github.token")
        owner = getConfig("github.owner")
        
        self.__gh = Github(token=token, user=owner, repo=repo)
        self.__id = id
        self.__title = title
        self.__body = body
        self.__assignee = assignee
        self.__milestoneNumber = milestoneNumber
        self.__labels = labels
        self.__repo = repo
        
    def create(self):
        if self.__title is None:
            #TODO: Log issue and return/throw exception
            return
        
        data = { 'title': self.__title }
            
        if self.__body is not None:
            data['body'] = self.__body
            
        if self.__assignee is not None:
            data['assignee'] = self.__assignee
            
        if self.__milestoneNumber is not None:
            data['milestone'] = self.__milestoneNumber
            
        if self.__labels is not None:
            data['labels'] = self.__labels
            
        try:
            ghIssue = self.__gh.issues.create(data)
            #TODO: Log info of created issue
            return ghIssue.number
        except UnprocessableEntity as mExistsError:
            #TODO: log error and handle exception
            # (maybe handle a more generic exception?)
            print mExistsError
            return None

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

    def getGitHub(self):
        return self.__gh
    
    def setGitHub(self, gitHub):
        self.__gh = gitHub
        
        