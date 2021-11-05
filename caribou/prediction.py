import pandas as pd
import main
import folium as fo
from sklearn.linear_model import LinearRegression
import visualisation as vs

test = 2030

df = pd.DataFrame(main.locations)
dataset = vs.lat_long
years = [[x] for x in range(2001, 2011)]
sample_lat = [item[1]for item in dataset]
sample_long = [item[0] for item in  dataset]

def get_linear_regression(years_data, sample):
    line_fitter = LinearRegression()
    line_fitter.fit(years_data, sample)
    fonc = [line_fitter.coef_[0], line_fitter.intercept_]
    predict = test * fonc[0] + fonc[1]
    return predict

predict_loca = [get_linear_regression(years, sample_long), get_linear_regression(years, sample_lat)]

def get_map_predict(dataset):
    deers_predict = fo.FeatureGroup(name="DeerPredict")
    colors = ['gray', 'lightgreen', 'cadetblue']
    for i in range(len(dataset)):
        deers_predict.add_child(fo.Marker(location=[dataset[i][1], dataset[i][0]], icon=fo.Icon(color=colors[i])))
    map_deers = fo.Map().add_child(deers_predict)
    map_deers.save("./templates/prediction.html")

data = [dataset[0], dataset[-1], predict_loca]
get_map_predict(data)