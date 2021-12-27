import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt 
import folium as fo
import json
import math
from scipy.spatial import distance
from scipy.interpolate import make_interp_spline

individuals = pd.read_csv("./datasets/individuals.csv", encoding = 'unicode_escape', sep=";")
locations = pd.read_csv("./datasets/locations.csv", encoding='unicode_escape', sep=";")
temperatures = pd.read_csv("./datasets/temperatures.csv", sep=";")
df_temp = pd.DataFrame(temperatures)
data_indi = pd.DataFrame(individuals)
data_loca = pd.DataFrame(locations)

indi_cardinality = individuals.groupby('study_site').animal_id.size().reset_index(name="count")
loca_hart = locations[locations['study_site'] == "Hart Ranges"]
loca_kennedy = locations[locations['study_site'] == "Kennedy"]

def get_concat_frame(df):
    df['timestamp'] = df.apply(lambda row: row.timestamp[:7], axis=1)

    df_winter = df[df['season'] == 'Winter']
    df_lat = df_winter.groupby(['season', 'timestamp']).latitude.mean().reset_index()
    df_long = df_winter.groupby(['season', 'timestamp']).longitude.mean().reset_index()
    df_winter = df_long.merge(df_lat)

    df_summer = df[df['season'] == 'Summer']
    df_lat = df_summer.groupby(['season', 'timestamp']).latitude.mean().reset_index()
    df_long = df_summer.groupby(['season', 'timestamp']).longitude.mean().reset_index()
    df_summer = df_long.merge(df_lat)

    new_df = pd.concat([df_summer, df_winter], axis=0)
    return new_df

def get_begin_end(df, start_date, end_date):
    df_begin = df[df['timestamp'].str.match(r'{0}'.format(start_date)) == True]
    df_begin['timestamp'] = pd.to_datetime(df_begin['timestamp'])
    df_begin.sort_values(by=['timestamp'], inplace=True, ascending=True)

    df_end = df[df['timestamp'].str.match(r'{0}'.format(end_date)) == True]
    df_end['timestamp'] = pd.to_datetime(df_end['timestamp'])
    df_end.sort_values(by=['timestamp'], inplace=True, ascending=True)
    return df_begin, df_end

def get_map(dataset):
    points = fo.FeatureGroup(name="Points")
    colors = ['lightgreen', 'cadetblue', 'darkgreen', 'purple']
    for i in range(len(dataset)):
        for pos in dataset[i]:
            if pos == dataset[i][0] or pos == dataset[i][-1]:
                points.add_child(fo.Marker(location=[pos[0], pos[1]], icon=fo.Icon(color=colors[i],icon_color='black')))
            else:
                points.add_child(fo.Marker(location=[pos[0], pos[1]], icon=fo.Icon(color=colors[i],icon_color='white')))
    map_deers = fo.Map().add_child(points)
    map_deers.save("./templates/compare.html")


def get_altitudes(points):
    apiKey = "AIzaSyAgz3mB09smlngG2H6psWClIobJZgXxEPA"
    altitudes = []
    for i in range(len(points)):
        alti = []
        for pos in points[i]:
            url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={pos[0]}%2C{pos[1]}&key={apiKey}"
            headers = {"method":'GET'}
            response = requests.request("GET", url, headers=headers)
            response_json = json.loads(response.content)
            elevation = response_json["results"][0]["elevation"]
            alti.append(elevation)
        altitudes.append(alti)
    return altitudes

def distance(value_u, value_v):
    R = 6378
    dif_long = math.radians(value_u[0]) - math.radians(value_v[0])
    dif_lat = math.radians(value_u[0]) - math.radians(value_v[0])
    mean_lat = (math.radians(value_u[1]) + math.radians(value_v[1])) / 2
    right_part = (math.cos(mean_lat)*dif_long)**2
    left_part = dif_lat**2
    distance = round(R*math.sqrt(left_part + right_part), 1)
    return distance


def get_distance(data):
    data['timestamp'] = data.apply(lambda row: row.timestamp[:4], axis=1)
    filter_long = data.groupby(['timestamp']).longitude.mean().reset_index()
    filter_lat = data.groupby(['timestamp']).latitude.mean().reset_index()
    filter_merge = filter_long.merge(filter_lat)
    distances = []
    for i in range(len(filter_merge)-1):
        lat1 = filter_merge.iloc[i]['latitude']
        long1 = filter_merge.iloc[i]['longitude']
        lat2 = filter_merge.iloc[i+1]['latitude']
        long2 = filter_merge.iloc[i+1]['longitude']
        point1 = (lat1, long1)
        point2 = (lat2, long2)
        dis = distance(point1, point2)
        distances.append(dis)
    lat1 = filter_merge.iloc[-2]['latitude']
    long1 = filter_merge.iloc[-2]['longitude']
    lat2 = filter_merge.iloc[-1]['latitude']
    long2 = filter_merge.iloc[-1]['longitude']
    point1 = (lat1, long1)
    point2 = (lat2, long2)
    dis = distance(point1, point2)
    distances.append(dis)
    return distances

hart = get_concat_frame(loca_hart)
kennedy = get_concat_frame(loca_kennedy)

hart_start, hart_stop = get_begin_end(hart, 1989, 2006)
kennedy_start, kennedy_stop = get_begin_end(kennedy, 2003, 2015)

