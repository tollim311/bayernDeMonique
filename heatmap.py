import json
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import pandas as pd

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
numeromaillot=input("Which player's heatmap do you want to see?")
playerpositionx=[]
playerpositiony=[]
numeromaillot=int(numeromaillot)
for j in range(0,nbFrames):
    if team=="1":
        for i in range (0,len(data[j]['homePlayers'])):
            if data[j]['homePlayers'][i]['number']==numeromaillot:
                playerpositionx.append(data[j]['homePlayers'][i]['xyz'][0])
                playerpositiony.append(data[j]['homePlayers'][i]['xyz'][1])
    elif team=="2":
        for i in range (0,len(data[j]['awayPlayers'])):
            if data[j]['awayPlayers'][i]['number']==numeromaillot:
                playerpositionx.append(data[j]['awayPlayers'][i]['xyz'][0])
                playerpositiony.append(data[j]['awayPlayers'][i]['xyz'][1])

df = pd.DataFrame({'x': playerpositionx, 'y': playerpositiony})
print(df)
pitch = Pitch(pitch_type='statsbomb', half=True)
fig, ax = pitch.draw()
pitch.heatmap(df, ax=ax, cmap='hot', edgecolors='#22312b')
pitch.lines(ax=ax)
pitch.goal_left(ax=ax)
pitch.goal_right(ax=ax)

plt.show()