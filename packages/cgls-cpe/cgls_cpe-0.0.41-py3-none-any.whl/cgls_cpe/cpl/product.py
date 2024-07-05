"""Common Python Library product class related functions.

This module provides functions to manipulate products

"""

import copy
import datetime
import os

from osgeo import gdal, gdalconst
from osgeo.gdalconst import *

import netCDF4

class Product:
    """Constructor Base class for all products.
        
    Parameters
    ----------
    productFileName : string or None
        product filename.
                
    """
    def __init__(self, productFileName=None):
        
        # TODO: read settings from configuration file 
        
        # Initialize internal product information dictionary
        self._productInfoDict = {}
        
        if(productFileName is None):
            self._productInfoDict['exists'] = 0
        else:
            self.getFileInfo(productFileName)

    """Deconstructor.
        
    Parameters
    ----------
            
    """
    def __del__(self):

        del self
        
    def __str__(self):
        """Convert product information to a string.
        
        Returns
        -------
        (string):
            product information string.
        
        """
        productInfoStr = 'Product information:\n'
        for key in self._productInfoDict:
            productInfoStr += key + ' = ' + str(self._productInfoDict[key]) + '\n'
        
        return productInfoStr

    def getProductInfo(self):
        """Get the product information.
        
        Returns
        -------
        dictionary
            product information dictionary.
        
        """        
        return copy.deepcopy(self._productInfoDict)

    def getFileInfo(self, productFileName):
        """Get the file information of the product and store the information in the internal product information dictionary.
        
        Parameters
        ----------
        productFileName : string
            product filename.
        
        """
        if(os.path.exists(productFileName)):
            self._productInfoDict['exists']           = 1
            self._productInfoDict['productname']      = os.path.basename(productFileName)
            self._productInfoDict['extension']        = os.path.splitext(os.path.basename(productFileName))[1][1:]
            self._productInfoDict['location']         = os.path.dirname(productFileName)
            self._productInfoDict['size']             = os.path.getsize(productFileName)
            self._productInfoDict['format']           = ''
            self._productInfoDict['creationdate']     = datetime.datetime.fromtimestamp(os.path.getctime(productFileName)).strftime('%Y-%m-%d %H:%M')
            self._productInfoDict['modificationdate'] = datetime.datetime.fromtimestamp(os.path.getmtime(productFileName)).strftime('%Y-%m-%d %H:%M')
            self._productInfoDict['accessdate']       = datetime.datetime.fromtimestamp(os.path.getatime(productFileName)).strftime('%Y-%m-%d %H:%M')
            self._productInfoDict['stat']             = os.stat(productFileName)
            
            # TODO: implementation other formats like HDF4, HDF5, ...
            if(self._productInfoDict['extension'].lower() == 'nc'):
                self._readFileInfoNetCDF4(productFileName)
            elif(self._productInfoDict['extension'].lower() == 'tif' or self._productInfoDict['extension'].lower() == 'tiff'):
                self._readFileInfoGeoTiff(productFileName)
            else:
                self._productInfoDict['format'] = 'unknown'
        else:
            self._productInfoDict['exists'] = 0
            
    def getFormat(self):
        """Get the file format of the product.
        
        Returns
        -------
        string
            the file format of the product (netCDF4, geotiff, ...).
        
        """
        return self._productInfoDict['format']

    def setProduct(self, productFileName):
        """Set the product filename.
        
        Parameters
        ----------
        productFileName: string
            product filename.
                
        """
        self._productInfoDict = {}
        self.getFileInfo(productFileName)
            
    def _readFileInfoNetCDF4(self, productFileName):
        """Read a netCDF4 file and get the file information of the product.
        
        Parameters
        ----------
        productFileName: string
            product filename.
            
        """            
        self._productInfoDict['format'] = 'netCDF4'
        
        # Open NetCDF4 file and get all the information
        with netCDF4.Dataset(productFileName) as fInput:        
            
            # get global metadata
            self._productInfoDict['metadata'] = fInput.__dict__
            
            # get dimension information
            dimensionsLst = []
            for name, dimension in fInput.dimensions.items():  
                dimensionsLst.append({ 'name' : name, 'size' : dimension.size })
                
            # get variable information
            variablesLst = []
            #print(type(fInput.variables.items()))
            for name, variable in fInput.variables.items():  
                variablesLst.append({ 'name' : name, 'attrs' : variable.ncattrs() })
            
            self._productInfoDict['dimensions'] = dimensionsLst
            self._productInfoDict['variables']  = variablesLst

    def _readFileInfoGeoTiff(self, productFileName):
        """Read a GeoTiff file and get the file information of the product.
        
        Parameters
        ----------
        productFileName: string
            product filename.
            
        """    
        self._productInfoDict['format'] = 'geotiff'
            
        dataset = gdal.Open(productFileName, GA_ReadOnly)
        if(dataset == None):
           print('-E- Error opening file: ' + productFileName)
           return

        self._productInfoDict['metadata']       = dataset.GetMetadata()

        self._productInfoDict['xsize']          = dataset.RasterXSize
        self._productInfoDict['ysize']          = dataset.RasterYSize
        self._productInfoDict['numberoflayers'] = dataset.RasterCount
        self._productInfoDict['projection']     = dataset.GetProjection()
        
        self._productInfoDict['origin']         = []
        self._productInfoDict['pixel_size']     = []
    
        geotransform = dataset.GetGeoTransform()
        if not geotransform is None:
           self._productInfoDict['origin']     = [ geotransform[0], geotransform[3] ]
           self._productInfoDict['pixel_size'] = [ geotransform[1], geotransform[5] ]
        
        self._productInfoDict['layersdatatype'] = []
        
        for idx in range(dataset.RasterCount):
            band = dataset.GetRasterBand(idx + 1)
            self._productInfoDict['layersdatatype'].append(gdal.GetDataTypeName(band.DataType))
 