import json
import time
import matplotlib.pyplot as plt
import time as time

#data to read a game in 2D
#create by matthieu
data=[]
with open('Data/MCI Womens/MCI Womens Files/g2312135_SecondSpectrum_tracking-produced.jsonl','r') as f:
    for line in  f:
        data.append(json.loads(line))
with open('Data/MCI Womens/MCI Womens Files/g2312135_SecondSpectrum_meta.json','r') as t:
    datamatch=json.load(t)
longueurTerrain=datamatch['pitchLength']
largeurTerrain=datamatch['pitchWidth']
nbFrames=len(data)
for j in range(0,nbFrames):
    plt.clf()
    for i in range (0,len(data[j]['homePlayers'])):
        plt.scatter(data[j]['homePlayers'][i]['xyz'][0],data[j]['homePlayers'][i]['xyz'][1],color="blue",marker="x")
    for i in range (0,len(data[j]['awayPlayers'])):
        plt.scatter(data[j]['awayPlayers'][i]['xyz'][0],data[j]['awayPlayers'][i]['xyz'][1],color="red",marker="x")
    plt.plot([-longueurTerrain/2,+longueurTerrain/2],[-largeurTerrain/2,-largeurTerrain/2],color="black",lw=1)
    plt.plot([-longueurTerrain/2,+longueurTerrain/2],[+largeurTerrain/2,+largeurTerrain/2],color="black",lw=1)
    plt.plot([-longueurTerrain/2,-longueurTerrain/2],[-largeurTerrain/2,+largeurTerrain/2],color="black",lw=1)
    plt.plot([+longueurTerrain/2,+longueurTerrain/2],[-largeurTerrain/2,+largeurTerrain/2],color="black",lw=1)
    plt.scatter(data[j]['ball']['xyz'][0],data[j]['ball']['xyz'][1],color="grey",marker="o")
    temps=45*(data[j]['period']-1)+data[j]['gameClock']/60
    tempsmin=int(temps)
    tempssec=int((temps-tempsmin)*60)
    plt.figtext(0.9, 0.7,tempsmin)
    plt.figtext(0.92,0.7,':')
    plt.figtext(0.93,0.7,tempssec)
    plt.pause(10e-5)
plt.xlim=(-longueurTerrain/2-5,longueurTerrain/2+5)
plt.ylim=(-largeurTerrain/2-5,largeurTerrain/2+5)
plt.show()