'''
Created on Dec 8, 2023

@author: oomsb
'''
import datetime
import traceback

from cgls_cpe.config.configuration import Configuration
from cgls_cpe.storage.implementation.s3_api import S3Api


s3_api = None

from cgls_cpe.logging import log
logger = log.logger(__name__)

def check_environment(context):
    if context.is_production() != Configuration().is_production():
        raise Exception("Mixing up environments")


class Eodata():
    def __init__(self):
        # get configuration parameters
        store = Configuration().get_storage()
        self.eo_data_s3 = S3Api(store.get_eodata_storage_endpoint(), store.get_eodata_acces_id(),
                           store.get_eodata_secret_acces_key())

    def download(self, remote_path, local_path, exclude_lst=[]):
        logger.debug("Downloading %s" % remote_path)
        try:
            self.eo_data_s3.download_dir_from_s3('EODATA', remote_path, local_path, exclude_lst=exclude_lst)
            return 0
        except:
            logger.error("Unable to download %s to %s" % (remote_path, local_path))
            traceback.print_exc()
            return -1