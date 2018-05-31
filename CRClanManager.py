# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 21:17:49 2017

@author: muahcheeee
"""
import json
import urllib.request
import requests
import pprint

oritteClanWarLogUrl = "https://api.royaleapi.com/clan/P9RGUC0Y/warlog"
oritteClanMembersUrl = "https://api.royaleapi.com/clan/P9RGUC0Y"

headers = {
    'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTgyLCJpZGVuIjoiMzU5MzQ2MTg1OTU1MTgwNTcwIiwibWQiOnt9fQ.bc98AXpS-wWGjbatAvgRoPJzCL--1XoE0l6qD82tQlU"
    }

response = requests.request("GET", oritteClanWarLogUrl, headers=headers)
warLogHistory = response.json()


# file = open("ClanWarLogExample.txt", 'w')
# file.write(str(warLogHistory))
# file.close()


response = requests.request("GET", oritteClanMembersUrl, headers=headers)
rawData = response.json()

# Format: Array of PlayerNames with list [PastParticipation, BattlesPlayed, BattlesWon]
def getClanPlayersWarStats():
    numRecentWars = 10
    clanPlayersWarStats = []
    for i in range(len(rawData['members'])):
        clanPlayersWarStats.append([rawData['members'][i]['name']])
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
    print(clanPlayersWarStats)
    return;

def getPlayerWarLossList(numRecentWars):
    playerWarLossList = []
    for i in range(numRecentWars):
        playerWarLossList.append([])
        for j in range(len(warLogHistory[i]['participants'])):
            member = warLogHistory[i]['participants'][j]
            if (member['battlesPlayed'] > 0 and member['wins'] < member['battlesPlayed']):
                warWinRatio = member['wins']/member['battlesPlayed'] 
                memberWarWinRatioPair = [member['name'] , warWinRatio]
                playerWarLossList[i].append(memberWarWinRatioPair)
    return playerWarLossList;

def printPlayerWarLossList(playerWarLossList):
    playerWarLossResultsText = "Players who loss in the recent" + str(len(playerWarLossList)) + "Wars:"
    for i in range(len(playerWarLossList)):
        playerWarLossResultsText += '\n'
        playerWarLossResultsText += str(i+1) + ":"
        for j in range(len(playerWarLossList[i])):
            if (playerWarLossList[i][j][1] != 0):
                playerWarLossResultsText += playerWarLossList[i][j][0]
                playerWarLossResultsText += "(" + str(playerWarLossList[i][j][1]) + "), "
            else:
                playerWarLossResultsText += playerWarLossList[i][j][0] + ", "
    
    print(playerWarLossResultsText[:-2])
    return;


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

# printFailToParticipateInWarList(getFailToParticipateInWarList(5))
# printFailToCompleteWarList(getFailToCompleteWarList(5))
# printFailToMeetDonationRequirementList(getDonationsLessThan(100))
# printPlayerWarLossList(getPlayerWarLossList(10))
getClanPlayersWarStats()