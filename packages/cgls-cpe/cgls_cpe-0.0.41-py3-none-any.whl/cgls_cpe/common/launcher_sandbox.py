'''
Created on Dec 16, 2023

@author: demunckd
'''
import sys
import os
import subprocess
import time
from importlib import reload

ENV_PARAM_TO_PATH='CGLS_CPE_SANDBOX_CODEBASE_MOUNT_PATH'

# this modules mounts the cgl-sandbox if requested and sets first sys path to value of environment variable CGLS_CPE_SANDBOX_CODEBASE_MOUNT_PATH
# returns env dict if mount was done

#no use of other cgls_cpe modules because of issues with reloading (notably the Configuration class)


def load_sandbox_if_requested():
    
    if ENV_PARAM_TO_PATH in os.environ:
        root_path_codebase = os.environ[ENV_PARAM_TO_PATH]
        print("SANDBOX MOUNT CODEPATH WAS REQUESTED, USING THE FOLLOWING PATH FOR LOADING MODULES: " + root_path_codebase)

        if not os.path.exists(root_path_codebase):
            print("Mounting sandbox first because it did not exist ")
            os.system('mkdir -p /mnt/sandbox')
            os.system('s3fs  cgl-sandbox /mnt/sandbox -o url=https://s3.waw3-2.cloudferro.com -o use_path_request_style')
            while not os.path.exists(root_path_codebase):
                print("Waiting for " + root_path_codebase +  "to become available...")
                time.sleep(1)
            print("Listing " + root_path_codebase )
            os.system('ls -l ' + root_path_codebase)
        else:
            print("Sandbox mount already existed")

        if sys.path[0] != root_path_codebase :
            sys.path.insert(0,root_path_codebase)
        print("Printing sys path: " + str(sys.path))

        #python sometimes preloads all modules available on the different paths
        list_of_modules_to_remove = [] 
        for module  in sys.modules:
            if module.startswith('cgls_'):
                print('Going to reload existing module ' + module + " for proper loading")
                list_of_modules_to_remove.append(module)
                
        for module in list_of_modules_to_remove:
            reload( sys.modules[module])
            
        print("Loading config module as test..." )
        import cgls_cpe.config.configuration as loaded_config
        print("Location of loaded config module: " + loaded_config.__file__)
        if not root_path_codebase in loaded_config.__file__ :
            raise Exception("Did not load sandbox version!")
        from cgls_cpe.logging import log
        
        env_copy = os.environ.copy()
        env_copy['PYTHONPATH'] = root_path_codebase + ':' + env_copy['PYTHONPATH']
        log.logger().warning("SANDBOX MOUNT ACTIVE ----- THIS SHOULD NOT BE THE CASE WHEN RUNNING IN PRODUCTION CHAINS!!!!!") 
        return env_copy
    else:
        return None
        

# You need to set the the following env variable to the mount path to use
# CGLS_CPE_SANDBOX_CODEBASE_MOUNT_PATH='/mnt/sandbox/code_base_ddm'
# Example usage:
#
# python3.11 cgls_cpe/common/launcher_sandbox.py '/mnt/sandbox/'  'ls -l'

def main(args):
    working_dir = args[0]
    cmd= args[1]
    env_dict = load_sandbox_if_requested()
    print('Going to start "' + cmd + '" in working dir "' + working_dir + '"' )
    if env_dict is not None:
        print("Using env with PYTHONPATH " + env_dict['PYTHONPATH'])
    result = subprocess.run(cmd, cwd=working_dir, shell=True, env=env_dict)
    print("Return code of command was was: " + str(result.returncode)) 
    exit(result.returncode)    
    

if __name__ == '__main__':
     main(sys.argv[1:])
    