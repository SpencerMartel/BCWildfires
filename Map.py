from functions import *
import json
import folium
from folium import plugins

def main_map_builder(request_text):
    my_map = map_initializing()
    locations_json = json.loads(request_text)
    counter = 0
    for obj in locations_json['features']:
        data = data_extraction(obj)
        obj = fire_point_data_builder(data)
        dict = obj.json_builder(data.get('fire status'), data.get(f'fire year') , data.get('ignition date') , data.get('fire cause') , data.get('object id'), data.get('geographic description') , data.get('latitude'), data.get('longitude'),
        data.get('fire number'), data.get('ignition month'),data.get('ignition day'))
        counter = counter +1
        location_markers(dict, my_map)
    return(my_map)

def map_initializing():
    bc_center = (54.054881,-124.115965)
    tooltip = 'More Info'
    my_map = folium.Map(location = bc_center, tiles = 'Stamen Terrain' , zoom_start = 6, tooltip = tooltip)
    minimap = plugins.MiniMap()
    my_map.add_child(minimap)
    return my_map

def location_markers(datadict, map):
    fire_status = datadict['properties']['fire status']
    if datadict['properties']['fire status'] == 'Out':
        fire_status_string = 'Fire is: Inactive'
        icon = folium.Icon(prefix = 'fa',icon='fire', color = 'green')
    elif datadict['properties']['fire status'] == 'Under Control':
        fire_status_string = f'Fire Is: {fire_status}'
        icon = folium.Icon(prefix = 'fa',icon='fire', color = 'lightred')
    else:
        fire_status_string = f'Fire Is: {fire_status}'
        icon = folium.Icon(prefix = 'fa',icon='fire', color = 'darkred')

    html=f"""
        <h1> {fire_status_string}</h1>
        Status: {datadict['properties']['fire status']}<br>
        Cause: {datadict['properties']['fire cause']}<br>
        Location: {datadict['properties']['location description']}<br>
        Ignition Date: {datadict['properties']['ignition date']}
        """
    iframe = folium.IFrame(html=html, width = 400, height = 200)
    tooltip = '<strong>Click for more info</strong>'
    popup = folium.Popup(iframe , max_width = 2650, )
    folium.Marker(
        location = (datadict['properties']['coordinates']['latitude'], datadict['properties']['coordinates']['longitude']),
        popup = popup,
        tooltip = tooltip,
        icon = icon
    ).add_to(map)