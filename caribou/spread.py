import pandas as pd

locations = pd.read_csv("./datasets/locations.csv", encoding='unicode_escape', sep=";")
locat_pos = locations[locations["study_site"] == "Kennedy"]
locat_time_2001 = locat_pos[locat_pos['timestamp'].str.match(r'2002.*') == True]
locat_time_2009 = locat_pos[locat_pos['timestamp'].str.match(r'2008.*') == True]
locat_time_2009 = locat_pos[locat_pos['timestamp'].str.match(r'2016.*') == True]


locat_deer = locat_time_2001.groupby('animal_id').timestamp.count().reset_index(name="count")
locat_deer2 = locat_time_2009.groupby('animal_id').timestamp.count().reset_index(name="count")
locat_deer3 = locat_time_2009.groupby('animal_id').timestamp.count().reset_index(name="count")


print(len(locat_deer), len(locat_deer2), len(locat_deer3))
