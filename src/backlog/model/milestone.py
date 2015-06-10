from pygithub3 import Github
from pygithub3.exceptions import UnprocessableEntity 

class Milestone(object):
    
    MILESTONE_URL = 'https://api.github.com/repos/%s/%s/milestones'
    OWNER = 'Northbridge'
    
    def __init__(self, id, title, state, desc, due_on, repo):
        config_file = open('CONFIG', 'r')
        # rstrip removes the \n from the token
        token = config_file.readline().rstrip()
        config_file.close()
        self.__gh = Github(token=token, user=Milestone.OWNER, repo=repo)
        self.__id = id
        self.__title = title
        self.__state = state
        self.__desc = desc
        self.__due_on = due_on
        self.__repo = repo
        self.__number = None
        
    #TODO: verify repo and data before submit
    def create(self, owner=OWNER):
        data = {
            'title': self.__title,
            'state': self.__state,
            'description': self.__desc,
            'due_on': self.__due_on
        }
        try:
            ghMilestone = self.__gh.issues.milestones.create(data)
            self.__number = ghMilestone.number
            from milestoneDAO import MilestoneDAO
            mDao = MilestoneDAO()
            mDao.updateMilestoneNumber(self)
            return self.__number
        except UnprocessableEntity as mExistsError:
            #TODO: log error
            print mExistsError
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
    
    