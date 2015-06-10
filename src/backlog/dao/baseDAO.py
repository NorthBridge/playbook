import psycopg2.extras
from configHelper import getConfig 

class BaseDAO(object):
    """BaseDAO is a base class that encapsulates basic logic necessary to 
        connect and interact with DB"""
    
    def __init__(self, database=None, host=None, user=None, password=None):
        
        if database or host or user or password is None:
            database = getConfig("database.name")
            host = getConfig("database.host")
            user = getConfig("database.user")
            password = getConfig("database.password")
            
        self.__conn = psycopg2.connect(database=database,
                            host=host, user=user,
                            password=password)
        
    def __del__(self):
        self.getConnection().close()
        
    def execute(self, stmt, params):
        cur = self.getConnection().cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(stmt, params)
        return cur
        
    def getConnection(self):
        return self.__conn
    
    def setConnection(self, connection):
        self.__conn = connection
        