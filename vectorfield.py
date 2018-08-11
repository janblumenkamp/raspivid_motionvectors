import math
import numpy as np

class VectorField:
  def __init__(self, rawData, originalWidth, originalHeight):
    self.originalWidth = originalWidth
    self.originalHeight = originalHeight
    self.width = int(originalWidth / 16)
    self.height = int(originalHeight / 16)
    self.data_cartesian = np.zeros((self.height, self.width, 2), np.int8)
    self.data_polar = np.zeros((self.height, self.width, 2), np.int16)
    index = 0
    for y in range(self.height):
      for x in range(self.width):
        dx = rawData[index + 0]
        dy = rawData[index + 1]
        self.data_cartesian[y][x][0] = np.int8(dx)
        self.data_cartesian[y][x][1] = np.int8(dy)
        
        angle = math.atan2(self.dy(x, y), self.dx(x, y)) * (90.0 / math.pi) + 90.0
        magnitude = math.sqrt(float(self.dx(x, y)) * float(self.dx(x, y)) + float(self.dy(x, y)) * float(self.dy(x, y)))
        self.data_polar[y][x][0] = np.int16(angle)
        self.data_polar[y][x][1] = np.int16(magnitude)
        
        index = index + 4
      index = index + 4
  
  def dx(self, x, y):
    return self.data_cartesian[y][x][0]
    
  def dy(self, x, y):
    return self.data_cartesian[y][x][1]
    
  def angle(self, x, y):
    return self.data_polar[y][x][0]
    
  def mag(self, x, y):
    return self.data_polar[y][x][1]
