import pandas as pd 
import numpy as np

def section(x,y):
    if (x <= 60 and y <= 18) or (x >= 60 and y >= 62):
        return 'RF'
    elif (x <= 60 and y >= 62) or (x >= 60 and y <= 18):
        return 'LF'
    elif (x <= 18 and 18 <= y <= 30) or (x >= 102 and 50 <= y <= 62):
        return 'RB'
    elif (x <= 18 and 30 <= y <= 50) or (x >= 102 and 30 <= y <= 50):
        return 'MB'
    elif (x <= 18 and 50 <= y <= 62) or (x >= 102 and 18 <= y <= 30):
        return 'LB'
    elif (18 <= x <= 60 and 18 <= y <= 62) or (60 <= x <= 102 and 18 <= y <= 62):
        return 'TOB'

mapping = {'RF': 0,
          'LF': 1,
          'RB': 2,
          'MB': 3,
          'LB': 4,
          'TOB': 5}

def generate_freeze_frames(cross_df):
    data_freeze_frame = pd.DataFrame()
    outcomes = []
    loc_xs = []
    loc_ys = []
    x_end_locations = []
    y_end_locations = []
    freeze_frames=  []

    for i in cross_df.id.unique():
        df = cross_df[cross_df['id'] == i]
        
        frame = []
        for id,row in df.iterrows():
            if row.actor == True:
                outcomes.append(row.pass_outcome)
                loc_xs.append(row.location_x[0])
                loc_ys.append(row.location_x[1])
                x_end_locations.append(row.pass_end_location[0])
                y_end_locations.append(row.pass_end_location[1])
            else:
                freeze_frame = {}
                freeze_frame['location'] = row.location_x
                freeze_frame['player'] = {'name': row.player}
                freeze_frame['position'] = {'name': row.position}
                freeze_frame['teammate'] = row.teammate
                frame.append(freeze_frame)
        freeze_frames.append(frame)

    print(len(outcomes), len(locations), len(end_locations), len(freeze_frames))    
    data_freeze_frame['loc_x'] = loc_xs
    data_freeze_frame['loc_y'] = loc_ys
    data_freeze_frame['cross_end_loc_x'] = x_end_locations
    data_freeze_frame['cross_end_loc_y'] = y_end_locations
    data_freeze_frame['freeze_frame'] = freeze_frames
    data_freeze_frame['outcome'] = outcomes
    print(data_freeze_frame.head())
    data_freeze_frame[['loc_x', 'loc_y']] = data_freeze_frame['location'].apply(pd.Series)
    data_freeze_frame[['cross_end_loc_x', 'cross_end_loc_y']] = data_freeze_frame['pass_end_location'].apply(pd.Series)
    data_freeze_frame = data_freeze_frame[['loc_x', 'loc_y', 'cross_end_loc_x', 'cross_end_loc_y', 'freeze_frame', 'outcome']]

    return data_freeze_frame

# def generate_features(data_freeze_frame):
#     outcomes = []
#     origin_sections = []
#     destination_sections = []
#     opp_in_dest = []
#     tm_in_dest = []
#     pressures = []

#     for id, row in data_freeze_frame.iterrows():
#         if row.outcome in ['Incomplete', 'Out']: outcomes.append(0)
#         else: outcomes.append(1)
        
#         cross_x = row.loc_x
#         cross_y = row.loc_y
        
#         destination = section(row.cross_end_loc_x, row.cross_end_loc_y)

#         origin_sections.append(mapping[section(cross_x, cross_y)])
#         destination_sections.append(mapping[destination])        
        
#         opp_count = 0
#         tm_count = 0
#         pressure = 0
        
#         for player in row.freeze_frame:
#             player_x = player['location'][0]
#             player_y = player['location'][1]
            
#             #count how many opponents are within 3 yards of player making the cross
#             if ((cross_x - player_x)**2 + (cross_y - player_y)**2) <= 3**2 and (player['teammate'] == False) and (player['position']['name'] != 'Goalkeeper'):
#                 pressure += 1
            
#             if player['teammate'] == True:
#                 if section(player_x, player_y) == destination:
#                     tm_count+=1
#             else:
#                 if section(player_x, player_y) == destination:
#                     opp_count+=1
                    
#         opp_in_dest.append(opp_count)
#         tm_in_dest.append(tm_count)
#         pressures.append(pressure)
                
#     data_freeze_frame['outcome'] = outcomes
#     data_freeze_frame['cross_origin'] = origin_sections
#     data_freeze_frame['cross_dest'] = destination_sections
#     data_freeze_frame['zone_pressure'] = opp_in_dest # num opp in dest zone
#     data_freeze_frame['zone_support'] = tm_in_dest # num teammates in dest zone 
#     data_freeze_frame['cross_pressure'] = pressures # num of opp on crosser