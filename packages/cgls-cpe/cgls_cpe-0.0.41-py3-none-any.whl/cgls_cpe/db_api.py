# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import psycopg2
import psycopg2.extras
import json

from cgls_cpe.config.configuration import Configuration
from cgls_cpe.logging import log
logger = log.logger()


class DB_product:
    def __init__(self, name:str, statusid:int, typeid:int, productversion:str, periodstartdate:datetime, id:int=None,
               processinglevel:str=None, periodicity:int=None, periodnumber:int=None, periodenddate:datetime=None, consolidation:int=None,
               roi:str=None, platformid:int=None, sensorid:int=None,accumulationstartdate:datetime=None, accumulationenddate:datetime=None,
               location:str=None, comment:str=None, testing:bool=False, creationdate:datetime=None, modificationdate:datetime=None,
               geometry=None, stats:'Stats'=None, logid=None):
        self.id = id
        self.name = name
        self.statusid = statusid
        self.typeid = typeid
        self.productversion = productversion
        self.periodstartdate  = periodstartdate
        self.processinglevel = processinglevel
        self.periodicity = periodicity
        self.periodnumber = periodnumber
        self.periodenddate = periodenddate
        self.consolidation = consolidation
        self.roi = roi
        self.platformid = platformid
        self.sensorid = sensorid
        self.accumulationstartdate = accumulationstartdate
        self.accumulationenddate = accumulationenddate
        self.location = location
        self.comment = comment
        self.creationdate = creationdate
        self.modificationdate = modificationdate
        self.testing = testing
        self.logid = logid
        self.geometry = geometry
        self.stats = stats

class Stats:
    def __init__(self, filesize_MB=None, cloud_cover=None, invalid_cover=None, land_cover=None, bbox=None):
        self.filesize_MB = filesize_MB
        self.cloud_cover = cloud_cover
        self.invalid_cover = invalid_cover
        self.land_cover = land_cover
        self.bbox = bbox
        self.top = None
        self.left = None
        self.bottom = None
        self.right = None
        if self.bbox is not None:
            try:
                self.top = round(bbox[0], 2)
                self.left = round(bbox[1], 2)
                self.bottom = round(bbox[2], 2)
                self.right = round(bbox[3], 2)
            except:
                logger.exception("Unable to parse bbox")

