'''
Created on Apr 24, 2024

@author: demunckd
'''
import time
from cgls_cpe.common.launcher_sandbox import load_sandbox_if_requested


def main():
    #needed when we use an executor
    load_sandbox_if_requested()
    from cgls_cpe.logging import log
    from cgls_cpe.processing import manager  
    logger =log.logger()
    logger.info("Log inside driver - newest")
    from cgls_cpe.config.configuration import Configuration
    Configuration()
    while True:
        manager.process_status_objects()
        logger.info('Sleeping for 15 seconds...')
        time.sleep(15)
        
if __name__ == '__main__':
    main()
    