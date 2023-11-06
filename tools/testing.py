import gspread
from brainParse import * 
#import pickle

gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key('1xijiwWLX5fwNYTJRgdCvz7g2G7wU4npk2-tedXStwSY')
worksheet1= sh.sheet1


#keep count of all of the variables
O1t = 0.0
O2t = 0.0
T3t = 0.0
T4t = 0.0

#row counter
count = 1

while(count <= worksheet1.row_count):
    brain = str(worksheet1.row_values(count)) #get row string and store in brain

    #parse out all of the variables
    O1 = (getO1(brain)[1])
    O2 = (getO2(brain)[1])
    T3 = (getT3(brain)[1])
    T4 = (getT4(brain)[1])

    #add variables as floats 
    O1t += float(O1) 
    O2t += float(O2)
    T3t += float(T3)
    T4t += float(T4)

    #print current variables
    print("O1: "+O1 +" "+"O2: "+O2+ " "+"T3: "+T3+ " "+"T4: "+T4) 
    count += 1 #update counter

print("done")

#find averages
O1t = O1t / count
O2t = O2t / count
T3t = T3t / count
T4t = T4t / count

#display averages
print("averages are: ")
print("01: " + str(O1t) + " O2: " + str(O2t) + " T3: " + str(T3t) + " T4: " + str(T4t))

# Load profiles from JSON files
with open("person1.json", "r") as file:
    person1_data = json.load(file)

with open("person2.json", "r") as file:
    person2_data = json.load(file)


result = euclidean(person1_data, person2_data)
print("the following is the eucledian distance between person1 and person 2: ")
print(result)
