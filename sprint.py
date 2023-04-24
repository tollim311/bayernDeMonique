import json
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import numpy as np

def meanspeed(list,indice):
    sum=0
    for i in range(100):
        sum+=list[indice+i]
    return(sum/100)

def get_teamhighintensitysprint(file,output1,output2):
    data=[]
    with open('Data/MCI Womens/MCI Womens Files/'+file+'_SecondSpectrum_tracking-produced.jsonl','r') as f:
        for line in f:
            data.append(json.loads(line))
    with open('Data/MCI Womens/MCI Womens Files/'+file+'_SecondSpectrum_meta.json','r') as t:
        datamatch=json.load(t)
    longueurTerrain=datamatch['pitchLength']
    largeurTerrain=datamatch['pitchWidth']
    nbFrames=len(data)
    team=input("Which team? 1 for home/2 for away")
    speeddata=[]
    numberhighintensity=0
    if team=="1":
            sprint=[[0,0]for i in range(len(datamatch['homePlayers']))]
            for i in range(0,len(datamatch['homePlayers'])):
                numberhighintensity=0
                speeddata=[]
                sprint[i][0]=datamatch['homePlayers'][i]["name"]
                shirtnumber=datamatch['homePlayers'][i]["number"]
                sprint[i][1]=shirtnumber
                for j in range(0,nbFrames):
                    for z in range (0,len(data[j]['homePlayers'])):
                        if data[j]['homePlayers'][z]['number']==shirtnumber:
                            speeddata.append(data[j]['homePlayers'][z]['speed']*3.6)
                k=0
                while k<=(len(speeddata)-100):
                    if meanspeed(speeddata,k)>20:
                        numberhighintensity+=1
                        k+=100
                    else:
                        k+=1
                sprint[i].append(numberhighintensity)
    elif team=="2":
            sprint=[[0,0]for i in range(len(datamatch['awayPlayers']))]
            for i in range(0,len(datamatch['awayPlayers'])):
                numberhighintensity=0
                speeddata=[]
                sprint[i][0]=datamatch['awayPlayers'][i]["name"]
                shirtnumber=datamatch['awayPlayers'][i]["number"]
                sprint[i][1]=shirtnumber
                for j in range(0,nbFrames):
                    for z in range (0,len(data[j]['awayPlayers'])):
                        if data[j]['awayPlayers'][z]['number']==shirtnumber:
                            speeddata.append(data[j]['awayPlayers'][z]['speed']*3.6)
                k=0
                while k<=(len(speeddata)-100):
                    if meanspeed(speeddata,k)>20:
                        numberhighintensity+=1
                        k+=100
                    else:
                        k+=1
                sprint[i].append(numberhighintensity)

    playersname=[]
    playerssprint=[]
    for i in range (len(sprint)):
        if sprint[i][2]!=0:
            playersname.append(sprint[i][0])
            playerssprint.append(sprint[i][2])
    plt.bar(playersname,playerssprint)
    plt.show()