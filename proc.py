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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 1234))

framedata = []
while 1:
    data = s.recv(1024)
    if not data: break
    
    framedata.extend(struct.unpack('>%db' % len(data), data))
    while (len(framedata)) >= framelength:
      showFlow(framedata)
      framedata = framedata[framelength:]

cv2.destroyAllWindows()

