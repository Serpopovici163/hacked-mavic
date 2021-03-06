#this file will handle speed and flight logic

import serial
import threading
from gps import *
from haversine import *
from math import *
from bmp280 import BMP280
from smbus import SMBus
from i2clibraries import i2c_hmc5883l

#serial = serial.Serial(port = '/dev/ttyS0', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1) #iBus not used rn
gpsd = None
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)
compass = i2c_hmc5883l.i2c_hmc5883l(1)

#not used anymore but good to know
#compassAddr = 0x10
#baromAddr = 0x70

#flight status variables
vel = 0 #units tbd
alt = 0 #m
lat = 0 #gotten from gpsd
lon = 0
bearing = 0 #gotten from I2C compass
target_bearing = 0
targetLat = 0
targetLon = 0
targetAlt = 0

thottle = 1500
yaw = 1500
pitch = 1500
roll = 1500

#initialize GPS
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
    #also init compass
    compass.setContinuousMode()
    compass.setDeclination(-12, 54)

  def run(self):
    global gpsd
    while self.running:
      gpsd.next()

gpsp = GpsPoller()
gpsp.start()

def updateSensors():
    global alt
    global lat
    global lon
    global bearing
    #read i2c and uart to update flight status vars
    lat = gpsd.fix.latitude #no way this works, need to prototype with RPi next week
    lon = gpsd.fix.longitude
    #integrate i2c code here
    pressure = bmp280.get_pressure()
    alt = 8.3 * (pressure - 1013) #convert pressure to altitude in m
    bearing, minutes = compass.getHeading()
    bearing = bearing + minutes*(1/60) #add minutes to bearing angle
    

#iBus function because SBUS is unnecessarily complex to deal with at a hardware level
def iBusOut(throttle, roll, pitch, yaw, arm):
    #requires inputs between 1 and 1024 and arm as 0 or 1
    #insert header
    dataString = "2040"  
    #for some reason ibus sends bytes in reverse so 1500 becomes 05DC which then becomes DC05
    #output is AETR + Flight Mode + Arm
    buffer = hex(roll).replace("x","")
    dataString = dataString + buffer[2] + buffer[3] + buffer[0] + buffer[1]
    buffer = hex(pitch).replace("x","")
    dataString = dataString + buffer[2] + buffer[3] + buffer[0] + buffer[1]
    buffer = hex(throttle).replace("x","")
    dataString = dataString + buffer[2] + buffer[3] + buffer[0] + buffer[1]
    buffer = hex(yaw).replace("x","")
    dataString = dataString + buffer[2] + buffer[3] + buffer[0] + buffer[1]
    #flight mode
    dataString = dataString + "E803"
    if (arm):
        dataString = dataString + "D007"
    else:
        dataString = dataString + "E803"

    #complete remainder of packet
    for i in range(8):
        dataString = dataString + "DC05"

    #separate into 2-char bytes for computation
    byteArray = []
    for i in range(0, len(dataString), 2):
        byteArray.append(dataString[i:i+2])

    #checksum computation, the iBus protocol starts at 0xFFFF and subtracts every byte except the checksum
    checksum = 0xffff
    for byte in byteArray:
        checksum = checksum - int("0x" + byte, 16)

    buffer = hex(checksum).replace("0x", "")
    dataString = dataString + buffer[2] + buffer[3] + buffer[0] + buffer[1]

    #serial.write(dataString)

def speed(delta):
    #here delta is distance to target in m so the drone will know to speed up if it is far and slow down when close
    #vel ranges from 1000-2000
    global vel

    if (delta > 50):
        vel = 2000
    elif (delta <= 50 and vel > 1900):
        vel = vel - 50 #change this to slow down faster or slower
    elif (delta > 10 and vel < 1900):
        vel = 1900
    elif (delta <= 10 and vel > 1600):
        vel = vel - 50
    elif (delta <= 2):
        vel = 1500 #stop

#used to determine bearing to target
def get_bearing(pointA, pointB):

    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = radians(pointA[0])
    lat2 = radians(pointB[0])

    diffLong = radians(pointB[1] - pointA[1])

    x = sin(diffLong) * cos(lat2)
    y = cos(lat1) * sin(lat2) - (sin(lat1)
            * cos(lat2) * cos(diffLong))

    initial_bearing = atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180?? to + 180?? which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def updateFlight(): 
    #ideally this code should make the drone circle around the target coords when it arrives
    #when the drone drifts off target it will simply turn back and approach the target again
    updateSensors()
    delta = haversine((lat, lon), (targetLat, targetLon), unit=Unit.METERS)
    target_bearing = get_bearing((lat, lon), (targetLat, targetLon))
    #manage that and also manage throttle
    bearingAdj = target_bearing - bearing
    if (abs(bearingAdj) > 10):
        if (bearingAdj > 0): #yaw right
            yaw = 1700
        else: #yaw left
            yaw = 1300
    else: #if target is straight ahead go forward
        pitch = speed(delta)

#7 is arbitrary but that's what ArduPilot taught me as being an adequate number of sats
def checkFix():
    if (gpsd.satellites > 7):
        return True
    return False