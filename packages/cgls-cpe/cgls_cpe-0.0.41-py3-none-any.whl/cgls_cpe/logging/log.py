'''
Created on Oct 20, 2023

@author: demunckd

'''

'''
    Placeholder for logging
     
'''
import traceback;
import logging.config

DEFAULT_LOGGER_NAME='cgls'    
#this is loaded before any configuration is loaded, so should NOT be modified
CGLS_CPE_LOGGING_CONFIG_DEFAULT = { 
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': { 
        'standard': { 
            'format': '%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: %(message)s'
        },
    },
    'handlers': { 
        'default': { 
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    'loggers': { 
        '': {  # root logger
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
    } 
}

def load_config(config_dict):
    logging.config.dictConfig(config_dict)


def load_default_config():
    print("Loading default log config - override by custom config or environment vars by calling Configuration() ")
    load_config(CGLS_CPE_LOGGING_CONFIG_DEFAULT)


def logger(name=None):
    if ( name is None):
        name =  DEFAULT_LOGGER_NAME
    return logging.getLogger(name)

load_default_config()

#in case we want a different logger
class LoggerCGLS_CPE(object):

    def debug(self, *args):
        print(*args)
    
    def info(self,*args ):
        print(*args)
    
    def warn(self, *args, exc=None):
        print(*args)
        if exc is not None:
            traceback.print_exc()
            print(exc)
    
    def error(self,*args, exc=None):
        print(*args)
        if exc is not None:
            traceback.print_exc()
            print(exc)
