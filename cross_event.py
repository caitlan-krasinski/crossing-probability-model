import pandas as pd
from pickle import load
from math import dist
from sklearn.linear_model import LogisticRegression


# load models
cross_prob = load(open("models/cross_model.pkl",'rb'))
xG = load(open("models/xG_historical_probs.pkl",'rb'))

mapping = {'RF': 0,
          'LF': 1,
          'RB': 2,
          'MB': 3,
          'LB': 4,
          'TOB': 5}

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


def create_freeze_frames(match_data, cross_id):
    x_locs, y_locs, origin_sections, freeze_frames, ids =  [], [], [], [], []
    df = match_data[match_data['id'] == cross_id]
    
    frame = []
    for id,row in df.iterrows():
        if row.actor == True:
            x_locs.append(row.location_x[0])
            y_locs.append(row.location_x[1])
            origin_sections.append(mapping[section(row.location_x[0], row.location_x[1])])
            ids.append(row.id)
        else:
            freeze_frame = {}
            freeze_frame['location'] = row.location_x
            freeze_frame['player'] = {'name': row.player}
            if row.keeper == True: freeze_frame['position'] = {'name': 'Goalkeeper'}
            else: freeze_frame['position'] = {'name': ''} # no pos data on non-actors
            freeze_frame['teammate'] = row.teammate
            frame.append(freeze_frame)
    freeze_frames.append(frame)
    
    d = {'loc_x': x_locs, 'loc_y': y_locs, 'origin_section': origin_sections,
        'freeze_frame': freeze_frames, 'id':ids }

    input_data = pd.DataFrame(data=d)
    return input_data

def get_probs(cross):
    cross_probs = {}
    xG_probs = {}
    for zone in mapping.values():
        if zone == list(cross.origin_section)[0]:
            continue
        else:
            cross_x = list(cross.loc_x)[0]
            cross_y = list(cross.loc_y)[0]
            cross_dest = zone
            tm_count, opp_count, pressure = 0,0,0
            
            for player in list(cross.freeze_frame)[0]:
                player_x = player['location'][0]
                player_y = player['location'][1]
            
                #count how many opponents are within 3 yards of player making the cross
                if ((cross_x - player_x)**2 + (cross_y - player_y)**2) <= 3**2 and (player['teammate'] == False) and (player['position']['name'] != 'Goalkeeper'):
                    pressure += 1
            
                if player['teammate'] == True:
                    if mapping[section(player_x, player_y)] == cross_dest:
                        tm_count+=1
                else:
                    if mapping[section(player_x, player_y)] == cross_dest:
                        opp_count+=1
            
            if tm_count == 0: # consider a zone with no teammates a bad zone to cross to 
                xG_probs[zone] = 0
                cross_probs[zone] = 0
            else:
                cross_features = [cross_y, cross_dest, opp_count, tm_count, pressure]
                pred = round(cross_prob.predict_proba([cross_features])[0][1],3)
                cross_probs[zone] = pred
                if opp_count <= 1: i=0         # 0 or 1 opps in zone
                elif 2 <= opp_count <= 3: i=1  # 2 or 3 opps in zone
                else: i=2                      # more than 3 opps in zone
                xG_probs[zone] = round(xG[i][cross_dest] / sum(xG[i]),3)

    return xG_probs, cross_probs