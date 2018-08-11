import numpy as np
import cv2
import os
import sys
import struct
from vectorfield import VectorField

def vectorFlow(data):
  # Load an color image in grayscale
  img = np.zeros((data.originalHeight, data.originalWidth, 3), np.uint8)
  for y in range(data.height):
    for x in range(data.width):
      if data.mag(x, y) > 0:
        img_pos_x = x * 16 + 8
        img_pos_y = y * 16 + 8
        cv2.line(img, (img_pos_x, img_pos_y), (img_pos_x + int(data.dx(x, y) / 15), img_pos_y + int(data.dy(x, y) / 15)), (255, 0, 0))
        
  return img

def denseFlow(data, ang_min, ang_max):
  # right: 
  # left: red
  # top: blue
  # down: green
  # Load an color image in grayscale
  hsv = np.zeros((data.height, data.width, 3), np.uint8)
  for y in range(data.height):
    for x in range(data.width):
      if data.angle(x, y) >= ang_min and data.angle(x, y) <= ang_max:
        hsv[y][x][0] = data.angle(x, y) # H: 0 - 179
        hsv[y][x][1] = 255.0 # S: 0 - 255
        mag = data.mag(x, y) * 2
        if mag > 255:
          mag = 255
        hsv[y][x][2] = float(mag) # V: 0 - 255
  bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
  img = cv2.resize(bgr, (0,0), fx=4, fy=4)
  return img

def proc(data):
  res = denseFlow(data, 0, 360)
  #res = vectorFlow(data)
  cv2.imshow('image',res)
  cv2.waitKey(1)

resolutions = [[1920, 1088], [640, 480]]
resolution = 1
framelength = int(((resolutions[resolution][0] + 16) / 16) * (resolutions[resolution][1] / 16) * 4)
framedata = []
stdin_no = sys.stdin.fileno()
while 1:
    data = os.read(stdin_no, 1024)
    framedata.extend(struct.unpack('>%db' % len(data), data))
    while (len(framedata)) >= framelength:
      data = VectorField(framedata, resolutions[resolution][0], resolutions[resolution][1])
      proc(data)
      framedata = framedata[framelength:]

cv2.destroyAllWindows()

