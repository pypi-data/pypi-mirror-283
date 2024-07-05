"""Common Python Library netCDF files.

This module provides functions for creating / writing / reading GeoTIFF/COG files
Some important notes about GeoTIFF:
 - only 1 nodata can be specified per file, also for multiband layers
 - only 1 dtype is allowed in a multiband
 - only 1 'unit' is allowed in a multiband
 - this means that multiband data has to host data of the same type!
 - probably some netcdf meta tags can be replaced by the georeference in geotiff. The question is which tags can be removed?
 -  grid_mapping=crs

 COG driver is available starting with GDAL 3.1.
"""

import os
import numpy as np
import rasterio
from rasterio.transform import from_origin
from rasterio.crs import CRS

from rio_cogeo.cogeo import cog_translate
from rio_cogeo.profiles import cog_profiles
from rio_cogeo.cogeo import cog_validate
import xarray as xr
import rioxarray as rio


class Georef():
    def __init__(self):
        self.transform = None
        self.crs = None
    def set_georef(self, epsg: int, west, north, xyresolution):
        self.epsg = epsg
        self.crs = CRS.from_epsg(self.epsg)

        self.west = west
        self.north = north
        self.xyresolution = xyresolution
        self.transform = from_origin(west, north, xyresolution, xyresolution)
        return

    def set_georef_by_file(self, infile):
        with rasterio.open(infile) as src:
            # set output profile based on masker (we are sure that the spatial stuff is ok!)
            profile = src.profile
            self.crs = src.crs
            self.transform = src.transform

def createGeoTIFF(outputPath, dtype,  georef : Georef, dimensions, nodata = None,
                  in_array = None,
                  bandsInfoLst = None, globalAttributes = None,
                  compress="ZSTD", blocksize=512,
                  close=True, predictor='2'):
    """Create a (empty)GeoTIFF. Data can be written immediately by this function, or can be written later(in_array=None) band by band to reduce memory consumption.
    The output can be a normal GeoTIFF or a COG, depending on the driver(COG, Gtiff) you choose.
    In contrast to a netcdf only 1 nodata and datatype can be chosen for a multiband
    Compression mode and blocksize are only used for when the GeoTIFF driver was selected

    Parameters
    ----------
    outputPath : str
        the output file path
    dtype : str or numpy dtype
        The data type for bands. For example: 'uint8' or
        ``rasterio.uint16``. Required in 'w' or 'w+' modes, it is
        ignored in 'r' or 'r+' modes.
    georef : Georef object
        The georef is defined by a crs and a geotransform.
    dimensions : (int,int,[int])
        the number of bands, the number of rows, number of columns and . If only 2 dimensions are available, it is a single band image
    nodata : int
        1 single value for each band that represents the nodata. It is not possible to have different nodata values
    bandsInfoLst : list of dict
        Metadata dictionary per band. The number of dictionaries must fit the number of bands. The dictionary will be flattend(just 1 level)
    globalAttributes : dict
        Global metadata. Only 1 level of key/values is allowed.
    in_array : numpy array
        (Optional), an array([z],x,y) can be provided to write immediately to the file
        the dimensions of the array should fit with the dimensions parameter. In this array is None, the tif will be
        generated without any (value)data
    close : bool
        True : close file after creation, the filename will be returned
        False : The file remains open, the file object will be returned

    compress : str
        Any compression algorithm that gdal support is allowed here. LZW or DEFLATE are very common.
    blocksize : int
        256 or 512 are common here

    Returns
    -------
    filename(for closed file) or file object(file remains open)
    """

    if len(dimensions) == 2:
        dimensions = tuple([1]) + dimensions     #add a new dimensions(1-band) to the tuple (5,20) => (1,5,20)
    elif len(dimensions) != 3:
        raise Exception("There is something wrong with the dimensions. It should be a tuple of 2 or 3 (%s)" % dimensions)

    nr_of_bands = dimensions[0]     #
    height = dimensions[1]
    width = dimensions[2]

    #cleanup tif if already present
    if os.path.exists(outputPath):
        os.remove(outputPath)

    #bandsInfoLst=cleanup_bandInfoLst(bandsInfoLst)  #flatten the dictionary structure
    my_tif = rasterio.open(outputPath, 'w', driver='GTiff',
                                    height=height, width=width,
                                    count=nr_of_bands,
                                    dtype=dtype,
                                    compress=compress,
                                    predictor=predictor,
                                    blockxsize=blocksize,
                                    blockysize=blocksize,
                                    tiled=True,
                                    nodata=nodata,
                                    crs=georef.crs,
                                    transform=georef.transform)

    if in_array is not None:
        # shape of in_array(if provided) must be the same as dimensions parameter
        if len(in_array.shape) == 2:
            in_array = np.array([in_array]) #create a 3D-array with 1 band

        in_dimensions = in_array.shape
        if in_dimensions[2] != width:
            raise Exception("Number of columns is different between dimensions and in_array")
        if in_dimensions[1] != height:
            raise Exception("Number of rows is different between dimensions and in_array")
        if in_dimensions[0] != nr_of_bands:
            raise Exception("Number of bands is different between dimensions and in_array")

        #write the numpy array to the file
        my_tif.write(in_array)  #write single or multiband data



    #write possible metadata to the file.
    updateMetadata(my_tif,
                   bandsInfoLst=bandsInfoLst, globalAttributes=globalAttributes,
                   clean_existing_meta=False)
    if close:
        my_tif.close()
        return outputPath
    else:
        return my_tif

