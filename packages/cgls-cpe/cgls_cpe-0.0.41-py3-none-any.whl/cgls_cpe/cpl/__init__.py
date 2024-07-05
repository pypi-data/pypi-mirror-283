"""Common Python Library 3rd generation

:module: cpl
:author: Vito - Tap Geomatic Global land IT <gmgit@vito.be>
:copyright: 2022 - vito

"""
__version__ = '0.0.1'

from cgls_cpe.cpl.grid import CglS3Grid, PBV300Grid
from cgls_cpe.cpl.product import Product
from cgls_cpe.cpl.transfer import ftpPull, sftpPull
from cgls_cpe.cpl import date_time as date_time
from cgls_cpe.cpl.netcdf import createLatLonNetCDF, writeBandNc, loadPropNc, loadValNc, createOutputNc
from cgls_cpe.cpl.geotiff import createGeoTIFF, writeBandGtiff, cleanup_bandInfoLst, updateMetadata,add_COG_overviews, validate_cog, convert_NC_to_COGs