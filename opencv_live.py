import cv2
import numpy as np
import time
import RPi.GPIO as GPIO

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

def gauche():
    print('Gauche!')
    GPIO.output(GPIO_PIN_VIT_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_VIT_DROITE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_GAUCHE, GPIO.LOW)
    GPIO.output(GPIO_PIN_DIR_DROITE, GPIO.LOW)
    time.sleep(0.01)

def droite():
    print('Droite!')
    GPIO.output(GPIO_PIN_VIT_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_VIT_DROITE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_GAUCHE, GPIO.HIGH)
    GPIO.output(GPIO_PIN_DIR_DROITE, GPIO.HIGH)
    time.sleep(0.01)

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
    lower_red = np.array([0, 200, 200])
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

# Example usage with a video file
cap = cv2.VideoCapture(0)

previous = "nothing"
lostCount = 0

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
        lostCount = 0
        if(center[0]>300):
            droite()
            previous = "droite"
        elif(center[0]<200):
            gauche()
            previous = "gauche"
        enAvant()
    elif previous == "gauche" and lostCount < 100:
        droite()
        lostCount+=1
    elif previous == "droite" and lostCount < 100:
        gauche()
        lostCount+=1

    stop()


    # Display the resulting frame
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
#https://prod.liveshare.vsengsaas.visualstudio.com/join?7965525734CBACA3A2FF4A6E4E10F2C513D0