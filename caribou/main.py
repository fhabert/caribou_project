import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt 
import folium as fo
import random
import math

individuals = pd.read_csv("./datasets/individuals.csv", encoding = 'unicode_escape', sep=";")
locations = pd.read_csv("./datasets/locations.csv", encoding='unicode_escape', sep=";")
temperatures = pd.read_csv("./datasets/temperatures.csv", sep=";")
df_temp = pd.DataFrame(temperatures)
data_indi = pd.DataFrame(individuals)
data_loca = pd.DataFrame(locations)

def presentation():
    print(individuals.head(), locations.head(), locations.describe())
    print(locations.head(), locations.head(), locations.describe())
    print(df_temp.head(), df_temp.head(), df_temp.describe())

individuals_w_start = data_indi[data_indi["deploy_on_longitude"].notnull()]
individual_good = individuals_w_start[data_indi["deploy_off_longitude"].notnull()]

deers_id = individual_good["animal_id"]
datasets = []
counter = 0
dates = []
for name in deers_id:
    temp_dataset = data_loca[data_loca["animal_id"] == name]
    temp_dataset['timestamp'] = pd.to_datetime(temp_dataset['timestamp'])
    data_sorted = temp_dataset.sort_values(by="timestamp")
    if len(temp_dataset) > 680:   #to get specificaly 20 caribou for the length of colors
        counter += 1
        dates.append([data_sorted.timestamp.min(), data_sorted.timestamp.max()])
        datasets.append(temp_dataset.head())
        datasets.append(temp_dataset.tail())

# maximum = dates[0][1] - dates[0][0]
# index = 0
# for i in range(len(dates)):
#     if (dates[i][1] - dates[i][0]) > maximum:
#         maximum = dates[i][1] - dates[i][0]
#         index = i
# deers_id_list = deers_id.tolist()
# print(dates[index], index)

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
    'darkpurple', 'darkred', 'darkgreen', 'purple']
    deers = fo.FeatureGroup(name="Deers")
    for i in range(len(data_x)):
        if i % 2 == 0:
            ordi = random.randint(0, len(colors) - 1)
        for j in range(len(data_x[i])):
            if i == 10:
                deers.add_child(fo.Marker(location=[data_x[i].iloc[j], data_y[i].iloc[j]], icon=fo.Icon(color='red')))
            else:
                deers.add_child(fo.Marker(location=[data_x[i].iloc[j], data_y[i].iloc[j]], icon=fo.Icon(color=colors[ordi])))
    map_deers = fo.Map().add_child(deers)
    map_deers.save("./templates/my_map.html")


def get_map_all(titles):
    colors_deer = ['gray', 'lightgreen', 'cadetblue', 'black', 'lightblue', 'darkblue', 'blue', 'orange']
    for i in range(len(titles)):
        data = locations[locations["study_site"] == titles[i]]
        data_x = data.latitude.tolist()
        data_y = data.longitude.tolist()
        deers_group = fo.FeatureGroup(name="Deers Site study")
        for j in range(1000):
            deers_group.add_child(fo.Marker(location=[data_x[j], data_y[j]], icon=fo.Icon(color=colors_deer[i])))
    map_group = fo.Map().add_child(deers_group)
    map_group.save("./templates/group_study.html")

list_deer_x = []
list_deer_y = []
for item in datasets:
    list_deer_x.append(item["latitude"])
    list_deer_y.append(item["longitude"])

# group = locations.groupby('study_site').event_id.count().reset_index(name="count")
# titles = group.study_site.tolist()
# get_map_all(titles)

get_map(list_deer_x, list_deer_y)
# data_mean_x, data_mean_y = get_x_y(pos_01_08)

# presentation()
# print(locations.columns.tolist(), individuals.columns.tolist(), temperatures.columns.tolist())