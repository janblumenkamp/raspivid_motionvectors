import numpy as np
import cv2
import socket
import math
import struct

width = 1920
height = 1080
framelength = int(((width+16)/16) * ((height+8)/16)*4)

def showFlow(data):
  index = 0
  # Load an color image in grayscale
  img = np.zeros((height,width,3), np.uint8)
  for y in range(8, height+8, 16):
    for x in range(8, width, 16):
      x_motion = int(data[index + 0] / 15)
      y_motion = int(data[index + 1] / 15)
      if math.sqrt(x_motion*x_motion + y_motion*y_motion) > 0:
        cv2.line(img, (x, y), (x + x_motion, y + y_motion), (255, 0, 0))
      
      index = index + 4
    index = index + 4
  
  cv2.imshow('image',img)
  cv2.waitKey(1)

def showDenseFlow(data, ang_min, ang_max):
  index = 0
  # Load an color image in grayscale
  hsv = np.zeros((int((height + 8) / 16), int(width / 16), 3), np.uint8)
  for y in range(int((height + 8) / 16)):
    for x in range(int(width / 16)):
      x_motion = float(data[index + 0])
      y_motion = float(data[index + 1])
      
      mag, ang = cv2.cartToPolar(x_motion, y_motion)
      ang_deg = ang[0]*180/np.pi/2
      if ang_deg >= ang_min and ang_deg <= ang_max:
        hsv[y][x][0] = ang_deg
        hsv[y][x][1] = 255.0
        if mag[0][0] > 255.0:
          mag[0][0] = 255.0
        hsv[y][x][2] = mag[0][0]
        
      index = index + 4
    index = index + 4
  
  bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
  img = cv2.resize(bgr, (640, 480))
  cv2.imshow('image',img)
  cv2.waitKey(1)
  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 1234))

framedata = []
while 1:
    data = s.recv(1024)
    if not data: break
    
    framedata.extend(struct.unpack('>%db' % len(data), data))
    while (len(framedata)) >= framelength:
      #showFlow(framedata)
      showDenseFlow(framedata, 0, 360)
      framedata = framedata[framelength:]

cv2.destroyAllWindows()