def writeBandGtiff(outputPath, band_nr, in_array, bandinfo=None, clean_existing_meta=False):
    """Write array data to the specific band
    WARNING: when using with a compressed band ,this gives unexpected results resulting in a very large tiff file
    Parameters
    ----------
    outputPath  :str
        The path of the file to write
    band_nr : int
        The number of the band to add/update (1-based counting)
    in_array : numpy array
        The 2D-array to write to the file. The datatype should match with the type specified while creating the tif
    bandinfo: dict
        (Optional) a metadata dict for this band
    clean_existing_meta : bool
        False : keep the metadata for this band
        True : clean all existing metadata for this band before updating it with bandinfo

    Returns
    -------

    """
    if not os.path.exists(outputPath):
        raise Exception("Unable to write data. File does not exist!")

    #read some metadata and do some checks
    with rasterio.open(outputPath, 'r') as src:
        profile = src.profile

    # checks
    available_bands = profile['count']
    available_rows = profile['height']
    available_columns = profile['width']
    available_dtype = profile['dtype']
    in_type = in_array.dtype

    if in_type != available_dtype and not available_dtype in in_type.name:
        raise Exception("The defined GeoTIFF dtype(%s) is different than the one from the in_array (%s)" % (available_dtype, in_type))
    if band_nr > available_bands:
        raise Exception("index of band is invalid: %s > %s. This array is 1-based!" % (band_nr, available_bands))
    if len(in_array.shape) !=2:
        raise Exception("The shape of the input array is wrong. We expect a 2D-array! Your shape : %s" % in_array.shape)

    rows, columns = in_array.shape
    if (rows != available_rows) or (columns != available_columns):
        raise Exception("The shape of the array is different than the shape of the GeoTIFF: (%s,%s) vs %s" %(available_rows,available_columns, in_array.shape))

    with rasterio.open(outputPath, 'r+') as dst:  #mode=r+ allows us to update the file
        if bandinfo is not None:
            if clean_existing_meta:
                existing_tags = {}
            else:
                existing_tags = dst.tags(band_nr)
            existing_tags.update(bandinfo)
            dst.update_tags(band_nr, **existing_tags)  #update metadata

        dst.write(in_array, band_nr)     #update data

def cleanup_bandInfoLst(bandInfoLst):
    """Cleanup, rename tags and flatten the dictionary of the bandInfoLst

    Parameters
    ----------
    bandinfo: list of dict
        (Optional) a metadata dict for this band
    Returns
    -------
    bandInfo : list of dicts
        a cleaned/flattened/updated dictionary which can be used by tifs
    """

    # flatten a nested dict
    flattend_bandInfoLst = []

    for bandInfo in bandInfoLst:
        new_dict = {}
        for key, value in bandInfo.items():

            if isinstance(value, dict):
                for key, value in value.items():
                    new_dict[key] = value
            else:
                new_dict[key] = value

        #change netcdf keys to GeoTIFF keys
        if 'scale_factor' in new_dict:
            new_dict['scale'] = new_dict.pop('scale_factor')
        if 'add_offset' in new_dict:
            new_dict['offset'] = new_dict.pop('add_offset')
        if 'fillValue' in new_dict:
            new_dict['nodata'] = new_dict.pop('fillValue')
        if '_fillValue' in new_dict:
            new_dict['nodata'] = new_dict.pop('_fillValue')
        if '_FillValue' in new_dict:
            new_dict['nodata'] = new_dict.pop('_FillValue')
        if 'dataType' in new_dict:
            #new_dict['dtype'] = new_dict.pop('dataType')
            new_dict.pop('dataType')    #remove because it should be set on global level

        flattend_bandInfoLst.append(new_dict)
    return flattend_bandInfoLst

