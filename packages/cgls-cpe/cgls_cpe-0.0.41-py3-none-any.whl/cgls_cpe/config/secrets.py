import os
import hvac

from cgls_cpe.logging import log
from pickle import NONE


logger = log.logger(__name__)


class Secrets:
    
    
    
    def __init__(self, config):
        self.config= config
        self.settings = self.config.get_settings()
        self.cache_of_keys = {}
        self.reset()

    def get_secret_key(self,key):
        """
        Default function for obtaining  credentials. The following order will be maintained:
            1. From environment: If environment variables with the same name are set, return those values.
            2. From vault: if key exists in the "extra_env_secrets" table, try to fetch it from the confgured vault using "vault_url" setting
            3. From config: If the keys are set via the normal settings files  return their values.
        
        """
        logger.info("Getting key %s from env...", key)
        if key in os.environ:
            value = os.getenv(key)
            return value
        
        try: 
            value = self.cache_of_keys[key]
            if value is not None:
                logger.info("Found key %s in cache, returning it" , key)
                return value
        except:
            pass
        
        logger.info("Did not work, now getting key %s from vault..." , key)
        key_from_vault = self.get_key_from_vault(key)
        
        if key_from_vault is not None:
            self.cache_of_keys[key] = key_from_vault
            return key_from_vault 
        logger.info("Last resort: checking if  key %s inside settings..." , key)
        return self.settings[key]
    
    def reset(self):
        self.hvac_client = None
        self.vault_disabled = False
        self.cache_of_keys = {}
        
        
    # https://git.vito.be/projects/BIGGEO/repos/image_build/browse/oscars-download-auth/files/check_login_flows_oscars_download.py#11,895
    def init_hvac(self):
        try:
            self.hvac_client = hvac.Client(url=self.settings.vault_url)
            #
            try:
                logger.info("Trying with app role...")
                self.hvac_client.auth.approle.login(role_id=self.settings.vault_role_id ,secret_id=self.settings.vault_secr_id )
            except Exception as exc:
                logger.info("App role did not work trying with token...")
                self.hvac_client.token =  self.settings.vault_token 
            
            if not self.hvac_client.is_authenticated():
                logger.info("Could not authenticate vault client, disabling it")
                self.vault_disabled = True
        except Exception as exc:
            logger.warning("Vault disabled because of error: %s" , str(exc))
            self.vault_disabled = True   
                                  
    def get_client(self):
        if self.vault_disabled:
            return None
        if self.hvac_client is None:
            self.init_hvac()

        return self.hvac_client    
    
    def get_key_from_vault(self,key:str):
        try:
            client = self.get_client()
            
            if client is not None:
                secret_path_and_key = self.settings.extra_env_secrets[key].split(' ')
                secret_path = secret_path_and_key[0]
                secret_key = secret_path_and_key[1]
                secret_version_response = client.secrets.kv.v2.read_secret_version(
                        mount_point='kv',
                        path=secret_path,
                )
                value = secret_version_response['data']['data'][secret_key]
                logger.info("Got key")
                return value
        except Exception as exc:
            logger.warning("Could not get info from vault: %s" , str(exc))
            self.vault_disabled = True;
            return None;
