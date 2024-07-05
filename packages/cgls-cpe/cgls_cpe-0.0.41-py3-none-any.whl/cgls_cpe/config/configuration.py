'''
Created on Oct 20, 2023

@author: demunckd
'''
from dynaconf import Dynaconf,Validator
import os
import json
import shutil
from pathlib import Path
from cgls_cpe.logging import log

from cgls_cpe.config.processing import Processing
from cgls_cpe.config.storage import Storage
from cgls_cpe.config.input import Input
from cgls_cpe.config.database import Database

from cgls_cpe.exceptions.exception import InvalidParameterError
from cgls_cpe.config.secrets import Secrets
from cgls_cpe.storage.implementation import s3_api


"""
    This singleton class (only one occurence) loads all the settings files and exposes them via fuctions
    It uses the Dynaconf package to make properties overridable via environment variables and include vault storage.
     
    Prefix for environment variables is CGLS_CPE
    
    Currently a basic  settingsfile is loaded (setttings/settings-toml) + a deploy specific setting file.
    
    The environment variable CGLS_CPE_SETTINGS_DEPLOY can set the path to the deploy specifc setting.
    
    If it is not set, the  settings/deploy-specific/settings-staging.toml is used
    
    If you introduce a header (table) in your TOML, best practice is to introduce a new class for it
    
    
    Inspiration from:
    https://dxiaochuan.medium.com/summary-of-python-config-626f2d5f6041
    https://tech.preferred.jp/en/blog/working-with-configuration-in-python/
    
    
    
    SEE ALSO UNIT TEST test_config.py 
    
       
"""

ENV_PROD = 'prod'
ENV_STAGING = 'stag'
ENV_UT = 'ut'

