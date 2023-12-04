import re
import pickle 

#wave = input("enter a brainwave to parse:\n")

with open('BrainDataFile.pkl', 'rb') as f: 
        wave = pickle.load(f)
        #Check to make sure unpickled data is deseralized 
        print("Unpickled Data: \n\n")
        print(wave)


def getO1(wave):

    # Use regex to find the numbers after "O1=" and before ","
    pattern = r'O1=([0-9.-]+),'

    # Find all matches
    matches = re.findall(pattern, wave)

    return(matches)

def getO2(wave):

    # Use regex to find the numbers after "O1=" and before ","
    pattern = r'O2=([0-9.-]+),'

    # Find all matches
    matches = re.findall(pattern, wave)

    return(matches)

def getT3(wave):

    # Use regex to find the numbers after "O1=" and before ","
    pattern = r'T3=([0-9.-]+),'

    # Find all matches
    matches = re.findall(pattern, wave)

    return(matches)

def getT4(wave):

    # Use regex to find the numbers after "O1=" and before ","
    pattern = r'T4=([0-9.-]+)'

    # Find all matches
    matches = re.findall(pattern, wave)

    return(matches)