class DatabaseConnection:

    def __init__(self, inConnectionString=None):
        db_settings = Configuration().get_database()
        if inConnectionString is None:
            inConnectionString=db_settings.get_connection_string()
        
        #mask the password in connectionstring
        masked_connection_str = inConnectionString.split("password=")
        masked_connection_str = masked_connection_str[0] + 'password=' + masked_connection_str[1][
                                                             0:2] + "***'"  # remove the password(only show first char) when printing error
        try:
            self.conn = psycopg2.connect(inConnectionString)
            
            logger.debug("Connected with %s" % masked_connection_str)
        except Exception as exc:
            
            logger.exception("I am unable to connect to the database using string %s : %s" %( masked_connection_str, str(exc)))    #remove the password
            #raise Exception()
            raise Exception("I am unable to connect to the database using string %s : %s" % (masked_connection_str, str(exc)))

    def doQuery(self, query, query_data=(), close_connection=True):
        with self.conn.cursor() as curs:   # TODO : does it(dict) has an impact on performance
            try:
                curs.execute(query, query_data)
            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(error)
            result = curs.fetchall()

        self.conn.commit()
        if close_connection:
            self.conn.close()
        return result

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()
    def add_multiple_products(self, product_lst:list[DB_product], close_connection=True):
        product_id_lst = []
        #add multiple products in one commit
        for product in product_lst:
            product_id = self.add_product(product, commit=False)    #commit all added products in a single command later on.
            product_id_lst.append(product_id)
        self.commit()
        if close_connection:
            self.close()
        return product_id_lst



    def add_product(self, product:DB_product, commit:bool=True, close_connection=False):
        query = 'INSERT INTO products( ' \
                 'id, name, statusid, typeid, productversion, processinglevel, periodicity, periodnumber, ' \
                 'periodstartdate, periodenddate, consolidation, roi, platformid, sensorid, creationdate, ' \
                 'modificationdate, accumulationstartdate, accumulationenddate, location, comment, testing)' \
                 "VALUES (NEXTVAL('products_seq'), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, current_timestamp, current_timestamp, %s, %s, %s, %s, %s) RETURNING id;"
        # creationdate =datetime.now()
        # modificationdate=datetime.now()
        p = product
        query_data = (p.name, p.statusid, p.typeid, p.productversion, p.processinglevel,
                      p.periodicity, p.periodnumber, p.periodstartdate, p.periodenddate, p.consolidation,
                      p.roi, p.platformid, p.sensorid, p.accumulationstartdate, p.accumulationenddate, p.location,
                      p.comment, p.testing)
        with self.conn.cursor() as curs:   # TODO : does it(dict) has an impact on performance
            try:
                curs.execute(query, query_data)
                product_id = curs.fetchone()[0]
                self.add_processing_history(product_id,  p.statusid, datetime.now(), runtime=None, logid=p.logid)
                if p.geometry is not None:
                    query = "INSERT INTO geometries(id, geometry) VALUES (%s,ST_SetSRID(ST_GeomFromText(%s), 4326))"
                    query_data = (product_id, p.geometry.wkt)
                    curs.execute(query, query_data)
                if p.stats is not None:
                    query = "INSERT INTO stats(productid, filesize_MB, cloud_cover,invalid_cover, land_cover, xleft, bottom, xright, top) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    query_data = (product_id, p.stats.filesize_MB, p.stats.cloud_cover, p.stats.invalid_cover, p.stats.land_cover, p.stats.left, p.stats.bottom, p.stats.right, p.stats.top)
                    curs.execute(query, query_data)
            except (Exception, psycopg2.DatabaseError) as error:
                logger.exception(error)
                product_id = None

        if commit:
            self.conn.commit()
        if close_connection:
            self.conn.close()
        return product_id

    def add_stats(self,product_id:int, stats:'Stats'):
        with self.conn.cursor() as curs:
            query = "INSERT INTO stats(productid, filesize_MB, cloud_cover,invalid_cover, land_cover, xleft, bottom, xright, top) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (productid) DO NOTHING"
            query_data = (product_id, stats.filesize_MB, stats.cloud_cover, stats.invalid_cover, stats.land_cover, stats.left, stats.bottom, stats.right, stats.top)
            logger.debug("About to execute query [%s]" % query)
            curs.execute(query, query_data)
            logger.debug(curs.statusmessage)

    def add_processing_history(self,product_id:int, new_status:int, now:datetime, runtime:int=None, logid=None):
        with self.conn.cursor() as curs:
            query = "INSERT INTO processinghistory ( id, productid, statusid, executiondate, runtime, logid ) VALUES (NEXTVAL('processinghistory_seq'), %s, %s, %s, %s, %s )"
            query_data = (product_id, new_status, now, runtime, logid)
            logger.debug("About to execute query [%s]" % query)
            curs.execute(query, query_data)
            logger.debug(curs.statusmessage)

    def update_by_id(self, product_id:int, startdate:datetime=None, enddate:datetime=None, statusid:int=None,
                     version:str=None, platformid:int=None, sensorid:int=None, roi:str=None, consolidation:int=None,
                     periodicity:int=None, location:str=None, runtime=None, logid=None,
                     close_connection=False, commit=True):
        curs = self.conn.cursor()
        update_statement = "UPDATE products SET "
        update_fields = []

        if startdate is not None:
            update_fields.append("periodstartdate=%s" % startdate)
        if enddate is not None:
            update_fields.append("periodenddate=%s" % enddate)
        if version is not None:
            update_fields.append("productversion = '%s'" % version)
        if platformid is not None:
            update_fields.append('platformid = %s' % platformid)
        if sensorid is not None:
            update_fields.append('sensorid = %s' % sensorid)
        if roi is not None:
            update_fields.append("roi = '%s'" % roi)
        if consolidation is not None:
            update_fields.append('consolidation=%s' % consolidation)
        if periodicity is not None:
            update_fields.append('periodicity=%s' % periodicity)
        if location is not None:
            update_fields.append("location='%s'" % location)
        if statusid is not None:
            update_fields.append("statusid=%s" % statusid)

        where_statement = " WHERE id=%s " % (product_id)
        query = update_statement + ', '.join(update_fields) + where_statement #building query string
        logger.debug(query)
        curs.execute(query)
        logger.debug(curs.statusmessage)

        if not statusid is None:
            now = datetime.now()
            self.add_processing_history(product_id, statusid, now, runtime, logid=logid)
        curs.close()
        if commit==True:
            self.conn.commit()
        if close_connection:
            self.conn.close()

    def update_status_by_id(self, product_id_lst:list[int], new_status:int, old_status_lst:list[int]=[],
                            runtime_lst:list[int]=None, logid:str=None, close_connection:bool=False, commit:bool=True):
        """Update the status in table products, add the history to the processinghistory table

        Parameters
        ----------
        product_id_lst: int
            The list of ids of the product
        new_status: int
            The new status of the product
        old_status_lst : [int,...,int]
            multiple statusses are possible, eg [0, ], by default([]) it is empty. So old_status is not taken into account

        runtime_lst : list[int], optional
            The number of seconds the algorithm was running
        logid : str, optional
            Extra info about the processinginfo
        close_connection : bool, optional
            close the current database connection after executing this query. By default, the connectin remains open.


        Returns
        -------
        pg_rows : list of dicts
            all rows, formatted as a dict.
        """
        if not isinstance(product_id_lst, list):
            product_id_lst = [product_id_lst]
        if not isinstance(runtime_lst, list):
            runtime_lst = [runtime_lst]
        now = datetime.now()

        curs = self.conn.cursor()

        for idx, product_id in enumerate(product_id_lst):
            #only if old_status is needed
            old_status = None
            if idx < len(runtime_lst): #if there is a runtime_lst, use it. Else it is empty
                runtime = runtime_lst[idx]
            else:
                runtime=None
            if len(old_status_lst) > 0:
                #we need to check the status of the product before we can update this
                old_status = self.get_status_by_id(product_id)

            if (old_status in old_status_lst) or (old_status is None):
                # query_data = (product_id, new_status, now, runtime)
                # logger.debug("About to execute query [%s]" % query)
                # curs.execute(query, query_data)

                self.add_processing_history(product_id, new_status, now, runtime, logid=logid)

                query = "UPDATE products SET statusid=%s where id=%s" % (new_status, product_id)
                curs.execute(query)
                logger.debug(curs.statusmessage)

        curs.close()
        if commit:
            self.conn.commit()
        if close_connection:
            self.conn.close()

    def update_status_by_name(self, product_name:str, new_status:int, old_status:int=None, runtime:int=None, close_connection:bool=False, commit:bool=True):
        """Update products with status ONHOLD to EXPECTED by name

        Parameters
        ----------
        product_name: str
            the name of the product

        new_status : int
            the new status id
        old_status : int
            the old status id. If this status doesn't match with the product current status. The update will be skipped.
            by default(None). The old status will be taken into account
        runtime : int
            the number of seconds the process was running(default=None)
        close_connection : bool, optional
            close the current database connection after executing this query. By default, the connectin remains open.

        Returns
        -------
        product_id : int
        """

        now = datetime.now()
        curs = self.conn.cursor()
        product = self.get_product_by_name(product_name)
        if product is None:
            return None

        if (product.statusid == old_status) or (old_status is None):
            logger.debug("Product with id=%s and name=%s has status %s, changing this to %s" % (product.id, product_name, old_status, new_status))
            # query = "INSERT INTO processinghistory ( id, productid, statusid, executiondate, runtime ) VALUES (NEXTVAL('processinghistory_seq'), %s, %s, %s, %s )"
            # query_data = (product_id, new_status , now, runtime)
            # logger.debug("About to execute query [%s]" % query)
            # curs.execute(query, query_data)
            self.add_processing_history(product.id, new_status, now, runtime)
            # logger.debug(curs.statusmessage)
            query = "UPDATE products SET statusid=%s where id=%s" % (new_status, product.id)
            curs.execute(query)
            logger.debug(curs.statusmessage)
        else:
            logger.debug("Product with id=%s and name=%s has status %s, NOT %s" % (product.id, product_name, product.statusid, old_status))

        curs.close()
        if commit:
            self.conn.commit()
        if close_connection:
            self.conn.close()
        return product.id

    def del_product(self, product_name:str, commit=True,  close_connection=False):
        query = "DELETE FROM products where name='%s'" % product_name
        with self.conn.cursor() as curs:   # TODO : does it(dict) has an impact on performance
            try:
                curs.execute(query)
                rows_deleted = curs.rowcount
            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(error)
                rows_deleted = 0

        if commit:
            self.conn.commit()
        if close_connection:
            self.conn.close()
        return rows_deleted

    def get_location_by_name(self, product_name:str):
        result = None

        query = "SELECT location FROM products WHERE name='%s'" % (product_name)

        logger.debug('get products by name : %s ' % query)
        with self.conn.cursor() as curs:
            try:
                curs.execute(query)
                result = curs.fetchone()[0]

            except (Exception, psycopg2.DatabaseError) as error:
                logger.exception(error)

        return result

    def get_product_by_name(self, product_name:str):
        id_lst = []
        result = None

        query = "SELECT * FROM products WHERE name='%s'" % (product_name)

        logger.debug('get products by name : %s ' % query)
        with self.conn.cursor() as curs:
            try:
                curs.execute(query)
                # pg_rows = curs.fetchall()
                # transform result
                columns = list(curs.description)
                result = curs.fetchall()

            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(error)


        #return as DB_product object

        results_as_DB_product = []
        for row in result:
            row_dict = {}
            for i, col in enumerate(columns):
                row_dict[col.name] = row[i]
            product = DB_product(**row_dict)
            results_as_DB_product.append(product)
        result = results_as_DB_product
        logger.debug('Returning %s records!' % len(result))

        if len(result) == 0:
            return None
        else:
            return result[0]

    def get_product_by_id(self, product_id:int):
        query = "SELECT * FROM products WHERE id=%s" % (product_id)

        logger.debug('get products by id : %s ' % query)
        with self.conn.cursor() as curs:
            try:
                curs.execute(query)
                # pg_rows = curs.fetchall()
                # transform result
                columns = list(curs.description)
                result = curs.fetchall()

            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(error)

        # make dict
        results_as_DB_product = []
        for row in result:
            row_dict = {}
            for i, col in enumerate(columns):
                row_dict[col.name] = row[i]
            product = DB_product(**row_dict)
            results_as_DB_product.append(product)
        return results_as_DB_product[0]


    def get_status_by_id(self, product_id:int):
        query = "SELECT statusid FROM products WHERE id=%s" % (product_id)

        logger.debug('get products by id : %s ' % query)
        with self.conn.cursor() as curs:
            try:
                curs.execute(query)
                # pg_rows = curs.fetchall()
                # transform result
                columns = list(curs.description)
                result = curs.fetchone()

            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(error)
            if result is not None:
                result = result[0]  # result is a tuple so only return first value
            return result

    def get_products(self, product_type:int, status_lst:int=None, startdate:datetime=None, enddate:datetime=None,
                     version:str=None, platformid:int=None, sensorid:int=None, roi:str=None, consolidation:int=None,
                     periodicity:int=None, location:str=None, limit:int=None):
        """get products from the database per product_type and status.
        Optionally, more filters can be provided for the query

        Parameters
        ----------
        product_type: int
            The id of the product type
        status_lst : list of int
            multiple statusses are possible, eg  [0,1]

        startdate  : datetime, optional
        enddate  : datetime, optional
        version :   str; optional
            the productversion
        platformid :    int, optional
            the id of the platform
        sensorid :  int, optional
            the id of the sensor
        roi :   str, optional
            the roi of the product, eg 'X01Y01', 'EUR', 'GLO'
        consolidation : int, optional
            the consolidation number, e.g 0 for nrt
        periodicity : int, optional
            the periodicity 0 : frame, 1 :daily, 10 : dekad, 365 : year
        limit : int, optional
            The max number of rows that should be returned



        Returns
        -------
        pg_rows : list of tuple
            all resulting rows.
        """

        query = "SELECT * FROM products WHERE typeid=%s" % (product_type)
        if status_lst is not None:
            id_lst = []
            if not isinstance(status_lst, list):  # convert possible str/int to [str]/[int]
                status_lst = [status_lst]
            status_ids_str = ','.join(map(str, status_lst))  # convert [1, 2, 5] to "1, 2, 5"
            query += " AND statusid in (%s)" % status_ids_str
        if startdate is not None and enddate is not None:
            #incr_enddate = datetime.strptime(enddate, '%Y%m%d') + timedelta(days=1) - timedelta(seconds=1)
            # incr_enddate = cgls_cpl.date_time.incrDate(enddate, days=1)     #increment the day +1 to completely include the enddate, but substract 1 second as we don't want the products with enddate having times to 00:00:0000
            query += " AND periodstartdate between '%s' AND '%s'" % (startdate, enddate)
        if version is not None:
            query += " AND productversion = '%s'" % version
        if platformid is not None:
            query += ' AND platformid = %s' % platformid
        if sensorid is not None:
            query += ' AND sensorid = %s' % sensorid
        if roi is not None:
            query += " AND roi = '%s'" % roi
        if consolidation is not None:
            query += ' AND consolidation=%s' % consolidation
        if periodicity is not None:
            query += ' AND periodicity=%s' % periodicity
        if location is not None:
            query += " AND location='%s'" % location

        # at the end we can define a limit
        if limit is not None:
            query += 'LIMIT %s;' % limit

        logger.debug('get products by query : %s ' % query)
        with self.conn.cursor() as curs:
            try:
                curs.execute(query)
                # pg_rows = curs.fetchall()
                # transform result
                columns = list(curs.description)
                result = curs.fetchall()

            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(error)

        results_as_DB_product = []
        for row in result:
            row_dict = {}
            for i, col in enumerate(columns):
                row_dict[col.name] = row[i]
            product = DB_product(**row_dict)
            results_as_DB_product.append(product)
        return results_as_DB_product
