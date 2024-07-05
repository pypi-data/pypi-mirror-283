"""Common Python Library netCDF files.

This module provides functions for creating / writing / reading netCDF files

"""

import os
import cgls_cpe.cpl as cgls_cpl
import numpy as np
from numpy import double
from netCDF4 import Dataset #@UnresolvedImport

""" The type conversion dictionary allows strings to be converted to numpy types"""
TYPECONVERTDICT = {
    'byte':     np.byte, #will be a np.int8
    'int8':     np.int8,
    'int16':    np.int16,
    'int32':    np.int32,
    'int64':    np.int64,
    'byte':     np.uint8,
    'uint8':    np.uint8,
    'uint16':   np.uint16,
    'uint32':   np.uint32,
    'uint64':   np.uint64,
    'float':    np.float32,
    'float32':  np.float32,
    'double':   np.float64,
    'float64' : np.float64
    }

def createLatLonNetCDF(outputPath, longitudes, latitudes,
                  bandsInfoLst, globalAttributes = None,
                  chunking=None,
                  refDate=None, prodDate=None            ):
    """Create a CF-1.6 compliant netCDF file
    
    Creates a netCDF file to store the product information in.
    The file will always have a latitude and longitude dimensional variable and crs.
    Resolution is determined by step of the longitude dimensional variable.
    
    Parameters
    ----------
    outputPath : str
        the output file path
    longitudes : numpy.ndarray
        float64 array of longitude coordinates
    latitudes : numpy.ndarray
        float64 array of latitude coordinates
    bandsInfoLst : list of dict
        List of band information dictionaries. Each dictionary should have the following keys:
        * 'dataType':   (np.dtype) the numpy datatype for the variable and attributes
        * 'fillValue':  (None, int or float) the nodata value for the variables to be filled with. The variable attributes _FillValue and missing_value will be set accordingly. If the variable has no noDataValue, set to None. The variable will be filled with zero's, but the _FillValue will not be set.
        * 'name':       (str) the name of the variable
        * 'attributes': (dict) a dictionary containing the variable attributes to be set.
       
       The variable attributes have the following keys, where any unused attributed can be omited or set to False (boolean):
       * 'standard_name' : (str) CF-1.6 compliant name, omit if not listed
       * 'long_name':      (str) long name
       * 'grid_mapping':   (str) 'crs'
       * 'scale_factor':   (float) omit if not used
       * 'add_offset':     (float) omit if not used
       * 'units':          (str) empty string if no units defined
       * 'valid_range':    (list of int or float) e.g. [0, 250] or [0.0, 1.0]
       * 'flag_values':    (list of int) omit if not used
       * 'flag_meanings':  (str) space separated entries for each flag, omit if not used
       * 'flag_mask':      (list of int) bitfields, omit if not used
    globalAttributes : dict, optional
        Global attributes to be added to the NetCDF file, defaults to None
        The following global attributes should be set for CF-16 compliance:
        * 'title':               (str) product tile
        * 'history':             (str) History, add to input file history on a newline. Format '<process_date> - <processing module> <version>'
        The following global attributes are CF-16 compliance and are recommended to be used:
        * 'parent_identifier':   (str) urn of collection
        * 'identifier':          (str) urn of file
        * 'long_name':           (str) official name according to CF-16 standard, omit if not applicable
        * 'product_version':     (str) version of the product, including the capital V
        * 'time_coverage_start': (str) ISO format time stamp, e.g. 2019-01-01T00:00:00Z
        * 'time_coverage_end':   (str) ISO format time stamp e.g. 2019-01-01T23:59:59Z
        * 'platform':            (str) satelite name, e.g. S3A
        * 'sensor':              (str) used sensor(s), e.g. OLCI, SLSTR
        * 'orbit_type':          (str) 'LEO',
        * 'processing_level':    (str) e.g. 'L3'
        * 'institution':         (str) processing facility e.g. 'VITO NV'
        * 'source':              (str) 'Derived from EO satellite imagery'
        * 'processing_mode':     (str) choose either 'Offline' or 'Near Real Time'
        * 'references':          (str) link to online documentation e.g. 'https://land.copernicus.eu/global/products/ndvi'
        * 'copyright':           (str) 'Copernicus Service information 2018'
        * 'archive_facility':    (str) 'VITO
    chunking : list of int
        list with an integer value for each dimension that will determine the chunksize
    refDate : (string) 
        reference date, if specified with prodDate, a time dimensional variable will created with refDate as reference date.
    prodDate :(string) 
        product date, if specified with refDate, a time dimensional variable will created with (prodDate - refDate) as value.
    """
    if os.path.exists(outputPath):
        os.remove(outputPath)
    
    with Dataset(outputPath,'w') as netCDF4File:
        netCDF4File.setncattr('Conventions', 'CF-1.6')
        #Set Longitude dimension scale
        netCDF4File.createDimension('lon', len(longitudes))
        netCDF4File.createVariable('lon', np.float64, ('lon',), complevel=9)
        netCDF4File.variables['lon'][:] = longitudes
        lonAttrDict = {'_CoordinateAxisType'  : np.string_('Lon'),
                        'axis'                : np.string_('X'),
                        'DIMENSION_LABELS'    : np.string_('lon'),
                        'long_name'           : np.string_('longitude'),
                        'standard_name'       : np.string_('longitude'),
                        'units'               : np.string_('degrees_east')}
        netCDF4File.variables['lon'].setncatts(lonAttrDict)

        #Set Latitude dimension scale
        netCDF4File.createDimension('lat', len(latitudes))
        netCDF4File.createVariable('lat', np.float64, ('lat',), complevel=9)

        netCDF4File.variables['lat'][:] = latitudes
        # Attributes dictionary needed for NetCDF
        latAttrDict  = {'_CoordinateAxisType' : np.string_('Lat'),
                        'axis'                : np.string_('Y'),
                        'DIMENSION_LABELS'    : np.string_('lat'),
                        'long_name'           : np.string_('latitude'),
                        'standard_name'       : np.string_('latitude'),
                        'units'               : np.string_('degrees_north')}
        netCDF4File.variables['lat'].setncatts(latAttrDict)

        #Set crs
        netCDF4File.createVariable('crs',  'c', complevel=9)
        crsAttrDict = {'long_name'                   : np.string_('coordinate reference system'),
                       '_CoordinateAxisTypes'        : np.string_('GeoX GeoY'),
                       '_CoordinateTransformType'    : np.string_('Projection'),
                       'grid_mapping_name'           : np.string_('latitude_longitude'),
                       'inverse_flattening'          : np.float64(298.257223563),
                       'longitude_of_prime_meridian' : np.float64(0),
                       'semi_major_axis'             : np.float64(6378137),
                       'spatial_ref'                 : np.string_('GEOGCS["WGS 84",DATUM["WGS_1984",' +
                                                                  'SPHEROID["WGS 84",6378137,298.257223563,' +
                                                                  'AUTHORITY["EPSG","7030"]],' + 
                                                                  'TOWGS84[0,0,0,0,0,0,0],' +
                                                                  'AUTHORITY["EPSG","6326"]],'+
                                                                  'PRIMEM["Greenwich",' +
                                                                  '0,' + 
                                                                  'AUTHORITY["EPSG","8901"]],' +
                                                                  'UNIT["degree",' + 
                                                                  '0.0174532925199433,' +
                                                                  'AUTHORITY["EPSG","9108"]],' +
                                                                  'AUTHORITY["EPSG","4326"]]'),
                       'GeoTransform'                : np.string_('{:.10f} {:.10f} 0.0 {:.10f} 0.0 {:.10f}'.format(
                                                                        longitudes[0],
                                                                        longitudes[1] - longitudes[0],
                                                                        latitudes[0],
                                                                        latitudes[1] - latitudes[0]))

                       }
        netCDF4File.variables['crs'].setncatts(crsAttrDict)
        
        # For non disseminated products, the time variable will not be set.
        if refDate and prodDate:
            refDateStr = str(refDate)
            refDateStr = refDateStr[0:4] + '-' + refDateStr[4:6] + '-' + refDateStr[6:8] + ' 00:00:00'
            if type(prodDate) == list: #TODO: Check if this is OK for the time dimension
                netCDF4File.createDimension('time', len(prodDate))
                netCDF4File.createVariable('time', np.float64, ('time',), complevel=9)

                timeAttrDict = {'axis'      : np.string_('T'),
                                'long_name' : np.string_('Time'),
                                'units'     : np.string_('days since ' + refDateStr),
                                'calendar'  : np.string_('standard')}
                netCDF4File.variables['time'].setncatts(timeAttrDict)
                netCDF4File.variables['time'][:] = np.array(prodDate, dtype=np.float64)
            else:
                netCDF4File.createDimension('time', None)
                netCDF4File.createVariable('time', np.float64, ('time',), complevel=9)

                daysSinceRef = cgls_cpl.date_time.countNbDays(refDate, prodDate)
                #GIOG-1416
                timeAttrDict = {'axis'      : np.string_('T'),
                                'long_name' : np.string_('Time'),
                                'units'     : np.string_('days since ' + refDateStr),
                                'calendar'  : np.string_('standard')}

                netCDF4File.variables['time'].setncatts(timeAttrDict)
                netCDF4File.variables['time'][0] = daysSinceRef
        
        # Setting attributes through dictionaries
        if globalAttributes:
            # Before we apply the Python dictionary as a attributes, we must ensure that the types are all correct
            newGlobalAttributes = {}
            for key, value in globalAttributes.items():
                if value == False:
                        pass
                elif isinstance(value, str):
                    newGlobalAttributes[key] = np.string_(value)
                else:
                    newGlobalAttributes[key] = value
            netCDF4File.setncatts(newGlobalAttributes)
        
        for bandInfoDict in bandsInfoLst:
            name      = bandInfoDict['name']
            dType     = bandInfoDict['dataType']
            # Convert to np data type if a string was provided
            if isinstance(dType, str):
                dType = TYPECONVERTDICT[dType]
            doZlib    = False if dType in [np.float32, np.float64] else True
            dimensions = (u'lat', u'lon')
            if refDate and prodDate:
                dimensions = (u'time', u'lat', u'lon')
            if 'fillValue' in bandInfoDict and (not bandInfoDict['fillValue'] == None):
                fillValue = dType(bandInfoDict['fillValue'])
                netCDF4File.createVariable(
                                            name,
                                            dType,
                                            dimensions,
                                            zlib=doZlib,
                                            fill_value=fillValue,
                                            chunksizes=chunking,
                                            complevel=9,
                                            )
                # Add missing value to the attributes
                bandInfoDict['attributes']['missing_value'] = fillValue
            else:
                netCDF4File.createVariable(
                                            name,
                                            dType,
                                            dimensions,
                                            zlib=doZlib,
                                            chunksizes=chunking,
                                            complevel=9,
                                            )
            # Before we apply the Python dictionary as a attributes, we must ensure that the types are all correct
            newBandAttributes = {}
            for key, value in bandInfoDict['attributes'].items():
                    # Remove unused attributes
                    if key in ['scale_factor', 'add_offset']: # GIOG-1306 Should be float64
                        newBandAttributes[key] = np.float64(value)
                    else:
                        if type(value) == str:
                            newBandAttributes[key] = np.string_(value)
                        elif type(value) in [int, float]:
                            newBandAttributes[key] = dType(value)
                        elif type(value) == double:
                            newBandAttributes[key] = np.float64(value)
                        elif type(value) == list:
                            if type(value[0]) == int:
                                newBandAttributes[key] = list(map(dType, value))
                            elif type(value[0]) == float:
                                newBandAttributes[key] = list(map(np.float32, value))
                            elif type(value[0]) == double:
                                newBandAttributes[key] = list(map(np.float64, value))
                        elif type(value) == map:
                            newBandAttributes[key] = list(value)
                        else:
                            newBandAttributes[key] = value
            netCDF4File.variables[name].setncatts(newBandAttributes)

