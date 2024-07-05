# -*- coding: utf-8 -*-


#TODO: can s3cmd not be replaced by boto3 entirely? YEs but with s3cmd, it is much easier to catch the possible errors!
import fnmatch  # for linux regex patterns
import os
from pickle import FALSE, NONE

import boto3
from botocore.exceptions import ClientError
from smart_open import open as s_open  # this will make openening a file local/s3 transparant

from cgls_cpe.common import helper
from cgls_cpe.logging import log
from cgls_cpe.exceptions.exception import InvalidParameterError


logger = log.logger()


S3PREFIX='s3://'


S3CMD_LOGIN='--host=${AWS_S3_ENDPOINT} --host-bucket=https://${AWS_S3_ENDPOINT} --secret_key=${AWS_SECRET_ACCESS_KEY} --access_key=${AWS_ACCESS_KEY_ID}'



class S3Api:

    def __init__(self, endpoint:str, access_key_id:str, secret_acces_key:str ):
        self.endpoint = endpoint
        self.access_key_id = access_key_id
        self.secret_acces_key = secret_acces_key
        self.reset_auth()
        

    def reset_auth(self):
        if hasattr(self,'s3client'):
            self.get_boto3_s3_client().close()
        if hasattr(self,'s3clientOO'):            
            self.get_boto3_s3_client_OO().close()
        self.s3client = None
        self.s3clientOO = None
        
    
    def get_env_for_object_storage(self):
        env_copy  = os.environ.copy()
        env_copy['AWS_S3_ENDPOINT']=  self.endpoint 
        env_copy['AWS_ACCESS_KEY_ID']= self.access_key_id
        env_copy['AWS_SECRET_ACCESS_KEY']= self.secret_acces_key
        return env_copy
    
    
    def export_credentials_to_env(self):
        os.environ['AWS_S3_ENDPOINT']=  self.endpoint 
        os.environ['AWS_ACCESS_KEY_ID']= self.access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY']= self.secret_acces_key
    
    
    def open_smart(self,url, mode='r'):
        if url.startswith(S3PREFIX):
            s3client = self.get_boto3_s3_client()
            params = {'client': s3client}
        else:
            params= {}
    
        return s_open(url,mode=mode, transport_params=params)
    
    
    def get_bucket_from_url(self, url):
        if url[0:7].lower() == '/vsis3/':   #remove /vsis3/
            url = url[7:]
        elif url[0:5].lower() == S3PREFIX:
            url = url[5:]   #remove s3://
        else:
            # no match, not s3 location
            return None, None
    
        bucket = url.split('/')[0]  #bucket is the first part of the string
        object_key = url.replace(bucket + '/' ,'')  #remove bucket and the slash right after it
        return bucket, object_key
    
    def download_from_s3(self,keys, local_path, options=''):
        #get all keys to local storage (before we start processing)
        # a key can be :
        #  - a complete directory
        #  - a single file
        # eg :s3://BUCKET[/PREFIX]
        #sync can not be used here as it doesn't complain if the file not exists
        final_status = 0
        file_paths=[]
        failed_files=[]
        done_files = []
        
    
        if not isinstance(keys, list):  #create a list of the string
            keys = [keys]
    
        #download files one by one
        for key in keys:
            fname = os.path.basename(key)
            full_local_path = os.path.join(local_path.rstrip('/'), fname)
            cmd = 's3cmd %s %s get %s %s' % (S3CMD_LOGIN, options, key, full_local_path)#s3://BUCKET[/PREFIX] local_path
            stdout, stderr, err_nr = helper.run_command(cmd, env=self.get_env_for_object_storage(), end_on_failure=False)
            if err_nr:
                logger.error(cmd)
                logger.error(stderr),
                logger.error(stdout)
                failed_files.append(key)
                final_status = 1
            else:
                done_files.append(key)
    
                new_file = os.path.join(local_path, fname)
                file_paths.append(new_file)
        if final_status > 0:
            logger.info("Files that have been downloaded successfully : %s" % done_files)
            logger.error("Files that have been failed %s" % failed_files)
        else:
            logger.info("Done downloading %s files from s3 : %s" %(len(done_files), os.path.basename(done_files[0])))
        return final_status, file_paths
    
    def upload_to_s3(self, local_files, s3_path, rename_during_transfer=True, options=''):
        s3_path= s3_path.rstrip('/') + '/' #ensure one / at the end
        final_status = 0
        done_files = []
        failed_files = []
        for file in local_files:
            #TODO rename during transfer
            cmd = 's3cmd %s %s put "%s" %s' % (S3CMD_LOGIN, options, file, s3_path)    #s3://BUCKET[/PREFIX] local_path
            stdout, stderr, err_nr = helper.run_command(cmd, env=self.get_env_for_object_storage(), end_on_failure=False)
            if err_nr:
                logger.error(cmd)
                logger.error(stderr)
                logger.error(stdout)
                final_status=1
                failed_files.append(file)
            else:
                done_files.append(file)
        if final_status > 0:
            logger.info("Files that have been uploaded successfully : %s" % done_files)
            logger.error("Files that have been failed %s" % failed_files)
        else:
            logger.info("Done uploading files to s3")
    
        return final_status
    
    def get_boto3_s3_client_OO(self):
        if ( self.s3clientOO is None):
            self.s3clientOO = boto3.resource('s3', aws_access_key_id=self.access_key_id ,
                            aws_secret_access_key=self.secret_acces_key,
                            endpoint_url='https://' + self.endpoint )
            
        return self.s3clientOO
    
    def get_boto3_s3_client(self):
        if ( self.s3client is None):
            self.s3client = boto3.client('s3',aws_access_key_id=self.access_key_id ,
                            aws_secret_access_key=self.secret_acces_key,
                            endpoint_url='https://' + self.endpoint )
            
        return self.s3client
    
    def check_if_bucket_exists(self,bucket_name):
        if bucket_name.startswith(S3PREFIX):
            bucket_name = bucket_name[5:]
        s3 = self.get_boto3_s3_client()
        # this is the best way - looping over your buckets is too consuming AND skips the buckets in other Openstack prjoects, even if you have permission!
        # https://stackoverflow.com/questions/26871884/how-can-i-easily-determine-if-a-boto-3-s3-bucket-resource-exists
        try:
            _ = s3.head_bucket(Bucket=bucket_name)
            return True
        except ClientError as exc:
            if '404' in str(exc):
                return False
            raise exc
    
    def to_url(self,bucket_name, key):
        return S3PREFIX +'%s/%s' % (bucket_name,key)
    
    
    def list_by_pattern(self,bucket, prefix, filepattern):
        _, all_keys = self.list_by_prefix(bucket, prefix)
        filtered_keys = []
    
        #loop over the list of files and keep the ones we only need
        for key in all_keys:
            if fnmatch.fnmatch(key, filepattern):   #when using fnmatch(not glob) we could use linux regex pattern
                logger.debug(key)
                filtered_keys.append(self.to_url(bucket,key))
    
        logger.debug("Listing by pattern(%s) on %s/%s has found %s objects" % (filepattern, bucket, prefix, len(filtered_keys)))
        return filtered_keys
    
    
    def list_by_prefix(self,bucket_name, prefix, return_s3_url_as_keys=False):
        try:
            s3 = self.get_boto3_s3_client_OO()
            bucket = s3.Bucket(bucket_name)
        
            count = 0
            keys = []
            logger.debug("Going to list on %s/%s" % (bucket, prefix))
            for bucket_object in bucket.objects.filter(Prefix=prefix):
                count += 1
                if return_s3_url_as_keys:
                    keys.append( self.to_url(bucket_name, bucket_object.key))
                else:
                    keys.append(bucket_object.key)
            logger.debug("Listing on %s/%s has found %s objects" % (bucket, prefix, count))
            return count, keys
        
        except Exception as exc:
                if 'NoSuchBucket' in str(exc):
                    logger.debug("Bucket did not exist %s so no objects" % (bucket))
                    return 0,[]
                else:
                    raise
                    
    
    def upload_single_file(self,file, bucket_name, key):
        logger.debug("Uploading file %s to bucket %s with key %s  " , file, bucket_name, key)
        s3 = self.get_boto3_s3_client()
        s3.upload_file(file, bucket_name,key)
    
    def download_single_file(self,bucket_name, key, dest_file):
        logger.debug("Downloading from bucket %s  key %s to file: %s" % (bucket_name, key, dest_file))
        s3 = self.get_boto3_s3_client()
        local_dir = os.path.dirname(dest_file)
        if (not os.path.exists(local_dir)) and (local_dir != ''):
                os.makedirs(local_dir)
        s3.download_file(bucket_name, key, dest_file)
        
    def get_contents_as_string(self,url):
        bucket,key =self.get_bucket_from_url(url)
        s3 = self.get_boto3_s3_client_OO()
        logger.debug('reading %s',  url)
        contents_bytes = s3.Object(bucket,key).get()['Body'].read()
        contents_string= contents_bytes.decode('utf-8')
        pos = min(10, len(contents_string))
        logger.debug('read  "%s"...',  contents_string[0:pos])
        return contents_string
    
    def put_contents_as_string_to_url(self,url, input_str):
        bucket,key =self.get_bucket_from_url(url)
        s3 = self.get_boto3_s3_client_OO()
        input_bytes = input_str.encode('utf-8')
        pos = min(10, len(input_str))
        logger.debug('writing "%s..." to %s', input_str[0:pos],  url)
        s3.Object(bucket,key).put(Body=input_bytes)
        
    
    def copy_or_move_object(self, src_url, tgt_url, is_move=False):
        s3_client = self.get_boto3_s3_client()
        src_bucket,src_key =self.get_bucket_from_url(src_url)
        tgt_bucket,tgt_key =self.get_bucket_from_url(tgt_url)
        # Copy the object to the new location
        s3_client.copy_object(Bucket=tgt_bucket, CopySource={'Bucket': src_bucket, 'Key': src_key}, Key=tgt_key)
        if is_move:
            # Delete the original object
            s3_client.delete_object(Bucket=src_bucket, Key=src_key)

    def download_dir_from_s3(
        self, bucket_name, remoteDirectoryName, local_dir, exclude_lst:list | str =[], overwrite=False, mk_s3_structure=False
    ):
        """@Lagaras added mk_s3_structure to create the same structure as in s3"""

        logger.debug(
            "Downloading directory from bucket %s  key %s to file: %s"
            % (bucket_name, remoteDirectoryName, local_dir)
        )

        os.makedirs(local_dir, exist_ok=True)

        if isinstance(exclude_lst, str):  # convert possible str to [str]
            exclude_lst = [exclude_lst]
        s3 = self.get_boto3_s3_client_OO()
        bucket = s3.Bucket(bucket_name)
        matched_keys = bucket.objects.filter(Prefix=remoteDirectoryName)

        if matched_keys is None:
            raise InvalidParameterError(
                'No keys found in %s/%s' % (bucket_name, remoteDirectoryName)
            ) #TODO what does filter return if no keys found? Current code will not raise an error
        for obj in matched_keys:
            exclude = False

            # skip if file matches the exclude_lst
            for exclude_pattern in exclude_lst:
                if fnmatch.fnmatch(
                    obj.key, exclude_pattern
                ):  # when using fnmatch(not glob) we could use linux regex pattern
                    exclude = True

            if exclude:  # skip if object matches one of the excludes
                continue
            
            if mk_s3_structure:
                local_file = helper.join_paths_with_common_part(local_dir, obj.key)
                local_file_dir = os.path.dirname(local_file)
                if not os.path.exists(local_file_dir):
                    os.makedirs(local_file_dir)
            else:
                local_file = os.path.join(local_dir, os.path.basename(obj.key))

            if not os.path.exists(local_file) or overwrite:
                logger.debug("Downloading %s to %s", obj.key, local_file)
                try:
                    bucket.download_file(obj.key, local_file)  # save to same path
                except Exception as exc:
                    logger.error(f"Error downloading {obj.key}, exception: {exc}")
            else:
                logger.debug('File %s already exists, skipping', local_file)

        
    def create_bucket(self,bucket_name):
        from cgls_cpe.storage import remote_storage
        if not remote_storage.is_valid_bucket_name(bucket_name):
            raise InvalidParameterError( ' bucket_name was invalid: ' + bucket_name)
         
        s3 = self.get_boto3_s3_client()
        s3.create_bucket(Bucket=bucket_name)
        
    def delete_bucket(self,bucket_name):
        s3 = self.get_boto3_s3_client()
        s3.delete_bucket(Bucket=bucket_name)
        
        
    def set_policy_on_bucket(self,bucket_name:str, policy:str):
        s3 = self.get_boto3_s3_client()    
        s3.put_bucket_policy(Bucket=bucket_name, Policy=policy)
        
    def get_policy_on_bucket(self,bucket_name:str):
        s3 = self.get_boto3_s3_client()    
        return s3.get_bucket_policy(Bucket=bucket_name)        
        
    #one method, low level?
    def remove_from_s3(self,bucket, key):
        s3 = self.get_boto3_s3_client_OO()
        s3.Object(bucket, key).delete()    
    
    def remove_object(self,bucket_name:str, key:str):
        logger.debug("Removing: %s , %s", bucket_name, key)
        s3 = self.get_boto3_s3_client()
        s3.delete_object(
            Bucket=bucket_name,
            Key=key)

def is_s3(url):
    if url is None:
        return False
    return str(url).startswith(S3PREFIX)    

def get_s3_url(container, key):
    return S3PREFIX + container + '/' + key    