def updateMetadata(outputPath, bandsInfoLst=None, globalAttributes=None, clean_existing_meta=False):
    """
    Update the global metadata and the metadata per band if provided
    Before updating the metadata, it will be cleaned and flattened.
    By cleaned we mean that tags will be replaced by a common tag, known by GDAL (_FillValue => nodata, scale_factor =>scale)
    Flattened means only 1 hierarchy level of a dictionary can be printed in the metadata. Nested dicts in the metadata will be moved up to the highest level.

    Parameters
    ----------
    outputPath : str or file object
        str : The output file path
        file object : the opened file
    bandsInfoLst : list of dict (optional)
        List of band information dictionaries. Each dictionary can have the following keys:
        * 'description' : (str) a description of the bands
        * 'units':      (str) the unit of the band
        * 'name':       (str) the name of the variable
        * 'scale' :     float/int
        * 'offset' :    float/int

       The variable attributes in a netcdf can have the following keys, where any unused attributed can be omited or set to False (boolean):
       * 'standard_name' : (str) CF-1.6 compliant name, omit if not listed
       * 'long_name':      (str) long name
       * 'scale_factor':   (float) omit if not used
       * 'add_offset':     (float) omit if not used
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
    clean_existing_meta : bool
        True : Clean all existing metadata tags before writing the new
        False(Default) : Keep existing metadata before updating

    """
    f_isopen=False
    if isinstance(outputPath, rasterio.io.DatasetWriterBase):
        f_isopen = True
    if bandsInfoLst is not None:
        if not isinstance(bandsInfoLst, list):
            bandsInfoLst = [bandsInfoLst]

        #convert typical netcdf tags to specific geotif tags (scale, offset)
        nodatas = []
        scales = []
        offsets = []
        descriptions = []
        bandsInfoLst = cleanup_bandInfoLst(bandsInfoLst)    #make tags uniform e.g : scale_factor=>scale

        #convert metatags in gdal compliant tags
        for bandnr, bandinfo in enumerate(bandsInfoLst, start=1):

            scale = bandinfo.get('scale', 1)   #if not exist, set scale to 1
            if 'scale' in bandinfo :
                del bandinfo['scale']    #remove tag to prevent having the same info in different tag names
            scales.append(scale)

            offset = bandinfo.get('offset', 0)   #if not exist, set offset to 0
            if 'offset' in bandinfo :
                del bandinfo['offset']  # remove tag to prevent having the same info in different tag names
            offsets.append(offset)

            #not working for nodata, only 1 value per file is possible using rasterio
            # nodata = bandinfo.get('NoData', None)  # if not exist, set offset to 0
            # if 'NoData' in bandinfo:
            #     del bandinfo['NoData']  # remove tag to prevent having the same info in different tag names
            # nodatas.append(nodata)

            description = bandinfo.get("description", None)
            if 'description' in bandinfo:
                del bandinfo['description']  # remove tag to prevent having the same info in different tag names
            descriptions.append(description)


    if f_isopen:
        #file is already open, just rename the file pointer
        dst = outputPath
    else:
        dst = rasterio.open(outputPath, 'r+')

    if globalAttributes is not None:
        if clean_existing_meta:
            existing_glo_attributes = {}
        else:
            existing_glo_attributes = dst.tags()
        existing_glo_attributes.update(globalAttributes)    #update existing tags with new ones
        dst.update_tags(**existing_glo_attributes)

    #update each band separately
    if bandsInfoLst is not None:
        for bandnr, bandinfo in enumerate(bandsInfoLst, start=1):
            if clean_existing_meta:
                existing_band_attributes = {}
            else:
                existing_band_attributes = dst.tags(bandnr)
            existing_band_attributes.update(bandinfo)   #update attributes for a single band
            dst.update_tags(bandnr, **existing_band_attributes)

        dst.descriptions = tuple(descriptions)
        dst.scales = tuple(scales)
        dst.offsets = tuple(offsets)

    #return the same as the input, an open file or a path to the file
    if f_isopen:
        return dst
    else:
        dst.close()
        return outputPath

def add_COG_overviews(infile, outfile, profile='zstd' ):
    """adding overviews without loosing COG-compliancy. Currently the infile will not be updated, a new file will be created

    Parameters
    ----------
    infile: str
        the path of the inputfile on which you need overviews
    outfile: str
        the path of the outputfile
    profile: str
        lzw(default), but other values are possible too. (check from rio_cogeo.profiles import cog_profiles)
    Returns
    -------

    """
    cog_translate(infile, outfile, cog_profiles.get(profile)) #TODO predictor????

def validate_cog(cogFile):
    """
        Validate Cloud Optimized Geotiff.

        This script is the rasterio equivalent of
        https://svn.osgeo.org/gdal/trunk/gdal/swig/python/samples/validate_cloud_optimized_geotiff.py

        Parameters
        ----------
        src_path: str or PathLike object
            A dataset path or URL. Will be opened in "r" mode.
        strict: bool
            Treat warnings as errors
        quiet: bool
            Remove standard outputs

        Returns
        -------
        is_valid: bool
            True is src_path is a valid COG.
        errors: list
            List of validation errors.
        warnings: list
            List of validation warnings.

        """

    return cog_validate(cogFile)

