import requests
import json
import Map
requested_years = [1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]
requested_years = [1997,2009,2021]

# Historical data.
def historical_fetch(main_map):
    # We do this in a loop to create seperate folim FeatureGroups containing only the heatmaps for that
    for year in requested_years:
        url = f'https://openmaps.gov.bc.ca/geo/pub/ows?service=WFS&version=2.0.0&request=GetFeature&typeName=pub:WHSE_LAND_AND_NATURAL_RESOURCE.PROT_HISTORICAL_INCIDENTS_SP&outputFormat=json&PROPERTYNAME=FIRE_YEAR&CQL_FILTER=FIRE_YEAR%3D{year}&PROPERTYNAME=FIRE_NUMBER&count=1'
        # For some reason I can only parse by fire year if I add the count to the end, so I make an initial call with count=1 and from that I can see how many features there actually are for that year
        count_historical_request = requests.get(url)
        j = json.loads(count_historical_request.text)
        # I then take this number and add it to the second actual request for it to run properly.
        count = j['totalFeatures']
        actual_historical_request = requests.get(f'https://openmaps.gov.bc.ca/geo/pub/ows?service=WFS&version=2.0.0&request=GetFeature&typeName=pub:WHSE_LAND_AND_NATURAL_RESOURCE.PROT_HISTORICAL_INCIDENTS_SP&outputFormat=json&PROPERTYNAME=FIRE_YEAR&CQL_FILTER=FIRE_YEAR%3D{year}&PROPERTYNAME=FIRE_NUMBER&count={count}')
        if actual_historical_request.status_code != 200:
            print(f'Historical fetch - current HTML code: {actual_historical_request.status_code}\nError connecting to server''')
        else:
            print(f'Historical fetch year: {year}\ncurrent HTML code: {actual_historical_request.status_code} - Successful connection established')
            historical_json = json.loads(actual_historical_request.text)
            coords = []
            for obj in historical_json['features']:
                obj_coords = [obj['properties']['LATITUDE'],obj['properties']['LONGITUDE']]
                coords.append(obj_coords)

        # I tried displaying the historical info with markers but there were too many
        # A heatmap is a good way of showing them and conserving computer resources.
        Map.heatmap(coords, main_map, year)
