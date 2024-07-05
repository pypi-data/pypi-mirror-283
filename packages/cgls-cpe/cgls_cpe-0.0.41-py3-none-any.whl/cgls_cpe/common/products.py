'''
Created on Dec 21, 2023

@author: oomsb
'''

import os
from datetime import datetime

def splitS3ProductName(filename: str) -> dict:
    #MMM_OL_L_TTTTTT_yyyymmddThhmmss_YYYYMMDDTHHMMSS_YYYYMMDDTHHMMSS_[instance ID]_GGG_[class ID].SEN3
    filename = os.path.basename(filename)   #remove path from location
    _filename, _file_ext = os.path.splitext(filename)
    otherParts = _filename[16:].split('_')
    s3Dict = {'mission':  _filename[0:3],
              'sensor':   _filename[4:6],
              'level':    _filename[7],
              'dataType': _filename[9:15],
              'sensingStartTime': otherParts[0],
              'sensingStopTime':  otherParts[1],
              'creationTime':     otherParts[2],
              'duration':         otherParts[3],
              'cycleNr':          otherParts[4],
              'relativeOrbitNr':  otherParts[5],
              'frameAlongTrackCoord': otherParts[6],
              'dataCenterID':         otherParts[7],
              'platform':             otherParts[8],
              'timeliness':           otherParts[9],
              'collection':           otherParts[10],
              'extension':_file_ext
              }
    return s3Dict

def splitCGLS3ProductName(productName):
    """ splits a CGL-S3 product name into its parts
    
    Parameters
    ----------
    productName : str
        The product name to be verified and split
    
    Returns
    -------
    dict
        The components
    """
    checkCGLS3ProductName(productName)
    (project, product, time, area, sensor, version) = productName.split('_')
    version = version[1:] #remove the 'v' character
    productElements = product.split('-', 1)
    product = productElements[0]
    if len(productElements) > 1:
        subtype = productElements[1]
    else:
        subtype = None
    (verMajor, verMinor, verRevision) = version.split('.')
    rc = None
    if verRevision.startswith('rc'):
        rc = 'rc'
        verRevision = verRevision[2:]

    productInfo = {
        'project' : project,
        'product' : product,
        'subtype' : subtype,
        'time'    : time,
        'area'    : area,
        'sensor'  : sensor,
        'version' : version,
        'verMajor': verMajor,
        'verMinor': verMinor,
        'verRev'  : verRevision,
        'rc'      : rc
        }
    return productInfo

def checkCGLS3ProductName(productName):
    """ Check if product Name complies to an official Copernicus Global Land Sentinel 3 based product name
    
    The function will check if all elements are present in the product name and 
    if the elements are correct.
    
    Parameters
    ----------
    productName : str
        The product name to be verified
    
    Raises
    ------
    ValueError
        If something is wrong with the name
    """
    try:
        (project, product, time, area, sensor, version) = productName.split('_')
    except:
        raise ValueError('Not all elements are present')
    
    if project != 'cgl': raise ValueError('Incorrect project')
    
    productElements = product.split('-', 1)
    product = productElements[0]
    if product != product.upper(): raise ValueError('Product type should be UPPER case')
    
    if len(productElements) > 1:
        subtype = productElements[1]
        if subtype != subtype.upper(): raise ValueError('Product subtype should be UPPER case')
    
    if len(time) > 14: raise ValueError('Incorrect length of time string')
    try:
        datetime.strptime(time[0:8], '%Y%m%d')
    except:
        raise ValueError('Date part of time is invalid')
    try:
        #We can not discriminate between a timestamp (HHmm) or an index (IIII)
        token = int(time[8:])
    except:
        raise ValueError('Time/index part of time is invalid')
    if int(time[0:8]) < 20160229: raise ValueError('There were no Sentinel 3 satellites before 20160229')
    
    if area != area.upper(): raise ValueError('area should be UPPER case')
    
    if sensor not in ['S3', 'S3A', 'S3B']: raise ValueError('Incorrect sensor value')
    
    if sensor[0:2] != 'S3':
        raise ValueError('Incorrect sensor value')
    
    try:
        (verMajor, verMinor, verRevision) = version.split('.')
    except:
        raise ValueError('Not all element specified in version')
    if verMajor[0] != 'v': raise ValueError('Incorrect version format')
    try: int(verMajor[1:])
    except: raise ValueError('version Major element incorrect')
    try: int(verMinor)
    except: raise ValueError('version Minor element incorrect')
    try:
        if verRevision[0] == 'r':
            if verRevision [1] == 'c':
                int(verRevision[2:])
            else:
                raise ValueError('version Revision element incorrect')
        else:
            int(verRevision)
    except:
        raise ValueError('version Revision element incorrect')
