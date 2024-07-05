'''
Created on Dec 8, 2023

@author: oomsb
'''
import datetime
import traceback
import os
import requests
import re
import time
import random

from cgls_cpe.config.configuration import Configuration
from cgls_cpe.common.helper import run_command

from cgls_cpe.logging import log
logger = log.logger()

def check_environment(context):
    if context.is_production() != Configuration().is_production():
        raise Exception("Mixing up environments")


class PRIP():
    def __init__(self):
        # get configuration parameters
        self.config = Configuration()
        self.username = self.config.get_secrets().get_secret_key('PRIP_usr')
        self.password = self.config.get_secrets().get_secret_key('PRIP_pwd')

    def do_request(self, url):
        r = requests.get(url, auth=(self.username, self.password), verify=False)
        return r

    def download_and_unzip(self, url, extract_to='.'):
        logger.debug("url: %s, extract to : %s" % (url, extract_to))
        match = re.search(r'Products\(([^)]+)\)', url)
        id = match.group(1)
        local_filename = '%s.zip' % id
        logger.debug('local filename: %s '% local_filename)

        max_retries = 10
        delay=60 #seconds to retry download * random number

        attempt = 0
        while attempt < max_retries:
            try:
                with requests.get(url, auth=(self.username, self.password), verify=False, stream=True) as r:
                    r.raise_for_status()
                    with open(local_filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                logger.info(f"Downloaded {local_filename}")
                break
            except Exception as e:
                attempt += 1
                logger.warning(f"Attempt {attempt} failed: Unable to download {url} to {local_filename}")
                logger.warning(f"Response status code: {r.status_code if 'r' in locals() else 'N/A'}")
                logger.warning(f"Error: {str(e)}")
                
                if attempt < max_retries:
                    time_to_sleep = random.random()*delay
                    logger.info(f"Retrying in {time_to_sleep} seconds...")
                    time.sleep(time_to_sleep)
                else:
                    logger.exception("Giving up after exception")
                    logger.error("All attempts failed.")
                    return -1, ''

        #get object name
        cmd = 'unzip -Z -1 %s | head -1' % local_filename
        stdout, stderr, err_nr = run_command(cmd, end_on_failure=True)
        logger.debug("stdout : %s" % stdout)
        match = re.search("b'(S3.*\.SEN3)", stdout)
        object_name = match.group(1)


        # Unzip the file using the system unzip command
        cmd = 'unzip -o %s -d %s' % (local_filename, extract_to)
        stdout, stderr, err_nr = run_command(cmd, end_on_failure=True)
        logger.debug(f"Extracted files to {extract_to}")

        # Optionally delete the zip file after extraction
        if os.path.exists(local_filename):
            #os.remove(local_filename)
            logger.debug(f"Deleted {local_filename}")

        return 0, os.path.join(extract_to, object_name)

    def download(self, remote_path, local_path, exclude_lst=[]):
        logger.debug("Downloading %s" % remote_path)
        try:
            self.eo_data_s3.download_dir_from_s3('EODATA', remote_path, local_path, exclude_lst=exclude_lst)
            return 0
        except:
            logger.error("Unable to download %s to %s" % (remote_path, local_path))
            traceback.print_exc()
            return -1