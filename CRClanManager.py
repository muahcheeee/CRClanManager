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

response = requests.request("GET", oritteClanMembersUrl, headers=headers)
rawData = response.json()

def getFailToCompleteWarList(numRecentWars):    
    failToCompleteWar = []
    warLogHistoryLength = numRecentWars #Seems like max is 10, len(warLogHistory)
    for i in range(warLogHistoryLength):
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
    failToMeetDonationsRequirementText = "People Who Failed To Hit Donation Requirement: "
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

printFailToParticipateInWarList(getFailToParticipateInWarList(5))
printFailToCompleteWarList(getFailToCompleteWarList(5))
printFailToMeetDonationRequirementList(getDonationsLessThan(100))
