from neurosdk.scanner import Scanner
from neurosdk.sensor import Sensor
from neurosdk.brainbit_sensor import BrainBitSensor
from neurosdk.cmn_types import *
from neurosdk.sensor import sys
from time import sleep 
import pickle 
import csv
import re
import time 
import gspread
#from Matching import *
#from app import *

from tools.logging import logger


def on_sensor_state_changed(sensor, state):
    logger.debug('Sensor {0} is {1}'.format(sensor.Name, state))

data_to_pickle = []
def on_brain_bit_signal_data_received(sensor, data):
    global data_to_pickle
    logger.debug(data)

    file = open('tools/MockBrainData1.pkl', 'r')
    data = file.readlines()
    file.close()

    data_to_pickle.append(data)

    print(data)


    """
    #Comment out when using headband
    #Get mock data to simulate using headband store into data 
    #file = open('tools/MockBrainData1.pkl', 'r')
    #data = file.readlines()
    #file.close()
    
   #Pickle testing: Send mock data to pickle file as if it were real data, pickle it then unpickle it/
    with open('BrainDataFile.pkl', 'wb') as file: 
        pickle.dump(data, file)
        file.close()

    with open('BrainDataFile.pkl', 'rb') as f: 
        data = pickle.load(f)
        #Check to make sure unpickled data is deseralized 
        print("Unpickled Data: \n\n")
        print(data)

    #get_avgs(data)

with open('BrainDataFile.pkl', 'wb') as file: 
        pickle.dump(data, file)
        file.close()

"""

def pickle_brain_bit_data(data): 
    with open('BrainDataFile.pkl', 'wb') as file: 
        pickle.dump(data, file)
        file.close()
    

logger.debug("Create Headband Scanner")
gl_scanner = Scanner([SensorFamily.SensorLEBrainBit])
gl_sensor = None
logger.debug("Sensor Found Callback")
def sensorFound(scanner, sensors):
    global gl_scanner
    global gl_sensor
    for i in range(len(sensors)):
        logger.debug('Sensor %s' % sensors[i])
        logger.debug('Connecting to sensor')
        gl_sensor = gl_scanner.create_sensor(sensors[i])
        gl_sensor.sensorStateChanged = on_sensor_state_changed
        gl_sensor.connect()
        gl_sensor.signalDataReceived = on_brain_bit_signal_data_received
        gl_scanner.stop()
        del gl_scanner

gl_scanner.sensorsChanged = sensorFound

logger.debug("Start scan")
gl_scanner.start()

#logger.debug("Stop Scan")
#gl_scanner.stop()


def get_head_band_sensor_object():
    return gl_sensor




"""
#doing all this a the "module level" in "Demo" server mode it will work fine :)

#for activation and access of the google sheets and python
gc = gspread.service_account('370credentials.json')
sh = gc.open_by_key('1Jwa2VL4aIiFerTGnpRbHw1DpKbLOHsojTJxU5n8mDaE')
worksheet = sh.sheet1

#holds values from the google sheets into variables 
names = worksheet.col_values(2) #names holds an array with all the values in column 2 (names of users)
print(names)

#make pickle files for users in the google sheets
filename = ""
for i in names: 
    filename = i + ".pkl"
    print(filename)
"""


