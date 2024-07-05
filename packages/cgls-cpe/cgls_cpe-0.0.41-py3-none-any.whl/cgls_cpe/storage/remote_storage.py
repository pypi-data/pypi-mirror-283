'''
Created on Nov 5, 2023

@author: demunckd
'''
import re

from cgls_cpe.config.model.context import Context
from cgls_cpe.config.configuration import Configuration

from cgls_cpe.storage.implementation.s3_api import S3Api
from cgls_cpe.storage.implementation.s3_api import S3PREFIX
from cgls_cpe.storage.implementation.s3_api import get_s3_url
from cgls_cpe.common import helper
from cgls_cpe.config.model.data_object import DataObject

s3_api = None

from cgls_cpe.logging import log

logger = log.logger()


def get_key_from_url(url):
    if url.startswith(S3PREFIX):
        no_prefix = url[len(S3PREFIX):]
        key = no_prefix[(no_prefix.index('/')+1):]
        return key
        

def check_environment(context):
    if context.is_production() != Configuration().is_production():
        raise Exception("Mixing up environments")
    
    
def is_valid_bucket_name(bucket_name):
    """
    Validates if a string is a valid bucket name according to AWS S3 naming rules.
    """
    # Bucket name must be between 3 and 63 characters
    if len(bucket_name) < 3 or len(bucket_name) > 63:
        return False

    # Bucket name can only contain lowercase letters, numbers, hyphens, and periods
    if not re.match("^[a-z0-9.-]+$", bucket_name):
        return False

    # Bucket name cannot start or end with a hyphen or period
    if bucket_name.startswith("-") or bucket_name.startswith("."):
        return False
    if bucket_name.endswith("-") or bucket_name.endswith("."):
        return False

    # Bucket name cannot have consecutive periods or hyphens
    if ".." in bucket_name or "--" in bucket_name:
        return False

    return True

#### SAT_IMAGE DOWNLOAD/STORE

def get_full_URL(image:DataObject,context:Context=None):
    if context is None:
        context = Configuration().get_storage().get_default_context()
    
    container = Configuration().get_storage().get_remote_container_for_image(image,context)
    key = Configuration().get_storage().get_remote_key_for_image(image,context)    
    return get_s3_url(container,key)

def get_location(image:DataObject,context:Context=None):
    full_url = get_full_URL(image,context)
    return full_url.rsplit('/', 1)[0]


def store_remotely(local_file:str, image:DataObject,context:Context=None):
    if context is None:
        context = Configuration().get_storage().get_default_context()
    else:
        check_environment(context)
    
    container = Configuration().get_storage().get_remote_container_for_image(image,context)
    key = Configuration().get_storage().get_remote_key_for_image(image,context)
    
    __create_container_with_correct_permissions_if_requried(container) 
    __get_s3_api().upload_single_file(local_file, container, key)


def remove_remotely(image:DataObject,context:Context=None):
    if context is None:
        context = Configuration().get_storage().get_default_context()
    else:
        check_environment(context)
    
    container = Configuration().get_storage().get_remote_container_for_image(image,context)
    key = Configuration().get_storage().get_remote_key_for_image(image,context)    
    __get_s3_api().remove_object(container, key)
    

def download_remote(image:DataObject,dest_file,context:Context=None):
    if context is None:
        context = Configuration().get_storage().get_default_context()
    else:
        check_environment(context)
    
    container = Configuration().get_storage().get_remote_container_for_image(image,context)
    key = Configuration().get_storage().get_remote_key_for_image(image,context)    
    __get_s3_api().download_single_file(container, key, dest_file)


def list_remote(image:DataObject,context:Context=None):
    if context is None:
        context = Configuration().get_storage().get_default_context()
    else:
        check_environment(context)

    container = Configuration().get_storage().get_remote_container_for_image(image,context)
    key = Configuration().get_storage().get_remote_key_for_image(image,context)
    return __get_s3_api().list_by_prefix(container,key,return_s3_url_as_keys=False)[1]

