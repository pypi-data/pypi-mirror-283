'''
Created on Mar 18, 2024

@author: demunckd
'''

import os

def get_spark_application_id():
    try:
        return os.environ['SPARK_APPLICATION_ID']
    except:
        return "unknown_spark_app_id" 
    
def get_pod_name():
    try:
        return os.environ['SPARK_EXECUTOR_POD_NAME']
    except:
        return "unknown_pod"