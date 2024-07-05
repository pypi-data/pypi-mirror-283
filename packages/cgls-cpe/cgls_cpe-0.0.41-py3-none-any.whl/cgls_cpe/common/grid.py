'''
Created on Dec 21, 2023

@author: demunckd
'''
from cgls_cpe.common import helper
import os.path

def convert_sen_tile_to_prob(tile:str):
    first_part = tile[0:3]
    probav_y_index = int(tile[4:6])-1
    if probav_y_index < 0:
        return None
    second_part = 'Y' +  helper.pad_two_digits(probav_y_index )
    result = first_part + second_part 
    return result

def convert_sen_tile_list_to_prob(list_of_sen_tiles:str):
    new_list = []
    for tile in list_of_sen_tiles:
        new_tile =convert_sen_tile_to_prob(tile)
        if new_tile is not None:
            new_list.append(new_tile)
    return new_list             


def convert_prob_tile_to_sen(tile:str):
    first_part = tile[0:3]
    sen_y_index = int(tile[4:6])+1
    second_part = 'Y' +  helper.pad_two_digits(sen_y_index )
    result = first_part + second_part 
    return result


def get_all_tiles_sen():
        list_of_tiles = []
        for x_index in range(36):
            for y_index in range(15):
                tile = 'X' + helper.pad_two_digits(x_index) +\
                        'Y' + helper.pad_two_digits(y_index)
                list_of_tiles.append(tile )

        return list_of_tiles
    
def get_s3GeoJsonFullGrid():
    return os.path.join( os.path.dirname(__file__),'cgl_s3_grid-geo.json' )

def get_pbvGeoJsonFullGrid():
    return os.path.join( os.path.dirname(__file__),'cgl_pv_grid_333m-geo.json' )

def showTiles(title, json_file, list_of_colors, list_of_list_of_tiles):
    #we only want to import these when really needed
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    import geopandas as gpd


    
    input_grid_json = gpd.read_file(json_file)
        #From GeoPandas, our world map data
    worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    # Creating axes and plotting world map
    fig, ax = plt.subplots(figsize=(20, 10))
    worldmap.plot(color="lightgrey", ax=ax)

    # Creating axis limits and title
    plt.xlim([-180, 180])
    plt.ylim([-90, 90])
    
    plt.title(title)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    
    i = 0
    while i < len(list_of_colors):
        tiles_in_grid = input_grid_json[input_grid_json.id.isin(list_of_list_of_tiles[i])]
        tiles_in_grid.plot(ax=ax, color=list_of_colors[i], alpha=0.3, edgecolor="black", label='')
        i+=1

    plt.show()