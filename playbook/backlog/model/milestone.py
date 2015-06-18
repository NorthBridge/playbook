from pygithub3 import Github
from ...utils.configHelper import getConfig
from .issue import ACCEPT_ISSUE_LABEL
from ...utils.constants import IN_PROGRESS_STATUS, ACCEPTED_STATUS, ACTION
import logging

logger = logging.getLogger("playbook")

def build_milestone_from_gh_payload(payload):
    try:
        title = payload['issue']['milestone']['title']
        state = payload['issue']['milestone']['state']
        desc = payload['issue']['milestone']['description']
        due_on = payload['issue']['milestone']['due_on']
        repo = payload['repository']['name']
        number = payload['issue']['milestone']['number']
        
        return Milestone(title=title,
                         state=state, 
                         desc=desc, 
                         due_on=due_on, 
                         number=number, 
                         repo=repo)
    except KeyError, error:
        logger.exception("Trying to get value from payload using invalid key:")
        raise
    
class Milestone(object):
    
    def __init__(self, **kwargs):
        self.__id = kwargs.get('id', None)
        self.__title = kwargs.get('title', None)
        self.__state = kwargs.get('state', None)
        self.__desc = kwargs.get('desc', None)
        self.__due_on = kwargs.get('due_on', None)
        self.__repo = kwargs.get('repo', None)
        self.__number = str(kwargs.get('number', None))
        
        #Importing here to avoid circular import issues 
        # (how to solve in a better way?).
        from ..dao.milestoneDAO import MilestoneDAO
        token = getConfig("github.token")
        owner = getConfig("github.owner")
        self.__gh = Github(token=token, user=owner, repo=self.getRepo())
        self.__milestoneDao = MilestoneDAO()
        
    def create(self):
        data = self.create_data()
        try:
            ghMilestone = self.getGitHub().issues.milestones.create(data)
            logger.info("Milestone exported to GitHub: %s", data)
            self.setNumber(str(ghMilestone.number))
            self.getMilestoneDao().updateMilestoneNumber(self)
            logger.info("Backlog table [id=%d] updated with status = %d and" +
                        " github_number = %s", 
                        self.getId(), 
                        IN_PROGRESS_STATUS, 
                        self.getNumber())
            return self.getNumber()
        except Exception, error:
            logger.exception("Error exporting milestone to GitHub:" +
                             "\n\tRepo: %s" +
                             "\n\tData: %s", 
                             self.getRepo(),
                             data)
            raise
    
    def updateStatus(self, issue, action):
        message = None
        is_acceptance_issue = any(label['name'] == ACCEPT_ISSUE_LABEL 
                                  for label in issue.getLabels())
        
        if not is_acceptance_issue:
            message = ("Trying to update a milestone using an issue that"
                       " does not contain the expected label (%s) or is not"
                       " in the correct state. Ignoring...") % ACCEPT_ISSUE_LABEL
            logger.debug(message)
            return message

        new_milestone_state = None
        new_milestone_status = None
        
        try:
            new_milestone_state = ACTION[action]['state']
            new_milestone_status = ACTION[action]['status']
            self.__state = new_milestone_state
            data = self.create_data()
            #Persist this milestone state into database
            self.getMilestoneDao().updateMilestoneStatus(self, 
                                                         new_milestone_status)
            #Update this milestone state in github
            self.getGitHub().issues.milestones.update(self.getNumber(), data)
            message = ("Milestone #%s from \'%s\' repo updated to" 
                       " status \'%s\' using issue \'%s\'") % (self.getNumber(), 
                                                               self.getRepo(), 
                                                               new_milestone_state,
                                                               issue.getTitle())
            logger.info(message)
            return message
        except KeyError, error:
            logger.error("Invalid action passed as argument: \'%s\'." +
                             " This request is being ignored...",
                             action)
            raise
        except Exception, error:
            logger.exception("Error updating milestone #%s from \'%s\'" +
                             " repo using issue \'%s\'",
                             self.getNumber(), 
                             self.getRepo(), 
                             issue.getTitle())
            raise
            
    def create_data(self):
        if self.__title is None:
            logger.error("Title is a required field. This milestone will not" +
                         " be exported to GitHub: %s", self.__dict__)
            raise RuntimeError('\'Title\' is required to create an issue')

        data = { 'title': self.getTitle() }
            
        if self.getState() is not None:
            data['state'] = self.getState()
        
        if self.getDesc() is not None:
            data['description'] = self.getDesc()
            
        if self.getDueOn() is not None:
            data['due_on'] = self.getDueOn()        
        
        return data
    
    def getId(self):
        return self.__id
    
    def getTitle(self):
        return self.__title
    
    def getState(self):
        return self.__state
    
    def getDesc(self):
        return self.__desc
    
    def getDueOn(self):
        return self.__due_on
    
    def getRepo(self):
        return self.__repo
        
    def getNumber(self):
        return self.__number
        
    def setNumber(self, number):
        self.__number = number
        
    def getGitHub(self):
        return self.__gh
    
    def setGitHub(self, gitHub):
        self.__gh = gitHub
        
    def getMilestoneDao(self):
        return self.__milestoneDao
    
    def setMilestoneDao(self, dao):
        self.__milestoneDao = dao
        
    
    