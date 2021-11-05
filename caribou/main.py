import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt 
import folium as fo
import random

individuals = pd.read_csv("./datasets/individuals.csv", encoding = 'unicode_escape', sep=";")
locations = pd.read_csv("./datasets/locations.csv", encoding='unicode_escape', sep=";")
data_indi = pd.DataFrame(individuals)
data_loca = pd.DataFrame(locations)

def presentation():
    print(individuals.head(), locations.head(), locations.describe())

individuals_w_start = data_indi[data_indi["deploy_on_longitude"].notnull()]
individual_good = individuals_w_start[data_indi["deploy_off_longitude"].notnull()]

deers_id = individual_good["animal_id"]

datasets = []
counter = 0
for name in deers_id:
    temp_dataset = data_loca[data_loca["animal_id"] == name]
    temp_dataset['timestamp'] = pd.to_datetime(temp_dataset['timestamp'])
    data_sorted = temp_dataset.sort_values(by="timestamp")
    if len(temp_dataset) > 680:   #to get specificaly 20 caribou for the length of colors
        counter += 1
        datasets.append(temp_dataset.head())
        datasets.append(temp_dataset.tail())

# print(counter)

def get_mean_long_lat(start_date, end_date):
    movement = data_loca[data_loca["timestamp"].between(start_date, end_date)]
    mean_lat = movement.latitude.mean()
    mean_long = movement.longitude.mean()
    return mean_lat, mean_long

start_date = ("2001-11-01T05:00:00Z", "2001-11-30T21:00:00Z")
pos_01_08 = [start_date, ("2008-01-06T20:30:00Z", "2008-03-22T21:48:00Z")]

def get_x_y(pos_list):
    stored_data_x = []
    stored_data_y = []
    for item in pos_list:
        mean_long, mean_lat = get_mean_long_lat(item[0], item[1])
        stored_data_x.append(mean_long)
        stored_data_y.append(mean_lat)
    return stored_data_x, stored_data_y


def get_map(data_x, data_y):
    colors = ['gray', 'lightgreen', 'cadetblue', 'black', 'lightblue', 'darkblue', 
    'blue', 'orange', 'green', 'lightred', 'pink', 'lightgray', 'beige', 
    'darkgreen', 'darkpurple', 'darkred', 'red', 'purple']
    deers = fo.FeatureGroup(name="Deers")
    for i in range(len(data_x)):
        if i % 2 == 0:
            ordi = random.randint(0, len(colors) - 1)
        for j in range(len(data_x[i])):
            deers.add_child(fo.Marker(location=[data_x[i].iloc[j], data_y[i].iloc[j]], icon=fo.Icon(color=colors[ordi])))
    map_deers = fo.Map().add_child(deers)
    map_deers.save("./templates/my_map.html")

list_deer_x = []
list_deer_y = []
for item in datasets:
    list_deer_x.append(item["latitude"])
    list_deer_y.append(item["longitude"])

get_map(list_deer_x, list_deer_y)
# data_mean_x, data_mean_y = get_x_y(pos_01_08)

