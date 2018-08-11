import numpy as np
import cv2
import os
import sys
import math
import struct

width = 1920
height = 1080
framelength = int(((width+16)/16) * ((height+8)/16)*4)

def convImg(data, width, height):
  index = 0
  proc = np.zeros((int((height + 8) / 16), int(width / 16), 2), np.int8)
  for y in range(int((height + 8) / 16)):
    for x in range(int(width / 16)):
      proc[y][x][0] = np.int8(data[index + 0])
      proc[y][x][1] = np.int8(data[index + 1])
      
      index = index + 4
    index = index + 4
  
  return proc

def vectorFlow(data):
  # Load an color image in grayscale
  img = np.zeros((height,width,3), np.uint8)
  for y in range(len(data)):
    for x in range(len(data[0])):
      if math.sqrt(int(data[y][x][0]) * int(data[y][x][0]) + int(data[y][x][1]) * int(data[y][x][1])) > 0:
        img_pos_x = x * 16 + 8
        img_pos_y = y * 16 + 8
        cv2.line(img, (img_pos_x, img_pos_y), (img_pos_x + int(data[y][x][0] / 15), img_pos_y + int(data[y][x][1] / 15)), (255, 0, 0))
        
  return img

def denseFlow(data, ang_min, ang_max):
  # right: green
  # links: red
  # top:
  # down: blue
  # Load an color image in grayscale
  hsv = np.zeros((int((height + 8) / 16), int(width / 16), 3), np.uint8)
  for y in range(len(data)):
    for x in range(len(data[0])):
      x_motion = float(data[y][x][0])
      y_motion = float(data[y][x][1])
      
      angle = math.atan2(y_motion, x_motion) * (90.0/math.pi) + 90.0
      magnitude = math.sqrt(x_motion * x_motion + y_motion * y_motion)
      if angle >= ang_min and angle <= ang_max:
        hsv[y][x][0] = angle
        hsv[y][x][1] = 255.0
        if magnitude > 255.0:
          magnitude = 255.0
        hsv[y][x][2] = magnitude
        
  bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
  img = cv2.resize(bgr, (0,0), fx=4, fy=4)
  return img

def proc(data):
  #res = denseFlow(data, 0, 360)
  res = vectorFlow(data)
  cv2.imshow('image',res)
  cv2.waitKey(1)

framedata = []
stdin_no = sys.stdin.fileno()
while 1:
    data = os.read(stdin_no, 1024)
    framedata.extend(struct.unpack('>%db' % len(data), data))
    while (len(framedata)) >= framelength:
      data = convImg(framedata, width, height)
      proc(data)
      framedata = framedata[framelength:]

cv2.destroyAllWindows()

