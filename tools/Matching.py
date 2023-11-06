from parseAlgo import *

#Algorithm and Calculations done by Abdiel 
#Functions implementing Abdiel's algorithm and calculations done by Matt 

def get_avgs(brainData): 
    O1 = (getO1(str(brainData)))
    O2 = (getO2(str(brainData)))
    T3 = (getT3(str(brainData)))
    T4 = (getT4(str(brainData)))

    #Get the length of each brainwave
    O1_length = len(O1)
    O2_length = len(O2)
    T3_length = len(T3)
    T4_length = len(T4)

    #for loops to calculate the sum of each brainwave
    for i in range(O1_length): 
        O1t += float(O1[i])
    
    for i in range(O2_length): 
        O2t += float(O2[i])

    for i in range(T3_length):     
        T3t += float(T3[i])
    
    for i in range(T4_length):
        T4t += float(T4[i])


    O1t = O1t / O1_length
    O2t = O2t / O2_length
    T3t = T3t / T3_length
    T4t = T4t / T4_length

    Data = {
        "fname": "Person",
        "lname": "1", 
        "O1avg": O1t,
        "O2avg": O2t, 
        "T3avg": T3t, 
        "T4avg": T4t
    }

    with open("tools/person1.json", "wb") as file: 
        file.write(Data)


