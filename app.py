from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import threading

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

#Flask page d'accueil
@app.route('/')
def index():
    return render_template('index.html')
 
#Flask test les IO
@app.route('/io', methods=['POST'])
def io():
    print(request.json)
    isVitGauche = request.json['isVitGauche']
    isVitDroite = request.json['isVitDroite']
    isDirDroite = request.json['isDirDroite']
    isDirGauche = request.json['isDirGauche']
    if isVitGauche:
        GPIO.output(GPIO_PIN_VIT_GAUCHE, GPIO.HIGH)
    elif isVitDroite:
        GPIO.output(GPIO_PIN_VIT_DROITE, GPIO.HIGH)
    elif isDirGauche:
        GPIO.output(GPIO_PIN_DIR_GAUCHE, GPIO.HIGH)
    elif isDirDroite:
        GPIO.output(GPIO_PIN_DIR_DROITE, GPIO.HIGH)
    else:
        print('ERREUR!')
        return jsonify({'message': 'Erreur dans la commande des IO!'})
    print('1 sec...')
    time.sleep(1)
    print('On arrete...')
    stop()
    print('Fini!')
    return jsonify({'message': 'IO controlé!'})

def gauche():
    print('Gauche!')
    GPIO.output(GPIO_PIN_VIT_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_VIT_DROITE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_GAUCHE, GPIO.LOW)
    GPIO.output(GPIO_PIN_DIR_DROITE, GPIO.LOW)

def droite():
    print('Droite!')
    GPIO.output(GPIO_PIN_VIT_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_VIT_DROITE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_DROITE, GPIO.HIGH)

def enAvant():
    print('En avant!')
    GPIO.output(GPIO_PIN_VIT_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_VIT_DROITE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_DROITE, GPIO.LOW)

def enArriere():
    print('En arriere!')
    GPIO.output(GPIO_PIN_VIT_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_VIT_DROITE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_GAUCHE, GPIO.LOW)
    GPIO.output(GPIO_PIN_DIR_DROITE, GPIO.HIGH)


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
        print('ERREUR!')
        return jsonify({'message': 'Erreur dans la commande du moteur!'})
    print('1 sec...')
    time.sleep(1)
    print('On arrete...')
    stop()
    print('Fini!')
    return jsonify({'message': 'Moteurs controlé!'})

def run_flask():
    app.run(host='0.0.0.0', use_reloader=False)  # Important: use_reloader=False in a thread


def detect_red_ball(frame):
    """
    Detects a red ball in an image using OpenCV.

    Args:
        frame: The input image frame.

    Returns:
        A tuple containing:
            - The center coordinates of the detected ball (x, y) if found, 
              otherwise None.
            - The radius of the detected ball if found, otherwise None.
    """

    # Define the lower and upper bounds for red color in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Convert the image from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the red color range
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Apply Gaussian blur to reduce noise
    mask = cv2.GaussianBlur(mask, (9, 9), 3, 3)

    # Find contours in the masked image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour (assuming it's the ball)
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)

        # Fit a circle to the contour
        (x, y), radius = cv2.minEnclosingCircle(largest_contour)
        center = (int(x), int(y))
        radius = int(radius)

        return center, radius
    else:
        return None, None

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # Allow the program to exit even if the thread is running
    flask_thread.start()

    # Example usage with a video file
    cap = cv2.VideoCapture(0)

    while(True):

        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            break

        # Detect the red ball
        center, radius = detect_red_ball(frame)

        # Draw a circle around the detected ball if found
        if center is not None:
            cv2.circle(frame, center, radius, (0, 255, 0), 2)
            print(center)
            if(center[0]>300):
                gauche()
                enAvant()
            elif(center[0]<200):
                droite()
                enAvant()

        # Display the resulting frame
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
