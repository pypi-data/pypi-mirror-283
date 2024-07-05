
import time
import argparse
import sys
import os
from datetime import datetime
import rasterio
from rasterio.windows import Window

from cgls_cpe.logging import log
logger = log.logger()

def read_test():
    from cgls_cpe.config.configuration import Configuration
    from cgls_cpe.storage.implementation.s3_api import S3Api

    store = Configuration().get_storage()
    s3_api = S3Api(store.get_object_storage_endpoint(), store.get_object_storage_acces_id(),
                   store.get_object_storage_secret_acces_key())
    s3_api.export_credentials_to_env()

    s3_root_dir = "s3://sandbox-oomsb/cog_test"
    compr_dirs = ['compressed','compressed_deflate_default', 'compressed_deflate_level9','compressed_deflate_predictor_yes',
                  'compressed_lzw','compressed_lzw_predictor_yes','compressed_zstd_default','compressed_zstd_default',
                  'compressed_zstd_predictor_yes','compressed_zstd_predictor_yes_blocksize_128']
    #compr_dirs =['compressed_zstd_default','compressed_zstd_predictor_yes']
    files = [
        'cgl_TOC_20180501102106_X17Y03_S3A_v2.3.cog_AC_process_flag.tif',
        'cgl_TOC_20180501102106_X17Y03_S3A_v2.3.cog_angles.tif',
        'cgl_TOC_20180501102106_X17Y03_S3A_v2.3.cog_cloud_an.tif',
        'cgl_TOC_20180501102106_X17Y03_S3A_v2.3.cog_Oa_toc_err.tif',
        'cgl_TOC_20180501102106_X17Y03_S3A_v2.3.cog_Oa_toc.tif',
        'cgl_TOC_20180501102106_X17Y03_S3A_v2.3.cog_pixel_classif_flags.tif',
        'cgl_TOC_20180501102106_X17Y03_S3A_v2.3.cog_quality_flags.tif',
        'cgl_TOC_20180501102106_X17Y03_S3A_v2.3.cog_S_an_toc_err.tif',
        'cgl_TOC_20180501102106_X17Y03_S3A_v2.3.cog_S_an_toc.tif',
        'cgl_TOC_20180501102406_X17Y03_S3A_v2.3.cog_AC_process_flag.tif',
        'cgl_TOC_20180501102406_X17Y03_S3A_v2.3.cog_angles.tif',
        'cgl_TOC_20180501102406_X17Y03_S3A_v2.3.cog_cloud_an.tif',
        'cgl_TOC_20180501102406_X17Y03_S3A_v2.3.cog_Oa_toc_err.tif',
        'cgl_TOC_20180501102406_X17Y03_S3A_v2.3.cog_Oa_toc.tif',
        'cgl_TOC_20180501102406_X17Y03_S3A_v2.3.cog_pixel_classif_flags.tif',
        'cgl_TOC_20180501102406_X17Y03_S3A_v2.3.cog_quality_flags.tif',
        'cgl_TOC_20180501102406_X17Y03_S3A_v2.3.cog_S_an_toc_err.tif',
        'cgl_TOC_20180501102406_X17Y03_S3A_v2.3.cog_S_an_toc.tif',
    ]
    result=[]
    for dir_idx, my_dir in enumerate(compr_dirs):
        # read single chunk
        print('SINGLE CHUNK')
        total_time_block = 0
        window = Window(50, 10, 200, 140)
        start = time.time()
        for myfile in files:
            fname = os.path.join(s3_root_dir, my_dir, myfile)
            with rasterio.open(fname, 'r') as src:
                for band_idx in range(1, src.count + 1):
                    print("Reading %s:%s " % (fname, band_idx))
                    r = src.read(band_idx, window=window)
        stop = time.time()
        total_time_block += int(1000*(stop - start))
        print("read runtime: %ss" % int(total_time_block))

        # #read full files
        print("FULL FILES")
        total_time_full = 0
        start = time.time()
        for myfile in files:

            fname = os.path.join(s3_root_dir, my_dir, myfile)

            with rasterio.open(fname,'r') as src:
                for band_idx in range(1, src.count+1):
                    print(" Reading %s:%s " % (fname, band_idx))
                    for ji, window in src.block_windows(1):
                        r = src.read(band_idx, window=window)
        stop = time.time()
        total_time_full += int(stop - start)
        print(" read runtime: %ss" % int(total_time_full))

        # #read full files
        print("FULL FILES in 1 read")
        total_time_full_single = 0
        start = time.time()
        for myfile in files:

            fname = os.path.join(s3_root_dir, my_dir, myfile)

            with rasterio.open(fname, 'r') as src:
                for band_idx in range(1, src.count + 1):
                    print(" Reading %s:%s " % (fname, band_idx))
                    r = src.read(band_idx)
        stop = time.time()
        total_time_full_single += int(stop - start)
        print(" read runtime: %ss" % int(total_time_full_single))
        record = [my_dir, total_time_block, total_time_full,total_time_full_single]
        result.append(record)
    print (result)
    return result

def main(args):
    logger.debug("main")
    #args = parse_arguments(args)
    return read_test()


if __name__ == '__main__':

    status = main(sys.argv[1:])
    sys.exit(0)