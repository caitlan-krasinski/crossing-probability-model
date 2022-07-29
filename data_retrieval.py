from statsbombpy import sb
import pandas as pd 

def get_match_data(match_id):
    cols = ['teammate', 'actor', 'keeper', 'location_x', 'id',
        'player', 'position', 'team', 'type', 'timestamp', 
        'pass_end_location', 'pass_outcome', 'pass_cross', 
        'interception_outcome', 'pass_aerial_won', 'visible_area']

    events = sb.events(match_id=match_id)
    match_frames = sb.frames(match_id=match_id, fmt='dataframe')

    # join the events to the frames 
    df = pd.merge(match_frames, events, left_on='id', right_on='id', how='left')

    # take relevant rows 
    df = df[cols]

    # filter for crosses only
    cross_df = df[df['pass_cross'] == True]
    
    return cross_df