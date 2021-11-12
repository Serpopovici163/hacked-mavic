#this file will handle speed and flight logic

import serial
import threading
from gps import *
from haversine import *
from math import *

gps = serial.Serial(port = '/dev/ttyS0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
sbus = serial.Serial(port = '/dev/ttyS1', baudrate=100000, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
gpsd = None

#flight status variables
vel = 0 #units tbd
alt = 0 #m
lat = 0 #gotten from gpsd
lon = 0
bearing = 0 #gotten from I2C compass

#initialize GPS
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    while self.running:
      gpsd.next()

gpsp = GpsPoller()
gpsp.start()

def updateSensors():
    #read i2c and uart to update flight status vars
    lat = gpsd.fix.latitude #no way this works, need to prototype with RPi next week
    lon = gpsd.fix.longitude
    #integrate i2c code here

#used in sbusOut function
def bitstring_to_bytes(data):
    output = bytearray()
    for channel in range(16):
        v = int(data[channel*8:channel*8+8], 2)
        print(data[channel*8:channel*8+8])
        output.extend(v.to_bytes(1, "big"))
    print(output)
    return output


def sbusOut(throttle, roll, elevator, yaw, arm):
    #requires inputs between 1 and 1024 and arm as 0 or 1
    #first we will generate a 176-character binary string representing all 16 channels within SBUS
    if (arm):
        dataString = format(roll, '011b') + format(elevator, '011b') + format(throttle, '011b') + format(yaw, '011b') + format(1024, '011b') + format(0, '0121b')
    else:
        dataString = format(roll, '011b') + format(elevator, '011b') + format(throttle, '011b') + format(yaw, '011b') + format(0, '011b') + format(0, '0121b')
    
    print(dataString) #debug
    
    #now lets build the SBUS packet
    packet = bytearray(b'\x0F') #start byte
    packet.extend(bitstring_to_bytes(dataString))
    packet.extend(b'\x00')
    packet.extend(b'\x00')

    print(packet)
    sbus.write(packet)

def speed(delta):
    #here delta is distance to target in m so the drone will know to speed up if it is far and slow down when close
    global vel

    if (delta > 50):
        vel = 100
    elif (delta <= 50 and vel > 15):
        vel = vel - 5 #change this to slow down faster or slower
    elif (delta > 5 and vel < 15):
        vel = 15
    elif (delta <= 2):
        vel = 0 #stop

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
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def updateFlight(target_lat, target_lon, target_alt):
    updateSensors()
    delta = haversine((lat, lon), (target_lat, target_lon), unit=Unit.METERS)
    speed(delta)
    target_bearing = get_bearing((lat, lon), (target_lat, target_lon))
    #manage that and also manage throttle
