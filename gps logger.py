import serial
from pynmea import nmea
import csv
from datetime import datetime
import sys
import glob

def serial_ports():
        """
        Read the all ports that are open for serial communication
        @returns array of COMS avaliable
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform') #if the OS is not one of the main

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
    
def converter_A(cord):
    #DDMM.MMMMM
    degrees=float(cord[0:2]) #DD
    minutes=float(cord[2:8]) #MM.MMMM
    decimal = degrees + (minutes/60)
    return decimal

def converter_B(cord):
    #DDDMM.MMMMM
    degrees=float(cord[0:3]) #DDD
    minutes=float(cord[3:9]) #MM.MMMM
    decimal = degrees + (minutes/60)
    return decimal

con=False
while not con: #loop till connection established
    try:
        print(serial_ports())
        serial=input("Enter your serial port: ")
        ser=serial.Serial(serial)
    except:
        pass
    
ser.baudrate=4800
name=input("What would you like to name your file? ")
f = open(name+'.csv', 'w')
f1 = open("debug "+name+'.txt', 'w')
print('Waiting for data')
while True:
    try:     
        message = ser.readline().decode() 
        message = message.strip()
        if '$GNGGA' in message:    
                gpgga = nmea.GPGGA()
                gpgga.parse(message)   
                lat = float(gpgga.latitude)
                lon = float(gpgga.longitude)
                print("Lat %f Long %f" % (lat, lon))
                for i in message:
                    coord_list = []
                    coord = [gpgga.latitude,gpgga.longitude]
                    
                    coord_list.append(coord)
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    lat=converter_A(str(gpgga.latitude))
                    lon=converter_B(str(gpgga.longitude))
                    if gpgga.lat_direction == "S":
                        lat*=-1
                    if gpgga.lon_direction == "W":
                        lon*=-1
                    #print("{},{},{},{}\n".format(current_time,gpgga.latitude, gpgga.longitude,gpgga.num_sats))
                    f.write("{},{:.20f},{:.20f},{}\n".format(current_time,lat,lon,gpgga.num_sats))
                    f1.write(message+"\n")

    except KeyboardInterrupt:
        raise
f.close()
f1.close()
ser.close()
