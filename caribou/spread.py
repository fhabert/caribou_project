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
icon_colors = ["white", "black"]

years_df = pd.DataFrame(years, columns=["years"])
counter = 0
for year in years:
    distances_sum = []
    locations_time = locations[locations["timestamp"].str.match(r'{0}'.format(year)) == True]
    location_q = locations_time[locations_time["study_site"] == "Quintette"]
    location_b = locations_time[locations_time["study_site"] == "Burnt Pine"]
    locations_place = [location_q, location_b]
    for i in range(len(locations_place)):
        if len(locations_place[i]) != 0:
            if i % 2 == 0:
                color_icon = icon_colors[0]
            else:
                color_icon = icon_colors[1]
            deer_lat_mean = locations_place[i].groupby('animal_id').latitude.mean().reset_index()
            deer_long_mean = locations_place[i].groupby('animal_id').longitude.mean().reset_index()
            deers = deer_lat_mean.merge(deer_long_mean)
            for j in range(len(deers)):
                fo.Marker(location=[deers.iloc[j][1], deers.iloc[j][2]], icon=fo.Icon(color=colors[counter], icon_color=color_icon), popup=f"{year},{deers.iloc[j][0]}").add_to(deers_spread)
                dist_temp = []
                for k in range(len(deers)):
                    dist = distance.euclidean([deers.iloc[k][1], deers.iloc[k][2]], [deers.iloc[k][1], deers.iloc[k][2]])
                    dist_temp.append(dist)
                distances_sum.append(sum(dist_temp))
            whole_mean = sum(distances_sum) / len(distances_sum)
            deer_spread[year] = whole_mean
    counter += 1
deers_spread.save("./templates/points_spread.html")

# def get_spread_graph():
#     for _, value in deer_spread.items():
#         spread_value.append(value)

#     np_years = np.array(years)
#     np_spread = np.array(spread_value)
#     X_Y_Spline = make_interp_spline(np_years, np_spread)
#     X_Final = np.linspace(2001, 2014, 500)
#     Y_Final = X_Y_Spline(X_Final)

#     plt.plot(X_Final, Y_Final, color="orange", alpha=0.7)
#     plt.xlabel("Years")
#     plt.ylabel("Spread relative value")
#     plt.title("Understanding the inner spread of the herd between each year")
#     plt.show()