# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 21:17:49 2017

@author: muahcheeee
"""
import json
import urllib.request
import requests
import pprint
import pandas as pd

oritteClanWarLogUrl = "https://api.royaleapi.com/clan/P9RGUC0Y/warlog"
oritteClanMembersUrl = "https://api.royaleapi.com/clan/P9RGUC0Y"
orriteClanWarUrl = "https://api.royaleapi.com/clan/P9RGUC0Y/war"

clanDonationHistory = pd.read_excel('OritteClanMembersDonation.xlsx', sheet_name='Sheet1')


headers = {
    'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTgyLCJpZGVuIjoiMzU5MzQ2MTg1OTU1MTgwNTcwIiwibWQiOnt9LCJ0cyI6MTUyOTU4MDM3MDY3NX0.9TXaCR36OpQ8Vr-eLawATyH-mpkhOTNaIwb5t3jw0no"
    }

response = requests.request("GET", orriteClanWarUrl, headers=headers)
warHistory = response.json()
#print(warHistory)

response = requests.request("GET", oritteClanWarLogUrl, headers=headers)
warLogHistory = response.json()

response = requests.request("GET", oritteClanMembersUrl, headers=headers)
rawData = response.json()


def updateClanMembers():
    latestClanTagList = []
    for i in range(len(rawData['members'])):
        latestClanTagList.append([rawData['members'][i]['tag'], rawData['members'][i]['name']])
    print(latestClanTagList)
    for i in range(len(rawData['members'])):
        if latestClanTagList[i][0] not in clanDonationHistory['tag']:
            memberData = {'tag': [latestClanTagList[i][0]], 'name':[latestClanTagList[i][1]]}
            newMember = pd.DataFrame(data=memberData)
            clanDonationHistory.append(newMember, ignore_index=True)
                
def getPlayerInformation(tag):
    response = requests.request("GET", "https://api.royaleapi.com/player/" + tag, headers=headers)
    playerInfo = response.json()
    return playerInfo

# Format: Array of PlayerNames with list 
# [PastParticipation, BattlesPlayed, BattlesWon, Participation Ratio, Win Ratio]
def getClanPlayersWarStats():
    numRecentWars = 10
    clanPlayersWarStats = []
    for i in range(len(rawData['members'])):
        clanPlayersWarStats.append([rawData['members'][i]['name']])
        clanPlayersWarStats[i].append(0)
        clanPlayersWarStats[i].append(0)
        clanPlayersWarStats[i].append(0)
        clanPlayersWarStats[i].append(0)
        clanPlayersWarStats[i].append(0)

    for i in range(numRecentWars):
        for k in range(len(clanPlayersWarStats)):
             for j in range(len(warLogHistory[i]['participants'])):
                if (clanPlayersWarStats[k][0] == warLogHistory[i]['participants'][j]['name']):
                    clanPlayersWarStats[k][1] += 1
                    clanPlayersWarStats[k][2] += warLogHistory[i]['participants'][j]['battlesPlayed']
                    clanPlayersWarStats[k][3] += warLogHistory[i]['participants'][j]['wins']
    
    for i in range(len(clanPlayersWarStats)):
        clanPlayersWarStats[i][4] = clanPlayersWarStats[i][1]/numRecentWars
        
        if (clanPlayersWarStats[i][2] == 0):
            clanPlayersWarStats[i][5] = 0
        else:
            clanPlayersWarStats[i][5] = clanPlayersWarStats[i][3]/clanPlayersWarStats[i][2]

    return clanPlayersWarStats;
    
def printClanPlayersWarStats(clanPlayersWarStats):
    playerWarStatsText = "Stats from most the 10 most recent wars \n"
    
    clanPlayersWarStats.sort(key=lambda x:float(x[4]), reverse=True)
    
    for i in range (len(clanPlayersWarStats)):
        playerWarStatsText += str(i + 1).rjust(3) + ". "
        playerWarStatsText += str(clanPlayersWarStats[i][0]).ljust(getLengthOfLongestClanMemberName())
        if (clanPlayersWarStats[i][1] == 0):
            playerWarStatsText += " | Participation Ratio = 0   "
        else:
            playerWarStatsText += " | Participation Ratio = "
            playerWarStatsText += str("{:.2f}".format(clanPlayersWarStats[i][4]))

        playerWarStatsText += " | Win Ratio = "
        playerWarStatsText += str("{:.2f}".format(clanPlayersWarStats[i][5]))
        playerWarStatsText += "\n"
        
    print(playerWarStatsText)

def getFailToCompleteWarList(numRecentWars):    
    failToCompleteWar = []
    for i in range(numRecentWars):
        failToCompleteWar.append([])
        for j in range(len(warLogHistory[i]['participants'])):
            member = warLogHistory[i]['participants'][j]
            if (member['battlesPlayed'] == 0):
                failToCompleteWar[i].append(member['name'])
    return failToCompleteWar;

def printFailToCompleteWarList(failToCompleteWar):
    failToCompleteWarResultsText = "Recent " + str(len(failToCompleteWar)) + " Wars Inactivity List:"
    for i in range(len(failToCompleteWar)):
        failToCompleteWarResultsText += "\n"
        failToCompleteWarResultsText += str(i + 1) + ": " 
        for j in range(len(failToCompleteWar[i])):
            failToCompleteWarResultsText += failToCompleteWar[i][j]
            if (j < len(failToCompleteWar[i]) - 1):
                failToCompleteWarResultsText += ", "
        
    print(failToCompleteWarResultsText)
    return;

def getDonationsLessThan(min):
    clanData = []
    for i in range(rawData['memberCount']):
        clanData.append([rawData['members'][i]['name'], rawData['members'][i]['donations'], rawData['members'][i]['donationsReceived']])
    DonationsLessThanMin = []
    for i in range(len(clanData)):
        if (clanData[i][1] < min):
            DonationsLessThanMin.append(clanData[i])
    return DonationsLessThanMin;

def printFailToMeetDonationRequirementList(DonationsLessThanMin):
    failToMeetDonationsRequirementText = "People Who Have NOT Hit Donation Requirement: "
    for i in range(len(DonationsLessThanMin)):
        failToMeetDonationsRequirementText += "\n" + str(i + 1) + ": " + str(DonationsLessThanMin[i][0]) + " (D = " + str(DonationsLessThanMin[i][1]) + " | R = " + str(DonationsLessThanMin[i][2]) + ")"
    print(failToMeetDonationsRequirementText)
    return;

def getFailToParticipateInWarList(numRecentWars):
    warParticipants = []
    clanMembers = []
    failToJoinWar = []

    for i in range(rawData['memberCount']):
        clanMembers.append(rawData['members'][i]['name'])
    
    for i in range(numRecentWars):
        warParticipants.append([])
        for j in range(len(warLogHistory[i]['participants'])):
            warParticipants[i].append(warLogHistory[i]['participants'][j]['name'])

    for i in range(numRecentWars):
        failToJoinWar.append(list(set(clanMembers) - set(warParticipants[i])))
    return failToJoinWar;

def printFailToParticipateInWarList(failToJoinWarList):
    failToParticipateInWarText = "List of People Who Did Not Participate in Some of the Past " + str(len(failToJoinWarList)) + " Wars:"
    for i in range (len(failToJoinWarList)):
        failToParticipateInWarText += "\n" + str(i + 1) + ": "
        for j in range (len(failToJoinWarList[i])):
            failToParticipateInWarText += failToJoinWarList[i][j]
            if (j < len(failToJoinWarList[i]) - 1):
                failToParticipateInWarText += ", "
    print(failToParticipateInWarText)
    return;

def getFailToFinishCollectionDayList():
    print(warLogHistory)

def printFailToFinishCollectionDayList():
    getFailToFinishCollectionDayList()

def getLengthOfLongestClanMemberName():
    lengthOfLongestName = 0
    for i in range(len(rawData['members'])):
        lengthOfLongestName = max(lengthOfLongestName, len(rawData['members'][i]['name']))
    return lengthOfLongestName        

#printFailToFinishCollectionDayList()
#printFailToParticipateInWarList(getFailToParticipateInWarList(5))
#printFailToCompleteWarList(getFailToCompleteWarList(10))
#printFailToMeetDonationRequirementList(getDonationsLessThan(100))
#printClanPlayersWarStats(getClanPlayersWarStats())
    