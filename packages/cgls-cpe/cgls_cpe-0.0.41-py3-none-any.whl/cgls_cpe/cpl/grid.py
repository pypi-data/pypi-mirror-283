"""Common Python Library grid related functions.

This module provides functions to manipulate coordinate girds

"""

from affine import Affine

class BaseGrid:
    """Base class for all grids.
    
    Parameters
    ----------
    geotransform : (float, float, float, float, float, float)
        Provide a geotransformation tuple of floats: pxStepX, 0.0, refX, 0.0, pxStepY, refY
        refX and refY center pixel coordinates
        pxStepX and pxStepY are in [deg/px]
    
    """
    def __init__ (self, geotransform):
        self._cpGrid = Affine(*geotransform)
        self._bbGrid = self._cpGrid * Affine.translation(-0.5,-0.5)
    
    def getColRow(self, lon, lat):
        """Get the column and row index in the grid, based on the provided lon lat coordinate.
        
        Parameters
        ----------
        lon : float
            Longitude
        lat : float
            Latitude

        Returns
        -------
        (int, int):
            a tuple containing (column, row) information
        
        """
        return map(int, ~self._bbGrid * (lon, lat))
    
    def getLonLat(self, col, row):
        """Get the lon/lat coordinate of a pixel, based on the provided col row information
        
        Parameters
        ----------
        col : int
            column, counted from the grid reference point
        row : int
            row, counted from the grid reference point

        Returns
        -------
        (float, float):
            a tuple containing (longitude, latitude) position
        
        """
        return self._cpGrid * (col, row)
    
    def getGridPoint(self, lon, lat):
        """Get the nearest lon/lat that fits from the grid, based on the provided lon lat coordinate
        
        Parameters
        ----------
        lon : float
            Longitude
        lat : float
            Latitude

        Returns
        -------
        (float, float):
            a tuple containing (longitude, latitude) grid position
        
        """
        (col, row) = self.getColRow(lon, lat)
        return self.getLonLat(col, row)
    
    def getGeotransform(self):
        """Get the nearest lon/lat that fits from the grid, based on the provided lon lat coordinate
        
        Returns
        -------
        (float, float, float, float, float, float):
            a geotransformation tuple of floats: pxStepX, 0.0, refX, 0.0, pxStepY, refY
            refX and refY center pixel coordinates
            pxStepX and pxStepY are in [deg/px]
        
        """
        return (self._cpGrid.a, self._cpGrid.b, self._cpGrid.c, self._cpGrid.d, self._cpGrid.e, self._cpGrid.f)

class TiledGrid(BaseGrid):
    """ Tiled based grid
    
    Parameters
    ----------
    geotransform : (float, float, float, float, float, float)
        Provide a geotransformation tuple of floats: pxStepX, 0.0, refX, 0.0, pxStepY, refY
        refX and refY center pixel coordinates
        pxStepX and pxStepY are in [deg/px]
    
    tileSize : int
        the number of pixels, X and Y direction
    
    """
    def __init__ (self, geotransform, tileSize):
        self._tileSize = tileSize # px per 10° x 10° tiles
        BaseGrid.__init__(self, geotransform)
    
    def getGridPoint(self, lon, lat):
        """Get the nearest lon/lat that fits from the grid, based on the provided lon lat coordinate
        
        Parameters
        ----------
        lon : float
            Longitude
        lat : float
            Latitude

        Returns
        -------
        (float, float):
            a tuple containing (longitude, latitude) grid position
        
        """
        (col, row) = self.getColRow(lon, lat)
        return self.getLonLat(col, row)
    
    def getGeotransform(self):
        """Get the nearest lon/lat that fits from the grid, based on the provided lon lat coordinate
        
        Returns
        -------
        (float, float, float, float, float, float):
            a geotransformation tuple of floats: pxStepX, 0.0, refX, 0.0, pxStepY, refY
            refX and refY center pixel coordinates
            pxStepX and pxStepY are in [deg/px]
        
        """
        return (self._cpGrid.a, self._cpGrid.b, self._cpGrid.c, self._cpGrid.d, self._cpGrid.e, self._cpGrid.f)
    
    def getTileFromColRow(self, col, row):
        """Get the X/Y tile index, based on the provided col row information
                
        Parameters
        ----------
        col : int
            column, counted from the grid reference point
        row : int
            row, counted from the grid reference point

        Returns
        -------
        (int, int):
            a tuple containing (X, Y) tile index
        
        """
        X = int (col / self._tileSize)
        Y = int (row / self._tileSize)
        return (X, Y)
    
    def getTileFromLonLat(self, lon, lat):
        """Get the X/Y tile index, based on the provided lon lat coordinate
                
        Parameters
        ----------
        lon : float
            Longitude
        lat : float
            Latitude
        
        Returns
        -------
        (int, int):
            a tuple containing (X, Y) tile index
        
        """
        col, row = self.getColRow(lon, lat)
        return self.getTileFromColRow(col, row)
    
    def getTileColRowFromColRow(self, col, row):
        """Get the X/Y tile index and the column and row index in the tile , based on the provided col row information
                
        Parameters
        ----------
        col : int
            column, counted from the grid reference point
        row : int
            row, counted from the grid reference point

        Returns
        -------
        (int, int, int, int):
            a tuple containing (tile X index, tile Y index, column, row)
        
        """
        (X, Y) = self.getTileFromColRow(col, row)
        col %= self._tileSize
        row %= self._tileSize
        return (X, Y, col, row)
    
    def getTileColRowFromLonLat(self, lon, lat):
        """Get the X/Y tile index and the column and row index in the tile , based on the provided lon lat coordinates
                
        Parameters
        ----------
        lon : float
            Longitude
        lat : float
            Latitude
        
        Returns
        -------
        (int, int, int, int):
            a tuple containing (tile X index, tile Y index, column, row)
        
        """
        col, row = self.getColRow(lon, lat)
        return self.getTileColRowFromColRow(col, row)    
    
    def getLonLatFromTileColRow(self, X, Y, col, row):
        """Get the lon/lat coordinate of a pixel, based on the provided tile index and col row information
        
        Parameters
        ----------
        X : int
            tile X index
        Y : int
            tile Y index
        col : int
            column, counted from the tile reference point (Upper Left)
        row : int
            row, counted from the tile reference point (Upper Left)

        Returns
        -------
        (float, float):
            a tuple containing (longitude, latitude) position
        
        """
        col += X * self._tileSize
        row += Y * self._tileSize
        return self.getLonLat(col, row)

class CglS3Grid(TiledGrid):
    """ Copernicus Global Land Sentinel 3 Grid
    
    The S3 grid specification can be found in the Interface Definition Document CGLOPS1_DD-IDD_MEP-VM.
    """
    def __init__ (self):
        S3GridGeotransform = (0.00297619047619, 0, -180.0, 0, -0.00297619047619, 85.0)
        tileSize = 3360 # px per 10° x 10° tiles
        TiledGrid.__init__(self, S3GridGeotransform, tileSize)
    
class PBV300Grid(TiledGrid):
    """ Proba-V 300 m Grid
    
    """
    def __init__ (self):
        S3GridGeotransform = (0.00297619047619, 0, -180.0, 0, -0.00297619047619, 75.0)
        tileSize = 3360 # px per 10° x 10° tiles
        TiledGrid.__init__(self, S3GridGeotransform, tileSize)