def _splitInOutOfBounds(coordLst,imgSizeXY):
    """_splitInOutOfBounds
    
    split coordinates up into inbounds and outbounds coordinates
        split up coordinates so the part that falls within an image
              is returned to e.g. cut out, and the part that falls outside
              is also returned to e.g. pad with nodata values
    
    Parameters:
    ----------
    # @param coordLst : (list )  
        coordinates that might be outside of an image
    # @param imgSizeXY : (tuple)  
        the x/y size of an image to check against
    Returns:
    -------
    splitBounds : (tuple)  
        coordinates inside and outside of the image
    
    """
    x_min,    y_min,    x_max,    y_max     = coordLst
    x_min_out,y_min_out,x_max_out,y_max_out = [0,0,0,0]
    #MAX
    if x_max   > imgSizeXY[0]:
        x_max_out = x_max - imgSizeXY[0]
        x_max     = imgSizeXY[0]
    elif x_max < 0:
        x_max_out = x_max
        x_max     = 0
    if y_max   > imgSizeXY[1]:
        y_max_out = y_max - imgSizeXY[1]
        y_max     = imgSizeXY[1]
    elif y_max < 0:
        y_max_out = y_max
        y_max     = 0
    #MIN
    if x_min   < 0:
        x_min_out  = x_min
        x_min      = 0
    elif x_min > imgSizeXY[0]:
        x_min_out  = 0
        x_min      = imgSizeXY[0]
    if y_min   < 0:
        y_min_out  = y_min
        y_min      = 0
    elif y_min > imgSizeXY[1]:
        y_min_out  = 0
        y_min      = imgSizeXY[1]
    inBoundsCoordLst  = [x_min,     y_min,    x_max,    y_max   ]
    outBoundsCoordLst = [x_min_out,y_min_out,x_max_out,y_max_out]
    splitBounds       = [inBoundsCoordLst,outBoundsCoordLst     ]
    return splitBounds

