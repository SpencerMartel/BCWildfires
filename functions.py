import json
from datetime import datetime

fire_points_file = 'Data/Fire_Points.json'
fire_perimeters_file = 'Data/Fire_Perimeters.json'
historical_point_file = 'Data/Historical_Points.json'
fire_points_json = {}
fire_perimeters_json = {}

class fire_point_data_builder:
    def __init__(self, data):
        self.data = data
    
    def point_json_builder(self, status, date, cause, id, description, lat, long, number):
        fire_number = number
        obj = {
            'properties': {
                'fire status': status,
                'fire cause': cause,
                'object_id': id,
                'location description': description,
                'coordinates':{
                    'latitude': lat,
                   'longitude': long
                },
                'ignition date': date
                }
        }
        add_fire_points_to_json(fire_number, obj)
        return(obj)

class fire_perimeter_data_builder:
    def __init__(self, data):
        self.data = data

    def perimeter_json_builder(self, number, status, cause, id, ignition_date, coordinates):
        fire_number = number
        obj = {
            'properties': {
                'fire status': status,
                'fire cause': cause,
                'object_id': id,
                'ignition date': ignition_date
            },
            'geometry': coordinates
        }
        add_fire_perimeter_to_json(fire_number, obj)
        return obj

def point_data_extraction(dataset):
    fire_date = dataset['properties']['IGNITION_DATE']
    fire_date_string = fire_date.replace('Z','')
    fire_year_split = fire_date_string.split('-',3)
    dict = {
        'fire number': dataset['properties']['FIRE_NUMBER'],
        'object id' : dataset['properties']['OBJECTID'],
        'fire status': dataset['properties']['FIRE_STATUS'],
        'ignition date' : fire_date_string,
        'fire year': int(fire_year_split[0]),
        'fire cause' : dataset['properties']['FIRE_CAUSE'],
        'geographic description' : dataset['properties']['GEOGRAPHIC_DESCRIPTION'],
        'latitude' : float(dataset['properties']['LATITUDE']),
        'longitude' : float(dataset['properties']['LONGITUDE'])
    }
    return dict 

def perimeter_data_extraction(dataset):
    fire_date = dataset['properties']['TRACK_DATE']
    fire_date_string = fire_date.replace('Z','')
    dict = {
        'fire number': dataset['properties']['FIRE_NUMBER'],
        'object id' : dataset['properties']['OBJECTID'],
        'ignition date': fire_date_string,
        'fire size square km': dataset['properties']['FEATURE_AREA_SQM'],
        'fire size hectares': dataset['properties']['FIRE_SIZE_HECTARES'],
        'fire status': dataset['properties']['FIRE_STATUS'],
        'source': dataset['properties']['SOURCE'],
        'geometry': dataset['geometry']['coordinates']
    }
    return dict

def sync_file(json_variable, path_to_file):
    with open(path_to_file, 'w') as file:
        now = datetime.today().strftime('%Y-%m-%d')
        dict_variable = {now: json_variable}
        json_variable = json.dumps(dict_variable, indent = 4, sort_keys=False)
        file.write(json_variable)

def add_fire_points_to_json(key_title, dict):
    fire_points_json[key_title] = dict
    sync_file(fire_points_json, 'Data/Fire_Points.json')

def add_fire_perimeter_to_json(key_title, dict):
    fire_perimeters_json[key_title] = dict
    sync_file(fire_perimeters_json, 'Data/Fire_Perimeters.json')

def read_file_as_json(file_path):
    with open(file_path, 'r') as file:
        file_string = file.read()
        json_object = json.loads(file_string)
        return json_object
