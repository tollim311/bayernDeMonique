import numpy as np
import json
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import math
import sys


def get_danger_pass(file, output1, output2):
    with open ('StatsBomb/Data/' + file) as t:
        data=json.load(t)

    data=pd.DataFrame(data)

    mask=(data['player'].notnull()) 
    data=data.loc[mask].reset_index(drop=True)

    danger_passes = pd.DataFrame()

    team_name=[]
    team_id=[]
    player_name=[]
    player_id=[]
    n=len(data['team'])

    for i in range(n):
        team_name.append(data['team'][i]["name"])
        team_id.append(data['team'][i]['id'])
        player_name.append(data['player'][i]['name'])
        player_id.append(data['player'][i]['id'])

    data['team_name']=team_name
    data['team_id']=team_id
    data['player_name']=player_name
    data['player_id']=player_id

    mask_pass=(data['pass'].notnull()) 
    data_pass=data.loc[mask_pass].reset_index(drop=True)


    #Take the information about the passes
    #ie the x,y coordonates for start and end, the height and the outcome(0 if incompleted or 1 if completed)
    n=len(data_pass['pass'])
    pass_details_length=[]
    pass_details_angle=[]
    pass_details_endloc_x=[]
    pass_details_endloc_y=[]
    pass_details_loc_x=[]
    pass_details_loc_y=[]
    pass_details_height=[]
    pass_outcome=[]

    for i in range (n):
        if('outcome' in data_pass['pass'][i]):
            pass_outcome.append(0)
        else:
            pass_outcome.append(1)

        pass_details_length.append(data_pass['pass'][i]['length'])
        pass_details_angle.append(data_pass['pass'][i]['angle'])
        pass_details_endloc_x.append(data_pass['pass'][i]['end_location'][0])
        pass_details_endloc_y.append(data_pass['pass'][i]['end_location'][1])
        pass_details_loc_x.append(pass_details_endloc_x[i] - (math.cos(pass_details_angle[i]) *pass_details_length[i]))
        pass_details_loc_y.append(pass_details_endloc_y[i] - (math.sin(pass_details_angle[i]) *pass_details_length[i])) 
        pass_details_height.append(data_pass['pass'][i]['height'])


    data_pass['pass_endloc_x']=pass_details_endloc_x
    data_pass['pass_endloc_y']=pass_details_endloc_y
    data_pass['pass_height']=pass_details_height
    data_pass['pass_loc_x']=pass_details_loc_x
    data_pass['pass_loc_y']=pass_details_loc_y
    data_pass['pass_outcome']=pass_outcome

    colors = list(clr.TABLEAU_COLORS)
    x_arrows=[]
    y_arrows=[]
    end_x_arrows=[]
    end_y_arrows=[]
    arrows_colors=[]

    #Pitch creation
    pitch = Pitch(line_zorder=2, line_color='grey')
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,endnote_height=0.04, title_space=0, endnote_space=0)

    for period in [1, 2]:

        #keep only accurate passes by MCW in this period
        mask_pass = (data_pass.team_id == 746) & (data_pass.pass_outcome==1) & (data_pass.period == period)
        #Only necessary columns
        passes = data_pass.loc[mask_pass, ["pass_loc_x", "pass_loc_y", "pass_endloc_x", "pass_endloc_y", "period", "minute", "second", "player_name"]]

        #keep only Shots by MCW in this period
        mask_shot = (data.team_id == 746) & (data['shot'].notnull()) & (data.period == period)
        shots = data.loc[mask_shot, ["minute", "second"]]
        #convert time to seconds
        shot_times = shots['minute']*60+shots['second']

        #define the time of shot window
        shot_window = 15
        #find starts of the shot window
        shot_start = shot_times - shot_window
        #But the beginning of the period for shot less than 15 seconds after kickoff
        shot_start = shot_start.apply(lambda i: i if i>0 else (period-1)*45)
        #convert to seconds pass times
        pass_times = passes['minute']*60+passes['second']
        #retrieve the pass which is in shot windows
        pass_to_shot = pass_times.apply(lambda x: True in ((shot_start < x) & (x < shot_times)).unique())
        #Retrieve the data of the passes in the window


        passes['time']=pass_times
        danger_passes_period = passes.loc[pass_to_shot].reset_index(drop=True)
        n=len(danger_passes_period['time']) -1
        k=0

        for i in range(n):
            if(danger_passes_period['time'][i] < danger_passes_period['time'][i+1]-15):
                k=k+1
                arrows_colors.append(colors[k])
            else:
                arrows_colors.append(colors[k])


        x_arrows.extend(danger_passes_period['pass_loc_x'])
        y_arrows.extend(danger_passes_period['pass_loc_y'])
        end_x_arrows.extend(danger_passes_period['pass_endloc_x'])
        end_y_arrows.extend(danger_passes_period['pass_endloc_y'])
        pitch.arrows(x_arrows, y_arrows, end_x_arrows, end_y_arrows, color=arrows_colors, ax=ax['pitch'], width=3)

        #concatenate dataframe with a previous one to keep danger passes from the whole tournament
        danger_passes = pd.concat([danger_passes, danger_passes_period])

    plt.savefig(output1)
    plt.close()

    pitch = Pitch(line_zorder=2, line_color='grey')
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,endnote_height=0.04, title_space=0, endnote_space=0)
    #get the 2D histogram
    bin_statistic = pitch.bin_statistic(danger_passes.pass_loc_x, danger_passes.pass_loc_y, statistic='count', bins=(6,5), normalize=False)

    #make a heatmap
    pcm  = pitch.heatmap(bin_statistic, cmap="Reds", edgecolor='grey', ax=ax['pitch'])
    #legend to our plot
    cbar = plt.colorbar(pcm)

    plt.savefig(output2)
    plt.close()
    return(output1, output2)


get_danger_pass('ManCity_Arsenal_events.json', 'arrows.png', 'img.png')