def writeBandNc(outputPath, datasetName, dataset,
                startRow=None, endRow=None, startCol=None, endCol=None,
                auto_maskandscale=False):
    """writeBandNc 
    write dataset values to an existing dataset
    
    Parameters:
    ----------
    outputPath      (string)
        the output file path
    datasetName     (string)
        the name of the dataset
    dataset        (np.array)
        the dataset to write - without time dimension
    startRow,endRow,startCol,endCol     (int)
        positioning of subtile-into-tile or tile-into-global-image
    auto_maskandscale (boolean)
        defaults to False - otherwise, data is scaled and offset before putting in the dsout
    
    """
    with Dataset(outputPath, 'a') as outFile:
        outFile.set_auto_maskandscale(auto_maskandscale) 
        #select output dataset
        dsOut          = outFile.variables[datasetName]

        timeDimOut     = False
        if len(dsOut.shape) > 2:
            timeDimOut = True
        
        inputShape     = dataset.shape[-2:]
        outputShape    = dsOut.shape[-2:]

        if None not in [startRow,endRow,startCol,endCol]:
            #get the indices that fit inside our ROI
            #note: coordinates here are [xmin,ymin,xmax,ymax]
            imgSizeXY      = (outputShape[1],outputShape[0])
            inputIdxLst    = [0,0] + list(inputShape)
            outputIdxLst   = [startCol,startRow,endCol,endRow]
            outputInsideIdxLst,invalidIdxLst = _splitInOutOfBounds(outputIdxLst,
                                                                  imgSizeXY      )
            outStartCol,outStartRow,outEndCol,outEndRow = outputInsideIdxLst
            inStartCol,inStartRow,inEndCol,inEndRow     = [(v - invalidIdxLst[i]) for i,v   \
                                                            in enumerate(inputIdxLst)       ]
            #write dataset to file
            # :-) startRow and startCol can have a valid value zero
            #GIOG-1282 quickfix instead of implementing intersect
            if (inEndRow < inStartRow) or (inEndCol < inStartCol):
                return
            if timeDimOut:
                dsOut[0,outStartRow:outEndRow,outStartCol:outEndCol] = dataset[inStartRow:inEndRow,inStartCol:inEndCol]
            else:
                dsOut[outStartRow:outEndRow,outStartCol:outEndCol] = dataset[inStartRow:inEndRow,inStartCol:inEndCol]
        else:
            if timeDimOut:
                dsOut[0,:,:] = dataset
            else:
                dsOut[:,:] = dataset

