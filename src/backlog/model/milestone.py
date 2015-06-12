from pygithub3 import Github
from ...utils.configHelper import getConfig
import logging

logger = logging.getLogger("playbook")

class Milestone(object):
    
    def __init__(self, id, title, state, desc, due_on, repo):
        #Importing here to avoid circular import issues 
        # (how to solve in a better way?).
        from ..dao.milestoneDAO import MilestoneDAO
        
        token = getConfig("github.token")
        owner = getConfig("github.owner")
        
        self.__gh = Github(token=token, user=owner, repo=repo)
        self.__milestoneDao = MilestoneDAO()
        self.__id = id
        self.__title = title
        self.__state = state
        self.__desc = desc
        self.__due_on = due_on
        self.__repo = repo
        self.__number = None
        
    def create(self):
        
        if self.__title is None:
            logger.error("Title is a required field. This milestone will not" +
                         " be exported to GitHub: %s", self.__dict__)
            #TODO: throw exception!?!?!?!
            return
        
        data = { 'title': self.__title }
            
        if self.__state is not None:
            data['state'] = self.__state
        
        if self.__desc is not None:
            data['description'] = self.__desc
            
        if self.__due_on is not None:
            data['due_on'] = self.__due_on
            
        try:
            ghMilestone = self.__gh.issues.milestones.create(data)
            logger.info("Milestone exported to GitHub: %s", data)
            self.__number = ghMilestone.number
            self.__milestoneDao.updateMilestoneNumber(self)
            logger.info("Backlog table [id=%d] updated with status = %d and" +
                        " github_number = %d", 
                         self.__id, self.__milestoneDao.IN_PROGRESS_STATUS, 
                         self.__number)
            return self.__number
        except Exception:
            logger.exception("Error exporting milestone to GitHub: %s", data)
            return None
    
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
        
    
    