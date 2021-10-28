import numpy as np
import matplotlib.pyplot as plt
import random
import folium as fo
import main
import pandas as pd

loca = main.data_loca
points_2001 = loca[loca["timestamp"].str.match(r'2001.*') == True]
points_2013 = loca[loca["timestamp"].str.match(r'2013.*') == True]

deers_pos = { 
    "deer_2001_winter" : [points_2001[points_2001["season"] == "Winter"]["latitude"].iloc[0:50], points_2001[points_2001["season"] == "Winter"]["longitude"].iloc[0:50], "orange"],
    "deer_2001_summer" : [points_2001[points_2001["season"] == "Summer"]["latitude"].iloc[0:50], points_2001[points_2001["season"] == "Summer"]["longitude"].iloc[0:50], "orange"],
    "deer_2013_winter" : [points_2013[points_2013["season"] == "Winter"]["latitude"].iloc[0:50], points_2013[points_2013["season"] == "Winter"]["longitude"].iloc[0:50], "cadetblue"],
    "deer_2013_summer" : [points_2013[points_2013["season"] == "Summer"]["latitude"].iloc[0:50], points_2013[points_2013["season"] == "Summer"]["longitude"].iloc[0:50], "cadetblue"]
}

def get_map_interval(dataset):
    deers_interval = fo.FeatureGroup(name="DeersInterval")
    for item in dataset:
        for j in range(len(dataset[item][0])):
            deers_interval.add_child(fo.Marker(location=[dataset[item][0].iloc[j], dataset[item][1].iloc[j]], icon=fo.Icon(color=dataset[item][2])))
    map_deers = fo.Map().add_child(deers_interval)
    map_deers.save("./templates/map_interval.html")

# get_map_interval(deers_pos)

