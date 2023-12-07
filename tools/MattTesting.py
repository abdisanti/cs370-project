#import gspread
from parseAlgo import * 
#from app import *
import pickle
#import json
import psycopg2
from app import current_user

hostname = 'umamind-1.crh1scx9g148.us-east-1.rds.amazonaws.com'
database = 'postgres'
username = 'UmaMindGroup'
pwd = 12132023
port_id = 5432
conn = None
cur = None

#queiries 
insertUser = 'INSERT INTO users (fname, lname, age, gender) VALUES (%s, %s, %s, %s)'
insertAvgs = 'INSERT INTO data (o1, o2, t3, t4) VALUES (%s, %s, %s, %s)'
insertEuc = 'INSERT INTO data (euclidean) VALUES (%s)'

def calcAndStoreAvg(current_user):
    try:
        conn = psycopg2.connect(host=hostname, dbname=database, user=username, password=pwd, port=port_id)
        print("connected")
        cur = conn.cursor()

        user = ("Stacy", "Nguyen", 21, "female")
        cur.execute(insertUser, user)
        #cur.execute("UPDATE users SET fname = 'John', lname = 'Smith' WHERE id = 1")
        conn.commit()

        #keep count of all of the variables
        O1t = 0.0
        O2t = 0.0
        T3t = 0.0
        T4t = 0.0

        #row counter
        count = 1

        with open('BrainDataFile.pkl', "rb") as file: 
            data = pickle.load(file)
            #parse out all of the variables
            O1 = (getO1(str(data)))
            O2 = (getO2(str(data)))
            T3 = (getT3(str(data)))
            T4 = (getT4(str(data)))

            #add variables as floats 
            O1_length = len(O1)
            O2_length = len(O2)
            T3_length = len(T3)
            T4_length = len(T4)

            for i in range(O1_length): 
                 O1t += float(O1[i])
    
            for i in range(O2_length): 
                O2t += float(O2[i])

            for i in range(T3_length):     
                T3t += float(T3[i])
    
            for i in range(T4_length):
                T4t += float(T4[i])

            #print current variables
            #print("O1: "+O1 +" "+"O2: "+O2+ " "+"T3: "+T3+ " "+"T4: "+T4) 
            count += 1 #update counter

            file.close()

        #find averages
        O1t = O1t / O1_length
        O2t = O2t / O2_length
        T3t = T3t / T3_length
        T4t = T4t / T4_length

        #display averages
        print("averages are: ")
        print("01: " + str(O1t) + " O2: " + str(O2t) + " T3: " + str(T3t) + " T4: " + str(T4t))

        averages = ( -0.101235684329872,  -0.112345678901234, -0.094567890123456, -0.109876543210987)
        cur.execute(insertAvgs, averages)

        conn.commit()
    except Exception as error:
        print(error)
    finally: 
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def calcEuclidean(currentID):
    try:
        conn = psycopg2.connect(host=hostname, dbname=database, user=username, password=pwd, port=port_id)
        print("connected")
        cur = conn.cursor()

        cur.execute(f"SELECT column1, column2, column3, column4 FROM your_table_name WHERE user_id = {currentID}")
        current_user_data = cur.fetchone()

        if current_user_data:
            current_column1, current_column2, current_column3, current_column4 = current_user_data

            # Fetch data for all users except the current one
            cur.execute(f"SELECT user_id, column1, column2, column3, column4 FROM your_table_name WHERE user_id <> {currentID}")
            other_users_data = cur.fetchall()

            





        conn.commit()
    except Exception as error:
        print(error)
    finally: 
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()    









'''
#Read current contents of file and update them with BrainBit averages
with open("profiles/Matt.json", "rb") as file: 
    data1 = json.load(file)
    data1_len = len(data1)
    print(data1_len)
    for i in range(data1_len): 
        data2 = data1[i]
        print(data2)

        
    data1.update({"fname": "Matt", "lname": "Miller", "O1avg": O1t, "O2avg": O2t, "T3avg": T3t, "T4avg": T4t})
    json_data = json.dumps(data1, indent=4)
    

#re-write the updata data back to the profile
with open("profiles/Matt.json", "w") as file: 
    file.write(f"{json_data}")

         
# Load profiles from JSON files
with open("profiles/Matt.json", "r") as file:
    person1_data = json.load(file)

with open("tools/person2.json", "r") as file:
    person2_data = json.load(file)


result = euclidean(person1_data, person2_data)
print("the following is the eucledian distance between person1 and person 2: ")
print(result)
'''
