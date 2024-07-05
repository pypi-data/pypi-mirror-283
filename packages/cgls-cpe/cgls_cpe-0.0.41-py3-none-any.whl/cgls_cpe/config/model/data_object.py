'''
Created on Jan 20, 2024

@author: demunckd
'''

CONTAINER_SEP = '-'


class DataObject(object):
    
    #returns what comes after the context: this defines the container structure                 
    def get_container_suffix(self):
        raise Exception("You need to implement this")
    
    #returns what comes after the container (so possibly extra folder and filename)
    def get_key_suffix(self):
        raise Exception("You need to implement this")
