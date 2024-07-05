'''
Created on Dec 16, 2023

@author: demunckd
'''
import sys
from cgls_cpe.testing import test_data
from cgls_cpe.storage import remote_storage
from cgls_cpe.common import helper
import time

from cgls_cpe.logging import log
from cgls_cpe.config.configuration import Configuration
logger=log.logger()

def mount_list(optional_list_of_mounts):
    if optional_list_of_mounts is not None:
        mounts = optional_list_of_mounts.split(' ')
        for pair_bucket_mntpnt in mounts:
            if len(pair_bucket_mntpnt) > 1:
                bucket,mnt = pair_bucket_mntpnt.split(',')
                remote_storage.mount_s3fs(bucket,mnt)
                logger.info("Waiting a bit")
                time.sleep(1)

def umount_list(optional_list_of_mounts):
    if optional_list_of_mounts is not None:
        mounts = optional_list_of_mounts.split(' ')
        for pair_bucket_mntpnt in mounts:
            if len(pair_bucket_mntpnt) > 1:
                _,mnt = pair_bucket_mntpnt.split(',')
                try:
                    remote_storage.unmount_s3fs(mnt)
                except:
                    logger.exception('Issue with unmount of %s' , mnt)

def main(args):
    working_dir = args[0]
    cmd= args[1]
    optional_list_of_mounts = None
    if len (args)> 2:
        #format: "bucket1,mntpnt1 bucket2,mntpnt2"
        optional_list_of_mounts = args[2]
    mnt_point = Configuration().get_storage().get_sandbox_mnt()
    try:        
                logger.info("Mounting sandbox first")
                remote_storage.mount_s3fs(test_data.BUCKET_SANDBOX_NAME,mnt_point)
                mount_list(optional_list_of_mounts)
                time.sleep(2)
                logger.info("Launching %s from directory %s", cmd, working_dir)
                helper.run_command_with_workingdir(working_dir, cmd)
    finally:
                umount_list(optional_list_of_mounts)
                remote_storage.unmount_s3fs(mnt_point)
                logger.info("Launcher completed successfully")

if __name__ == '__main__':
     main(sys.argv[1:])
    
    
    