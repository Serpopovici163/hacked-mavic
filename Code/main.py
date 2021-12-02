#this file will handle networking and delegate flight tasks to flight.py 
import flight
import network
import time

#before anything, wait for wifi and setup GPIO comms with Arduino
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT) # +1
GPIO.setup(20, GPIO.OUT) # +2
GPIO.setup(21, GPIO.OUT) # +4

GPIO.output(19, 1)

#next wait for P2P server
while (not network.init()):
    time.sleep(1)

#advance system state
GPIO.output(20, 1)
GPIO.output(19, 0)

#next wait for GPS fix
#while (not flight.checkFix()):
#    time.sleep(1)

time.sleep(3)

#advance system state
GPIO.output(19, 1)

try:
    while True:
        flight.targetLat, flight.targetLon = network.target
        flight.targetAlt = network.alt
        time.sleep(1)
except KeyboardInterrupt:
    print("Ctrl-C exception")