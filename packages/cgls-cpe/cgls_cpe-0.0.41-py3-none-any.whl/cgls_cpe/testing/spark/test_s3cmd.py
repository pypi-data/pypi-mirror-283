import os
import sys
import time
import random
from cgls_cpe.common.launcher_sandbox import load_sandbox_if_requested



def list_files(startpath=None):
    if startpath is None:
        startpath = os.path.dirname(os.path.realpath(__file__))
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

def work(t: int):
    print("loading sandbox for executor... current file: " + __file__)
    load_sandbox_if_requested()
    print("done loading sandbox, loading configuration...")
    from cgls_cpe.storage import local_storage
    from cgls_cpe.common import cloud_helper
    from cgls_cpe.storage import remote_storage

    #hereafter 
    from cgls_cpe.config.configuration import Configuration
    
    
    Configuration()
    logger.info("Going to start real work:")
    #print("os env latest:" + str(os.environ))
    do_work_real(1)
    
    try:        
                t = int(t)
                time_to_sleep = random.random()*t
                do_work_real(time_to_sleep)
    except:
                logger.exception("Something went wrong!")
    
    finally:
        local_storage.cleanup_tempfolder_for_this_execute()
                
                
def do_work_real(t): 
    from cgls_cpe.common import cloud_helper
    from cgls_cpe.storage import remote_storage

    i = 0
    from cgls_cpe.storage import local_storage
    
    src_path_s3 = 's3://cgl-reference-data/result/unit-tests/transfer/cgl_TOC_20190306035602_X25Y13_S3A_v2.3.rc3.nc'
    local_path =os.path.join(local_storage.get_scratch_root() , 'large.nc')
    logger.info("Downloading %s to %s" % (src_path_s3, local_path))
    dl_start = time.time()
    #remote_storage.download_remote_to_local_folder([src_path_s3], local_storage.get_scratch_root() , False)    
    remote_storage.download_single_file_to_local_path(src_path_s3, local_path )
    dl_stop = time.time()
    logger.info("Download runtime: %ss" % int(dl_stop-dl_start))
               
    while i < t :
        try:
            tgt_path_s3 =  's3://cgl-sandbox/upload-test/' + cloud_helper.get_pod_name() 
            logger.info("Uploading %s to %s" % (local_path, tgt_path_s3))
            dl_start = time.time()
            #remote_storage.upload_local_to_remote([local_path], tgt_path_s3)
            remote_storage.upload_single_file_to_remote_path(local_path, tgt_path_s3)
            dl_stop = time.time()
            logger.info("Upload runtime: %ss" % int(dl_stop-dl_start))
            print("Sleeping " + str(i))
            print("Listing mnt/:")
            list_files('/opt/spark/work-dir')
            #print("burnging...")
            #burn_cpu(1)
            time.sleep(1)
            print("Next loop...")
        except Exception as exc:
            print(str(exc))
        i+=1

def burn_cpu(n):
    
    start_time = time.time()
    i = 1.0
    while time.time() - start_time < n:
        i = i + 0.000001

if __name__ == "__main__":
    #needed when we use an executor
    load_sandbox_if_requested()
    from pyspark import SparkContext
    #print("os env from driver:" + str(os.environ))
    
    from cgls_cpe.logging import log
    logger =log.logger()
    logger.info("Log inside driver - newest")
    from cgls_cpe.config.configuration import Configuration
    Configuration()
    sc = SparkContext()
    sleep_time = sys.argv[1]
    nb_runs = int(sys.argv[2])
    i=0
    mylist =[]
    while i < nb_runs:
        mylist.append(sleep_time)
        i+=1
        
    
    try:
        #sc.parallelize(list_a_chunck_per_tile, len(list_a_chunck_per_tile)).foreach(process_target_with_api_rebels)
        listRDD = sc.parallelize(mylist, nb_runs).foreach(work)
        print("All done!")
    finally:
        sc.stop()
        print("keep running for 3 minutes ")
        time.sleep(180)
