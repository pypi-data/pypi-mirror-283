'''
Created on Nov 5, 2023

@author: demunckd
'''


from cgls_cpe.config.configuration import Configuration
from cgls_cpe.storage.implementation.s3_api import S3Api
import json
from cgls_cpe.storage import remote_storage

s3_api = None

BUCKET_SANDBOX_NAME='cgl-sandbox'
BUCKET_REF_DATA_NAME='cgl-reference-data'

TEST_INPUT_NAME='input'
TEST_RESULT_NAME='result'

TEST_UNIT_TEST_NAME='unit-tests'
TEST_INTEGRATION_TEST_NAME='integration-tests'

#TODO: return transparantly locations also with STAG/PROD prefix depending on environment if they exist


def get_url_ref_data_input(path):
    return 's3://' + BUCKET_REF_DATA_NAME + '/' + TEST_INPUT_NAME + '/' + path


def get_url_ref_data_result(path):
    return 's3://' + BUCKET_REF_DATA_NAME + '/' + TEST_RESULT_NAME + '/' + path

def get_url_ref_data_result_unit_tests(path):
    return get_url_ref_data_result(TEST_UNIT_TEST_NAME + '/' + path)  

def get_url_ref_data_result_integration_tests(path):
    return get_url_ref_data_result(TEST_INTEGRATION_TEST_NAME + '/' + path)  


def get_url_sandbox_unit_test(path):
    return 's3://' + BUCKET_SANDBOX_NAME + '/' +TEST_UNIT_TEST_NAME + '/' + path

def __init_permission():
        policy_json = Configuration().get_settings().s3_perm_sandbox
        custom_policy = json.dumps(policy_json)
        
        remote_storage.__get_s3_api().set_policy_on_bucket(BUCKET_SANDBOX_NAME, custom_policy)
        
        policy_json = Configuration().get_settings().s3_perm_reference_data
        custom_policy = json.dumps(policy_json)
        remote_storage.__get_s3_api().set_policy_on_bucket(BUCKET_REF_DATA_NAME, custom_policy)

#__init_permission()
        