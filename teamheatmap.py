import json
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import numpy as np
from scipy.ndimage import gaussian_filter

def get_teamheatmap(file,output1,output2):
    data=[]
    with open('Data/'+file+'_SecondSpectrum_tracking-produced.jsonl','r') as f:
        for line in f:
            data.append(json.loads(line))

    with open('Data/'+file+'_SecondSpectrum_meta.json','r') as t:
        datamatch=json.load(t)
        
    longueurTerrain=datamatch['pitchLength']
    largeurTerrain=datamatch['pitchWidth']
    teamsname=datamatch['description']
    nbFrames=len(data)
    playerpositionx1=[]
    playerpositiony1=[]
    playerpositionx2=[]
    playerpositiony2=[]
    homegoalkeeper=[]
    awaygoalkeeper=[]
    for i in range(0,len(datamatch['homePlayers'])):
        if datamatch['homePlayers'][i]['position']=="GK":
            homegoalkeeper.append(int(datamatch['homePlayers'][i]['number']))
    for i in range(0,len(datamatch['awayPlayers'])):
        if datamatch['awayPlayers'][i]['position']=="GK":
            awaygoalkeeper.append(int(datamatch['awayPlayers'][i]['number']))
    label1=''
    label2=''
    for j in range(0,nbFrames):
        label1=teamsname[0:5]
        for i in range (0,len(data[j]['homePlayers'])):
            if data[j]['homePlayers'][i]['number'] not in homegoalkeeper:
                if data[j]["period"]==1:
                    playerpositionx1.append(data[j]['homePlayers'][i]['xyz'][0])
                    playerpositiony1.append(data[j]['homePlayers'][i]['xyz'][1])
                else: 
                    playerpositionx1.append(-data[j]['homePlayers'][i]['xyz'][0])
                    playerpositiony1.append(-data[j]['homePlayers'][i]['xyz'][1])
        label2=teamsname[8:13]
        for i in range (0,len(data[j]['awayPlayers'])):
            if data[j]['awayPlayers'][i]['number'] not in homegoalkeeper:
                if data[j]["period"]==1:
                    playerpositionx2.append(data[j]['awayPlayers'][i]['xyz'][0])
                    playerpositiony2.append(data[j]['awayPlayers'][i]['xyz'][1])
                else: 
                    playerpositionx2.append(-data[j]['awayPlayers'][i]['xyz'][0])
                    playerpositiony2.append(-data[j]['awayPlayers'][i]['xyz'][1])

    pitch = Pitch(pitch_type='secondspectrum', line_zorder=2,
                  pitch_length=longueurTerrain, pitch_width=largeurTerrain,
                  pitch_color='green', line_color='#efefef')

    fig, ax = pitch.draw(figsize=(6.6, 4.125))
    fig.set_facecolor('white')
    bin_statistic = pitch.bin_statistic(np.array(playerpositionx1),np.array(playerpositiony1), statistic='count', bins=(25, 25))
    bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'], 1)
    pcm = pitch.heatmap(bin_statistic, ax=ax, cmap='hot', edgecolors='#22312b')

    cbar = fig.colorbar(pcm, ax=ax, shrink=0.6)
    cbar.outline.set_edgecolor('#efefef')
    cbar.ax.yaxis.set_tick_params(color='#efefef')
    ticks = plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='black')
    fig.suptitle("Position of "+label1+" players", x=0.5,fontsize=20)

    plt.savefig(output1)
    plt.close()

    pitch1 = Pitch(pitch_type='secondspectrum', line_zorder=2,
                  pitch_length=longueurTerrain, pitch_width=largeurTerrain,
                  pitch_color='green', line_color='#efefef')

    fig1, ax1 = pitch1.draw(figsize=(6.6, 4.125))
    fig1.set_facecolor('white')
    bin_statistic1 = pitch1.bin_statistic(np.array(playerpositionx2),np.array(playerpositiony2), statistic='count', bins=(25, 25))
    bin_statistic1['statistic'] = gaussian_filter(bin_statistic1['statistic'], 1)
    pcm1 = pitch1.heatmap(bin_statistic1, ax=ax1, cmap='hot', edgecolors='#22312b')

    cbar1 = fig1.colorbar(pcm1, ax=ax1, shrink=0.6)
    cbar1.outline.set_edgecolor('#efefef')
    cbar1.ax.yaxis.set_tick_params(color='#efefef')
    ticks1 = plt.setp(plt.getp(cbar1.ax.axes, 'yticklabels'), color='black')
    fig1.suptitle("Position of "+label2+" players", x=0.5,fontsize=20)

    plt.savefig(output2)
    plt.close()
    return output1,output2
