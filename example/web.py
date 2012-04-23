
from enable.tools.api import ViewportPanTool
from traits.api import HasTraits, Instance, Str, List, Property, Dict

from mapping.mapping_viewport import MappingViewport
from mapping.mapping_canvas import MappingCanvas
from mapping.mapping_zoom import MappingZoomTool

from mapping.http_tile_manager import HTTPTileManager


class Model(HasTraits):

    canvas = Instance(MappingCanvas)
    viewport = Instance(MappingViewport)

    server = Str
    servers = Dict
    
    def _server_changed(self, new):
        server, url = self.servers[new]
        self.canvas.tile_cache.trait_set(server=server, url=url)

    def _server_default(self):
        return self.servers.keys()[0]
        
    def _servers_default(self):
        return dict([
            ('MapQuest', ('otile1.mqcdn.com','/tiles/1.0.0/osm/%d/%d/%d.jpg')),
            ('MapQuest Arial', ('oatile1.mqcdn.com','/tiles/1.0.0/sat/%d/%d/%d.jpg')),
            ('OpenStreetMap', ('tile.openstreetmap.org', '/%d/%d/%d.png')),
            ('MapBox', ('d.tiles.mapbox.com', '/v3/mapbox.mapbox-streets/%d/%d/%d.png')),
            ('MapBox Lacquer', ('d.tiles.mapbox.com', '/v3/mapbox.mapbox-lacquer/%d/%d/%d.png')),
            ('MapBox Light', ('d.tiles.mapbox.com', '/v3/mapbox.mapbox-light/%d/%d/%d.png')),
            ('MapBox Simple', ('d.tiles.mapbox.com', '/v3/mapbox.mapbox-simple/%d/%d/%d.png')),
            ('Stamen Watercolor', ('a.tile.stamen.com', '/watercolor/%d/%d/%d.jpg')),
            ('Stamen Toner', ('tile.stamen.com', '/toner/%d/%d/%d.jpg')),
            ('Stamen Terrain', ('tile.stamen.com', '/terrain-background/%d/%d/%d.png')),
            ]
            )


def main():
    manager = HTTPTileManager(
                              min_level = 0,
                              max_level = 15)

    canvas = MappingCanvas(bgcolor="lightsteelblue", 
                           tile_cache = manager)

    viewport = MappingViewport(component=canvas, 
                        stay_inside=True)
    viewport.tools.append(ViewportPanTool(viewport))
    viewport.zoom_tool = MappingZoomTool(viewport)
    viewport.enable_zoom = True

    viewport.zoom_level = 12
    viewport.view_position = (308500, 654200)

    model = Model(canvas=canvas, viewport=viewport)
    model.server = 'MapBox Simple'

    import enaml
    with enaml.imports():
        from webmap_view import Main
    window = Main(model=model)
    manager.start()
    window.show()

if __name__ == "__main__":
    main()
