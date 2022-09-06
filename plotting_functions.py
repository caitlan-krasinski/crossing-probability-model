# this file draws the plot for the specified cross event 

from mplsoccer import Pitch, VerticalPitch

# coordinates according statsbomb specified coordinates 
right_zone_coordinates = {0: [[102,62], [102,80], [120,80], [120,62]],
                    1: [[102,0], [102,18], [120,18], [120,0]],
                    2: [[102,50], [102,62], [120,62], [120,50]],
                    3: [[102,30], [102,50], [120,50], [120,30]],
                    4: [[102,18], [102,30], [120,30], [120,18]],
                    5: [[102,18],[102,62],[90,62],[90,18]]}

left_zone_coordinates = {0: [[0,0], [0,18], [18,18], [18,0]],
                    1: [[0,62], [0,80], [18,80], [18,62]],
                    2: [[0,18], [0,30], [18,30], [18,18]],
                    3: [[0,30], [0,50], [18,50], [18,30]],
                    4: [[0,50], [0,62], [18,62], [18,50]],
                    5: [[18,18],[18,62],[30,62],[30,18]]}

label_coordinates = {0: [111,71],
                    1: [111,9],
                    2: [111,56],
                    3: [111,40],
                    4: [111,24],
                    5: [93,40]}

# draw plot 
def generate_plot(cross, optimal_zone, cross_probs, xG_probs, actual_end_zone):
    pitch = Pitch()

    fig, ax = pitch.draw(figsize=(10,8))

    # plot players 
    for player in list(cross.freeze_frame)[0]:
        if player['teammate']:
            pitch.scatter(player['location'][0], player['location'][1], c='blue',  ax=ax)
        else:
            pitch.scatter(player['location'][0], player['location'][1], c='red',  ax=ax)


    # plot cross event 
    pitch.scatter(list(cross.loc_x)[0], list(cross.loc_y)[0], marker='football', edgecolors= "blue",
                        s=100, ax=ax, label='passer', zorder=1.2)

    # plot sections
    if 60 - list(cross.loc_x)[0] > 0:
        pitch.polygon([left_zone_coordinates[optimal_zone]], color=(1, 0, 0, 0.3), ax=ax ) # optimal section 
        for zone in cross_probs.keys():
            pitch.polygon([left_zone_coordinates[zone]], edgecolor='red', ax=ax )
        pitch.polygon([left_zone_coordinates[actual_end_zone]], edgecolor='blue', ax=ax )
    else:
        pitch.polygon([right_zone_coordinates[optimal_zone]], edgecolor='red', linewidth=1, color=(1, 0, 0, 0.3), ax=ax )
        for zone in cross_probs.keys():
            pitch.polygon([right_zone_coordinates[zone]], color=(1, 0, 0,0), ec='red', linewidth=1, ax=ax )
        pitch.polygon([right_zone_coordinates[actual_end_zone]], color=(0, 0, 1, 0.25), ax=ax)

    # plot data labels 
    for zone in cross_probs.keys():
        ax.annotate(cross_probs[zone], (label_coordinates[zone][0], label_coordinates[zone][1]))
        if xG_probs[zone] != 0:
            ax.annotate(f'xG: {xG_probs[zone]}', (label_coordinates[zone][0]-2, label_coordinates[zone][1]+3))

    return fig