import pandas as pd
import folium
import random


data = "./datasets/canada_pos.csv"
state_data = pd.read_csv(data, encoding = 'unicode_escape', sep=";")
df = pd.DataFrame(state_data)
df_state = state_data[['Geographic name, english', 'Geographic code', 'Provincial / territory abbreviation, english']]
array_defo = [random.randint(0, 500) for _ in range(len(df))]
df_state["Deforestation"] = array_defo
df_state = df_state.rename(columns={"Geographic name, english": "Name"})
m = folium.Map(location=[48, -102], zoom_start=3)

folium.Choropleth(
    geo_data=array_defo,
    name="choropleth",
    data=array_defo,
    columns=["State", "Unemployment"],
    key_on="feature.id",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Unemployment Rate (%)",
).add_to(m)

folium.LayerControl().add_to(m)
m.save("./templates/chloro.html")
