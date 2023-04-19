import numpy as np
import json
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt
import math

with open ('StatsBomb/Data/ManCity_Arsenal_events.json') as t:
    data=json.load(t)

data=pd.DataFrame(data)

#Select the Man City pass only
team_name=[]
team_id=[]
n=len(data['team'])

for i in range(n):
    team_name.append(data['team'][i]["name"])
    team_id.append(data['team'][i]['id'])

data['team_name']=team_name
data['team_id']=team_id

mask_pass_MCW=(data['pass'].notnull()) & (data.team_id == 746)

df_pass_MCW = data.loc[mask_pass_MCW]
df_pass_MCW = df_pass_MCW.reset_index(drop=True)

#Take the information about the passes
#ie the x,y coordonates for start and end, the height and the outcome(0 if incompleted or 1 if completed)
n=len(df_pass_MCW['pass'])
pass_details_length=[]
pass_details_angle=[]
pass_details_endloc_x=[]
pass_details_endloc_y=[]
pass_details_loc_x=[]
pass_details_loc_y=[]
pass_details_height=[]
pass_outcome=[]

for i in range (n):
    if('outcome' in df_pass_MCW['pass'][i]):
        pass_outcome.append(0)
    else:
        pass_outcome.append(1)

    pass_details_length.append(df_pass_MCW['pass'][i]['length'])
    pass_details_angle.append(df_pass_MCW['pass'][i]['angle'])
    pass_details_endloc_x.append(df_pass_MCW['pass'][i]['end_location'][0])
    pass_details_endloc_y.append(df_pass_MCW['pass'][i]['end_location'][1])
    pass_details_loc_x.append(pass_details_endloc_x[i] - (math.cos(pass_details_angle[i]) *pass_details_length[i]))
    pass_details_loc_y.append(pass_details_endloc_y[i] - (math.sin(pass_details_angle[i]) *pass_details_length[i])) 
    pass_details_height.append(df_pass_MCW['pass'][i]['height'])


df_pass_MCW['pass_endloc_x']=pass_details_endloc_x
df_pass_MCW['pass_endloc_y']=pass_details_endloc_y
df_pass_MCW['pass_height']=pass_details_height
df_pass_MCW['pass_loc_x']=pass_details_loc_x
df_pass_MCW['pass_loc_y']=pass_details_loc_y
df_pass_MCW['pass_outcome']=pass_outcome

#Create a df with the pass and their caracteristics
mask_area_pass=(df_pass_MCW['pass_endloc_x'] > 102) & (df_pass_MCW['pass_endloc_y'] > 18) & (df_pass_MCW['pass_endloc_y'] < 62)
df_area_pass_MCW=df_pass_MCW.loc[mask_area_pass].reset_index(drop=True)

#Select the completed pass
mask_completed=(df_area_pass_MCW['pass_outcome']==1)
df_area_pass_MCW_completed=df_area_pass_MCW.loc[mask_completed].reset_index(drop=True)

#Select the incompleted pass
mask_incompleted=(df_area_pass_MCW['pass_outcome']==0)
df_area_pass_MCW_incompleted=df_area_pass_MCW.loc[mask_incompleted].reset_index(drop=True)

#Create a pitch as a graph
pitch = Pitch(line_color = "black")
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False, 
                      endnote_height=0.04, title_space=0, endnote_space=0)
#Circle for the pass
#pitch.scatter(df_seger.x, df_seger.y, alpha = 0.7, s=100, color='blue', ax=ax['pitch'])


#Just a vizualition test
#Arrows for the direction and length of Pass
pitch.arrows(df_area_pass_MCW_completed.pass_loc_x, df_area_pass_MCW_completed.pass_loc_y, df_area_pass_MCW_completed.pass_endloc_x, df_area_pass_MCW_completed.pass_endloc_y,width=3, color='blue', ax=ax['pitch'])
pitch.arrows(df_area_pass_MCW_incompleted.pass_loc_x, df_area_pass_MCW_incompleted.pass_loc_y, df_area_pass_MCW_incompleted.pass_endloc_x, df_area_pass_MCW_incompleted.pass_endloc_y,width=3, color='red', ax=ax['pitch'])
fig.suptitle("passes through penlaty area", fontsize=25)
plt.show()
