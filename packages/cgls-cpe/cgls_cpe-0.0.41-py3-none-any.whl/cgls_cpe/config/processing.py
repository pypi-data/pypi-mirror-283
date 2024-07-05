'''
Created on Oct 24, 2023

@author: demunckd
'''
class Processing:

    def __init__(self, setting):
        self.setting = setting.get_settings()
        
    def getMaxNbOfNodes(self):
        return  self.setting.max_nb_of_nodes
    
    def getInfoMailAddress(self):
        return  self.setting.info_mail
