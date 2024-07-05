'''
Created on Nov 19, 2023

@author: demunckd
'''

class Area(object):
    '''
    classdocs
    '''
    @staticmethod
    def create_globe():
        return Area('GLOBE')
    
    @staticmethod
    def create_subtile(tile:str, subtile_indicator:str):
        return Area( tile + '-' + subtile_indicator)
     
    def __init__(self, value:str):
        '''
        Constructor
        '''
        self.value = value
        
        
    def __str__(self):
        return self.get_value()
    
    def get_value(self) -> str:
        return self.value
    
    def is_global(self):
        return self.get_value().lower().startswith('glob')
    
