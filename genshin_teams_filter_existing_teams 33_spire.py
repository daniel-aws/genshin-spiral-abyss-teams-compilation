import os
import csv
import json
import numpy as np
import numba as nb

primarySustain = ["Hu Tao", "Beidou", "Thoma", "Layla", "Xinyan"]
secondarySustain = ["Xingqiu"]
fullSustain = ["Barbara", "Bennett", "Diona", "Dori", "Jean", "Shinobu", "Noelle", "Qiqi", "Kokomi", "Sayu", "Zhongli"]
freezeTeamBans = ["dendro", "electro", "geo", "pyro"]
geoTeams = ["Albedo", "Zhongli", "TravelerGeo", "Ningguang"]
banList = ["Diluc", "Aloy", "Amber", "Eula", "Razor", "Tighnari", "Yoimiya", "TravelerAnemo", "TravelerElectro"]

def setdiff2d_bc(arr1, arr2):
    idx = (arr1[:, None] != arr2).any(-1).all(1)
    return arr1[idx]

print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print("SANITIZING AND COMBINING ENTRIES TO SINGLE OUTPUT CSV")
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

jsonFile = open("../genshin-impact-team-randomizer/src/data/characterData.json")

mainFileName = "genshinTeamsNamed.csv"
denyListFileName = "denyList.csv"
travelerReviewFileName = "reviewTravelerTeams.csv"
directory = "./inputs"
characterData = json.load(jsonFile)

print("LOADING MAIN CSV TO COMPARE AGAINST")

fr = open(mainFileName, 'r')
mainFileArray = np.loadtxt(fr, delimiter=",", dtype=str)
mainFileArray = mainFileArray[1:]
mainFileArray = np.sort(mainFileArray)
fr.close()

# Moving entries that are lacking proper sustain (will not be stable for majority of players) to denyList automatically
denyListAppend = np.empty((0, 4), str)
# Moving entries that have ambiguous traveler and need to be manually reviewed to reviewTravelerTeams automatically
travelerReview = np.empty((0, 4), str)

# Parse through data
idx = -1
for team in mainFileArray:
    idx += 1
    passGeoCheck = False
    banned = False
    # Check if freeze team
    for character in team:
        # Must have a hydro and cryo, and no pyro, geo, electro, dendro
        for charData in characterData:
            if character == charData["shortName"]:
                if character in banList:
                    banned = True
                    break
                if character in geoTeams:
                    passGeoCheck = True
                    break
    if banned == False and passGeoCheck == True:
        # If team is just "Traveler" it needs to know what kind of Traveler contextually so for now it must go to auto review.
        if "Traveler" in team:
            mainFileArray = np.delete(mainFileArray, idx, axis=0)
            idx -= 1
            continue
        # If either has character in fullSustain or a character in secondarySustain AND primarySustain, continue
        if np.any(np.in1d(fullSustain, team)):
            continue
        if np.any(np.in1d(primarySustain, team)) and np.any(np.in1d(secondarySustain, team)):
            continue
    # Remove from main array
    mainFileArray = np.delete(mainFileArray, idx, axis=0)
    idx -= 1

print("CLEANING UP FILES")

# Removing duplicates
uniqueConvert = [tuple(row) for row in mainFileArray]
mainFileArray = np.unique(uniqueConvert, axis=0)

# Append data to aggregatedTeams

print("SAVING OUTPUT CSV FILES")

np.savetxt("./outputs/" + "aggregatedTeams33second.csv", mainFileArray, fmt='%s', delimiter=',', newline='\n', header='', footer='', comments='# ', encoding=None)

print("COMPLETE")