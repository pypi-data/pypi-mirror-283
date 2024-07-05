'''
Created on Oct 27, 2023

@author: demunckd
'''

from abc import ABC, abstractmethod
from cgls_cpe.exceptions.exception import InvalidParameterError
from cgls_cpe.config.model import data_object

def get_prod_prefix():
    return 'prod'
    
# class syntax
class Context(ABC):
    @abstractmethod
    def get_value(self):
        pass

    def is_production(self):
        if self.get_value().startswith(get_prod_prefix()):
            return True
        return False

class Production(Context):
    def get_value(self):
        return  get_prod_prefix()     

class ProductionTesting(Context):
    def get_value(self):
        return get_prod_prefix() + '.testing'       
class UnitTesting(Context):
    def get_value(self):
        return 'ut'

class Staging(Context):
    def get_value(self):
        return 'stag'       

class StagingTDS(Context):
    def get_value(self):
        return 'stag.tds'       

class CustomContext(Context):
    def __init__(self, suffix):
        self.suffix = suffix.replace(data_object.CONTAINER_SEP,'.')
        from cgls_cpe.storage import remote_storage 
        if not remote_storage.is_valid_bucket_name( self.get_value()):
            raise InvalidParameterError("Using this suffix would result in invalid container name: " + suffix)
        
    def get_value(self):
        return 'stag.custom.' + self.suffix       
    