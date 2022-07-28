import pandas as pd 
# import data_cleaning

data = pd.read_csv('cross_data_sample.csv')

# data = data_cleaning.generate_freeze_frames(data)
# data = data_cleaning.generate_features(data)

print(data.head())