class Configuration(object):
    """Main Configuration object - this is a singleton

    You can access the instance by calling the Configuration() constructor without an argument
    If you provide the extra_setting_files in the constructor, the Configuration will be initialized
    
    You can reload the settings anytime by calling loadSettings - this will load all settings files and reread  the environment variables    
    
    Parameters
    ----------
    extra_setting_files : path or list of paths to other settingsfiles that need to be loaded


    #Singleton pattern
    #https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/
    
    """
    
    def __new__(cls,extra_setting_files=None):
        if not hasattr(cls, 'instance') or extra_setting_files is not None:
          cls.instance = super(Configuration, cls).__new__(cls)
        return cls.instance

    def __init__(self, extra_setting_files=None):
        if not hasattr(self,'settings'):
            self.loadSettings(extra_setting_files)
                
    def loadSettings(self,extra_setting_files=None):
        
        extra_setting_files_to_use = []
        extra_setting_files_on_remote_storage= []
        mapping_remote_local = {}
        
        if extra_setting_files is not None:
            if not isinstance(extra_setting_files, list):
                extra_setting_files = [ extra_setting_files ]
            for extra_file  in extra_setting_files:
                if ( s3_api.is_s3(extra_file)):
                    extra_setting_files_on_remote_storage.append(extra_file)
                
        if len(extra_setting_files_on_remote_storage) > 0:
            #to init authentication
            self.loadSettingsBase();
            from cgls_cpe.storage import local_storage, remote_storage
            destination_root = local_storage.get_scratch_root() + "/s3-config_cache/"
            index=0 #to make folder unique
            for s3_url in extra_setting_files_on_remote_storage:
                destination = destination_root + str(index) + "/" + s3_url.split('/')[-1]
                remote_storage.download_single_file_to_local_path(s3_url, destination)
                mapping_remote_local[s3_url] = destination
                index +=1 
            
            for extra_file  in extra_setting_files:
                try:
                    extra_setting_files_to_use.append(mapping_remote_local[extra_file])
                except:
                    extra_setting_files_to_use.append(extra_file)
            self.loadSettingsBase(extra_setting_files_to_use)
            shutil.rmtree(destination_root)        
        else:
            self.loadSettingsBase(extra_setting_files)
                    
    
    def loadSettingsBase(self,extra_setting_files=None):
        log.logger().info("LOADING CONFIGURATION... - version 3 with cfg inside package")
        
        #this is current implemenation with settings in same repository, this can be moved later
        cfg_root_path =  Path(__file__).parent.parent.resolve().joinpath('cfg')
        base_settings = cfg_root_path.joinpath('settings.toml').absolute()
        log_settings = cfg_root_path.joinpath('logging-conf.json').absolute()
        s3_settings = cfg_root_path.joinpath('s3-permissions.json').absolute()

        #a config file is force
        if 'CGLS_CPE_SETTINGS_DEPLOY' in os.environ:
            deploy_settings = os.environ['CGLS_CPE_SETTINGS_DEPLOY']
        else:
            if 'CGLS_CPE_ENV' in os.environ:
                env_via_env_var= os.environ['CGLS_CPE_ENV']
                if env_via_env_var == ENV_PROD:
                    log.logger().info("We are running in production")
                    deploy_settings = cfg_root_path.joinpath('deploy-specific/settings-prod.toml').absolute()
                elif env_via_env_var == ENV_STAGING:
                    deploy_settings = cfg_root_path.joinpath('deploy-specific/settings-staging.toml').absolute()
                else:
                    deploy_settings = cfg_root_path.joinpath('deploy-specific/settings-ut.toml').absolute()
            else:
                if self.is_production():
                    log.logger().info("We are running in production")
                    deploy_settings = cfg_root_path.joinpath('deploy-specific/settings-prod.toml').absolute()
                else:
                    deploy_settings = cfg_root_path.joinpath('deploy-specific/settings-ut.toml').absolute()
                
        
        if not os.path.isfile(base_settings):
            raise Exception('Could not find settings file: %s' ,  base_settings)
        log.logger().info('Loading base settings: %s', base_settings)
        
        if not os.path.isfile(log_settings):
            raise Exception('Could not find log settings file: %s' ,  log_settings)
        log.logger().info('Loading logging settings: %s', log_settings)
        
        
        if not os.path.isfile(s3_settings):
            raise Exception('Could not find s3 permissions settings file: %s' ,  s3_settings)
        log.logger().info('Loading s3 permission settings: %s', s3_settings)
        

        
        if not os.path.isfile(deploy_settings):
            raise Exception('Could not find settings file:' +  deploy_settings)
        log.logger().info('Loading deploy settings: %s', deploy_settings)
        
        list_settings_files = [base_settings, log_settings, s3_settings, deploy_settings]
        
        if extra_setting_files is not None:
            if not isinstance(extra_setting_files, list):
                extra_setting_files = [ extra_setting_files ]
            list_settings_files.extend(extra_setting_files)
            log.logger().info("Adding extra_setting_files : " + str(extra_setting_files))
        
        
        #final check
        for file in list_settings_files:
            if not os.path.isfile(file):
                raise InvalidParameterError("This path did not resolve to a  file: " + str(file))
        
        #we down't use  environments=True because we want to keep top level table structure
        #we don't use merge_enabled=True because this will merge all lists and dicts where most often we just want t! 
        self.settings = Dynaconf(
            envvar_prefix='CGLS_CPE',
            settings_files= list_settings_files
            )
        
        self.settings.validators.register(
                    Validator("info_mail", cont="@"),
                    Validator("storage_end_point", cont=".")
                )
        
        log.logger().info("VALIDATING...")
        self.settings.validators.validate()
        
        log.logger().info("NOW READING ANY CUSTOM LOGGING CONF...")
        log.load_config(self.settings.logging_config)
        
        
        self.processing = Processing(self)
        self.storage = Storage(self)
        self.input = Input(self)
        self.secrets = Secrets(self)
        self.database = Database(self)
        
        
        from cgls_cpe.storage import remote_storage
        remote_storage.reset_auth() 
        
        log.logger().info("DONE LOADING CONFIGURATION.")

    def get_datadump(self):
        data = self.get_settings().as_dict()
        dict_copy = data.copy()
        for key in dict_copy:
            try:
                if 'TOKEN' in key or 'SECR' in key or 'PWD' in key:
                    data.pop(key)
            except:
                pass
        return json.dumps(data)
    
    def dump_data_to_log(self):
        log.logger().info("Dumping config")
        log.logger().info(self.get_datadump())
        log.logger().info("done dumping config")
    
    
    def get_settings(self):
        return self.settings
    
    def force_env_production(self):
        os.environ['CGLS_CPE_ENV'] = ENV_PROD
        self.get_settings().env = ENV_PROD
        
    def force_env_staging(self):
        os.environ['CGLS_CPE_ENV'] = ENV_STAGING
        self.get_settings().env = ENV_STAGING        
        
    # general settings
    def is_production(self):
        
        try:
            if self.get_settings() is None:
                return False
            return self.get_settings().env == ENV_PROD
        except:
            return False
    
    def get_proj_abbrev(self):
        return self.get_settings().project_abbrev
    
    def get_dissemenation_prefix(self):
        return self.get_settings().dissemination_prefix
    
    def get_environment_name(self):
        return self.get_settings().env
    
    # supporting classes
    def get_processing(self) -> Processing:
        return self.processing
    
    def get_storage(self) -> Storage:
        return self.storage
    
    def get_input(self) -> Input:
        return self.input

    def get_database(self) -> Database:
        return self.database
    
    def get_secrets(self) -> Secrets:
        return self.secrets
    