hart_pos_s = []
hart_pos_e = []
for i in range(len(hart_start)):
    line_hart = hart_start.iloc[i]
    hart_pos_s.append((line_hart['latitude'], line_hart['longitude']))
for i in range(len(hart_stop)):
    line_ken = hart_stop.iloc[i]
    hart_pos_e.append((line_ken['latitude'], line_ken['longitude']))

ken_pos_s = []
ken_pos_e = []
for i in range(len(kennedy_start)):
    line_hart = kennedy_start.iloc[i]
    ken_pos_s.append((line_hart['latitude'], line_hart['longitude']))
for i in range(len(kennedy_stop)):
    line_ken = kennedy_stop.iloc[i]
    ken_pos_e.append((line_ken['latitude'], line_ken['longitude']))

# total_points = [hart_pos_s, hart_pos_e, ken_pos_s, ken_pos_e]
# total_years = [hart_start.timestamp.tolist(), hart_stop.timestamp.tolist(), kennedy_start.timestamp.tolist(), kennedy_stop.timestamp.tolist()]
altitudes = get_altitudes(total_points)

def get_alti_graph(alti, years):
    years_string = []
    for li in years:
        years_st = []
        for item in li:
            years_st.append(str(item)[5:7])
        years_string.append(years_st)

    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(18, 5))
    ax[0,0].plot(years_string[0], alti[0], label="Hart Ranges Begin", color="orange")
    ax[0,1].plot(years_string[1], alti[1], label="Hart Ranges End", color="blue")
    ax[1,0].plot(years_string[2], alti[2], label="Kennedy Begin", color="red")
    ax[1,1].plot(years_string[3], alti[3], label="Kennedy End", color="green")

    ax[0, 0].set_xlabel('1989')
    ax[0, 0].set_ylabel('Elevation (m)')
    ax[0, 0].set_title("Hart Ranges herd")

    ax[0, 1].set_xlabel('2006')
    ax[0, 1].set_ylabel('Elevation (m)')
    ax[0, 1].set_title("Hart Ranges herd")

    ax[1, 0].set_xlabel('2003')
    ax[1, 0].set_ylabel('Elevation (m)')
    ax[1, 0].set_title("Kennedy herd")

    ax[1, 1].set_xlabel('2015')
    ax[1, 1].set_ylabel('Elevation (m)')
    ax[1, 1].set_title("Kennedy herd")
    plt.savefig("./images/comparison.png")
    plt.show()

data_hart_distance = hart.loc[(hart['timestamp'] >= '2002') & (hart['timestamp'] <= '2006')]
data_ken_distance = kennedy.loc[(kennedy['timestamp'] >= '2002') & (kennedy['timestamp'] <= '2016')]
hart_dis = get_distance(data_hart_distance)
ken_dis = get_distance(data_ken_distance)
# print(sum(hart_dis))
# forest_data = [16.7, 17.1, 26.6, 31.1, 30, 38, 40, 32, 23, 22, 17, 29, 20, 21]
# hart_forest = [16.7, 17.1, 26.6, 31.1]
# years = [x for x in range(2002, 2006)]

# fig, ax1 = plt.subplots() 
# ax1.set_title("Analysis of the impact of deforestation on the distance travelled")
# ax1.set_xlabel('Years') 
# ax1.set_ylabel('Distance travelled (km)', color = 'blue') 
# ax1.plot(years, hart_dis, color = 'blue') 
# ax1.tick_params(axis='y', labelcolor = 'blue') 
# ax2 = ax1.twinx()  
# ax2.set_ylabel('Deforestation in kha', color = 'green') 
# ax2.plot(years, hart_forest, color = 'green') 
# ax2.tick_params(axis ='y', labelcolor = 'green') 

# plt.savefig("./images/defo_hart.png")
# plt.show()



# fig1, ax1 = plt.subplots(nrows=2, ncols=1, figsize=(18, 5))
# ax1[0].plot(years, hart_dis, label="Hart Ranges Begin", color="orange")
# ax1[1].plot(years, forest_data, label="Hart Ranges Begin", color="green")
# ax1[0].set_xlabel('Years')
# ax1[0].set_ylabel('Distance in km')
# ax1[0].set_title("Distance of Kennedy herd")

# ax1[1].set_xlabel('Years')
# ax1[1].set_ylabel('Deforestation in m²')
# ax1[1].set_title("Deforestation in Fraser-Fort George")
# plt.show()

# total_val = [ken_dis, forest_data]
# colors = ["orange", "blue"]
# for i in range(len(total_val)):
#     np_years = np.array(years)
#     np_spread = np.array(total_val[i])
#     X_Y_Spline = make_interp_spline(np_years, np_spread)
#     X_Final = np.linspace(2002, 2016, 10)
#     Y_Final = X_Y_Spline(X_Final)
#     plt.plot(X_Final, Y_Final, color=colors[i], alpha=0.7)
# plt.show()



# plt.plot(years, hart_dis, color="orange", alpha=0.8)
# plt.plot(years, ken_dis, color="blue", alpha=0.8)
# plt.plot(years, forest_data, color="green")
# plt.show()

# get_alti_graph(altitudes, total_years)
# get_map(total_points)

