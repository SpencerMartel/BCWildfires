import webbrowser
import requests
from Map import *
from functions import *
from Historical import *
from folium import LayerControl


my_map = map_initializing()
now = datetime.today().strftime('%Y-%m-%d')
current_feature_group = FeatureGroup(name=f'2022 Fire Data', overlay=True, control=True, show=True)

# Fire points - current.
# More info here: https://catalogue.data.gov.bc.ca/dataset/fire-locations-current
def current_point_fetch():
    request = requests.get('https://openmaps.gov.bc.ca/geo/pub/ows?service=WFS&version=2.0.0&request=GetFeature&typeName=pub:WHSE_LAND_AND_NATURAL_RESOURCE.PROT_CURRENT_FIRE_PNTS_SP&outputFormat=json')
    if request.status_code != 200:
        print(f'Fire locations - current HTML code: {request.status_code}\nError connecting to server')
    else:
        print(f'Fire locations - current HTML code: {request.status_code}\nSuccessful connection established')
        fire_locations_json = json.loads(request.text)
        # Begining of saving data locally, our map will grab data from locally stored files.
        point_list_of_coords = []       
        for obj in fire_locations_json['features']:
            coords = (obj['properties']['LATITUDE'], obj['properties']['LONGITUDE'])
            point_list_of_coords.append(coords)
            data = point_data_extraction(obj)
            obj = fire_point_data_builder(data)
            dict = obj.point_json_builder(data.get('fire status'), data.get('ignition date'), data.get('fire cause'), data.get('fire cause'), data.get('geographic description'), data.get('latitude'), data.get('longitude'), data.get('fire number'))
        json_object = read_file_as_json('Data/Fire_Points.json')
        location_markers(json_object[f'{now}'], current_feature_group)
    heatmap(point_list_of_coords, current_feature_group, 2022)

# Fire perimiters - curent.
# More info here: https://catalogue.data.gov.bc.ca/dataset/fire-perimeters-current/resource/fc86711c-d9a9-4431-9f89-f69c4203d5b0
perimeter_request = requests.get('https://openmaps.gov.bc.ca/geo/pub/ows?service=WFS&version=2.0.0&request=GetFeature&typeName=pub:WHSE_LAND_AND_NATURAL_RESOURCE.PROT_CURRENT_FIRE_POLYS_SP&outputFormat=json')
if perimeter_request.status_code != 200:
    print(f'Fire perimeters - current HTML code: {perimeter_request.status_code}\nError connecting to server''')
else:
    print(f'Fire perimiters - current HTML code: {perimeter_request.status_code}\nSuccessful connection established')
    p_json = json.loads(perimeter_request.text)
    perimeters_json = p_json['features']
    list_of_coords = []
    for obj in perimeters_json:
        # Only add the perimeter if the fire is active.
        if obj['properties']['FIRE_STATUS'].lower() == 'out':
            color = 'green'
        else:
            color = 'red'
        polygon_type = obj['geometry']['type'].lower()
        if polygon_type == 'multipolygon':

            length = len(obj['geometry']['coordinates'])
            fire_date = obj['properties']['TRACK_DATE']
            fire_date_string = fire_date.replace('Z','')
            status = obj['properties']['FIRE_STATUS']
            size = obj['properties']['FIRE_SIZE_HECTARES']
            tooltip = f"""
                <strong>Status:</strong> {status}<br>
                <strong>Size:</strong> {size} Hectares<br>
                <strong>Started Tracking:</strong> {fire_date_string}
                """

            for obj in obj['geometry']['coordinates']:
                multi_polygon_list = []
                for coords in obj:
                    coords_list = []
                    reprojected_coords = reproject(coords)
                    coords_list.append(reprojected_coords)
                multi_polygon_list.append(coords_list)
            perimeters(multi_polygon_list, current_feature_group, tooltip, color)
            
        else:
            polygon_list = []
            for lists in obj['geometry']['coordinates']:
                fire_date = obj['properties']['TRACK_DATE']
                fire_date_string = fire_date.replace('Z','')
                status = obj['properties']['FIRE_STATUS']
                size = obj['properties']['FIRE_SIZE_HECTARES']
                tooltip = f"""
                    <strong>Status:</strong> {status}<br>
                    <strong>Size:</strong> {size} Hectares<br>
                    <strong>Started Tracking:</strong> {fire_date_string}
                    """
                reprojected_coords = reproject(lists)
                polygon_list.append(reprojected_coords)
                perimeters(polygon_list, current_feature_group, tooltip, color)


current_feature_group.add_to(my_map)
current_point_fetch()
my_map.add_child(LayerControl())
my_map.save("map.html")

webbrowser.open('map.html')