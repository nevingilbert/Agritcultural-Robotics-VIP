import math
class Point:
    def __init__(self, x, y, z=None):
        self.x = x
        self.y = y
        self.z = z

    def equals(self, p):
        if p.z is None:
            return p.x == self.x and p.y == self.y
        else:
            return p.x == self.x and p.y == self.y and self.z == p.z

    def __repr__(self):
        if self.z is None:
            return ('(' + str(self.x) + ', ' + str(self.y) + ')')
        else:
            return ('(' + str(self.x) + ', ' + str(self.y) + ',' + str(self.z) + ')')

class Vector:
    def __init__(self, x, y, z):
      self.x = x
      self.y = y
      self.z = z
   
    def magnitude(self):
      return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
   
    def normalize(self):
      return Vector(self.x / self.magnitude(), self.y / self.magnitude(), self.z / self.magnitude())
   
    def add(self, v):
      return Vector(self.x + v.x, self.y + v.y, self.z + v.z)

    def scale(self, s):
        return Vector(self.x * 2, self.y * 2, self.z * 2)
    
    def __repr__(self):
      return ('<' + str(self.x) + ', ' + str(self.y) + ',' + str(self.z) + '>')


def distance (a : Point, b :Point):
   return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z-b.z) ** 2)