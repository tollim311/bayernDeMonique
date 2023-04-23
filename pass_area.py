import numpy as np
import json
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt
import math
import sys

files=sys.argv[1]

with open (files) as t:
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

#Create a df with the pass and their caracteristics in penalty area
mask_area_pass=(df_pass_MCW['pass_endloc_x'] > 102) & (df_pass_MCW['pass_endloc_y'] > 18) & (df_pass_MCW['pass_endloc_y'] < 62)
df_area_pass_MCW=df_pass_MCW.loc[mask_area_pass].reset_index(drop=True)

y_limit_zone=[0,18,40,62,80]
x_limit_zone=[60,102,120]
n=len(df_area_pass_MCW['pass'])
completed_zone=[0,0,0,0,0,0,0]
total_zone=[0,0,0,0,0,0,0]

ending_completed_zone=[0,0]
ending_total_zone=[0,0]

#Count the number of pass in each area and the number of completed ones
for i in range(n):
    if (df_area_pass_MCW['pass_loc_x'][i]>60 and df_area_pass_MCW['pass_loc_x'][i]<102):
        if(df_area_pass_MCW['pass_loc_y'][i]>0 and df_area_pass_MCW['pass_loc_y'][i]<=18):
            completed_zone[0]=completed_zone[0]+df_area_pass_MCW['pass_outcome'][i]
            total_zone[0]=total_zone[0]+1
        elif(df_area_pass_MCW['pass_loc_y'][i]>18 and df_area_pass_MCW['pass_loc_y'][i]<=40):
            completed_zone[1]=completed_zone[1]+df_area_pass_MCW['pass_outcome'][i]
            total_zone[1]=total_zone[1]+1
        elif(df_area_pass_MCW['pass_loc_y'][i]>40 and df_area_pass_MCW['pass_loc_y'][i]<62):
            completed_zone[2]=completed_zone[2]+df_area_pass_MCW['pass_outcome'][i]
            total_zone[2]=total_zone[2]+1
        elif(df_area_pass_MCW['pass_loc_y'][i]>62 and df_area_pass_MCW['pass_loc_y'][i]<80):
            completed_zone[3]=completed_zone[3]+df_area_pass_MCW['pass_outcome'][i]
            total_zone[3]=total_zone[3]+1
        else:
            completed_zone[6]=completed_zone[6]+df_area_pass_MCW['pass_outcome'][i]
            total_zone[6]=total_zone[6]+1

    elif(df_area_pass_MCW['pass_loc_x'][i]>=102 and df_area_pass_MCW['pass_loc_x'][i]<120):
        if(df_area_pass_MCW['pass_loc_y'][i]>0 and df_area_pass_MCW['pass_loc_y'][i]<18):
            completed_zone[4]=completed_zone[4]+df_area_pass_MCW['pass_outcome'][i]
            total_zone[4]=total_zone[4]+1
        elif(df_area_pass_MCW['pass_loc_y'][i]>62 and df_area_pass_MCW['pass_loc_y'][i]<80):
            completed_zone[5]=completed_zone[5]+df_area_pass_MCW['pass_outcome'][i]
            total_zone[5]=total_zone[5]+1
        else:
            completed_zone[6]=completed_zone[6]+df_area_pass_MCW['pass_outcome'][i]
            total_zone[6]=total_zone[6]+1

    else:
        completed_zone[6]=completed_zone[6]+df_area_pass_MCW['pass_outcome'][i]
        total_zone[6]=total_zone[6]+1

    if(df_area_pass_MCW['pass_endloc_y'][i]<40):
        ending_completed_zone[0]=ending_completed_zone[0]+np.abs(df_area_pass_MCW['pass_outcome'][i]-1)
        ending_total_zone[0]=ending_total_zone[0]+1
    else:
        ending_completed_zone[1]=ending_completed_zone[1]+np.abs(df_area_pass_MCW['pass_outcome'][i]-1)
        ending_total_zone[1]=ending_total_zone[1]+1

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

#Plot the number of pass through the penalty area by area and label the accuracy in each area
for i in range (4):
    if(total_zone[i]!=0):
        pitch.scatter(81, (y_limit_zone[i]+y_limit_zone[i+1])/2, alpha = 0.6, s=(completed_zone[i]/total_zone[i])*10000, color='lightblue', ax=ax['pitch'])
        pitch.annotate(str(completed_zone[i])+"/"+str(total_zone[i]), xy=(81, (y_limit_zone[i]+y_limit_zone[i+1])/2), c='black', va='center', ha='center', weight = "bold", size=16, ax=ax["pitch"], zorder = 4)

for i in range(2):
    if(ending_total_zone[i]!=0):
        pitch.scatter(111, (y_limit_zone[i+1]+y_limit_zone[i+2])/2, alpha = 0.6, s=(ending_completed_zone[i]/ending_total_zone[i])*10000, color='gold', ax=ax['pitch'])
        pitch.annotate(str(ending_completed_zone[i])+"/"+str(ending_total_zone[i]), xy=(111, (y_limit_zone[i+1]+y_limit_zone[i+2])/2), c='black', va='center', ha='center', weight = "bold", size=16, ax=ax["pitch"], zorder = 4)
    if(total_zone[4+i]!=0):
        pitch.scatter(111, (y_limit_zone[3*i]+y_limit_zone[3*i+1])/2, alpha = 0.6, s=(completed_zone[4+i]/total_zone[4+i])*10000, color='lightblue', ax=ax['pitch'])
        pitch.annotate(str(completed_zone[4+i])+"/"+str(total_zone[4+i]), xy=(111, (y_limit_zone[3*i]+y_limit_zone[3*i+1])/2), c='black', va='center', ha='center', weight = "bold", size=16, ax=ax["pitch"], zorder = 4)

pitch.annotate("Blue : the pass through the box\nGold : the pass reiceves in the box\n Diameter of the circle represents the accuracy", xy=(30,10), c='black', va='center', ha='center', weight = "bold", size=16, ax=ax["pitch"], zorder = 4)
fig.suptitle("passes through penalty area by area on pitch and their success in the box", fontsize=25)
plt.savefig('plot_ball_through_surface.png')
plt.close()
