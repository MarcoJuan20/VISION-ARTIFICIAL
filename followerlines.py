import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

# Inicialización de los pines GPIO para el puente H
motor1_pin1 = 17
motor1_pin2 = 18
motor1_enable = 27

motor2_pin1 = 22
motor2_pin2 = 23
motor2_enable = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor1_pin1, GPIO.OUT)
GPIO.setup(motor1_pin2, GPIO.OUT)
GPIO.setup(motor1_enable, GPIO.OUT)
GPIO.setup(motor2_pin1, GPIO.OUT)
GPIO.setup(motor2_pin2, GPIO.OUT)
GPIO.setup(motor2_enable, GPIO.OUT)

# Funciones para controlar los motores
def forward():
    GPIO.output(motor1_pin1, GPIO.HIGH)
    GPIO.output(motor1_pin2, GPIO.LOW)
    GPIO.output(motor1_enable, GPIO.HIGH)
    GPIO.output(motor2_pin1, GPIO.HIGH)
    GPIO.output(motor2_pin2, GPIO.LOW)
    GPIO.output(motor2_enable, GPIO.HIGH)

def left():
    GPIO.output(motor1_pin1, GPIO.HIGH)
    GPIO.output(motor1_pin2, GPIO.LOW)
    GPIO.output(motor1_enable, GPIO.HIGH)
    GPIO.output(motor2_pin1, GPIO.LOW)
    GPIO.output(motor2_pin2, GPIO.HIGH)
    GPIO.output(motor2_enable, GPIO.HIGH)

def right():
    GPIO.output(motor1_pin1, GPIO.LOW)
    GPIO.output(motor1_pin2, GPIO.HIGH)
    GPIO.output(motor1_enable, GPIO.HIGH)
    GPIO.output(motor2_pin1, GPIO.HIGH)
    GPIO.output(motor2_pin2, GPIO.LOW)
    GPIO.output(motor2_enable, GPIO.HIGH)

def stop():
    GPIO.output(motor1_enable, GPIO.LOW)
    GPIO.output(motor2_enable, GPIO.LOW)

# Captura de video desde la cámara de la Raspberry Pi
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if ret:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Umbral para detectar el color de la línea (ajusta los valores según tu entorno)
        lower_color = np.array([0, 0, 0])
        upper_color = np.array([179, 255, 50])
        mask = cv2.inRange(hsv, lower_color, upper_color)

        # Encuentra el contorno más grande
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            biggest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(biggest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Dibuja un círculo en el centro del contorno más grande
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                
                # Lógica de seguimiento de línea basada en la posición del centro del contorno
                if cx < 220:
                    left()
                elif cx > 420:
                    right()
                else:
                    forward()
        else:
            # Si no se detecta línea, gira hacia la derecha
            right()

        cv2.imshow('Frame', frame)
        cv2.imshow('Mask', mask)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Detiene los motores y libera la captura de video
stop()
GPIO.cleanup()
cv2.destroyAllWindows()
cap.release()
