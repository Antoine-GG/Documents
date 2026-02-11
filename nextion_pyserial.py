#Écriture 1 fois
import serial
ser = serial.Serial('COM32', 9600, timeout=1)
ser.write(b'txtDebug.txt="Allo"')
ser.write(b'\xFF\xFF\xFF')#Il faut tjrs finir avec FFFFFF
ser.close()

#Lecture 1 fois
import serial
ser = serial.Serial('COM32', 9600, timeout=1)#timeout 1s
print(f"Byte reçu: {ser.read()}")
ser.close()

#Lecture en continue. Il faut un thread séparé
import serial
import threading
def rx_serie_callback(bytes):
    if(len(bytes)>0):#Si au moins 1 byte
        print(f"Byte reçu: {bytes.hex()}")
def lire_serie_sans_arret():
    while(True):
        rx_serie_callback(ser.read())#Lire 1 byte
ser = serial.Serial('COM32', 9600, timeout=1)#timeout 1s
thread = threading.Thread(target=lire_serie_sans_arret)
thread.start()