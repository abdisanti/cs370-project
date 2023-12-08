from flask import Flask,render_template,request, redirect, url_for, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import sys
sys.path.append('cs370-project/tools')
import datetime
import bcrypt
import traceback
import json #for file creation in .json
import os #for directory specifiy
import psycopg2
from tools.MattTesting import *

from tools.eeg import get_head_band_sensor_object


from db_con import get_db_instance, get_db

from tools.token_required import token_required

#used if you want to store your secrets in the aws valut
#from tools.get_aws_secrets import get_secrets

from tools.logging import logger

#variables for database communication
hostname = 'umamind-1.crh1scx9g148.us-east-1.rds.amazonaws.com'
database = 'postgres'
username = 'UmaMindGroup'
pwd = 12132023
port_id = 5432
#conn = None
#cur = None

database_info = {

}

ERROR_MSG = "Ooops.. Didn't work!"
global_array = []#an array that holds json/database profiles
current_user = "no_user"#string value that holds first name to locate current user

#Create our app
app = Flask(__name__, template_folder = 'static')
#add in flask json
FlaskJSON(app)

#print("This is on startup")



#Function obtains all current profiles in from database to a global array
def ar_profile():
    conn = None
    cur = None 
    try:
        conn = psycopg2.connect(host = hostname, dbname = database, user = username, password = pwd, port = port_id)
        print("connected")
        cur = conn.cursor()

        get_profile_script = 'SELECT * FROM users'
        cur.execute(get_profile_script)
        #print(cur.fetchall())
        rows = cur.fetchall()

        for row in rows:
            global_array.append(row)
            #print(row)
    
        #print(global_array[0])
        #print(global_array[1])
        #print(global_array[2])


        conn.commit()
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def update_current_user(new_user):#function that updates current_user string
    global current_user
    current_user = new_user

@app.route('/search', methods=['POST', 'GET'])
def search_func():
    calcEuclidean(current_user)
    users = match()
    p1_id = users[0][0][0]
    p1_score = users[0][0][1]

    p2_id = users[0][1][0]
    p2_score = users[0][1][1]

    p3_id = users[0][2][0]
    p3_score = users[0][2][1]
    
    ar_profile()#update array
    count = len(global_array)
    for i in range(count):
        if p1_id == global_array[i][0]:
            f1 = global_array[i][1]
            l1 = global_array[i][2]
            a1 = global_array[i][3]
            g1 = global_array[i][4]
            break
        else:
            i = i + 1

    for i in range(count):
        if p2_id == global_array[i][0]:
            f2 = global_array[i][1]
            l2 = global_array[i][2]
            a2 = global_array[i][3]
            g2 = global_array[i][4]
            break
        else:
            i = i + 1

    for i in range(count):
        if p3_id == global_array[i][0]:
            f3 = global_array[i][1]
            l3 = global_array[i][2]
            a3 = global_array[i][3]
            g3 = global_array[i][4]
            break
        else:
            i = i + 1

    print(f1,f2,f3)

    return render_template('SearchPage.html', f1=f1,l1=l1,a1=a1,g1=g1,f2=f2,l2=l2,a2=a2,g2=g2,f3=f3,l3=l3,a3=a3,g3=g3,p1_score=p1_score,p2_score=p2_score,p3_score=p3_score)

#search_func()


@app.route('/login', methods=['POST', 'GET'])
def login_form():
    #print("Login button")
    ar_profile()#update array with current database data
    count = len(global_array)
    first = request.form['First Name']
    last = request.form['Last Name']
    
    for i in range(count):
        if first == global_array[i][1]: #1 is tuple for first name & i is array slot
            if last == global_array[i][2]:
                update_current_user(global_array[i])
                return redirect('static/UmamindHome.html')
            else:
                i = i + 1
        else:
            i = i + 1#incriment
    
    #print(global_array[0])
    #print(global_array[0][1])
    #print("Profile not found")
    return redirect('static/2nd Login.html')


