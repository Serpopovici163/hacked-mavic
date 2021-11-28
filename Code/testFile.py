dataString = "2040" 

buffer = hex(1500).replace("x","")
dataString = dataString + buffer[2] + buffer[3] + buffer[0] + buffer[1]
buffer = hex(1499).replace("x","")
dataString = dataString + buffer[2] + buffer[3] + buffer[0] + buffer[1]
buffer = hex(1007).replace("x","")
dataString = dataString + buffer[2] + buffer[3] + buffer[0] + buffer[1]
buffer = hex(1501).replace("x","")
dataString = dataString + buffer[2] + buffer[3] + buffer[0] + buffer[1]
dataString = dataString + "D007"
dataString = dataString + "D007"

for i in range(8):
    dataString = dataString + "DC05"

byteArray = []
for i in range(0, len(dataString), 2):
    byteArray.append(dataString[i:i+2])

checksum = 0xffff
for byte in byteArray:
    checksum = checksum - int("0x" + byte, 16)

buffer = hex(checksum).replace("0x", "")
dataString = dataString + buffer[2] + buffer[3] + buffer[0] + buffer[1]

print(str(dataString))
print(str(checksum))
print(0xF354)