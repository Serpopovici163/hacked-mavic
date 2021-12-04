info = 0
warn = 1
err = 2

#not very used, just made this file out of habit since I normally have
#a lot more common functions in here. I probably should have written 
#the target data in here so it could easily be referenced by all files

def log(logLevel, msg):
    if logLevel == info:
        print("[INFO] --> " + msg)
    elif logLevel == warn:
        print("[WARN] --> " + msg)
    elif logLevel == err:
        print("[ERR] --> " + msg)