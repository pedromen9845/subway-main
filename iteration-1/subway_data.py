import requests
import json

# Get subway data
response = requests.get('http://map.amap.com/service/subway?_1469083453978&srhdata=1100_drw_beijing.json')
data = json.loads(response.text)

# Save JSON data to a file
with open('subway_data.json', 'w') as file:
    json.dump(data, file, indent=4)

print("JSON data saved to subway_data.json file.")

# Extract station information
stations_info = {}
for line in data['l']:
    for station in line['st']:
        station_name = station['n']
        lng, lat = station['sl'].split(',')
        stations_info[station_name] = (float(lng), float(lat))

# Build adjacency list
neighbor_info = {}
lines_info = {}
for line in data['l']:
    line_name = line['kn']
    lines_info[line_name] = []
    neighbor_info[line_name] = []
    for i in range(len(line['st']) - 1):
        station1 = line['st'][i]['n']
        station2 = line['st'][i+1]['n']
        lines_info[line_name].append(station1)
        neighbor_info[line_name].append((station1, station2))




