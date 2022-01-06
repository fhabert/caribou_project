import pandas as pd
import folium as fo
from sklearn.linear_model import LinearRegression
import requests
import json

test = 2020

locations = pd.read_csv("./datasets/locations.csv", encoding='unicode_escape', sep=";")
df = pd.DataFrame(locations)
loca_hart = df[df['study_site'] == "Hart Ranges"]
loca_hart['timestamp'] = loca_hart.apply(lambda row: row.timestamp[:4], axis=1)
hart_lat = loca_hart.groupby(['timestamp']).latitude.mean().reset_index()
hart_long = loca_hart.groupby(['timestamp']).longitude.mean().reset_index()
hart_merge = hart_lat.merge(hart_long)
years = [[1988],[1989],[1990],[1991],[1992],[2002],[2003],[2004],[2005],[2006], [2007]]
pos_lat = []
pos_long = []

for i in range(len(hart_merge)):
    pos_lat.append([hart_merge.iloc[i]['latitude']])
    pos_long.append([hart_merge.iloc[i]['longitude']])

def get_linear_regression(years_data, sample):
    line_fitter = LinearRegression()
    line_fitter.fit(years_data, sample)
    fonc = [line_fitter.coef_[0], line_fitter.intercept_]
    predict = test * fonc[0] + fonc[1]
    return predict


predict_lat = get_linear_regression(years, pos_lat)
predict_long = get_linear_regression(years, pos_long)
predicted_point = (predict_lat, predict_long)

first_point = (hart_merge.iloc[0]['latitude'], hart_merge.iloc[0]['longitude'])
last_point = (hart_merge.iloc[-1]['latitude'], hart_merge.iloc[-1]['longitude'])

print(predicted_point)
def get_map_predict(fp, lp, pp):
    points = [fp, lp,  pp]
    deers_predict = fo.FeatureGroup(name="DeerPredict")
    colors = ['gray', 'lightgreen', 'cadetblue']
    for i in range(len(points)):
        deers_predict.add_child(fo.Marker(location=[points[i][0], points[i][1]], icon=fo.Icon(color=colors[i])))
    map_deers = fo.Map().add_child(deers_predict)
    map_deers.save("./templates/prediction.html")

def get_altitudes(lati_longi):
    url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={lati_longi[1]}%2C{lati_longi[0]}&key={apiKey}"
    headers = {"method":'GET'}
    response = requests.request("GET", url, headers=headers)
    response_json = json.loads(response.content)
    elevation = response_json["results"][0]["elevation"]
    return elevation


# get_map_predict(first_point, last_point, predicted_point)