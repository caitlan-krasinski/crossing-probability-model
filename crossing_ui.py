# general imports
import pandas as pd 
import matplotlib.pyplot as plt
from pickle import load

# football imports
from statsbombpy import sb
from mplsoccer import Pitch, VerticalPitch

# function imports
import data_retrieval as dr
import cross_event as cross
import plotting_functions as plot

# ui imports
import streamlit as st


# title
st.sidebar.title('Cross Probability Tool')

# tournament dropdown
gender_option = st.sidebar.selectbox('Select tournament', ["2020 Men's Euro", "2022 Women's Euro"])

if gender_option == "2020 Men's Euro":
    comp_id = 55
    s_id = 43
    # load models
    cross_prob = load(open("models/cross_model.pkl",'rb'))
    xG = load(open("models/xG_historical_probs.pkl",'rb'))
else:
    comp_id = 53
    s_id = 106
    # load models
    cross_prob = load(open("models/cross_model_womens_euros.pkl",'rb'))
    xG = load(open("models/xG_historical_probs_womens_euros.pkl",'rb'))


matches = sb.matches(competition_id=comp_id, season_id=s_id)
matches = matches[matches['match_status_360'] == 'available'].sort_values(by=['match_date'])

match_names = []

for id, row in matches.iterrows():
    match_id = row.match_id
    match = matches[matches['match_id'] == match_id]
    display_name = f'{list(match.home_team)[0]} v. {list(match.away_team)[0]} - {list(match.match_date)[0]} (match_id: {list(match.match_id)[0]})'
    match_names.append(display_name)

# match dropdown
match_option = st.sidebar.selectbox('Select match', match_names)

selected_match_id = match_option.split('match_id: ')[1].strip(')')

# get match data 
match_data = dr.get_match_data(selected_match_id)

# team dropdown
team_select = st.sidebar.selectbox('Select Team', list(match_data.team.unique()))

# convert cross_ids to descriptive events
team_data = match_data[match_data['team'] == team_select].sort_values(by=['timestamp'])

desc_to_id = {}
for cross_id in team_data.id.unique():
    row = team_data[team_data['id'] == cross_id].iloc[0]
    description = f'{row.player} ({row.timestamp})'
    desc_to_id[description] = row.id

cross_option = st.sidebar.selectbox('Select cross', desc_to_id.keys())
cross_id = desc_to_id[cross_option]

# weight sliders
risk_weight = st.sidebar.slider('risk tolerance', min_value=0.0, max_value=1.0, value=0.5, step=0.05)

# process cross
data_freeze_frame = cross.create_freeze_frames(match_data, cross_id)
xG_probs, cross_probs, actual_end_zone, actual_outcome = cross.get_probs(data_freeze_frame, cross_prob, xG)

# determine optimal destination zone for cross  
maximum = 0
optimal_zone = 0
optimal_probs = []

for zone in cross_probs.keys():
    obj = cross_probs[zone] + (risk_weight - 0.2)*xG_probs[zone]
    if maximum < obj:
        maximum = obj
        optimal_zone = zone 
        optimal_probs = [cross_probs[zone], xG_probs[zone]]

st.write(f'**{cross_option}**')
# draw and output plot 
if optimal_probs != []:
    if actual_outcome == 'Incomplete':
        st.write(f'Actual cross outcome: Incomplete')
    else: 
        st.write(f'Actual cross outcome: Completed')
    # st.write(f'**Predicted cross values:**')
    # st.write(f'Cross probability: {optimal_probs[0]}')
    # st.write(f'xG gain from completed cross: {optimal_probs[1]}')

    # plot
    cross_plot = plot.generate_plot(data_freeze_frame, optimal_zone, cross_probs, xG_probs, actual_end_zone)
    st.pyplot(cross_plot)
else:
    st.write(f'Model did not identify a desirable cross')


st.write('''Welcome to the Cross Probability Tool! This tool was built to 
help coaching staff analyze and identify optimal cross locations based on their risk tolerance. The zone highlighted in red indicates 
the predicted/suggested optimal zone, the zone highlighted in blue is where the cross was actually made to, and if the zone 
is purple it indicates the cross was made to the predicted zone.''')
st.write('''If, as a coach, you prefer to make the sure bets to keep possesion, you may input your risk tolerance 
lower so that the optimization model knows you value completed crosses over potential high rewards. Conversely, if you are a 
risk-taker and value a potential high reward, you would input a higher risk tolerance. Each output shows the probability 
of a successful cross and the corresponding xG if that cross is a success. This model assumes that crosses are made to 
generate scoring chances, thus the reward in this model is xG. Since crosses are often made to space,
 the optimal zone is highlighted to identify which cross is ideal given the user's risk tolerance.''')
st.write('''Note that the model only suggests a cross destination if there is support in that zone (ie: at least one teammate)''')
