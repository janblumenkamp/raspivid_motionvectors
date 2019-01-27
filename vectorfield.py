import math
import numpy as np

class VectorField:
  def __init__(self, rawData, originalWidth, originalHeight):
    self.width = int(originalWidth / 16)
    self.height = int(originalHeight / 16)
    self.data = np.reshape(rawData[:(self.height * (self.width + 1) * 4)], (self.height, self.width + 1, 4)).astype(np.int8, copy=False)

  def dx(self, x, y):
    return self.data[y][x][0]

  def dy(self, x, y):
    return self.data[y][x][1]

  def angle(self, x, y):
    return math.atan2(self.dy(x, y), self.dx(x, y)) * (90.0 / math.pi) + 90.0

  def mag(self, x, y):
    return math.sqrt(float(self.dx(x, y)) * float(self.dx(x, y)) + float(self.dy(x, y)) * float(self.dy(x, y)))

  def getData(self):
    return self.data
