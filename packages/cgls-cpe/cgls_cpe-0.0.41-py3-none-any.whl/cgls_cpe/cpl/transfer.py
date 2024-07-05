"""Common Python Library file transfer functions.

This module provides functions to transfer files (ftp, sftp, ...)

"""
import os
import re
from time import sleep

def ftpPull(serverCfgDict, fileLst=None, destination='/tmp',fileFilterFunc=lambda x:x):
    """ Download a list of files from a server to a local destination

    Parameters
    ----------
    serverCfgDict : dict
        configuration dictionary which should contain the following key/value pairs:
        'server' : str, containing the url of the server
        'user' : str, containing the login user credentials
        'psw' : str, containing the login password credentials
        'remoteDir' : str, containing the remote directory on the server
        'numberOfAttempts' : int, total number of pull attempts
        'sleepTime' : int, time to wait between attempts in seconds
    fileLst : list of str
        Files to download relative to remoteDir. (default=None;all files in remoteDir)
    destination: str
        Path to the directory where the files get downloaded to. (default='/tmp')
    fileFilterFunc: func
        Function that takes the fileLst & returns a filtered list. (default=lambda x:x)

    Returns
    -------
    (success, fileInfoLst) : tuple (bool, list of dict):
        success is True when all files are successful downloaded
        fileInfoLst is a list dictionaries containing the following key/value pairs:
        'fileName' : str, the filename
        'location' : str, the path where the file is stored, excluding the filename
        'success' : bool, true is download is successful
        'attempts' : int, number of attempts to download the file
        'error': str, ftplib error of the last failed attempt

    Raises
    ------
    ftplib exceptions in case connection fails.

    Note
    ----
    Errors during download are caught and stored in the result list of dictionaries

    """
    from ftplib import FTP

    fileInfoLst = []
    success = True

    ftp = FTP(serverCfgDict['server'])
    ftp.login(user   = serverCfgDict['user'],
              passwd = serverCfgDict['psw'])
    ftp.cwd(serverCfgDict['remoteDir'])

    #[HSPF-308] download all files if none are provided
    # note: if there is a foolproof way to get a dry file list, 
    #       please implement.
    if fileLst == None: 
        fileLst = []
        ftp.dir(fileLst.append)
        #capture everything ((.*)) following everything but a colon ([^:]+),
        # a colon, multiple numbers ([0-9]+) and spaces ( +)
        #eg: '-rw-r--r--    1 841      50            118 Mar 22 12:00 unit_test.txt'
        #becomes 'unit_test.txt'
        #HSPF-295
        #Unit test failes as ftp.dir() no longer returns the hours:minutes for the file:
        #'-rw-r--r--    1 841      50            118 Mar 22  2022 unit_test.txt'
        #as such, the regex produces an empty list.
        fileLst = [d.split(' ')[-1] for d in fileLst]
    #filter the fileLst based on filename
    fileLst = fileFilterFunc(fileLst)

    for fl in fileLst:
        resultDict = {
        'fileName' : fl,
        'location' : destination,
        'success'  : False,
        'attempts' : 0,
        'error'    : ''
        }
        fileLocal = os.path.join(destination, fl)
        fileLocalPart = os.path.splitext(fileLocal)[0] + '.part'
        for attempt in range(1, serverCfgDict['numberOfAttempts']+1):
            try:
                with open(fileLocalPart, 'wb') as hFileLocal:
                    ftp.retrbinary('RETR ' + fl, hFileLocal.write, 1024)
                os.rename(fileLocalPart, fileLocal)
                resultDict['success'] = True
                resultDict['attempts'] = attempt
                break
            except Exception as err:
                resultDict['error'] = '{}'.format(err)
                resultDict['attempts'] = attempt
                success = False
                if os.path.exists(fileLocalPart):
                    os.remove(fileLocalPart)
                sleep(serverCfgDict['sleepTime'])
        fileInfoLst.append(resultDict)
    ftp.close()
    return success, fileInfoLst

def sftpPull(serverCfgDict, fileLst=None, destination='/tmp',fileFilterFunc=lambda x:x):
    """ Download a list of files from a server to a local destination

    Parameters
    ----------
    serverCfgDict : dict
        configuration dictionary which should contain the following key/value pairs:
        'server' : str, containing the url of the server
        'user' : str, containing the login user credentials
        'psw' : str, containing the login password credentials
        'remoteDir' : str, containing the remote directory on the server
        'numberOfAttempts' : int, total number of pull attempts
        'sleepTime' : int, time to wait between attempts in seconds
    fileLst : list of str
        Files to download relative to remoteDir. (default=None;all files in remoteDir)
    destination: str
        Path to the directory where the files get downloaded to. (default='/tmp')
    fileFilterFunc: func
        Function that takes the fileLst & returns a filtered list. (default=lambda x:x)

    Returns
    -------
    (success, fileInfoLst) : tuple (bool, list of dict):
        success is True when all files are successful downloaded
        fileInfoLst is a list dictionaries containing the following key/value pairs:
        'fileName' : str, the filename
        'location' : str, the path where the file is stored, excluding the filename
        'success' : bool, true is download is successful
        'attempts' : int, number of attempts to download the file
        'error': str, ftplib error of the last failed attempt

    Raises
    ------
    pysftp exceptions in case connection fails.

    Note
    ----
    Errors during download are caught and stored in the result list of dictionaries

    """
    import pysftp

    fileInfoLst = []
    success = True

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys.load(serverCfgDict['known_hosts'])
    with pysftp.Connection(host=serverCfgDict['server'],
                             username=serverCfgDict['user'],
                             password=serverCfgDict['psw'],
                             cnopts=cnopts) as sftp:
        sftp.cwd(serverCfgDict['remoteDir'])

        #[HSPF-308] download all files if none are provided
        if fileLst == None: fileLst = sftp.listdir()
        #filter the fileLst based on filename
        fileLst = fileFilterFunc(fileLst)

        for fl in fileLst:
            resultDict = {
            'fileName' : fl,
            'location' : destination,
            'success'  : False,
            'attempts' : 0,
            'error'    : ''
            }
            fileLocal  = os.path.join(destination, fl)
            fileLocalPart = os.path.splitext(fileLocal)[0] + '.part'
            for attempt in range(1, serverCfgDict['numberOfAttempts']+1):
                try:
                    sftp.get(fl, fileLocalPart)
                    os.rename(fileLocalPart, fileLocal)
                    resultDict['success'] = True
                    resultDict['attempts'] = attempt
                    break
                except Exception as err:
                    resultDict['error'] = '{}'.format(err)
                    resultDict['attempts'] = attempt
                    success = False
                    if os.path.exists(fileLocalPart):
                        os.remove(fileLocalPart)
                    sleep(serverCfgDict['sleepTime'])
            fileInfoLst.append(resultDict)
    return success, fileInfoLst