def convert_NC_to_COGs(nc_file, outDir, variable_lst, outfilepattern):
    """
        Validate Cloud Optimized Geotiff.

        This script is the rasterio equivalent of
        https://svn.osgeo.org/gdal/trunk/gdal/swig/python/samples/validate_cloud_optimized_geotiff.py

        Parameters
        ----------
        nc_file: str
            the netCDF file that needs to be converted to COG
        outDir: str
            The directory to write the COG files to
        variable_lst: lst of str
            All the variables from the netCDF that needs to be exported as COG
        outfilepattern : str
            the pattern of the cog filename
            <var> will be replaced by the variable in the variable_lst

        an example:
        print convert_NC_to_COGs('/data/S3/testdata/NDVI/output/cgl_NDVI300_202303110000_X18Y03_OLCI_V2.0.1.nc', '/tmp/', ['NDVI', 'NOBS', 'NDVI_unc', 'QFLAG'], 'cgl_NDVI300_202303110000_X18Y03_OLCI_V2.0.1_<var>.tif'
        ['cgl_NDVI300_202303110000_X18Y03_OLCI_V2.0.1_NDVI.tif','cgl_NDVI300_202303110000_X18Y03_OLCI_V2.0.1_NOBS.tif','cgl_NDVI300_202303110000_X18Y03_OLCI_V2.0.1_NDVI_unc.tif','cgl_NDVI300_202303110000_X18Y03_OLCI_V2.0.1_QFLAG.tif']
        gdalinfo on one of these files gives us the following info(metadata is included!):
            Driver: GTiff/GeoTIFF
            Files: cgl_NDVI300_202303110000_X18Y03_OLCI_V2.0.1_NOBS.tif
            Size is 3360, 3360
            Coordinate System is:
            GEOGCRS["WGS 84",
                DATUM["World Geodetic System 1984",
                    ELLIPSOID["WGS 84",6378137,298.257223563,
                        LENGTHUNIT["metre",1]]],
                PRIMEM["Greenwich",0,
                    ANGLEUNIT["degree",0.0174532925199433]],
                CS[ellipsoidal,2],
                    AXIS["geodetic latitude (Lat)",north,
                        ORDER[1],
                        ANGLEUNIT["degree",0.0174532925199433]],
                    AXIS["geodetic longitude (Lon)",east,
                        ORDER[2],
                        ANGLEUNIT["degree",0.0174532925199433]],
                ID["EPSG",4326]]
            Data axis to CRS axis mapping: 2,1
            Origin = (-0.001488095238100,55.001488095238095)
            Pixel Size = (0.002976190476200,-0.002976190476200)
            Metadata:
              AREA_OR_POINT=Area
              lat#axis=Y
              lat#DIMENSION_LABELS=lat
              lat#long_name=latitude
              lat#standard_name=latitude
              lat#units=degrees_north
              lat#_CoordinateAxisType=Lat
              lon#axis=X
              lon#DIMENSION_LABELS=lon
              lon#long_name=longitude
              lon#standard_name=longitude
              lon#units=degrees_east
              lon#_CoordinateAxisType=Lon
              standard_name=normalized_difference_vegetation_index number_of_observations
              valid_range=[ 0. 32.]
            Image Structure Metadata:
              COMPRESSION=LZW
              INTERLEAVE=BAND
              LAYOUT=COG
            Corner Coordinates:
            Upper Left  (  -0.0014881,  55.0014881) (  0d 0' 5.36"W, 55d 0' 5.36"N)
            Lower Left  (  -0.0014881,  45.0014881) (  0d 0' 5.36"W, 45d 0' 5.36"N)
            Upper Right (   9.9985119,  55.0014881) (  9d59'54.64"E, 55d 0' 5.36"N)
            Lower Right (   9.9985119,  45.0014881) (  9d59'54.64"E, 45d 0' 5.36"N)
            Center      (   4.9985119,  50.0014881) (  4d59'54.64"E, 50d 0' 5.36"N)
            Band 1 Block=512x512 Type=Byte, ColorInterp=Gray
              Description = NOBS
              NoData Value=255
        Returns
        -------
        cog_files : lst of str
            a list of all files(without outDir) that have been written

        """
    cog_files = []
    rds: xr.DataArray = rio.open_rasterio(
        filename=nc_file,
        mask_and_scale=False,
    )
    # Prevent creating overviews automatically
    cog_meta = {
        'overviews': None
    }
    for var in variable_lst:
        # Save output to a regular GeoTIFF
        ds = rds[var]
        fname = outfilepattern.replace("<var>", var)
        outfile = os.path.join(outDir, fname)
        ds.rio.to_raster(raster_path=outfile, driver='COG', **cog_meta)
        cog_files.append(fname)
    return cog_files