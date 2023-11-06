import re
import json
from math import sqrt


def getO1(wave):

    # Use regex to find the numbers after "O1=" and before ","
    pattern = r'O1=([0-9.-]+),'

    # Find all matches
    matches = re.findall(pattern, wave)

    return(matches)

def getO2(wave):

    # Use regex to find the numbers after "O2=" and before ","
    pattern = r'O2=([0-9.-]+),'

    # Find all matches
    matches = re.findall(pattern, wave)

    return(matches)

def getT3(wave):

    # Use regex to find the numbers after "T3=" and before ","
    pattern = r'T3=([0-9.-]+),'

    # Find all matches
    matches = re.findall(pattern, wave)

    return(matches)

def getT4(wave):

    # Use regex to find the numbers after "T4=" and before ","
    pattern = r'T4=([0-9.-]+)'

    # Find all matches
    matches = re.findall(pattern, wave)

    return(matches)

#finds the eucledian distances between two users (takes json objects)
def euclidean(profile1, profile2):
    distance = sqrt(
        (profile1["O1avg"] - profile2["O1avg"])**2 +
        (profile1["O2avg"] - profile2["O2avg"])**2 +
        (profile1["T3avg"] - profile2["T3avg"])**2 +
        (profile1["T4avg"] - profile2["T4avg"])**2
    )
    return distance