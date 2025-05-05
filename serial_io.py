#Écriture 1 fois
import serial
ser = serial.Serial('COM7', 9600, timeout=1)
ser.write(b'btnDirD.bco=65504')
ser.write(b'\xFF\xFF\xFF')
ser.write(b'ref btnDirD')
ser.write(b'\xFF\xFF\xFF')
ser.write(b'btnDirG.bco=65504')
ser.write(b'\xFF\xFF\xFF')
ser.write(b'ref btnDirG')
ser.write(b'\xFF\xFF\xFF')
ser.write(b'btnVitD.bco=63488')
ser.write(b'\xFF\xFF\xFF')
ser.write(b'ref btnVitD')
ser.write(b'\xFF\xFF\xFF')
ser.write(b'btnVitG.bco=63488')
ser.write(b'\xFF\xFF\xFF')
ser.write(b'ref btnVitG')
ser.write(b'\xFF\xFF\xFF')
ser.write(b'txtDebug.txt="Receiving..."')
ser.write(b'\xFF\xFF\xFF')#Il faut tjrs finir avec FFFFFF
ser.close()
""" 
#Lecture 1 fois
import serial
ser = serial.Serial('COM7', 9600, timeout=1)#timeout 1s
print(f"Received byte: {ser.read()}")
ser.close()

#Lecture en continue. Il faut un thread séparé
import serial
import threading
def rxSerieCallback(bytes):
    if(len(bytes)>0):#Si au moins 1 byte
        print(f"Received byte: {bytes.hex()}")
def lireSerieSansArret():
    while(True):
        rxSerieCallback(ser.read())#Lire 1 byte
ser = serial.Serial('COM7', 9600, timeout=1)#timeout 1s
thread = threading.Thread(target=lireSerieSansArret)
thread.start()
 """