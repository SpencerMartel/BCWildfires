from functions import *
import folium
from folium import FeatureGroup, TileLayer, plugins
from Historical import *
import pyproj

def map_initializing():
    my_map = folium.Map(location = (55.107,-124.925), tiles = None , zoom_start = 6, control=False, control_scale=True)
    tile_layer = TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', control=False, attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community')
    my_map.add_child(tile_layer)
    my_map.add_child(plugins.MiniMap())
    historical_fetch(my_map)
    return my_map

def location_markers(datadict, group):
    feature_group = FeatureGroup(overlay=True, control=False, show=True)
    for obj in datadict:
        fire_status = datadict[obj]['properties']['fire status']
        location = datadict[obj]['properties']['location description']
        if datadict[obj]['properties']['fire status'].lower() != 'out':
            fire_status_string = f'Fire Is: {fire_status}'
            icon = folium.Icon(prefix = 'fa',icon='fire', color = 'darkred')
            html=f"""
                <h1>{datadict[obj]['properties']['location description']} Fire</h1>
                Status: {datadict[obj]['properties']['fire status']}<br>
                Cause: {datadict[obj]['properties']['fire cause']}<br>
                Ignition Date: {datadict[obj]['properties']['ignition date']}
                """
            iframe = folium.IFrame(html=html, width = 350, height = 175)
            tooltip = f'<strong>{location} Fire</strong>'
            popup = folium.Popup(iframe , max_width = 2650)
            folium.Marker(
                location = (datadict[obj]['properties']['coordinates']['latitude'], datadict[obj]['properties']['coordinates']['longitude']),
                popup = popup,
                tooltip = tooltip,
                icon = icon).add_to(feature_group)
    feature_group.add_to(group)

# Used only to project from epsg3005 to 4326, currently used to reproject perimeter data.
# Returns a list of tuples with the reprojected coordinates.
def reproject(list_of_coords):
    init = pyproj.Transformer.from_crs(3005,4326)
    list_of_tuples = []
    for coords in list_of_coords:
        x , y = coords[0], coords[1]
        x1 , y1 = init.transform(x,y)
        list_of_tuples.append((x1,y1))
    return list_of_tuples
    
def perimeters(lists, group, tooltip, color):
    for list in lists:
        folium.Polygon(list,
            color = color,
            weight = 7,
            fill = True,
            tooltip = tooltip).add_to(group)

def heatmap(list, parent, year):
    heatmap = plugins.HeatMap(list, show=False, name=f'{year} Heatmap - {len(list)} Fires', min_opacity=0.2, blur=15, radius=18)
    heatmap.add_to(parent)

