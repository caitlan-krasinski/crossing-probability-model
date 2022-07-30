# general imports
import pandas as pd 
import matplotlib.pyplot as plt

# football imports
from statsbombpy import sb
from mplsoccer import Pitch, VerticalPitch

# function imports
import data_retrieval as dr
import cross_event as cross
import plotting_functions as plot

# ui imports
import streamlit as st


matches = sb.matches(competition_id=55, season_id=43)
matches = matches[matches['match_status_360'] == 'available'].sort_values(by=['match_date'])

match_names = []

for id, row in matches.iterrows():
    match_id = row.match_id
    match = matches[matches['match_id'] == match_id]
    display_name = f'{list(match.home_team)[0]} v. {list(match.away_team)[0]} - {list(match.match_date)[0]} (match_id: {list(match.match_id)[0]})'
    match_names.append(display_name)

# title
st.sidebar.title('Cross Probability Tool')

# match dropdown
match_option = st.sidebar.selectbox('Select match', match_names)

selected_match_id = match_option.split('match_id: ')[1].strip(')')

# cross_id dropdown 
match_data = dr.get_match_data(selected_match_id)
cross_ids = match_data.id.unique()
cross_option = st.sidebar.selectbox('Select cross', cross_ids)

# weight sliders
risk_weight = st.sidebar.slider('risk tolerance', min_value=0.0, max_value=1.0, value=0.5, step=0.05)

# process cross
data_freeze_frame = cross.create_freeze_frames(match_data, cross_option)
xG_probs, cross_probs = cross.get_probs(data_freeze_frame)

# determine optimal destination zone for cross  
maximum = 0
optimal_zone = 0
optimal_probs = []

for zone in cross_probs.keys():
    obj = cross_probs[zone] + (risk_weight)*xG_probs[zone] #+ reward_weight*xG_probs[zone] 
    print(obj)
    if maximum < obj:
        maximum = obj
        optimal_zone = zone 
        optimal_probs = [cross_probs[zone], xG_probs[zone]]

# draw and output plot 
if optimal_probs != []:
    st.write(f'Cross probability: {optimal_probs[0]}')
    st.write(f'xG gain from completed cross: {optimal_probs[1]}')

    # plot
    cross_plot = plot.generate_plot(data_freeze_frame, optimal_zone, cross_probs, xG_probs)
    st.pyplot(cross_plot)
else:
    st.write(f'Model did not identify a desirable cross')


st.write('''Welcome to the Cross Probability Tool! This tool was built to 
help coaching staff analyze and identify optimal cross locations based on their risk tolerance. Feel free to 
browse historical games and flip through different cross events.''')
st.write('''If, as a coach, you prefer to make the sure bets to keep possesion, you may input your risk tolerance 
lower so that the optimization model knows you value completed crosses over potential high rewards. Conversely, if you are a 
risk-taker and value a potential high reward, you would input a higher risk tolerance. Each output shows the probability 
of a successful cross and the corresponding xG if that cross is a success. This model assumes that crosses are made to 
generate scoring chances, thus the reward in this model is xG. Since crosses are often made to space,
 the optimal zone is highlighted to identify which cross is ideal given the user's risk tolerance.''')