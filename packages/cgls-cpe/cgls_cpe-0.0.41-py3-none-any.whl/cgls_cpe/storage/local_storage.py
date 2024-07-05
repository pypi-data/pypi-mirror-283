import os.path
from cgls_cpe.common import helper
import tempfile
from cgls_cpe.config.configuration import Configuration

tempfolder = None

from cgls_cpe.logging import log

logger = log.logger()


# Returns the default base scratch location - will be reused for sequential runs on the same executor pod and not cleaned up
def get_scratch_root():
    
    if os.path.exists('/opt/spark/work-dir'):
        folder = '/opt/spark/work-dir'
    else:
        folder = '/tmp/cgls_cpe-cache'
        
    helper.mkdir_p(folder)
    
    return folder


# Returns a unique temp folder location for this run
# if you call it twice inside an executor run, it will return the same folder again

# You NEED to call cleanup_tempfolder_for_this_execute
# to be sure a cleanup occurs in between executor runs
def get_tempfolder_for_this_execute_run():
    global tempfolder
    if tempfolder is None:
        tempfolder = tempfile.TemporaryDirectory(prefix=Configuration().get_proj_abbrev() + '-temp-', dir=get_scratch_root())
        logger.debug("returning temp folder: " + tempfolder.name)
         
    return tempfolder.name

# Cleanup temp folder of execute
def cleanup_tempfolder_for_this_execute():
    global tempfolder
    if tempfolder is not None:
        logger.debug("cleaning up temp folder: " + tempfolder.name)
        tempfolder.cleanup()
        logger.debug("done cleaning up temp folder: " + tempfolder.name)
    else:
        logger.debug("temp folder was not created so nothing to clean up")
    


