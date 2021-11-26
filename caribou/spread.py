import numpy as np
import matplotlib.pyplot as plt
import folium as fo
import pandas as pd
import branca
import json
from scipy.spatial import distance
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline


individuals = pd.read_csv("./datasets/individuals.csv", encoding = 'unicode_escape', sep=";")
locations = pd.read_csv("./datasets/locations.csv", encoding='unicode_escape', sep=";")
data_indi = pd.DataFrame(individuals)
data_loca = pd.DataFrame(locations)

sample = locations.iloc[:15000]
deer_spread = {}
years = [x for x in range(2001, 2015)]
spread_value = []

deers_spread = fo.Map(name="DeerSpread")
colors = ['gray', 'lightgreen', 'cadetblue', 'black', 'lightblue', 'darkblue', 
    'blue', 'orange', 'green', 'lightred', 'pink', 'lightgray', 'beige', 
    'darkpurple']

years_df = pd.DataFrame(years, columns=["years"])
counter = 0
for year in years:
    distances_sum = []
    locations_time = locations[locations["timestamp"].str.match(r'{0}'.format(year)) == True]
    if len(locations_time) != 0:
        deer_lat_mean = locations_time.groupby('animal_id').latitude.mean().reset_index()
        deer_long_mean = locations_time.groupby('animal_id').longitude.mean().reset_index()
        deers = deer_lat_mean.merge(deer_long_mean)
        for i in range(len(deers)):
            fo.Marker(location=[deers.iloc[i][1], deers.iloc[i][2]], icon=fo.Icon(color=colors[counter]), popup=f"{year},{deers.iloc[i][0]}").add_to(deers_spread)
            dist_temp = []
            for j in range(len(deers)):
                dist = distance.euclidean([deers.iloc[i][1], deers.iloc[i][2]], [deers.iloc[j][1], deers.iloc[j][2]])
                dist_temp.append(dist)
            distances_sum.append(sum(dist_temp))
        whole_mean = sum(distances_sum) / len(distances_sum)
        deer_spread[year] = whole_mean
    counter += 1
deers_spread.save("./templates/points_spread.html")


def get_spread_graph():
    for _, value in deer_spread.items():
        spread_value.append(value)

    np_years = np.array(years)
    np_spread = np.array(spread_value)
    X_Y_Spline = make_interp_spline(np_years, np_spread)
    X_Final = np.linspace(2001, 2014, 500)
    Y_Final = X_Y_Spline(X_Final)

    plt.plot(X_Final, Y_Final, color="orange", alpha=0.7)
    plt.xlabel("Years")
    plt.ylabel("Spread relative value")
    plt.title("Understanding the inner spread of the herd between each year")
    plt.show()