def download_dir_as_path(remote_dir:str, local_dir:str, exclude_lst=[], overwrite=False):
    """Downloads a directory and all its subdirectories recursively from s3. Treats s3 keys as filesystem paths,
    for easy replication of directory structures to the local filesystem.

    :param str remote_dir: remote target directory
    :param str local_dir: local destination directory
    :param list exclude_lst: keys that want to be excluded from copying, defaults to []
    :param bool overwrite: overwrites existing files in local filesystem, defaults to False
    :return : None
    """
    container, key = __get_s3_api().get_bucket_from_url(remote_dir)
    return __get_s3_api().download_dir_from_s3(container, key, local_dir, exclude_lst, overwrite)

### GENERIC URL COMMANDS

#returns urls with given prefix
def list_objects(url):
    container, key = __get_s3_api().get_bucket_from_url(url)
    return __get_s3_api().list_by_prefix(container,key,return_s3_url_as_keys=True)[1]

#url_with_pattern is s3:// style
def list_objects_using_pattern( url_with_pattern ):
    container, key = __get_s3_api().get_bucket_from_url(url_with_pattern)
    prefix = key
    if  '*' in key:
        prefix = key.split('*')[0]   #remove possible leading slash
    return __get_s3_api().list_by_pattern(container, prefix, key)

def download_remote_to_local_folder(remotekeys, local_path, overwrite=True, options=''):
    options='--force'
    if not overwrite :
        options = '--skip-existing'
        
    return __get_s3_api().download_from_s3(remotekeys, local_path,options)

def upload_local_to_remote(local_files, s3_path, rename_during_transfer=True, options=''):
    return __get_s3_api().upload_to_s3(local_files, s3_path, rename_during_transfer, options) 


def upload_single_file_to_remote_path(local_path, remote_path):
    container, key = __get_s3_api().get_bucket_from_url(remote_path)
    __create_container_with_correct_permissions_if_requried(container)    
    __get_s3_api().upload_single_file(local_path, container,key)
    return 0

def download_single_file_to_local_path(remote_url, dest_file):
    bucket, key = __get_s3_api().get_bucket_from_url(remote_url)
    __get_s3_api().download_single_file(bucket, key, dest_file) 
    return 0

def get_contents_as_string(url):
    return __get_s3_api().get_contents_as_string(url)

def put_contents_as_string_to_url(url,input_str):
    return __get_s3_api().put_contents_as_string_to_url(url, input_str)

def copy_or_move_object(src_url, tgt_url, is_move=False):
    return __get_s3_api().copy_or_move_object(src_url, tgt_url, is_move)


def remove_object(url):
    bucket, key = __get_s3_api().get_bucket_from_url(url)
    __get_s3_api().remove_object(bucket, key)


def open_smart(url, mode='r'):
        return __get_s3_api().open_smart(url,mode)    

def export_credentials_to_env():
    __get_s3_api().export_credentials_to_env()

def mount_s3fs(bucket_name, mount_point):
    helper.mkdir_p(mount_point)
    
    cmd = 's3fs  ' + bucket_name + ' ' + mount_point + ' -o url=https://' + Configuration().get_storage().get_object_storage_endpoint() + ' -o use_path_request_style '
    logger.info("Going to execute mount cmd: " + cmd)
    helper.exec_with_env( cmd, __get_s3_api().get_env_for_object_storage())
    logger.info("Mounting finished")

def unmount_s3fs(mount_point):
    cmd = 'fusermount -u ' + mount_point
    logger.info("Going to execute umount cmd: " + cmd)
    helper.exec_with_env(cmd)
    logger.info("Unmounting finished")

#trigger

def get_process_status_container(context:Context=None):
    if context is None:
        context = Configuration().get_storage().get_default_context()
    else:
        check_environment(context)
    
    container =  '%s-processing-status' % context.get_value()
    __create_container_with_correct_permissions_if_requried(container)
    return container


# INTERNAL FUNCTIONS, should normally NOT be called by external

def reset_auth():
    global s3_api
    s3_api = None

def __get_s3_api():
    global s3_api
    if s3_api is None:
        store = Configuration().get_storage()
        s3_api = S3Api(store.get_object_storage_endpoint(), store.get_object_storage_acces_id(), store.get_object_storage_secret_acces_key())
    return s3_api


def __create_container_with_correct_permissions_if_requried(container):
    bucket_exists = __get_s3_api().check_if_bucket_exists(container)
    if not bucket_exists:
        __get_s3_api().create_bucket(container)
        custom_policy = Configuration().get_storage().get_s3_policy_for_container(container)
        __get_s3_api().set_policy_on_bucket(container, custom_policy) 
 

        