def loadPropNc(file, bandNameLst=None, logger=None):
    '''
    loadPropNc extracts dataset properties
        if no bandNameLst is provided, properties of all bands are extracted
        'lon', 'lat', 'crs' bands are excluded
    
    Params:
    ------
    file : string
        filename
    bandNameLst : list
        the list of band names to be extracted, defaults to None
    logger : object
        Instance to log to, defaults to print
    
    Returns:
    --------
    dataset properties dictionary holding properties as needed by cpls3_netcdf
    '''
    if not os.path.isfile(file):
        if logger:
            logger('warning: no file available ' + file)
        return {}
    excludeLst = ['lon', 'lat', 'crs'] # added when creating new netCDF file
    
    bandnameLst         = []
    nodataLst           = []
    typeLst             = []
    global_attrs_dict   = dict()
    variable_attrs_lst  = []
    
    with Dataset(file) as ds:
        if not bandNameLst:
            bandNameLst = ds.variables
        for a in ds.ncattrs():
            global_attrs_dict[a] = ds.getncattr(a)
        for b in bandNameLst:
            if b in excludeLst:
                continue
            d = ds[b]
            bandnameLst.append(b)
            attrs = dict()
            for a in d.ncattrs():
                attrs[a] = d.getncattr(a)
            if ('_FillValue' in attrs):
                fill_value = d._FillValue
            else:
                fill_value = None
            
            bandInfoDict = dict()
            bandInfoDict['name']        = b
            bandInfoDict['dataType']    = d.dtype.type
            #do not add None value
            if fill_value:
                bandInfoDict['fillValue']   = fill_value
            bandInfoDict['attributes']  = attrs
            variable_attrs_lst.append(bandInfoDict)
            nodataLst.append(fill_value)
            typeLst.append(d.dtype.type)
        
        propCfg = {'global_attrs_dict'  : global_attrs_dict,
                   'variable_attrs_lst' : variable_attrs_lst,
                   'bandnameLst'        : bandnameLst,
                   'nodataLst'          : nodataLst, 
                   'typeLst'            : typeLst, 
                   'sizex'              : len(ds['lon']),
                   'sizey'              : len(ds['lat']),
                  }
    return propCfg

