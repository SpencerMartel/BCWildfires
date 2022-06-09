import datetime
import time
import webbrowser
import requests
from Map import *
from functions import *


# TODO get fire perimiters - curent.
# More info here: https://catalogue.data.gov.bc.ca/dataset/fire-perimeters-current/resource/fc86711c-d9a9-4431-9f89-f69c4203d5b0
# r1 = requests.get('https://openmaps.gov.bc.ca/geo/pub/ows?service=WFS&version=2.0.0&request=GetFeature&typeName=pub:WHSE_LAND_AND_NATURAL_RESOURCE.PROT_CURRENT_FIRE_POLYS_SP&outputFormat=json')
# perimeters_json = json.loads(r1.text)

# TODO Get historical data.
# historical_data = requests.get('https://openmaps.gov.bc.ca/geo/pub/ows?service=WFS&version=2.0.0&request=GetFeature&typeName=pub:WHSE_FOREST_VEGETATION.VEG_BURN_SEVERITY_SP&outputFormat=json&SrsName=EPSG%3A4326&SrsName=EPSG%3A4326&PROPERTYNAME=FIRE_YEAR&CQL_FILTER=FIRE_YEAR%3D2016')
# print(json.loads(historical_data.text))
# correct_counter = 0
# other_counter = 0
# fire_years = [2015,2016,2017,2018,2019,2020]
# for year in fire_years:
#     #  historical_data = requests.get(f'https://openmaps.gov.bc.ca/geo/pub/ows?service=WFS&version=2.0.0&request=GetFeature&typeName=pub:WHSE_FOREST_VEGETATION.VEG_BURN_SEVERITY_SP&outputFormat=json&SrsName=EPSG%3A4326&SrsName=EPSG%3A4326&PROPERTYNAME=FIRE_YEAR&CQL_FILTER=FIRE_YEAR%3D{year}')
#     historical_data = requests.get('https://openmaps.gov.bc.ca/geo/pub/ows?service=WFS&version=2.0.0&request=GetFeature&typeName=pub:WHSE_FOREST_VEGETATION.VEG_BURN_SEVERITY_SP&outputFormat=json')
#     historical_data_json = (json.loads(historical_data.text))
#     print(f'historical_json for the year {year} is:',historical_data_json,'\n')
#     for obj in historical_data_json:
#         coords = []
#         other_counter = other_counter + 1
# coords = []
# counter = 0
# for obj in perimeters_json['features']:
#     obj_coords = obj['geometry']['coordinates'][0]
#     dict = {'Polygon': []}
#     for i in obj_coords:
#         coords_tupple = (i[0],i[1])
#         dict['Polygon'] += coords_tupple
#     coords.append(dict)


# for obj['Polygon'] in coords:
#     list = obj['Polygon'].values()
#     print(list)
#     Polygon(list).add_to(my_map)

# Get fire locations - current
# More info here: https://catalogue.data.gov.bc.ca/dataset/fire-locations-current
request = requests.get('https://openmaps.gov.bc.ca/geo/pub/ows?service=WFS&version=2.0.0&request=GetFeature&typeName=pub:WHSE_LAND_AND_NATURAL_RESOURCE.PROT_CURRENT_FIRE_PNTS_SP&outputFormat=json')
if request.status_code != 200:
    print(f'HTML code: {request.status_code}\nError connecting to server''')
else:
    print(f'HTML code: {request.status_code}\nSuccessful connection established')
    my_map = main_map_builder(request.text)

my_map.save("map.html")
webbrowser.open("map.html")

add_day_break(fire_points_json, 'Data/Fire_Points.json')

last_day = datetime.now().day

# while True:
#     day = datetime.datetime.now().day
#     if day != last_day:
#         last_day = day
#         add_day_break(fire_points_json, 'Data/Fire_Points.json')
#     time.sleep(1)

