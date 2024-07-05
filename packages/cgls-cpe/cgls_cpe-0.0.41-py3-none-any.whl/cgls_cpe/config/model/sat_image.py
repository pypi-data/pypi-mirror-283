'''
Created on Nov 19, 2023

@author: demunckd
'''
from datetime import datetime
import os
from cgls_cpe.config.model.timestamp import Timestamp
from cgls_cpe.config.model.enums import ProductType, Subtype, SensorAbbr,\
    FileTypeExtension, Periodicity, Consolidation, Timeliness
from cgls_cpe.config.model.subtypes import Subtypes
from cgls_cpe.config.model.area import Area
from cgls_cpe.config.model.version import Version
from cgls_cpe.config.model.data_object import DataObject
from cgls_cpe.common.products import splitCGLS3ProductName

class SatImage(DataObject):

    def __init__(self, prodType:ProductType, subtypes:Subtypes, periodicity:Periodicity, timestamp:Timestamp, 
                 area:Area, sensor:SensorAbbr, version:Version, ext:FileTypeExtension, 
                 conso:Consolidation=None, timeliness:Timeliness=None, is_dissemination=False, band_group:str=None):
        
        # AI Generated -by using following query:
        # Can you generate in python dynamic isinstance checks for these parameters and throw an error on failure: prodType:ProductType, subtypes:Subtypes, timestamp:Timestamp, area:Area, sensor:SensorAbbr, version:Version, ext:FileTypeExtension ?
        if not isinstance(prodType, ProductType):
            raise TypeError("prodType must be a ProductType object")
        if not isinstance(periodicity, Periodicity):
            raise TypeError("periodicity must be a Periodicity object")
        if subtypes is not None and not isinstance(subtypes, Subtypes):
            raise TypeError("subtypes must be a Subtypes object")
        if not isinstance(timestamp, Timestamp):
            raise TypeError("timestamp must be a Timestamp object")
        if area is not None and not isinstance(area, Area):
            raise TypeError("area must be an Area object")
        if not isinstance(sensor, SensorAbbr):
            raise TypeError("sensor must be a SensorAbbr object")
        if not isinstance(version, Version):
            raise TypeError("version must be a Version object")
        if not isinstance(ext, FileTypeExtension):
            raise TypeError("ext must be a FileTypeExtension object")
        if conso is not None and not isinstance(conso, Consolidation):
            raise TypeError("conso must be a Consolidation object")
        if timeliness is not None and not isinstance(timeliness, Timeliness):
            raise TypeError("timeliness must be a Timeliness object")
        
        # If no error is raised, return True
        
        self.prodType = prodType
        self.periodicity = periodicity
        self.subtypes = subtypes
        self.timestamp = timestamp
        self.area = area
        self.sensor = sensor
        self.version = version
        self.ext = ext
        self.conso = conso
        self.timeliness = timeliness
        self.is_dissemination = is_dissemination
        self.band_group = band_group
        self.__do_extra_imports()
        
        #will check valid bucket name
        self.get_container_suffix()
        
    
    @staticmethod
    def create_from_filename(fname, prodType:ProductType=None, subtypes:Subtypes=None, periodicity:Periodicity=None, timestamp:Timestamp=None, 
                 area:Area=None, sensor:SensorAbbr=None, version:Version=None, ext:FileTypeExtension=None, 
                 conso:Consolidation=None, timeliness:Timeliness=None, is_dissemination=False, band_group:str=None):
        '''
        create_from_filename creates setImage with same filename elements as available in the filenamefrom filename
        
        method can also be used to derive e.g. TOC filename from TOA filename, and overrule some elements from filename
        '''
        cgl_dict = splitCGLS3ProductName(fname)
        if prodType == None:
            if cgl_dict['product'] in ProductType.__members__:
                prodType = ProductType(cgl_dict['product'])
        if subtypes == None:
            if cgl_dict['subtype'] in Subtype.__members__:
                subtypes = Subtypes(cgl_dict['subtype'])
        if timeliness == None:
            if cgl_dict['subtype'] in Timeliness.__members__:
                subtypes = Timeliness(cgl_dict['subtype'])
        if conso == None:
            if cgl_dict['subtype'] in Consolidation.__members__:
                conso = Consolidation(cgl_dict['subtype'])
        if timestamp == None:
            time      = cgl_dict['time']
            timestamp = Timestamp(year=time[:4], month=time[4:6], day=time[6:8], 
                                hour=time[8:10], minutes=time[10:12], seconds=time[12:14])
        if area == None:
            area = Area(cgl_dict['area'])
        if sensor == None:
            if cgl_dict['sensor'] in SensorAbbr.__members__:
                sensor = SensorAbbr(cgl_dict['sensor'])
        if version == None: 
            version = Version(cgl_dict['verMajor'],cgl_dict['verMinor'],cgl_dict['verRev'],cgl_dict['rc'])
        if ext == None:
            ext_ = os.path.splitext(fname)[1]
            if ext_ in FileTypeExtension.__members__:
                ext = FileTypeExtension(ext)
            
        image = SatImage(prodType = prodType, 
                         subtypes = subtypes, 
                         periodicity = periodicity, 
                         timestamp = timestamp, 
                         area = area, 
                         sensor = sensor, 
                         version = version, 
                         ext = ext,
                         conso = conso,
                         timeliness = timeliness,
                         band_group = band_group)
        
        return image
    
    def __str__(self):
        return self.get_value()
    
    # Define getter methods for each attribute
    def get_product_type(self)-> ProductType:
        return self.prodType
    
    def get_periodicity(self)-> Periodicity:
        return self.periodicity

    def get_subtypes(self) -> Subtypes:
        return self.subtypes

    def get_timestamp(self) -> Timestamp:
        return self.timestamp

    def get_area(self) -> Area:
        return self.area

    def get_sensor(self) -> SensorAbbr:
        return self.sensor

    def get_version(self) -> Version:
        return self.version

    def get_ext(self) -> FileTypeExtension:
        return self.ext
    
    def get_conso(self) -> Consolidation:
        return self.conso
    
    def get_timeliness(self) -> Timeliness:
        return self.timeliness

    def __do_extra_imports(self):
        #to avoid circular imports
        from cgls_cpe.config.configuration import Configuration
        self.config = Configuration()

    def set_dissemination(self, value):
        self.is_dissemination = value          
    
    #based on https://confluence.vito.be/pages/viewpage.action?pageId=72548398
    #see also functions here: https://git.vito.be/projects/GEOM/repos/pl_s3-preproc_cgl/browse/step_all/scripts/fnc_s3_preproc_common.py
    
    def get_objectname(self):
        if self.is_dissemination:
            prefix = self.config.get_dissemenation_prefix()
        else:
            prefix = self.config.get_proj_abbrev()
        
        prod_string = self.prodType.value
        if  self.conso is not None:
            prod_string += '-' + self.conso.value 
        if  self.timeliness is not None:
            prod_string += '-' + self.timeliness.value 
        if  self.subtypes is not None:
            prod_string += '-' + self.subtypes.get_value() 
        return  '_'.join([prefix, prod_string, self.timestamp.get_value(), \
                self.area.get_value(), self.sensor.value, self.version.get_value()])
    
    def get_filename(self):
        objectname = '_'.join(self.get_objectname().split('_')[:-1])
        band_version_part = self.version.get_value()
        if self.band_group is not None:
            band_version_part = self.band_group + "_" +  self.version.get_value()
        return  '_'.join([objectname, band_version_part]) +\
                '.' + self.ext.value
                
    def get_container_suffix(self):
        platform = self.get_sensor().to_platform()
        return  self.config.get_storage().get_remote_container(platform, self.get_product_type(), self.get_periodicity() , \
                                             self.get_version(),
                                             self.get_timestamp().get_year(),
                                             self.get_timestamp().get_month()
                                             )
    
    def get_key_suffix(self):
        key_suffix = os.path.join(self.get_timestamp().get_date_short(), self.get_objectname(), self.get_filename())
        return  key_suffix
    
    
