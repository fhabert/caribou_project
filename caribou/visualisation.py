import numpy as np
import matplotlib.pyplot as plt
import folium as fo
import main
import pandas as pd

loca = main.data_loca
points_2001 = loca[loca["timestamp"].str.match(r'2001.*') == True]
points_2013 = loca[loca["timestamp"].str.match(r'2013.*') == True]
temperatures = pd.read_csv("./datasets/temperatures.csv", sep=";")
df = pd.DataFrame(temperatures)
deers_individuals = main.deers_id
years_appart = [f'{x}-{x+1}' for x in range(2001, 2010)]

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
    return distance_calculated

def dis_wt_years(distances, years):
    plt.bar(years, distances)
    plt.xlabel('Years')
    plt.ylabel('Relative distance')
    plt.title('Distance in terms of coordinates for caribou')
    plt.show()
    pass

# dis_means = get_distance_mean(temp_years)
# dis_wt_years(dis_means, years_appart)
# temp_means = get_temp_mean(temp_years)
# temp_wt_years(temp_means, temp_years[:-1])
# get_map_interval(deers_pos)


