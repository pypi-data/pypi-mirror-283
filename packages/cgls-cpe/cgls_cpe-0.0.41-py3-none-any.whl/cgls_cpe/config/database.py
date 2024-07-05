'''
Created on Oct 24, 2023

@author: demunckd
'''

CONTAINER_SEP = '-'



class Database:

    def __init__(self, config):
        self.config = config
        self.settings = self.config.get_settings()
        self.default_context = None
        
    def get_connection_string(self):

        db_name = self.settings.pg_database_name
        db_host = self.settings.pg_database_host
        db_user = self.settings.pg_database_user
        db_pwd = self.config.get_secrets().get_secret_key('pg_database_pwd')
        connection_string = "dbname='" + db_name + "' user='" + db_user + "' host='" + db_host + "' password='" + db_pwd + "'"
        return connection_string
    

    
