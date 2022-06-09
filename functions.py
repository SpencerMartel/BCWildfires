import json
from datetime import datetime

fire_points_file = 'Data/Fire_Points.json'
fire_points_json = {}

class fire_point_data_builder:
    def __init__(self, data):
        self.data = data
    
    def json_builder(self, status, year, date, cause, id, description, lat, long, number, month, day):
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
                'ignition date': {
                    'complete': date,
                    'day': day,
                    'month': month,
                    'year': year
                }
            }
        }

        add_fire_points(fire_number, obj)
        return(obj)


def data_extraction(dataset):
    fire_year = dataset['properties']['IGNITION_DATE']
    fire_date_string = fire_year.replace('Z','')
    fire_year_split = fire_date_string.split('-',3)
    ignition_year = int(fire_year_split[0])
    ignition_month = int(fire_year_split[1])
    ignition_day = int(fire_year_split[2])
    dict = {
        'fire number': dataset['properties']['FIRE_NUMBER'],
        'object id' : dataset['properties']['OBJECTID'],
        'fire status': dataset['properties']['FIRE_STATUS'],
        'ignition date' : fire_date_string,
        'ignition month' : ignition_month,
        'ignition day' : ignition_day,
        'fire year': int(fire_year_split[0]),
        'fire cause' : dataset['properties']['FIRE_CAUSE'],
        'geographic description' : dataset['properties']['GEOGRAPHIC_DESCRIPTION'],
        'latitude' : float(dataset['properties']['LATITUDE']),
        'longitude' : float(dataset['properties']['LONGITUDE'])
    }
    return(dict)

def sync_file(json_variable, path_to_file):
    with open(path_to_file, 'w') as file:
        dict_variable = {'Fire points': fire_points_json}
        json_variable = json.dumps(dict_variable, indent = 4, sort_keys=False)
        file.write(json_variable)

def add_fire_points(key_title, dict):
    fire_points_json[key_title] = dict
    sync_file(dict, 'Data/Fire_Points.json')

def add_day_break(dict, path_to_file):
    now = datetime.today().strftime('%Y-%m-%d')
    dict[now] = {}
    sync_file(dict, path_to_file)

def read_file_as_json(file_path):
    with open(file_path, 'r') as file:
        file_string = file.read()
        json_object = json.loads(file_string)
        return json_object

def initialize_file(path_to_file):
    now = datetime.today().strftime('%Y-%m-%d')
    dict[now] = {}
