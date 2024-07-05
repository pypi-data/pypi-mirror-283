'''
Created on Mar 16, 2024

@author: demunckd
'''
from cgls_cpe.config.configuration import Configuration
from cgls_cpe.logging import log
from cgls_cpe.db_api import DB_product, DatabaseConnection
from cgls_cpe.config.model.enums import DB_status, ProductType, DB_product_type,\
    DB_sensor, DB_platform
from cgls_cpe.common.products import splitS3ProductName
import os
logger = log.logger()


updaters = {}

def get_cached_updater(producttype:str, DB):
    try:
        updater = updaters[producttype]
    except:
        if  producttype == ProductType.TOA.value:
            updaters[producttype] = ToaFrameUpdater([])
        else:
            updaters[producttype] = Updater([])
        updater = updaters[producttype]       
    
    updater.DB = DB
    return updater

def get_fixed_values(record_fields):
        db_id = int(record_fields[0])  # DB id number
        return_status = int(record_fields[1])  # 0 is OK, all others are failed
        runtime = record_fields[2]  # runtime in s, or None if not applicable
        if runtime is not None and runtime.upper() != 'NONE':
            runtime = int(runtime)
        else:
            runtime = None
        
        sparkApplicationId = record_fields[3]
        podName = record_fields[4]
        log_id = sparkApplicationId + '|' + podName
        return db_id,return_status,runtime, log_id 

class Updater():
    def __init__(self, records, delimiter='|', dry_run=False):
        self.dry_run = dry_run
        self.delimiter = delimiter
        self.records = records
        self.DB = None

    def _process_all_records(self):
        for record in self.records:
            record = record.strip()
            if len(record) == 0:
                logger.warn("Skipping empty line in result file")
                continue
            try:
                record_fields = record.split(self.delimiter)
                self.process_record(record_fields)

            except:
                logger.exception("Got error")
                raise Exception("Unable to parse line from resultfile: %s " % record)
            
    def run_and_commit_all(self):
        db_settings = Configuration().get_database()
        self.DB = DatabaseConnection(db_settings.get_connection_string())
        self._process_all_records()
        self.DB.commit()
        self.DB.close()       
        
             
    def process_record(self,record_fields):
        logger.debug('Default process_record {}'.format(record_fields))
        if len(record_fields) < 6:
            raise Exception("Parsing failed. Expected 5 values, is %s (%s)" % (len(record_fields), record_fields))
        db_id,return_status,runtime, log_id =get_fixed_values(record_fields)
        try:
            location = record_fields[5]  # location on s3
        except:
            logger.debug("Using empty location")
            location = ''
        
        
        # status
        if return_status == 0:
            db_status = DB_status.PROCESSED.value
        elif return_status == 99:
            db_status = DB_status.EMPTY.value
        else:
            db_status = DB_status.FAILED.value
        
        if self.dry_run:
            logger.info("Not updating DB, it is a dry_run")
        else:
            #we need to check the status of the product before we can update this
            old_status = self.DB.get_status_by_id(db_id)
            if old_status == DB_status.PROCESSING.value:
                self.DB.update_by_id(db_id, location=location, statusid=db_status, runtime=runtime, logid=log_id, commit=False)
            else:
                logger.info("Not updating since state not processing")
            
            
            
class ToaFrameUpdater(Updater):
    def __init__(self, records, dry_run=False):
        super().__init__(records, dry_run=dry_run)
    
    def process_record(self, record_fields):

        db_id,return_status,runtime, log_id =get_fixed_values(record_fields)
        # TOA FRAME
        if record_fields[5] == 'TOA_FRAME' or len(record_fields) < 7:
            
            if not self.dry_run: #don't update DB when it is a dry_run
                if return_status == 0:
                    self.DB.update_status_by_id(db_id, DB_status.PROCESSED.value, old_status_lst=[DB_status.PROCESSING.value], runtime_lst=runtime, logid=log_id, commit=False)  # only update values that have status PROCESSING
                else:
                    self.DB.update_status_by_id(db_id, DB_status.FAILED.value,old_status_lst=[DB_status.PROCESSING.value], commit=False, logid=log_id)  # alwasy set to FAILED

        # TOA TILE
        else:
            # we need to add/update this to the DB
            # e.g TOA_TILE|X31Y14|0|S3A_OL_1_EFR____20240226T215923_20240226T220223_20240226T232139_0179_109_257_4140_PS1_O_NR_003.SEN3_TOA|210|s3://stag-sen3-TOA-0-v1.0.0-2024-02/stag/sen3/TOA/0/v1.0.0/2024/02/20240226/cgl_TOA_20240226215923__S3A_v1.0.0.tiff/cgs_TOA_20240226215923_X31Y14_S3A_1.0.0.nc
            db_id = None
            roi = record_fields[6]#5 entries
            return_status = int(record_fields[7])
            toa_frame_product_name = record_fields[8]
            runtime = record_fields[9]
            location = record_fields[10]
            S3parts = splitS3ProductName(toa_frame_product_name.replace("_TOA",''))   #replace the _TOA suffix to get the full OLCI filename
            if runtime is not None:
                runtime = int(runtime)
            tile_product_name = os.path.basename(location).replace("cgs_","").replace(".nc",'') #remove prefix and file extention
            product_version = tile_product_name.split('_')[-1]

            # status
            if return_status == 0:
                db_status = DB_status.PROCESSED.value
            elif return_status == 99:
                #skip empty tiles
                return
            elif return_status == -1:
                db_status = DB_status.FAILED.value
                location = ''
            else:
                logger.exception("Return status is invalid : %s" % return_status)


            # check if the tile is already available in the DB
            toa_tile_product = self.DB.get_product_by_name(tile_product_name)
            new = False
            if toa_tile_product is None:
                new = True         #this is a new product, not yet in the DB
                toa_tile_product = DB_product(tile_product_name, db_status,
                                                DB_product_type.TOA_TILE.value,
                                                product_version,
                                                S3parts['sensingStartTime'],
                                                roi=roi,
                                                periodenddate=S3parts['sensingStopTime'],
                                                periodicity=0, periodnumber=0, consolidation=0, platformid=DB_platform[S3parts['mission']].value,
                                                sensorid=DB_sensor.OLCI_SLSTR.value,
                                                accumulationenddate=S3parts['sensingStopTime'],
                                                accumulationstartdate=S3parts['sensingStartTime'],
                                                testing=False,
                                                location=location,
                                                logid=log_id,
                                                )
                if not self.dry_run:
                    product_id = self.DB.add_product(toa_tile_product, commit=False)
                else:
                    logger.info("It's a dry_run, DON'T add the product (%s) to the DB" % toa_tile_product.name)

            else:
                #product already in DB
                product_id = toa_tile_product.id


            if not self.dry_run:
                #self.DB.update_status_by_id(product_id, db_status, old_status_lst=[], runtime=runtime)
                if not new: #if the product is new, the location was already updated with the insert, so we could skip this
                    self.DB.update_by_id(product_id, location=location, statusid=db_status, runtime=runtime, logid=log_id, commit=False)

                #add all other tiles products to the DB in status EXPECTED/ONHOLD
                #self._update_downstream_products(toa_tile_product)
            else:
                logger.info("It's a dry_run, DON'T update the DB")
