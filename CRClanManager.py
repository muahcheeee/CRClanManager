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
for i in range(numMembers):
    clanData.append([rawData['members'][i]['name'],rawData['members'][i]['donations'],rawData['members'][i]['clanChestCrowns']])

#Sort according to donations
clanData.sort(key=lambda x: x[1])
print("Weekly Clan Report")
print("")
print("Top 3 Donators")
for i in range(3):
    print("No.",str(i+1), ": ", clanData[numMembers-(i+ 1)][0] , "(", clanData[numMembers-(i +1)][1], ")")

print("")
print("Members with less than 100 Donations")
for i in range(numMembers):
    if (int(clanData[i][1] < 100)):
        print(clanData[i][0], "(", clanData[i][1], ")")

clanData.sort(key=lambda x: x[2])

print("")
print("Top 3 Clan Chest Contributers")
for i in range(3):
    print("No.",str(i+1), ": ", clanData[numMembers-(i+ 1)][0] , "(", clanData[numMembers-(i +1)][2], ")")

print("")
print("Members with less than 10 Clan Chest Crowns")
for i in range(numMembers):
    if (int(clanData[i][2] < 10)):
        print(clanData[i][0], "(", clanData[i][2], ")")
