'''
Created on Jan 19, 2024

@author: demunckd
'''
from cgls_cpe.common import helper
from cgls_cpe.config.model.enums import AncillaryDataInputCategory,\
    AncillaryDataSourceName
from cgls_cpe.config.model.data_object import DataObject
from cgls_cpe.exceptions.exception import InvalidParameterError

'''
Created on Nov 19, 2023

@author: demunckd
'''
from cgls_cpe.config.model.data_object import CONTAINER_SEP

PREFIX = 'anc' 

class AncillaryData(DataObject):
    
    

    def __init__(self, category:AncillaryDataInputCategory, datasource_name:AncillaryDataSourceName, year=None, month=None, day=None, filename:str=''):
        self.category = category
        self.datasource_name = datasource_name
        self.year = year
        self.month = month
        self.day = day 
        self.filename = filename
        
        #will check valid bucket name
        self.get_container_suffix()
        
                 
    def get_container_suffix(self):
        if self.month is None and self.year is not None:
            return CONTAINER_SEP.join( [ PREFIX , self.category.value , self.datasource_name.value, str(self.year)] )
        
        if self.year is None:
            return CONTAINER_SEP.join( [PREFIX , self.category.value , self.datasource_name.value] )
        
        result = CONTAINER_SEP.join( [ PREFIX, self.category.value , self.datasource_name.value , str(self.year), helper.pad_two_digits(self.month)])
        from cgls_cpe.storage import remote_storage 
        if not remote_storage.is_valid_bucket_name(  'stag.tds-' + result):
            raise InvalidParameterError( 'Resulting container name invalid: ' + result + " with prefix context " + 'stag.tds-')
        return result
    
    def get_key_suffix(self):
        if self.day is None and self.month is not None: 
            return  str(self.year) + helper.pad_two_digits(self.month)  + '/' + self.filename
        
        if self.month is None and self.year is not None: 
            return  str(self.year)  + '/' + self.filename
        
        if self.year is None: 
            return  self.filename
        
        return str(self.year) + helper.pad_two_digits(self.month) + helper.pad_two_digits(self.day) + '/' + self.filename 
    
