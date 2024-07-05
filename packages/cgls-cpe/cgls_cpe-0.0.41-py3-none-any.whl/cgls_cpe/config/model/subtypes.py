'''
Created on Nov 19, 2023

@author: demunckd
'''
from cgls_cpe.config.model.enums import Subtype
from typing import List
SubtypeList = List[Subtype]

class Subtypes(object):


    def __init__(self, subtypes:SubtypeList=None):
        if subtypes is not None:
            for subtype in subtypes:
                if not isinstance(subtype, Subtype):
                    raise TypeError("each element in subtypes must be a SubType object")
        self.subtypes = subtypes

    def __str__(self):
        return self.get_value()
    
    def get_value(self):
        if self.subtypes is None:
            return ''
        return '-'.join(  [ subtype.value for subtype in self.subtypes]) 
    