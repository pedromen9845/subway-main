import networkx as nx
import matplotlib.pyplot as plt
import requests
import json
import os
import time
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']  # Specify default font
# Get subway data
# code for refactoring
response = requests.get(
    'http://map.amap.com/service/subway?_1469083453978&srhdata=1100_drw_beijing.json')
data = json.loads(response.text)

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


def generate_map(source, target):
    # Create graph
    city_graph = nx.Graph()
    city_graph.add_nodes_from(stations_info.keys())

    # Add edges to the graph
    for line_name, stations in neighbor_info.items():
        for station1, station2 in stations:
            city_graph.add_edge(station1, station2, line=line_name)

    # Compute the shortest path
    shortest_path = nx.shortest_path(city_graph, source, target)

    # Highlight the shortest path edges
    highlighted_edges = [(shortest_path[i], shortest_path[i+1])
                         for i in range(len(shortest_path)-1)]
    
    # Print all subway lines
print("Subway Lines:")
for line_name, stations in lines_info.items():
    print(f"{line_name}: {', '.join(stations)}")


    # Draw the graph
    plt.figure(figsize=(35, 35))
    pos = stations_info
    nx.draw_networkx_nodes(city_graph, pos, node_size=50, node_color='red')
    nx.draw_networkx_labels(city_graph, pos, font_size=8)
    color_list = list(lines_info.keys())
    for line_name, stations in neighbor_info.items():
        edges = [(station1, station2) for station1, station2 in stations]
        color = plt.cm.tab20(color_list.index(line_name))
        nx.draw_networkx_edges(
            city_graph, pos, edgelist=edges, width=2, alpha=0.5, edge_color=color)
    nx.draw_networkx_edges(
        city_graph, pos, edgelist=highlighted_edges, width=3, edge_color='blue')
    plt.axis('off')

    # Save the plot to a file
    plt.savefig('static/subway_map.png', format='png')

    plt.close()  # Close the plot
    # Return the result
    result = "Shortest path between {} and {}: {}".format(
        source, target, shortest_path)
    return result
