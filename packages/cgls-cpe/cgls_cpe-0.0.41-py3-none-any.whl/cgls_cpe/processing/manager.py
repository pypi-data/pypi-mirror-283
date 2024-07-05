'''
Created on Mar 16, 2024

@author: demunckd
'''


import time

from cgls_cpe.storage import remote_storage
from cgls_cpe.config.model.enums import DB_status, ProductType
from cgls_cpe.storage.remote_storage import S3Api
from cgls_cpe.logging import log
from cgls_cpe.config.model import enums
from cgls_cpe.common import cloud_helper
from cgls_cpe.config.model.context import Context
from cgls_cpe.db_api import DatabaseConnection
from cgls_cpe.config.configuration import Configuration
from cgls_cpe.config import configuration 

import cgls_cpe.processing.updaters as updaters
from cgls_cpe.common.launcher_sandbox import load_sandbox_if_requested


logger = log.logger()

FOLDER_SUCCESS="success"
FOLDER_FAILURE="failure"

FOLDER_FAILURE_UPDATEDB="failure_db_update"

PREFIX_OK = 'ok_'
PREFIX_FAILURE= 'fail_'

RECORD_FIELD_SEP='|'

SPARK_UNITTEST_ID='spark-unittest-id'

#variabel part should contain location (or be equal to the location  
def set_success_status(product_type:ProductType, db_id:int, runtime:str, name:str, variabel_last_part, context:Context=None):
    exit_code = 0
    object_key = get_status_key(FOLDER_SUCCESS,PREFIX_OK, product_type, db_id, exit_code, runtime,name)
    container = remote_storage.get_process_status_container(context)                                    
    url = remote_storage.get_s3_url(container,object_key )
    contents = get_processing_result_line(db_id, exit_code, runtime, variabel_last_part)
    remote_storage.put_contents_as_string_to_url(url, contents)

def set_failure_status(product_type:ProductType, db_id:int, failure_exit_code:int, runtime:str, name:str, variabel_last_part='No upload location because of error', context:Context=None):
    object_key = get_status_key(FOLDER_FAILURE,PREFIX_FAILURE,product_type, db_id, failure_exit_code, runtime,name)
    container = remote_storage.get_process_status_container(context)                                    
    url = remote_storage.get_s3_url(container,object_key )
    contents = get_processing_result_line(db_id, failure_exit_code, runtime, variabel_last_part)
    remote_storage.put_contents_as_string_to_url(url, contents)

def get_status_key(folder, prefix,product_type:ProductType, db_id:int, exit_code:int, runtime:int, name:str):
        if name is None:
            name = '<unknown name>'
        object_key = folder + '/' + product_type.value + '/' + prefix+ '_'.join( [product_type.value, str(db_id), str(exit_code), str(runtime), cloud_helper.get_spark_application_id(), cloud_helper.get_pod_name(),  name ]) + '.txt'
        return object_key

def get_status_elements(key):
        real_parts = key[key.index('_'):] 
        result = real_parts.split('_')
        return result

def list_success_triggers(context:Context=None):
    #local file can be empty, than it will be created
    container = remote_storage.get_process_status_container(context)
    url = remote_storage.get_s3_url(container, FOLDER_SUCCESS + '/')
    return remote_storage.list_objects(url)

def list_failure_triggers(context:Context=None):
    #local file can be empty, than it will be created
    container = remote_storage.get_process_status_container(context)
    url = remote_storage.get_s3_url(container, FOLDER_FAILURE+ '/')
    return remote_storage.list_objects(url)
    

def get_failure_db_update_url(status_url):
    folder_part =  status_url.split('_')[0]
    if '/' + FOLDER_SUCCESS + '/' in folder_part:
        return status_url.replace( '/' + FOLDER_SUCCESS + '/' ,'/' + FOLDER_FAILURE_UPDATEDB  + '/')
    else:
        return status_url.replace( '/' + FOLDER_FAILURE +'/' , '/' + FOLDER_FAILURE_UPDATEDB  + '/')

def get_processing_result_line(product_db_id, status, runtime, variable_part, sparkApplicationId:str=None, podName:str=None):
    if sparkApplicationId is None:
        sparkApplicationId = cloud_helper.get_spark_application_id()
    if podName  is None:
        podName = cloud_helper.get_pod_name()
    if variable_part is None:
        variable_part = ''
        
    if isinstance(variable_part, list):
        contents = ''
        for part in variable_part:
            if len(contents) > 2:
                contents+= "\n"
            contents += RECORD_FIELD_SEP.join( [str(product_db_id), str(status), str(runtime), sparkApplicationId, podName,part])
        return contents     
    else:
        return RECORD_FIELD_SEP.join( [str(product_db_id), str(status), str(runtime), sparkApplicationId, podName,variable_part])
                                  
def process_status_objects():
    status_ok= list_success_triggers()
    status_failure = list_failure_triggers()
    db_settings = Configuration().get_database()
    DB = DatabaseConnection(db_settings.get_connection_string())
   
    list_of_ok_records_idepix = []
    triggers =  status_ok + status_failure
    for url in triggers:
        key = remote_storage.get_key_from_url(url)
        logger.info("Doing ok key: " + key)
        parts = key.split('_')
        if len(parts) < 5:
            print("Skipping since not enough parts: " + key)
            continue
        #first part is folder location
        product_type = parts[1]
        updater = updaters.get_cached_updater(product_type,DB)
        #inside filename but also inside key
        db_id = parts[2]
        run_time= parts[3]
        name = parts[4]
        sparkApplicationId = parts[5]
        env = Configuration().get_environment_name()
        if sparkApplicationId == SPARK_UNITTEST_ID:
            if configuration.ENV_UT != env:
                logger.info("Skipping unit test")
                continue 
            else:
                logger.info("Handling unit test")
        else:
            if configuration.ENV_UT == env:
                logger.info("Not handling non unit test")
                continue
        
        podNameId = parts[6]
            
        contents = remote_storage.get_contents_as_string(url)
        lines = contents.split('\n')
        
        for line in lines:
            if len(line) < 2:
                continue
            recordfields = line.split(RECORD_FIELD_SEP)
            try:
                updater.process_record(recordfields)
                list_of_ok_records_idepix.append( (url, recordfields))
                updater.DB.conn.commit()
                
            except Exception as exc:
                logger.exception("Setting to failure DB because of exception: " + str(exc) + " -> "  + get_failure_db_update_url(url))
                error_url = get_failure_db_update_url(url)
                remote_storage.copy_or_move_object(url,error_url ,is_move=True)
                logger.debug("Done")
                updater.DB.conn.rollback()
                break
            
        logger.info("Committed to DB, now removing status file if necessary: " + url)
        remote_storage.remove_object(url)
    DB.close()     
