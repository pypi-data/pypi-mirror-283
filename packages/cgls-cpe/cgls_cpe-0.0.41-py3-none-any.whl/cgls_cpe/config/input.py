'''
Created on Oct 24, 2023

@author: demunckd
'''
from cgls_cpe.common import grid
from cgls_cpe.common import helper
import os
import geojson




class Input:

    def __init__(self, setting):
        self.settings = setting.get_settings()
        
        
    #TODO:
    # reading roiFile setting ( = json with grid, default to s3 grid)
    # reading ro_filter
    # reading roi_skip -> get resulting tiles - see hspf helper code
    def get_filtered_roi_dict(self):
        
        if self.get_roi_file():
            roi_file =  self.get_roi_file()
        else:
            roi_file = grid.get_s3GeoJsonFullGrid()
        return self.parseRoiInfo(roi_file, roiFilter = self.get_roi_filter(), roiSkipFilter=self.get_roi_skip_filter_sen_grid())
    
    def parseRoiInfo(self,roiFile,roiFilter=None,roiSkipFilter=None):
        """parse geoJson R.O.I. files

        Reads the geoJson file and parses it into a geojson.feature.FeatureCollection.

        Parameters
        ----------
        roiFile : str
            R.O.I. json file ; can be S3 URL
        roiFilter : list
            list of R.O.I. id's (all if empty,default=None)
        roiSkipFilter: list
            list of R.O.I. id's not to process (default=None)

        Returns
        -------
        roiCollInfo : geojson.feature.FeatureCollection
            R.O.I. info object
        """
        from cgls_cpe.storage import remote_storage
        roiCollInfo = None
        if roiFile:
            with remote_storage.open_smart(roiFile) as roiFileHandle:
                roiCollInfo = geojson.loads(roiFileHandle.read())
            #if ROI filter is set, keep only the selected ROI id's
            if roiFilter:
                if type(roiFilter) == str and ',' in roiFilter:
                    roiFilter = roiFilter.split(',')
                roiCollInfo.features[:] = [feature for feature in roiCollInfo.features  \
                                           if feature["id"] in roiFilter                ]
            if roiSkipFilter:
                # HSPF-218 fix roi skip filter
                roiCollInfo.features[:] = [feature for feature in roiCollInfo.features \
                                           if feature["id"] not in roiSkipFilter       ]
            #Check if roiCollInfo is still a valid GeoJSON configuration
            assert(roiCollInfo.is_valid), 'GeoJSON file content is invalid ({})'.format(roiFile)
        return roiCollInfo
        
        
    def get_roi_skip_filter_sen_grid(self):
        return  self.settings.roiSkipFilter
    
    
    def get_extended_roi_skip_filter_sen_grid(self):
        return self.get_roi_skip_filter_sen_grid() +  self.settings.roiSkipFilterExtensionProbaVSeaTiles
    
    
    def get_roi_skip_filter_prob_grid(self):
        return grid.convert_sen_tile_list_to_prob( self.get_roi_skip_filter_sen_grid())
    
    
    def get_extended_roi_skip_filter_prob_grid(self):
        return grid.convert_sen_tile_list_to_prob(self.get_extended_roi_skip_filter_sen_grid())
    
    
    def show_roi_skip_filters(self):
        grid.showTiles('Showing skipped tiles' , grid.get_s3GeoJsonFullGrid() , ['yellow', 'red'], [self.get_roi_skip_filter_sen_grid(),self.get_extended_roi_skip_filter_sen_grid() ] )

        
        
    def get_tiles_to_process_sen_grid(self):
        all_tiles = grid.get_all_tiles_sen()
        tiles_to_skip = self.get_roi_skip_filter_sen_grid()
        to_process = []
        for tile in all_tiles:
            if tile not in tiles_to_skip:
                to_process.append(tile)
        return to_process
    
    def get_tiles_to_process_prob_grid(self):
        return grid.convert_sen_tile_list_to_prob(self.get_tiles_to_process_sen_grid())
    
    
    def get_minimal_tiles_to_process_sen_grid(self):
        all_tiles = grid.get_all_tiles_sen()
        tiles_to_skip = self.get_extended_roi_skip_filter_sen_grid() 
        to_process = []
        for tile in all_tiles:
            if tile not in tiles_to_skip:
                to_process.append(tile)
        return to_process
    
    def get_minimal_tiles_to_process_prob_grid(self):
        return grid.convert_sen_tile_list_to_prob(self.get_minimal_tiles_to_process_sen_grid())
        
    
    def get_roi_file(self):
        return  self.settings.roiFile
    
    
    def get_roi_filter(self):
        return  self.settings.roiFilter
    


