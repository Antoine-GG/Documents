from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import threading
import sqlite3

#Moteurs
GPIO_PIN_VIT_GAUCHE = 27
GPIO_PIN_VIT_DROITE = 23
GPIO_PIN_DIR_GAUCHE = 17
GPIO_PIN_DIR_DROITE = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN_VIT_GAUCHE, GPIO.OUT)
GPIO.setup(GPIO_PIN_VIT_DROITE, GPIO.OUT)
GPIO.setup(GPIO_PIN_DIR_GAUCHE, GPIO.OUT)
GPIO.setup(GPIO_PIN_DIR_DROITE, GPIO.OUT)

def stop():
    GPIO.output(GPIO_PIN_VIT_GAUCHE, GPIO.LOW)
    GPIO.output(GPIO_PIN_VIT_DROITE, GPIO.LOW)
    GPIO.output(GPIO_PIN_DIR_GAUCHE, GPIO.LOW)
    GPIO.output(GPIO_PIN_DIR_DROITE, GPIO.LOW)

#Flask
app = Flask(__name__)
CORS(app)

#Flask page d'accueil
@app.route('/')
def index():
    return render_template('index.html')
 
class Moteur:
  def __init__(self, isVitGauche, isVitDroite, isDirDroite, isDirGauche):
    self.isVitGauche = isVitGauche
    self.isVitDroite = isVitDroite
    self.isDirDroite = isDirDroite
    self.isDirGauche = isDirGauche

@app.route('/trajectoire', methods=['POST'])
def trajectoire():
    connection = sqlite3.connect('robot.db')
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS trajectoire ( id INTEGER PRIMARY KEY, dirG REAL, vitG REAL, dirD REAL, vitD REAL )")
    trajectoire = request.json['trajectoire']
    for moteur in trajectoire:
        cursor.execute("INSERT INTO trajectoire (id, dirG, vitG, dirD, vitD) VALUES (?, ?, ?, ?, ?)", (moteur.isDirGauche, moteur.isVitGauche, moteur.isDirDroite, moteur.isVitDroite))
    connection.commit()

#Flask test les IO
@app.route('/io', methods=['POST'])
def io():
    print(request.json)
    isVitGauche = request.json['isVitGauche']
    isVitDroite = request.json['isVitDroite']
    isDirDroite = request.json['isDirDroite']
    isDirGauche = request.json['isDirGauche']
    GPIO.output(GPIO_PIN_VIT_GAUCHE, isVitGauche)
    GPIO.output(GPIO_PIN_VIT_DROITE, isVitDroite)
    GPIO.output(GPIO_PIN_DIR_GAUCHE, isDirGauche)
    GPIO.output(GPIO_PIN_DIR_DROITE, isDirDroite)
    return jsonify({'message': 'IO controlés!'})

def gauche():
    print('Gauche!')
    GPIO.output(GPIO_PIN_VIT_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_VIT_DROITE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_GAUCHE, GPIO.LOW)
    GPIO.output(GPIO_PIN_DIR_DROITE, GPIO.LOW)
    time.sleep(1)

def droite():
    print('Droite!')
    GPIO.output(GPIO_PIN_VIT_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_VIT_DROITE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_DROITE, GPIO.HIGH)
    time.sleep(1)

def enAvant():
    print('En avant!')
    GPIO.output(GPIO_PIN_VIT_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_VIT_DROITE, GPIO.LOW)
    GPIO.output(GPIO_PIN_DIR_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_DROITE, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(GPIO_PIN_VIT_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_VIT_DROITE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_DROITE, GPIO.LOW)
    time.sleep(0.4)
    GPIO.output(GPIO_PIN_VIT_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_VIT_DROITE, GPIO.LOW)
    GPIO.output(GPIO_PIN_DIR_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_DROITE, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(GPIO_PIN_VIT_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_VIT_DROITE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_DROITE, GPIO.LOW)
    time.sleep(0.4)
    GPIO.output(GPIO_PIN_VIT_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_VIT_DROITE, GPIO.LOW)
    GPIO.output(GPIO_PIN_DIR_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_DROITE, GPIO.LOW)
    time.sleep(0.1)

def enArriere():
    print('En arriere!')
    GPIO.output(GPIO_PIN_VIT_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_VIT_DROITE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_GAUCHE, GPIO.LOW)
    GPIO.output(GPIO_PIN_DIR_DROITE, GPIO.HIGH)
    time.sleep(1)

#Flask controle moteurs
@app.route('/moteurs', methods=['POST'])
def moteurs():
    print(request.json)
    isLeftPressed = request.json['isLeftPressed']
    isRightPressed = request.json['isRightPressed']
    isForwardPressed = request.json['isForwardPressed']
    isReversePressed = request.json['isReversePressed']
    if isLeftPressed:
        gauche()
    elif isRightPressed:
        droite()
    elif isForwardPressed:
        enAvant()
    elif isReversePressed:
        enArriere()
    else:
        stop()
    return jsonify({'message': 'Moteurs controlés!'})

#Start/stop opencv
@app.route('/opencv', methods=['POST'])
def opencv():
    print(request.json)
    return jsonify({'message': 'opencv controlé!'})

if __name__ == '__main__':
    stop()
    app.run(host='0.0.0.0')