'''
Created on Oct 27, 2023

@author: demunckd
'''

from enum import Enum


class Platform(Enum):
    PROBAV    = 'probav'
    SENTINEL3 = 'sen3'
class DB_platform(Enum):
    PROBAV      = 1
    S3A         = 2
    S3B         = 3
    S3          = 4    #S3 A+B

class DB_sensor(Enum):
    OLCI               = 1
    SLSTR              = 2
    OLCI_SLSTR         = 3
class SensorAbbr(Enum):
    PROBAV = 'PBV'
    SEN3   = 'S3'
    S3A    = 'S3A'
    S3B    = 'S3B'
    OLCI   = 'OLCI'
    
    def to_platform(self):
        if self == SensorAbbr.PROBAV:
            return Platform.PROBAV
        return Platform.SENTINEL3



#no _ or - here please - to allow for parsing
class ProductType(Enum):
    TOA         = 'TOA'
    IDEPIX      = 'IDEPIX'
    TOCR       = 'TOCR'
    GEO         = 'GEO'
    TOC         = 'TOC'
    BA300       = 'BA300'
    NDVI300     = 'NDVI300'
    LAI300      = 'LAI300'
    FCOVER300   = 'FCOVER300'
    FAPAR300    = 'FAPAR300'
    DMP300      = 'DMP300'
    GMP300      = 'GMP300'
    NPP300      = 'NPP300'
    GPP300      = 'GPP300'
    MAX1        = 'MAX1'
    MAX10       = 'MAX10'
    PREVEBF     = 'PREVEBF'

class Subtype(Enum):
    """
    FRAME = 'FRAME'
    S1 = 'S1'
    S10 = 'S10'
    M1 = 'M1'
    M10 = 'M10'
    GFC = 'GFC'
    """
    QL = 'QL'

class Timeliness(Enum):
    NRT = 'NRT'
    NTC = 'NTC'

class Consolidation(Enum):
    RT0 = 'RT0'
    RT1 = 'RT1'
    RT2 = 'RT2'
    RT6 = 'RT6'

class Periodicity(Enum):
    FRAME = 0
    DAILY = 1
    DEKAD = 10
    MONTHLY = 30
    YEARLY = 365

class AncillaryDataInputCategory(Enum):
    CLIMATE =  'climato'
    AF      = 'activefire'
    DEM     = 'dem'
    LAND    = 'landmask'
    LUE     = 'land.use.efficiency'
    WB      = 'waterbodies'
    WFS     = 'workflow.specific'
    MISSING = 'missing.tiles'

class AncillaryDataSourceName(Enum):
    CAMS_NRT_SURF   = 'cams.nrt.surface.ext'
    METEOC          = 'meteoconsult'                        #climato
    AEROSOL         = 'aer.extinction.monthly'              #climato/merra
    PRESSURE        = 'surf.press.water.vapor.monthly'   #climato/merra
    VIIRS_NRT       = 'nrt'                                 #AF/VIIRS  shp_nrt  txt/nrt
    VIIRS_NTC       = 'ntc'                                 #AF/VIIRS  shp_ntc  txt/archive
    USGS            = 'usgs'                                 #dem
    CCI             = 'cci'                                 # LAND = same as landcover/cci/tiles and WB
    OLCI            = 'esa.olci.sc.adf'                     # LAND
    GAUL            = 'gaul'                                # LAND still used? previously used in BAV1 / GEO, now esa_olci landmask is used
    JRC             = 'jrc'                                 # LAND still used? BAV1
    PRIOR           = 'brdf.pror'                           # WFS NDVI300
    EBFNOEBF        = 'ebf.noebf'                           # WFS/s3_geo/ebf_noebf for NRT  #WFS/reproc/s3_geo/ebf_noebf for reprocessing
    PREVEBF         = 'prevebf'                             # WFS/s3_geo/prevebf for NRT    #WFS/reproc/s3_geo/prevebf for reprocessing
    NDVI300         = 's3.ndvi3'                            # MISSING
    GEO300          = 's3.geo'                              # MISSING
    BA300           = 's3.bav3'                             # MISSING

class FileTypeExtension(Enum):
    NC = 'nc'
    TIFF = 'tiff'
    PNG = 'png'     # wordt gemaakt tijdens globale mosaic. Kleiner dan tiff -  doel: gebruik in dashboard
    H5 = 'h5'       # momenteel nog veel intermediate data in hdf5 formaat ...
    NPY = 'npy'     # subtiles GEO kan mss aangepast worden naar npy.npz
    NPZ = 'npy.npz'     #subtiles GEO - compressed numpy
    JSON = 'json'   # brdf intermediate
    TXT = 'txt'

class DB_status(Enum):
    FAILED = -1
    EXPECTED = 0
    AVAILABLE = 1
    ONHOLD = 2
    PROCESSING = 8
    PROCESSED = 9
    OBSOLETE = 10
    EMPTY = 99

class DB_product_type(Enum):
    OLCI_L1B    = 1
    SLSTR_L1B   = 2
    OLCI_IDEPIX = 3
    TOA_FRAME   = 4
    TOA_TILE    = 5
    TOC         = 6
    CAMS_NRT    = 7
    CAMS_NTC    = 8
    NDVI        = 10
    GEO_DAY     = 11
    LAI300      = 12
    FAPAR300    = 13
    FCOVER300   = 14
    GEO_PREVEBF = 15
    TEST_PRODUCT = 9999
