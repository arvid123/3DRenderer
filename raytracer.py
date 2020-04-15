#from PIL import Image
#from numpy import asarray
#img = Image.new(mode = "RGB", size = (3, 4), color = 'red')
#img2 = Image.fromarray(asarray(img), "RGB")
#print(asarray(img))
#img2.save("red3x4.png")

from numpy import array
import util

# A ray is similar to a line except that it doesn't extend behind the origin.
# A ray is defined as the set of points described by these equations:
#
# x = origin.x + t * direction.x
# y = origin.y + t * direction.y
# z = origin.z + t * direction.z
# t > 0
# 
# Where t is an independent parameter.
class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = util.normalize(direction)

class Sphere:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        # The multiplicative inverse of the radius.
        # Used to make calculations faster since multiplication often is faster than division
        self.inv_radius = 1.0 / radius
        # The square of the radius.
        # Precomputed for performance reasons.
        self.square_radius = radius * radius 

