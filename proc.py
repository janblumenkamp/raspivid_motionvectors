import numpy as np
import cv2
import socket

width = 1920
height = 1080
framelength = int(((width+16)/16) * ((height+8)/16)*4)

def showFlow(data):
  index = 0
  # Load an color image in grayscale
  img = np.zeros((height,width,3), np.uint8)
  for y in range(8, height+16, 16):
    for x in range(8, width, 16):
      x_motion = int(data[index + 0] / 15)
      y_motion = int(data[index + 1] / 15)
      if x == (8+16*10) and y == (8 + 16*10) and (data[index + 0] > 10 or data[index + 1] > 10):
        print(data[index + 0], data[index + 1])
      cv2.line(img, (x, y), (x + x_motion, y + y_motion), (255, 0, 0))
      
      index = index + 4
    index = index + 4
  
  cv2.imshow('image',img)
  cv2.waitKey(1)
'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('raspberrypi.local', 1234))

framedata = bytearray()
while 1:
    data = s.recv(1024)
    if not data: break
    framedata.extend(data)
    while (len(framedata)) >= framelength:
      showFlow(framedata)
      framedata = framedata[framelength:]

'''  
rawInput = np.fromfile('out_stream.txt', np.byte)
print("len", len(rawInput))
for i in range(100):
  if len(rawInput) < framelength:
    print("err: len")
    break
    
  showFlow(rawInput)
  rawInput = rawInput[framelength:]

cv2.destroyAllWindows()

