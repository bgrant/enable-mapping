
import math

# Enthought library imports
from traits.api import Tuple, Int, Float, Instance, Property, on_trait_change

from kiva.constants import FILL
from enable.api import Canvas

# Local imports
from i_tile_manager import ITileManager

class MappingCanvas(Canvas):
    """
    An infinite tiled canvas for showing maps
    """

    tile_cache = Instance(ITileManager)
    
    # FIXME This is a hack - remove when viewport is fixed
    _zoom_level = Int(0)

    @on_trait_change('tile_cache:tile_ready')
    def _tile_ready(self, (zoom, row, col)):
        self.request_redraw()

    def _draw_underlay(self, gc, view_bounds=None, mode="default"):
        x, y, width, height = view_bounds
        zoom = self._zoom_level
        with gc:
            gc.clip_to_rect(x,y,width, height)

            # Tile image
            tile_size = self.tile_cache.get_tile_size()
            startx = int(x) / tile_size * tile_size
            starty = int(y) / tile_size * tile_size
            endx = int(x+width)
            endy = int(y+height)

            lim = 2**zoom * tile_size

            if starty < 0: starty = 0
            if endy > lim: endy = lim

            for tx in range(startx, endx, tile_size):
                for ty in range(starty, endy, tile_size):
                    zoom, row, col = self.tile_cache.convert_to_tilenum(tx, ty, zoom)
                    gc.draw_image(self.tile_cache.get_tile(zoom, row, col), (tx,ty,tile_size, tile_size))
        super(MappingCanvas, self)._draw_underlay(gc, view_bounds, mode)

    def transformToScreen(self, lon, lat):
        return self._WGS84_to_screen(lon, lat, self._zoom_level)
    
    def _WGS84_to_screen(self, lon, lat, zoom):
        """
         lat = Latitude in degrees
         lon = Longitute in degrees
         zoom = zoom level
        """
        lat_rad = math.radians(lat)
        mapsize = self.tile_cache.get_tile_size() << zoom
        x = (lon + 180.0) / 360.0 * mapsize
        y = (1- (1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) 
                    / 2.0) * mapsize
        return (x, y)

    def _screen_to_WGS84(self, x, y, zoom):
        """ This is currently incorrect - needs to use screen coords
        """
        mapsize = self.tile_cache.get_tile_size() << zoom
        n = 2.0 ** zoom
        lon_deg = col / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * row / n)))
        lat_deg = math.degrees(lat_rad)
        return (lat_deg, lon_deg)
