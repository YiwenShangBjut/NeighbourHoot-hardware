import time
import os
import fcntl
import serial
import pygame, pygame.mixer


pygame.mixer.init()

pygame.mixer.music.load(os.path.join("owlintro1.mp3"))
pygame.mixer.music.play()

deviceName = "USB Adapter USB Device"

# TODO: Change the device path below if required
ser = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=0)

# Utility funtion to write lines to the serial port
def write(message):
    ser.write((message + '\n').encode('utf-8'))
    ser.flush()

# Utility generator funtion to read all lines from the serial port
def read():
    buff = ''
    while True:
        # Split out any read lines
        idx = buff.find('\n')
        if idx > 0:
            line = buff[0:idx].strip()
            buff = buff[idx+1:]
            yield line
        else:
            # Need to read additional chunks to find the end of a line
            waiting = ser.inWaiting()
            if (waiting <= 0):
                # No data waiting
                yield None
            else:
                # Read next chunk of data
                buff = buff + ser.read(waiting).decode('ascii') 

class KeyReader:
    """
        Key Reader
        Dan Jackson, 2023
    """

    def __init__(self, deviceName="USB Keyboard"):
        self.deviceName = deviceName.strip()
        self.file = None
        self.line = ""
        self.input = ""
        self.last = None
    
    def __del__(self):
        self.close()
    
    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, type, value, tb):
        self.close()
    
    def open(self):
        print("KeyReader: Opening..." + self.deviceName)
        inputDeviceBase = "/sys/class/input/"
        inputPathBase = "/dev/input/"        
        inputDevice = None
        for device in os.listdir(inputDeviceBase):
            if not device.startswith("event"):
                continue
            nameFile = inputDeviceBase + device + "/device/name"
            with open(nameFile, 'r') as nf:
                name = nf.read().strip()
            #print("KeyReader: Checking input [" + device + "]: '" + name + "'")
            if name != self.deviceName:
                continue
            inputDevice = inputPathBase + device
        if inputDevice == None:
            print("KeyReader: Cannot find input device: " + self.deviceName)
            raise Exception("Cannot find input device")
        print("KeyReader: Found input device: " + inputDevice)
        self.file = open(inputDevice, "rb", buffering=0)
        # Non-blocking mode
        fd = self.file.fileno()
        fcntl.fcntl(fd, fcntl.F_SETFL, fcntl.fcntl(fd, fcntl.F_GETFL) | os.O_NONBLOCK)
    
    def close(self):
        if self.file == None:
            return
        #print("KeyReader: Closing...")
        self.file.close()
        self.file = None
    
    def read(self):
        #print("KeyReader: Query...")
        self.line = ""
        now = time.time()
        if (self.input != "" and self.last != None and now - self.last > 2):
            print("KeyReader: Input timeout")
            self.input = ""
            self.last = None
        while True:
            eventData = None
            try:
                eventData = self.file.read(24)
            except IOError as e:
                # [Errno 11] Resource temporarily unavailable
                if e.errno == 11:
                    break
                raise

            if eventData is None:
                break

            self.last = now 

            # 28=Enter, 2='1', 3='2', ..., 10='9', 11='0'
            code = eventData[10]
            # 0=release, 1=press, 2=repeat
            value = eventData[12]

            if value == 1:
                #print(">" + str(code) + " -- " + self.input)
                if (code == 28):
                    self.line = self.input
                    self.input = ""
                elif code >= 2 and code <= 11:
                    self.input = self.input + str((code - 1) % 10)
                else:
                    # Ignore other characters
                    pass
        
        # No line contents
        if self.line == "":
            return None
        return self.line

with KeyReader(deviceName) as keyReader:
    # Loop forever, checking serial input
    for line in read():

        scannerLine = keyReader.read()
        if scannerLine != None:
            print("READ: " + scannerLine)
            value = int(scannerLine)
            print("VALUE: " + str(value))
            pygame.mixer.music.load(os.path.join("Scanned item.mp3"))
            pygame.mixer.music.play()
            write(scannerLine + " points")

        # Check serial input line
        if line is None:
            # No data - don't busy-wait too aggressively
            time.sleep(0.05)
        else:
            # Handle received line
            print('RECV: ' + line)

            if line ==  "0" or line == "1" or line == "2" or line == "3":
                print(line)

                pygame.mixer.music.load(os.path.join("Goodbye.mp3"))
                pygame.mixer.music.play()
