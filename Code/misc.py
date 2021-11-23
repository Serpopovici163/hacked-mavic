info = 0
warn = 1
err = 2

def log(logLevel, msg):
    if logLevel == info:
        print("[INFO] --> " + msg)
    elif logLevel == warn:
        print("[WARN] --> " + msg)
    elif logLevel == err:
        print("[ERR] --> " + msg)