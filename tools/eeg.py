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

from tools.logging import logger   

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



def on_sensor_state_changed(sensor, state):
    logger.debug('Sensor {0} is {1}'.format(sensor.Name, state))

def on_brain_bit_signal_data_received(sensor, data):
    logger.debug(data)
    
    #Comment out when using headband
    #Get mock data to simulate using headband store into data 
    file = open('tools/MockBrainData1.pkl', 'r')
    data = file.readlines()
    file.close()
    
   #Pickle testing: Send mock data to pickle file as if it were real data, pickle it then unpickle it/
    with open('BrainDataFile.pkl', 'wb') as file: 
        pickle.dump(data, file)
        file.close()

    with open('BrainDataFile.pkl', 'rb') as f: 
        unpickle_data = pickle.load(f)
        #Check to make sure unpickled data is deseralized 
        print("Unpickled Data: \n\n")
        print(unpickle_data)

    


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

logger.debug("Stop Scan")
gl_scanner.stop()


def get_head_band_sensor_object():
    return gl_sensor





"""
desired_order = ["PackNum", "Marker", "O1", "O2", "T3", "T4", "Marker", "O1", "O2", "T3", "T4"]
def create_csv_from_data(filename, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',')

with open('output.csv', 'w', newline='') as file:
            sys.stdout = file  # Redirect stdout to the file
            if Sensor.is_supported_command(SensorCommand.CommandStartSignal):
                Sensor.exec_command(SensorCommand.CommandStartSignal) #this line prints the data
                print("Start signal")
                sleep(5)
                Sensor.exec_command(SensorCommand.CommandStopSignal)
                print("Stop signal")
            sys.stdout = sys.stdout
"""

