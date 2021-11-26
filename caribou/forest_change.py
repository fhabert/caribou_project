import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dates = np.array([x for x in range(2001, 2008)])
# Calculated through google Earth Engine
forest_data = np.array([5625867781.0, 12337223503.8, 5343288412.3, 7622180761.7, 
                11064384760.0, 6282969315.1, 8206212790.3])
                
def get_forest_years():
    plt.style.use('seaborn')
    plt.plot(dates, forest_data, color="orange", alpha=0.7)
    plt.xlabel('Years')
    plt.ylabel('Forest loss in m²')
    plt.title('Plotting forest loss in terms of time')
    plt.show()

get_forest_years()