def loadValNc(file, bandNameLst, rowMin, rowMax,colMin, colMax, nodata=np.nan, dtype=np.float32, maskandscale=False, logger=None):
    '''
    loadValNc extracts subset of netCDF file based on rowMin, rowMax,colMin, colMax
        if no bandNameLst is provided, all bands are extracted
            'lon' 'lat', 'crs are excluded
    Params:
    ------
    rowMin, rowMax,colMin, colMax, : int
        coordinates of window to be extracted
    file : string
        filename
    bandNameLst : list
        the list of band names to be extracted
    logger : object
        Instance to log to, defaults to print    
    
    Returns:
    --------
    dataset 
    '''
    # note: to be optimized for time dimension !!!
    if not os.path.isfile(file):
        if logger:
            logger('warning: no file available ' + file)
        
        return np.full((rowMax-rowMin,colMax-colMin), nodata, dtype=dtype)
    
    if logger:
        logger('info: reading {}'.format(file))
    excludeLst = ['lon', 'lat', 'crs'] # added when creating new netCDF file
    ds = Dataset(file)
    if ds is None:
        if logger:
            logger('Failed open file')
        return np.full((rowMax-rowMin,colMax-colMin), nodata, dtype=dtype)
    
    ds.set_auto_maskandscale(maskandscale)
    
    structval = []
    for b in ds.variables:
        if b in excludeLst:
            continue
        #check if band values are to be returned
        addValues = False
        if (not bandNameLst) or (b in bandNameLst):
            addValues = True
        if addValues:
            if len(ds[b].shape) == 3:
                structval.append(ds[b][0,rowMin:rowMax,colMin:colMax])
            else:
                structval.append(ds[b][rowMin:rowMax,colMin:colMax])
    ds.close()
    del ds
    return structval
    
def createOutputNc (outputPath, longitudes, latitudes,
                    bandLst, fillValueLst, typeLst,
                    global_attributes=None, variable_attributes=None,
                    refDate=None, prodDate=None):
    '''wrapper method createOutputNc - deprecated method provided for backward compatibility
    
    Creates a netCDF file to store the information in.
    The file will always have a latitude and longitude dimensional variable and crs.
    When a reference date and product data are specified, a time dimensional variable will be created as well.
    If global and/or variable attributes are specified, they will be added to the file.
    
    Params:
    ------
    outputPath  (string) the output file path
    longitudes  (numpy.ndarray) float64 array of longitudes coordinates
    latitudes   (numpy.ndarray) float64 array of latitude coordinates
    bandLst     (list) strings that represent the bands to be written
    fillValueLst (list) fill values to be added
    global_attributes   (dict) Global netCDF attributes: key = attribute name, value = attribute value
    variable_attributes (dict) Variable attributes nested dictionary: key = variable name as in bandLst, value = attributes dictionary as described for glabal_attributes
    refDate  (string) reference date, if specified with prodDate, a time dimensional variable will created with refDate as reference date.
    prodDate (string) product date, if specified with refDate, a time dimensional variable will created with (prodDate - refDate) as value.
    
    '''
    bandInfoLst = []
    for index in range(len(bandLst)):
        name = bandLst[index]
        bandInfoDict = {'dataType'  : typeLst[index],
                        'fillValue' : fillValueLst[index],
                        'name'      : name,
                        'attributes': variable_attributes[name]['attributes'],
                        }
        bandInfoLst.append(bandInfoDict)
    
    createLatLonNetCDF(outputPath, longitudes, latitudes, bandInfoLst, global_attributes, chunking=None, refDate=refDate, prodDate=prodDate)


