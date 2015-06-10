import psycopg2.extras

class BaseDAO(object):
    """BaseDAO is a base class that encapsulates basic logic necessary to 
        connect and interact with DB"""
    
    def __init__(self):
        config_file = open('CONFIG', 'r')
        config_file.readline() #skip the GH auth token
        db = config_file.readline().rstrip()
        hst = config_file.readline().rstrip()
        usr = config_file.readline().rstrip()
        pswrd = config_file.readline().rstrip()
        config_file.close()
        self.__conn = psycopg2.connect(database=db,
                            host=hst, user=usr,
                            password=pswrd)
        
    def __del__(self):
        self.getConnection().close()
        
    def execute(self, stmt, params):
        cur = self.getConnection().cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(stmt, params)
        return cur
        
    def getConnection(self):
        return self.__conn