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