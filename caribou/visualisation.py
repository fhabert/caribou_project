import numpy as np
import matplotlib.pyplot as plt
import folium as fo
import main
import pandas as pd
import math
import requests
import json
import statsmodels.api as sms


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

def euclidean_distance(value_u, value_v):
    R = 6378
    dif_long = math.radians(value_u[0]) - math.radians(value_v[0])
    dif_lat = math.radians(value_u[0]) - math.radians(value_v[0])
    mean_lat = (math.radians(value_u[1]) + math.radians(value_v[1]))/2
    right_part = (math.cos(mean_lat)*dif_long)**2
    left_part = dif_lat**2
    distance = round(R*math.sqrt(left_part + right_part), 1)
    return distance


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
    dis_years_separated = []
    for i in range(len(years)-2):
        sample_test = loca[loca['timestamp'].between(str(years[i]), str(years[i + 2]))]
        sample = sample_test[sample_test['study_site'] == "Graham"]
        sample_winter = sample[sample["season"] == "Winter"]
        sample_summer = sample[sample["season"] == "Summer"]
        dis_years_separated.append([round(sample_winter['longitude'].mean(), 5), round(sample_winter['latitude'].mean(), 5)])
        dis_years_separated.append([round(sample_summer['longitude'].mean(), 5), round(sample_summer['latitude'].mean(), 5)])
        mean_long = round(sample['longitude'].mean(), 8)
        mean_lat = round(sample['latitude'].mean(), 8)
        dis_years.append([mean_long, mean_lat])
    for i in range(len(dis_years)-1):
        dis = euclidean_distance(dis_years[i], dis_years[i+1])
        distance_calculated.append(round(dis, 2))
    return dis_years, distance_calculated, dis_years_separated

def bar_plot(distances, years):
    plt.bar(years, distances)
    plt.xlabel('Years')
    plt.ylabel('Relative distance')
    plt.title('Distance in terms of coordinates for caribou')
    plt.show()

def scatter_plot(data_x, data_y, xlabel, ylabel):
    print(data_x, data_y)
    plt.scatter(data_x, data_y, color="orange")
    plt.xlabel(f'{xlabel}')
    plt.ylabel(f'{ylabel}')
    plt.title(f'Impact of deforestation on the movement from Burnt Pine herd')
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
        elevation = response_json["results"][0]["elevation"]
        altitudes.append(elevation)
    return altitudes


def get_altitudes_season(lati_longi):
    apiKey = "AIzaSyAgz3mB09smlngG2H6psWClIobJZgXxEPA"
    altitudes_winter = []
    altitudes_summer = []
    for i in range(len(lati_longi)):
        url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={lati_longi[i][1]}%2C{lati_longi[i][0]}&key={apiKey}"
        headers = {"method":'GET'}
        response = requests.request("GET", url, headers=headers)
        response_json = json.loads(response.content)
        elevation = response_json["results"][0]["elevation"]
        if i % 2 == 0:
            altitudes_winter.append(elevation)
        else:
            altitudes_summer.append(elevation)
    return altitudes_winter, altitudes_summer

lat_long, dis_means, lat_long_season = get_distance_mean(temp_years)
forest_data = np.array([5625867781.0, 12337223503.8, 5343288412.3, 7622180761.7, 
                11064384760.0, 6282969315.1, 8206212790.3])
print(len(forest_data), len(dis_means))
scatter_plot(forest_data, dis_means[:-2], "Deforestation (m²)", "Distance travelled (km)")
# temp_means = get_temp_mean(temp_years)
# print(lat_long_season)
# scatter_plot(temp_means, temp_years[:-1], 'Temperature', 'Years Apart')
# dis_ln, temp_ln = log_data(dis_means, temp_means)
# scatter_plot(dis_means, temp_means[:-1], 'Relative distance', 'Temperature (°C)')
# get_map_interval(deers_pos)
# altitudes_points = get_altitudes(lat_long)
# altitudes_winter, altitudes_summer = get_altitudes_season(lat_long_season)
# mean_sum = sum(altitudes_summer) / len(altitudes_summer)
# mean_win = sum(altitudes_winter) / len(altitudes_winter)
# print(mean_sum)
# print(mean_win)

# plt.clf()
# plt.scatter(years_appart, altitudes_summer, color="b", label='summer', alpha=0.7)
# plt.scatter(years_appart, altitudes_winter, color="orange", label='winter', alpha=0.7)
# plt.legend(loc='lower left')
# plt.xlabel("Years")
# plt.ylabel("ALtitude of the fields (m)")
# plt.title("The influence of the seasons on the field altitude of the deer")
# plt.show()

# print(temperatures.describe())

# def get_description_regression(data_x, data_y):
#     X_values = sms.add_constant(dis_means)
#     regression_model_a = sms.OLS(temp_means[:-1], X_values)
#     regression_model_b = regression_model_a.fit()
#     print(regression_model_b.summary())
#     print("gradient  =", regression_model_b.params[1])
#     print("intercept =", regression_model_b.params[0])
#     print("Rsquared  =", regression_model_b.rsquared)
#     print("MSE       =", regression_model_b.mse_resid)
#     print("pvalue    =", regression_model_b.f_pvalue)
