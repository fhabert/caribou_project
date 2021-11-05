import numpy as np
import matplotlib.pyplot as plt
import folium as fo
import main
import pandas as pd
import math
import requests
import json

loca = main.data_loca
points_2001 = loca[loca["timestamp"].str.match(r'2001.*') == True]
points_2013 = loca[loca["timestamp"].str.match(r'2016.*') == True]
temperatures = pd.read_csv("./datasets/temperatures.csv", sep=";")
df = pd.DataFrame(temperatures)
deers_individuals = main.deers_id
years_appart = [f'{x}-{x+1}' for x in range(2001, 2011)]
deers_pos = { 
    "deer_2001_winter" : [points_2001[points_2001["season"] == "Winter"]["latitude"].iloc[0:50], points_2001[points_2001["season"] == "Winter"]["longitude"].iloc[0:50], "orange"],
    "deer_2001_summer" : [points_2001[points_2001["season"] == "Summer"]["latitude"].iloc[0:50], points_2001[points_2001["season"] == "Summer"]["longitude"].iloc[0:50], "darkpurple"],
    "deer_2013_winter" : [points_2013[points_2013["season"] == "Winter"]["latitude"].iloc[0:50], points_2013[points_2013["season"] == "Winter"]["longitude"].iloc[0:50], "cadetblue"],
    "deer_2013_summer" : [points_2013[points_2013["season"] == "Summer"]["latitude"].iloc[0:50], points_2013[points_2013["season"] == "Summer"]["longitude"].iloc[0:50], "beige"]
}
temp_years = [x for x in range(2001, 2013)]

def get_temp_mean(li_years):
    temp = []
    for i in range(len(li_years)-1):
        select_year = df[df["dt_iso"].between(str(li_years[i]), str(li_years[i+1]))]
        mean_temp = select_year.mean(skipna=False)
        temp.append(round(mean_temp.temp, 2))
    return temp

def temp_wt_years(tp, li_years):
    plt.plot(li_years, tp)
    plt.xlabel('Years')
    plt.ylabel('Mean temperatures')
    plt.title('Temperatures')
    plt.show()
    pass

def euclidean_distance(pt1, pt2):
  distance = 0
  for i in range(len(pt1)):
    distance += (pt1[i] - pt2[i]) ** 2
  return distance ** 0.5

def get_map_interval(dataset):
    deers_interval = fo.FeatureGroup(name="DeersInterval")
    for item in dataset:
        for j in range(len(dataset[item][0])):
            deers_interval.add_child(fo.Marker(location=[dataset[item][0].iloc[j], dataset[item][1].iloc[j]], icon=fo.Icon(color=dataset[item][2])))
    map_deers = fo.Map().add_child(deers_interval)
    map_deers.save("./templates/map_interval.html")


def get_distance_mean(years):
    dis_years = []
    distance_calculated = []
    for i in range(len(years)-2):
        sample = loca[loca['timestamp'].between(str(years[i]), str(years[i + 2]))]
        mean_long = round(sample['longitude'].mean(), 5)
        mean_lat = round(sample['latitude'].mean(), 5)
        dis_years.append([mean_long, mean_lat])
    for i in range(len(dis_years)-1):
        dis = euclidean_distance(dis_years[i], dis_years[i+1])
        distance_calculated.append(dis)
    dis = euclidean_distance(dis_years[-2], dis_years[-1])
    distance_calculated.append(dis)
    return dis_years, distance_calculated

def bar_plot(distances, years):
    plt.bar(years, distances)
    plt.xlabel('Years')
    plt.ylabel('Relative distance')
    plt.title('Distance in terms of coordinates for caribou')
    plt.show()

def scatter_plot(data_x, data_y, xlabel, ylabel):
    plt.scatter(data_x, data_y)
    plt.xlabel(f'{xlabel}')
    plt.ylabel(f'{ylabel}')
    plt.title(f'{xlabel} in relation to the {ylabel}')
    plt.show()

def log_data(distances, temp):
    ln_dis = []
    ln_temp = []
    for i in range(len(distances)):
        if distances[i] > 0 and temp[i] > 0:
            ln_dis.append(math.log(distances[i]))
            ln_temp.append(math.log(temp[i]))
    return ln_dis, ln_temp


def get_altitudes(lati_longi):
    apiKey = "AIzaSyAgz3mB09smlngG2H6psWClIobJZgXxEPA"
    altitudes = []
    for item in lati_longi:
        url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={item[1]}%2C{item[0]}&key={apiKey}"
        headers = {"method":'GET'}
        response = requests.request("GET", url, headers=headers)
        response_json = json.loads(response.content)
        altitudes.append(response_json["results"][0]["elevation"])
    return altitudes


lat_long, dis_means = get_distance_mean(temp_years)
# bar_plot(dis_means, years_appart)
# temp_means = get_temp_mean(temp_years)
# scatter_plot(temp_means, temp_years[:-1], 'Temperature', 'Years Apart')
# dis_ln, temp_ln = log_data(dis_means, temp_means)
# dis_wt_temp(dis_means, temp_means)
# get_map_interval(deers_pos)
# altitudes_points = get_altitudes(lat_long)
# scatter_plot(years_appart, altitudes_points, "Years Apart", "Altitude")
