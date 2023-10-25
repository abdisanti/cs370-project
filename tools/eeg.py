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

from tools.logging import logger   


#doing all this a the "module level" in "Demo" server mode it will work fine :)

def on_sensor_state_changed(sensor, state):
    logger.debug('Sensor {0} is {1}'.format(sensor.Name, state))

def on_brain_bit_signal_data_received(sensor, data):
    logger.debug(data)
    
    start = time.time()

    #Send data to Pickle file
    with open('BrainDataFile.pkl', 'wb') as f: 
        pickle.dump(data, f)
        f.close()

    with open('BrainDataFile.pkl', 'rb') as f: 
        unpickle_data = pickle.load(f)
        #Check to make sure unpickled data is deseralized 
        print(unpickle_data)

    #check to see the time it takes to pickle
    end = time.time()
    print('Total pickle time: ', end - start)
    
    #with open('BrainDataFile.pkl', 'rb') as f: 
        #data_loaded

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

