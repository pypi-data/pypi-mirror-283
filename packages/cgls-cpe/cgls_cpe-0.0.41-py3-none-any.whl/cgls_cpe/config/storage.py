'''
Created on Oct 24, 2023

@author: demunckd
'''


import json



from cgls_cpe.config.model.context import Context, Production, Staging
from cgls_cpe.config.model.version import Version
from cgls_cpe.config.model.enums import Platform, ProductType,Periodicity
from cgls_cpe.exceptions.exception import InvalidParameterError
from cgls_cpe.config.model import context
from cgls_cpe.config.model.data_object import DataObject
from cgls_cpe.config.model.data_object import CONTAINER_SEP

class Storage:

    def __init__(self, config):
        self.config= config
        self.settings = self.config.get_settings()
        self.default_context = None
        
    
    def get_sandbox_mnt(self):
        return  self.settings.storage_sandbox_mnt
    
    def get_object_storage_endpoint(self):
        return  self.settings.storage_end_point
    
    def get_object_storage_acces_id(self):
        return self.config.get_secrets().get_secret_key('AWS_ACCESS_KEY_ID')
        
    def get_object_storage_secret_acces_key(self):
        return self.config.get_secrets().get_secret_key('AWS_SECRET_ACCESS_KEY')
    
    def get_eodata_storage_endpoint(self):
        return  self.settings.eo_data_storage_end_point
    
    def get_eodata_acces_id(self):
        return self.config.get_secrets().get_secret_key('EO_DATA_ACCESS_KEY_ID')
        
    def get_eodata_secret_acces_key(self):
        return self.config.get_secrets().get_secret_key('EO_DATA_SECRET_ACCESS_KEY')
    
    def get_remote_container_for_image(self, image:DataObject, context:Context):
        if not isinstance (context,Context):
            raise InvalidParameterError("Invalid context param, use Context class")
        if not isinstance (image,DataObject):
            raise InvalidParameterError("Invalid image, use DataObject type")
        
        return context.get_value() + CONTAINER_SEP + image.get_container_suffix()

    def get_remote_container_for_ok_trigger(self, context: Context):
        if not isinstance(context, Context):
            raise InvalidParameterError("Invalid context param, use Context class")

        return context.get_value() + '-ok-triggers'
            

    def get_remote_key_for_image(self, image:DataObject, context:Context):
        base_folder =  self.get_remote_container_for_image(image,context).replace(CONTAINER_SEP,'/')
        return base_folder + '/' + image.get_key_suffix()
    
    
    def get_remote_container(self, platform:Platform , producttype: ProductType, periodicity:Periodicity, version:Version, year:int, month:int):
        if not isinstance (platform,Platform):
            raise InvalidParameterError("Invalid sensor param, use Sensor enum")
        if not isinstance (producttype,ProductType):
            raise InvalidParameterError("Invalid producttype param, use ProductType enum")
        if not isinstance (periodicity,Periodicity):
            raise InvalidParameterError("Invalid periodicity: " + str(periodicity))
        if not isinstance (version,Version):
            raise InvalidParameterError("Invalid version: " + str(Version))
        if (year < 1800 or year > 2222):
            raise InvalidParameterError("Invalid year: " + str(year))
        if (month < 1 or month > 12):
            raise InvalidParameterError("Invalid month: " + str(month))
        
        #self.settings.project_abbrev = ""
        #-<context>-<sensor>-idata-<prod_type>-<periodicity>-<version>-<YYYY>-<MM>
        month_s = str(month).rjust(2, '0')
        parts = [ platform.value ,\
                producttype.value , str(periodicity.value) , version.get_value(),
                str(year),month_s]
        for part in parts:
            if CONTAINER_SEP in part:
                raise InvalidParameterError( CONTAINER_SEP + ' not allowed but was present in input: ' + part)
            if '_' in part:
                raise InvalidParameterError( ' _ not allowed but was present in input: ' + part)
            
        result = CONTAINER_SEP.join(parts).lower()
        from cgls_cpe.storage import remote_storage
        if not remote_storage.is_valid_bucket_name(  'stag.tds-' + result):
            raise InvalidParameterError( 'Resulting container name invalid: ' + result + " with prefix context " + 'stag.tds-')
        return result

    def get_default_context(self):
        if self.default_context is None:
            if self.config.is_production():
                self.default_context = Production()
            else:
                self.default_context  = Staging()
        return self.default_context
        
    def set_default_context(self, context:Context):
        self.default_context = context
        
    
    def get_s3_policy_for_container(self, container):
        #the default
        policy_json = self.settings.s3_perm_cglops_to_cglops_stag
        
        if container.startswith( context.get_prod_prefix()): 
            policy_json = self.settings.s3_perm_cglops_to_cglops_prod
        else:    
            if CONTAINER_SEP in container:
                relevant_container_part = container[(container.index(CONTAINER_SEP)+1):]
                if relevant_container_part.startswith( context.get_prod_prefix()):
                        policy_json = self.settings.s3_perm_cglops_to_cglops_prod    
        
        custom_policy = json.dumps(policy_json)
        return custom_policy
         