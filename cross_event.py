# This file generates the freeze frame df for the passed cross id 
# and then calculates and returns the xG and expected cross probabilities 
# for each potential cross section 

import pandas as pd
from pickle import load
from math import dist
from sklearn.linear_model import LogisticRegression

# zone label mapping 
mapping = {'RF': 0,
          'LF': 1,
          'RB': 2,
          'MB': 3,
          'LB': 4,
          'TOB': 5}

# Identifies the section / zone based on the x,y coordinates 
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


# Generate freeze frame for each cross event, much like you the shot_freeze_frame from shot events 
def create_freeze_frames(match_data, cross_id):
    x_locs, y_locs, origin_sections, freeze_frames, ids, outcomes, end_sections =  [], [], [], [], [], [],[]
    df = match_data[match_data['id'] == cross_id]
    
    frame = []
    for id,row in df.iterrows():
        if row.actor == True:
            x_locs.append(row.location_x[0])
            y_locs.append(row.location_x[1])
            origin_sections.append(mapping[section(row.location_x[0], row.location_x[1])])
            ids.append(row.id)
            outcomes.append(row.pass_outcome)
            end_sections.append(mapping[section(row.pass_end_location[0], row.pass_end_location[1])])
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
        'freeze_frame': freeze_frames, 'id':ids, 'actual_end_zone': end_sections, 'outcome': outcomes}

    input_data = pd.DataFrame(data=d)
    return input_data

# probs 
def get_probs(cross, cross_prob, xG):
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
                # count number of teammates in destination zone 
                if player_x > 90:
                    if player['teammate'] == True:
                        if mapping[section(player_x, player_y)] == cross_dest:
                            tm_count+=1
                    # count number of opponents in destination zone 
                    else:
                        if mapping[section(player_x, player_y)] == cross_dest:
                            opp_count+=1
            
            if tm_count == 0: # consider a zone with NO teammates a bad zone to cross to 
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

    return xG_probs, cross_probs, list(cross.actual_end_zone)[0], list(cross.outcome)[0]