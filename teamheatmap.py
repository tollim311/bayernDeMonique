import json
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import numpy as np
from scipy.ndimage import gaussian_filter

data=[]
with open('Data/MCI Womens/MCI Womens Files/g2312135_SecondSpectrum_tracking-produced.jsonl','r') as f:
    for line in f:
        data.append(json.loads(line))
with open('Data/MCI Womens/MCI Womens Files/g2312135_SecondSpectrum_meta.json','r') as t:
    datamatch=json.load(t)
longueurTerrain=datamatch['pitchLength']
largeurTerrain=datamatch['pitchWidth']
nbFrames=len(data)
team=input("Which team? 1 for home/2 for away")
playerpositionx=[]
playerpositiony=[]
homegoalkeeper=[]
awaygoalkeeper=[]
for i in range(0,len(datamatch['homePlayers'])):
    if datamatch['homePlayers'][i]['position']=="GK":
        homegoalkeeper.append(int(datamatch['homePlayers'][i]['number']))
for i in range(0,len(datamatch['awayPlayers'])):
    if datamatch['awayPlayers'][i]['position']=="GK":
        awaygoalkeeper.append(int(datamatch['awayPlayers'][i]['number']))
print(homegoalkeeper,awaygoalkeeper)


for j in range(0,nbFrames):
    if team=="1":
        for i in range (0,len(data[j]['homePlayers'])):
            if data[j]['homePlayers'][i]['number'] not in homegoalkeeper:
                if data[j]["period"]==1:
                    playerpositionx.append(data[j]['homePlayers'][i]['xyz'][0])
                    playerpositiony.append(data[j]['homePlayers'][i]['xyz'][1])
                else: 
                    playerpositionx.append(-data[j]['homePlayers'][i]['xyz'][0])
                    playerpositiony.append(-data[j]['homePlayers'][i]['xyz'][1])
    elif team=="2":
        for i in range (0,len(data[j]['awayPlayers'])):
            if data[j]['awayPlayers'][i]['number'] not in homegoalkeeper:
                if data[j]["period"]==1:
                    playerpositionx.append(data[j]['awayPlayers'][i]['xyz'][0])
                    playerpositiony.append(data[j]['awayPlayers'][i]['xyz'][1])
                else: 
                    playerpositionx.append(-data[j]['awayPlayers'][i]['xyz'][0])
                    playerpositiony.append(-data[j]['awayPlayers'][i]['xyz'][1])

pitch = Pitch(pitch_type='secondspectrum', line_zorder=2,
              pitch_length=longueurTerrain, pitch_width=largeurTerrain,
              pitch_color='green', line_color='#efefef')
# draw
fig, ax = pitch.draw(figsize=(6.6, 4.125))
fig.set_facecolor('#22312b')
bin_statistic = pitch.bin_statistic(np.array(playerpositionx),np.array(playerpositiony), statistic='count', bins=(25, 25))
bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'], 1)
pcm = pitch.heatmap(bin_statistic, ax=ax, cmap='hot', edgecolors='#22312b')
# Add the colorbar and format off-white
cbar = fig.colorbar(pcm, ax=ax, shrink=0.6)
cbar.outline.set_edgecolor('#efefef')
cbar.ax.yaxis.set_tick_params(color='#efefef')
ticks = plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#efefef')

plt.show()