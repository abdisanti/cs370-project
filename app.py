from flask import Flask,render_template,request, redirect, url_for, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import sys
import datetime
import bcrypt
import traceback
import json #for file creation in .json
import os #for directory specifiy

from tools.eeg import get_head_band_sensor_object


from db_con import get_db_instance, get_db

from tools.token_required import token_required

#used if you want to store your secrets in the aws valut
#from tools.get_aws_secrets import get_secrets

from tools.logging import logger

ERROR_MSG = "Ooops.. Didn't work!"
global_array = []#an array that holds json profiles
current_user = "no_user"#string value that holds first name to locate current user

#Create our app
app = Flask(__name__, template_folder = 'static')
#add in flask json
FlaskJSON(app)

#print("This is on startup")



#Function obtains all current profiles in profiles folder to a global array
def ar_profile():
    files = os.listdir('profiles')#files varible points to profiles folder
    json_files = [file for file in files if file.endswith('json')]#filter
    count = len(json_files)#collects number of files found
    if len(json_files) > 0:
        for i in range(count):#for loop fills/updates array with all json objs into array
            with open(os.path.join('profiles', json_files[i]), 'r') as file:
                data = json.load(file)
                #print(i)
                global_array.append(data)
    else:
        print("no profiles to obtain")

#ar_profile()
#print(global_array[0])
#print(global_array[1])
#print(global_array[2])
def update_current_user(new_user):#function that updates current_user string
    global current_user
    current_user = new_user

@app.route('/submit', methods=['POST'])#function that creates a .json file with user inputed first and last name and stores in profiles folder
def submit_form():
    if request.method == 'POST':
        FirstName = request.form['fname']
        LastName = request.form['lname']
        Age = request.form['Age']
        Gender = request.form['Gender']

        data = {#creates a .js object file that holds first and last name
            'fname': FirstName,
            'lname': LastName,
            'Age': Age,
            'Gender' : Gender

        }

        update_current_user(FirstName) #update current_user strong to later identify specific profile in use/login

        json_data = json.dumps(data, indent=4)
        dir = "profiles"#directory path for file creation
        if not os.path.exists(dir):
            os.makedirs(dir)

        FirstName += ".json"
        with open(os.path.join(dir, FirstName), "a") as js_file:#creates a file in append mode with 'with' func to close file creation once complete
            js_file.write(f"{json_data}")
            #js_file.write(f"const myData = {json_data};")
        
        
        
        #ar_profile()#function fills array of profile json objects


        #print(FirstName)
        #print(LastName)
    return redirect('/static/FoodForThought.html')


@app.route('/profile', methods=['POST'])#function that executes on accesss to prfile page and searches for correct profile to display
def access_profile():

    if request.method == 'POST':
        #print("test")
        count = len(global_array)#obtain num of elemnts in array
        #print("current is: ",current_user)
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

    