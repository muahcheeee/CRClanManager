# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 21:17:49 2017

@author: CheeYeo
"""
import json
import urllib.request
import requests
import numpy as np

#with urllib.request.urlopen('http://api.cr-api.com/clan/U0GGUR') as url:
#    clanData = json.loads(url.read().decode())
#    print(clanData)

#jsonurl =  urlopen("http://api.cr-api.com/clan/U0GGUR")
#text = json.loads(jsonurl.read())
#print(text)


#with urllib.request.urlopen('http://api.cr-api.com/clan/U0GGUR') as url:
#    clandata = url.read()
sevenMinutesClanUrl = "http://api.cr-api.com/clan/U0GGUR"
clanJsonData = requests.get(sevenMinutesClanUrl)
#print(r.json())
#print(r.text)
rawData = json.loads(clanJsonData.text)
#print(data[2])
#print(data[3])

#jsonin = r.json()
#print(jsonin)
#data = json.loads(jsonin)
#print(data)
numMembers = len(rawData['members'])

clanData = np.empty((numMembers, 3), dtype ='object, i4, i4')
clanData = [[]]
print(rawData['members'][0]['name'])
for i in range(numMembers):
    clanData[i] = [rawData['members'][i]['name'],int(rawData['members'][i]['donations']),int(rawData['members'][i]['clanChestCrowns'])]
#    clanData[i,0] = rawData['members'][i]['name']
#    clanData[i,1] = int(rawData['members'][i]['donations'])
#    clanData[i,2] = int(rawData['members'][i]['clanChestCrowns'])

print(clanData)