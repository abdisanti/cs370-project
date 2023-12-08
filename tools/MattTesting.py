#import gspread
from parseAlgo import * 
#from app import *
import pickle
#import json
import psycopg2
#from app import current_user

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

#this function calculates averages from mock pickl file and stores the results to the data table in database
def calcAndStoreAvg():
    try:
        conn = psycopg2.connect(host=hostname, dbname=database, user=username, password=pwd, port=port_id)
        print("connected")
        cur = conn.cursor()

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
        '''
        print("averages are: ")
        print("01: " + str(O1t) + " O2: " + str(O2t) + " T3: " + str(T3t) + " T4: " + str(T4t))
        '''
        #insertHardCode = (-0.107654321098765, -0.106543210987654, -0.095432109876543, -0.112345678901234)

        #averagesInsert = (O1t,  O2t, T3t, T4t)  #used for when current user is new to the database
        #averagesUpdate = (O1t,  O2t, T3t, T4t, current_userID)  #used for when current user is already in db

        '''   
        matchFound = False
        getUserInfo_script = 'SELECT id FROM users'

        cur.execute(getUserInfo_script)
        user_ids = [row[0] for row in cur.fetchall()]

        for id in user_ids:
            if current_userID == id:
                matchFound = True
    
        if matchFound == True:
            cur.execute('UPDATE data SET o1 = %s, o2 = %s, t3 = %s, t4 = %s WHERE user_id = %s', averagesUpdate)
            print("already in database, updating averages")
        else:
            cur.execute(insertUser, ("Bob", "Builder", 25, "male"))
            cur.execute(insertAvgs, insertHardCode)
            print("new to database, adding new averages to database")
        ''' 
        #store calculated averages into averages, send them to the data table using insertAvg query
        averagesInsert = (O1t,  O2t, T3t, T4t)
        cur.execute(insertAvgs, averagesInsert)

        conn.commit()
    except Exception as error:
        print(error)
    finally: 
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


#This function will calculate the Eucledian scores for all user in the table based on the current user ID#.
def calcEuclidean(currentID):
    try:
        conn = psycopg2.connect(host=hostname, dbname=database, user=username, password=pwd, port=port_id)
        print("connected")
        cur = conn.cursor()

        #get averages data of the current user
        cur.execute(f"SELECT o1, o2, t3, t4 FROM data WHERE user_id = {currentID}")
        current_user_data = cur.fetchone()
        

        if current_user_data:
            cur_o1, cur_o2, cur_t3, cur_t4 = current_user_data #insert current user data into variables

            #Fetch data for all users except the current one
            cur.execute(f"SELECT user_id, o1, o2, t3, t4 FROM data WHERE user_id <> {currentID}")
            other_users_data = cur.fetchall() #store it all in one variable

            #loop through other_users_data, run the euclidean equation, store it into the other user euclidean field
            for other_user_id, other_o1, other_o2, other_t3, other_t4 in other_users_data:
                euclideanVal = sqrt(
                    (cur_o1 - other_o1)**2 +
                    (cur_o2 - other_o2)**2 +
                    (cur_t3 - other_t3)**2 +
                    (cur_t4 - other_t4)**2
                )
                #query for inserting euclidean values
                variables = (euclideanVal,other_user_id)
                cur.execute('UPDATE data SET euclidean = %s WHERE user_id = %s', variables)

            variables = (None, currentID)
            cur.execute('UPDATE data SET euclidean = %s WHERE user_id = %s', variables)
                
            
            #end of for
        #end of if

        conn.commit()
    except Exception as error:
        print(error)
    finally: 
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()    