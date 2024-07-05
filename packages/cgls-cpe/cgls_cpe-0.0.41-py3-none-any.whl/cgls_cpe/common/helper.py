'''
Created on Nov 18, 2023

@author: demunckd
'''

import os
import signal
import subprocess
import time
from subprocess import STDOUT, check_output

from cgls_cpe.logging import log

logger=log.logger()


current_subprocs=set()
sighandlerset = False

def pad_two_digits(input_val):
    result = str(input_val).rjust(2, '0')
    return result
    
def mkdir_p(path):
    os.makedirs(path, exist_ok=True)

def run_command_with_workingdir(working_dir, cmd_line):
    global current_subprocs
    global sighandlerset
    if ( not sighandlerset ):
        logger.info("Coupling sigterm handler")
        signal.signal(signal.SIGTERM,handle_shutdown)
        sighandlerset = True
    with subprocess.Popen(cmd_line, cwd=working_dir, shell=True) as p:
        current_subprocs.add(p)

def run_command(cmd, env=None, end_on_failure=False):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, shell=True)
    stdout, stderr = p.communicate()
    err_nr = p.returncode
    if end_on_failure and err_nr:
        logger.exception("Failure on running %s" % cmd)
        logger.exception(" stdout : %s" % stdout)
        logger.exception(" stderr : %s" % stderr)
        raise Exception("Failure on running %s" % cmd)

    return str(stdout), str(stderr), err_nr

def run_command_with_timeout(cmd, timeout=None, env=None):
    try:
        runtime = None
        dl_start = time.time()
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, shell=True, timeout=timeout, check=True)
        dl_stop = time.time()
        runtime = int(dl_stop-dl_start)
        stdout = result.stdout.decode('utf-8')
        stderr = result.stderr.decode('utf-8')
        errnr = result.returncode
    except subprocess.TimeoutExpired:
        logger.exception("Timeout expired for command: %s" % cmd)
        stdout = None
        stderr = None
        runtime = timeout
        errnr = -15
    except subprocess.CalledProcessError as e:
        logger.exception("Failure on running %s" % cmd)
        logger.exception(" stdout : %s" % e.stdout.decode('utf-8'))
        logger.exception(" stderr : %s" % e.stderr.decode('utf-8'))
        stdout = e.stdout.decode('utf-8')
        stderr = e.stderr.decode('utf-8')
        errnr = e.returncode
        dl_stop = time.time()
        runtime = int(dl_stop - dl_start)
    return stdout, stderr, errnr , runtime

def exec_with_env(argv, env=None, log=print, check=True, log_proc=False):
    global current_subprocs
    global sighandlerset
    if ( not sighandlerset ):
        logger.info("Coupling sigterm handler")
        signal.signal(signal.SIGTERM,handle_shutdown)
        sighandlerset = True


    from subprocess import PIPE, STDOUT, Popen, SubprocessError

    # Run as an external process, with stderr redirected to stdout, and
    # with an unbuffered text stream as output

    with Popen(argv, stdout=PIPE, stderr=STDOUT, env=env,
               bufsize=1, universal_newlines=True, shell=True) as p:

        
        # Here you can get the PID
        global child_pid
        child_pid = p.pid
        current_subprocs.add(p)
        # Optionally log the process object as first message

        if log_proc:
            log(p)

        # Read output lines.  The loop will end just before the process
        # finishes, when it closes the stdout pipe

        for line in p.stdout:

            # We expect log to behave like print(), so it automatically
            # adds a newline.  We need to strip it off if there is one
            # already...

            line = line.rstrip('\n')

            log(line)

        # Make sure the process is finished.  This also sets and returns
        # the process's exit value

        exit_val = p.wait()
        current_subprocs.remove(p)

    # Throw an exception if the process returned a non-zero exit value
    if check and exit_val != 0:
        raise SubprocessError(f'"{" ".join(argv)}" returned {exit_val}')

    return exit_val

def join_paths_with_common_part(path_a:str, path_b:str):
    """Helper made for download_dir_from_s3, to join two paths with a common part.
    Example: path_a = '/my_bucket/sub_dir/date_sub_dir/', path_b = '/date_sub_dir/file.txt'

    :param str path_a: first part of path
    :param str path_b: second part of path containing the key
    :return _type_: a merged path withouth duplicate common part
    """
    parts_a = path_a.split(os.sep)
    parts_b = path_b.split(os.sep)
    
    parts_b = [p for p in parts_b if p not in parts_a]
    res_path = parts_a + parts_b
    if path_a.startswith(os.sep):
        return os.path.join(os.sep,*res_path)
    else:
        return os.path.join(*res_path)

def handle_shutdown(signum,frame):
    global current_subprocs
    logger.info("Shutting down")
    for proc in current_subprocs:
        try:
            logger.info("terminating zombie subprocess")
            proc.terminate()
        except:
            logger.info("killing zombie subprocess")
            proc.kill()
    exit(1)

def _str2bool(v):
    #this function can be used as an argument type in the argparser. The bool value can be represented in several formats
    import argparse
    try:
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        if v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
    except:
        raise argparse.ArgumentTypeError('Wrong value in _str2bool: '+str(v))
    
    
def exit_with_failure():
    logger.error("Error occured, exiting with failure")
    print("Error occured during processing, exiting")
    raise Exception("Error occured")
        