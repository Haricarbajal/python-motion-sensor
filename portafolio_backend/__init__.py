import cv2
import time
import datetime
import numpy as np
from sys import exit

display = True

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)


def marcar_zonas(frame_mov, frame_original):
    frame_mov = cv2.GaussianBlur(frame_mov, (21, 21), 0)
    limites = cv2.threshold(frame_mov, 5, 255, cv2.THRESH_BINARY)[1]
    limites = cv2.dilate(limites, None, iterations=2)
    contours, hierarchy = cv2.findContours(limites.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    movimiento_detectado = False
    for c in contours:
        if cv2.contourArea(c) < 800:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        print(x, y, w, h)
        cv2.rectangle(frame_original, (x, y), (x + w, y + h), (0, 0, 255), 1)
        movimiento_detectado = True

    if movimiento_detectado:
        timestamp = datetime.datetime.now()
        ts = timestamp.strftime("%d %B %Y %I:%M:%S%p")
        cv2.rectangle(frame_original, (2, 220), (185, 235), (0, 0, 0), -1)
        cv2.putText(frame_original, ts, (5, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255))
        # save the file with detected movement
        cv2.imwrite("captura_actual.jpg", frame_original)
    return frame_original


# OpenCV version information
print("OpenCV Version: {}".format(cv2.__version__))

# Initialize camera
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("ERROR: Camera not operational")
    exit(-1)  # Camera access error

if display:
    win_zonas = "Differential Image"
    win_original = "Original Image"
    win_marcas = "Marked Zones"
    cv2.namedWindow(win_zonas)
    cv2.namedWindow(win_original)
    cv2.namedWindow(win_marcas)

# Read the first three images
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

original = cv2.resize(cam.read()[1], (320, 240), interpolation=cv2.INTER_CUBIC)

while True:
    # Calculate the changed zones
    imagen_delta = diffImg(
        cv2.resize(t_minus, (320, 240), interpolation=cv2.INTER_CUBIC),
        cv2.resize(t, (320, 240), interpolation=cv2.INTER_CUBIC),
        cv2.resize(t_plus, (320, 240), interpolation=cv2.INTER_CUBIC),
    )
    imagen_zonas_marcadas = marcar_zonas(imagen_delta, original.copy())

    if display:
        cv2.imshow(win_marcas, imagen_zonas_marcadas)
        cv2.imshow(win_zonas, imagen_delta)
        cv2.imshow(win_original, original)

    # Read the next images
    t_minus = t
    t = t_plus
    t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    original = cv2.resize(cam.read()[1], (320, 240), interpolation=cv2.INTER_CUBIC)

    # If we press the "q" key we exit the loop and finish
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Finish
cam.release()
cv2.destroyAllWindows()
print("End!!!")
