import json
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import numpy as np

def meanspeed(list,indice):
    sum=0
    for i in range(100):
        sum+=list[indice+i]
    return(sum/100)

def get_sprint(file,output1,output2):
    data=[]
    with open('Data/'+file+'_SecondSpectrum_tracking-produced.jsonl','r') as f:
        for line in f:
            data.append(json.loads(line))
    with open('Data/'+file+'_SecondSpectrum_meta.json','r') as t:
        datamatch=json.load(t)
    longueurTerrain=datamatch['pitchLength']
    largeurTerrain=datamatch['pitchWidth']
    nbFrames=len(data)
    speeddata=[]
    numberhighintensity=0
    teamsname=datamatch['description']
    label1=teamsname[0:5]
    label2=teamsname[8:13]


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

    playersshirt=[]
    playerssprint=[]
    for i in range (len(sprint)):
        if sprint[i][2]!=0:
            playersshirt.append(str(sprint[i][1]))
            playerssprint.append(sprint[i][2])
    plt.bar(playersshirt,playerssprint)
    plt.suptitle("Number of high intensity sprint of "+label1+" players", x=0.5,fontsize=20)
    plt.xlabel(label1+"players")
    plt.ylabel("Number of high intensity sprint")
    plt.savefig(output1)
    plt.close()

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

    playersshirt=[]
    playerssprint=[]
    for i in range (len(sprint)):
        if sprint[i][2]!=0:
            playersshirt.append(str(sprint[i][1]))
            playerssprint.append(sprint[i][2])
    plt.bar(playersshirt,playerssprint)
    plt.suptitle("Number of high intensity sprint of "+label2+" players", x=0.5,fontsize=20)
    plt.xlabel(label2+"players")
    plt.ylabel("Number of high intensity sprint")
    plt.savefig(output2)
    plt.close()
    return(output1,output2)