@app.route('/submit', methods=['POST'])#function that creates a .json file with user inputed first and last name and stores in profiles folder
def submit_form():
    if request.method == 'POST':
        FirstName = request.form['fname']
        LastName = request.form['lname']
        Age = request.form['Age']
        Gender = request.form['Gender']
        '''
        data = {#creates a .js object file that holds first and last name
            'fname': FirstName,
            'lname': LastName,
            'Age': Age,
            'Gender' : Gender

        }
        '''
        #database update/communication:
        conn = None
        cur = None

        try:
            conn = psycopg2.connect(host = hostname, dbname = database, user = username, password = pwd, port = port_id)
            print("connected")
            cur = conn.cursor()

            enterProfile_script = 'INSERT INTO users (fname, lname, age, gender) VALUES (%s, %s, %s, %s)'
            user_values = (FirstName, LastName, Age, Gender)
            cur.execute(enterProfile_script,user_values)


            conn.commit()
        except Exception as error:
            print(error)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
               
        ar_profile()#function fills array of profile database data
        update_current_user(global_array[-1])#current_user hold tupal of created user
        #current_user = global_array[-1]#current_user hold tupal of created user
        
    return redirect('/static/UmamindFoodInfo.html')


@app.route('/profile', methods=['POST', 'GET'])#function that executes on accesss to prfile page and searches for correct profile to display
def access_profile():

    #if request.method == 'POST':
        #print("test")
        count = len(global_array)#obtain num of elements in array
        print("current is: ")
        print(current_user)
        ID = current_user[0]
        fn = current_user[1]
        ls = current_user[2]
        age = current_user[3]
        gender = current_user[4]
        print("test")
        print(ID,fn,ls,age,gender)
        
        return render_template('UmamindProfile.html', f = fn, l = ls, a = age, g = gender)
        
        '''
        for i in range(count):
            data = global_array[i]
            fn = data['fname']
            if fn == current_user:
                #print("test")
                prof_info = global_array[i]
                i = count + 1#end for loop
                print("entered if state")
                break
            else:
                print("In else state")
                prof_info = "no_user"

        print("fn is: ",fn)
        print("prof_info is: ",prof_info)
        if prof_info == "no_user":
            return render_template('UmamindProfile.html', f = "no data found", l = "no data found")#variables f and l are sent and used in UmamindProfile.html
        f_name = prof_info['fname']
        l_name = prof_info['lname']

    return render_template('UmamindProfile.html', f = f_name, l = l_name)#variables f and l are sent and used in UmamindProfile.html
    '''



#g is flask for a global var storage 
def init_new_env():
    #To connect to DB
    if 'db' not in g:
        g.db = get_db()

    if 'hb' not in g:
        g.hb = get_head_band_sensor_object()

    #g.secrets = get_secrets()
    #g.sms_client = get_sms_client()

#This gets executed by default by the browser if no page is specified
#So.. we redirect to the endpoint we want to load the base page
@app.route('/') #endpoint
def index():
    return redirect('/static/UmamindData.html')


@app.route("/secure_api/<proc_name>",methods=['GET', 'POST'])
@token_required
def exec_secure_proc(proc_name):
    logger.debug(f"Secure Call to {proc_name}")

    #setup the env
    init_new_env()

    #see if we can execute it..
    resp = ""
    try:
        fn = getattr(__import__('secure_calls.'+proc_name), proc_name)
        resp = fn.handle_request()
    except Exception as err:
        ex_data = str(Exception) + '\n'
        ex_data = ex_data + str(err) + '\n'
        ex_data = ex_data + traceback.format_exc()
        logger.error(ex_data)
        return json_response(status_=500 ,data=ERROR_MSG)

    return resp



@app.route("/open_api/<proc_name>",methods=['GET', 'POST'])
def exec_proc(proc_name):
    logger.debug(f"Call to {proc_name}")

    #setup the env
    init_new_env()

    #see if we can execute it..
    resp = ""
    try:
        fn = getattr(__import__('open_calls.'+proc_name), proc_name)
        resp = fn.handle_request()
    except Exception as err:
        ex_data = str(Exception) + '\n'
        ex_data = ex_data + str(err) + '\n'
        ex_data = ex_data + traceback.format_exc()
        logger.error(ex_data)
        return json_response(status_=500 ,data=ERROR_MSG)

    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

    