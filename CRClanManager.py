# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 21:17:49 2017

@author: CheeYeo
"""
import json
import urllib.request
import requests

sevenMinutesClanUrl = "http://api.cr-api.com/clan/U0GGUR"
clanJsonData = requests.get(sevenMinutesClanUrl)
rawData = json.loads(clanJsonData.text)

numMembers = len(rawData['members'])

clanData = []
print(rawData['members'][0]['name'])
for i in range(numMembers):
    clanData.append([rawData['members'][i]['name'],int(rawData['members'][i]['donations']),int(rawData['members'][i]['clanChestCrowns'])])

print(clanData)