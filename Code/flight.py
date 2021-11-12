#this file will handle speed and flight logic

#import serial

#gps = serial.Serial(port = '/dev/ttyS0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
#sbus = serial.Serial(port = '/dev/ttyS1', baudrate=100000, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

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
    #sbus.write(packet)