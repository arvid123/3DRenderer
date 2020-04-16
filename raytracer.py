#from PIL import Image
#from numpy import asarray
#img = Image.new(mode = "RGB", size = (3, 4), color = 'red')
#img2 = Image.fromarray(asarray(img), "RGB")
#print(asarray(img))
#img2.save("red3x4.png")

from numpy import array
from util import square
from util import normalize
from math import sqrt

class Vector:
    def __init__(self, x, y, z):
        self.__vec_array = array([x, y, z])
    
    @property
    def x(self):
        return self.__vec_array[0]
    
    @property
    def y(self):
        return self.__vec_array[1]

    @property
    def z(self):
        return self.__vec_array[2]

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
    def __init__(self, origin : Vector, direction : Vector):
        self.origin = origin
        self.direction = normalize(direction)

class Sphere:
    def __init__(self, center : Vector, radius : float):
        self.center = center
        self.radius = radius
        # Used to make calculations faster since multiplication often is faster than division
        self.inv_radius = 1.0 / radius
        # Precomputed for performance reasons.
        self.square_radius = radius * radius 

    # The "pure mathematical" way of finding the intersection points.
    # The equations for the ray and the sphere are combined and then solved to find up to two
    # intersection points, than the closest one is selected (if it exists).
    # t0 and t1 are the intersection points, t1 is only computed if t0 is found to be negative (and therefore invalid).
    # For a more in-depth look at the math see p. 35 of An Introduction to Ray Tracing by Morgan Kaufmann
    def intersect(self, ray):
        b = 2 * (ray.direction.x * (ray.origin.x - self.center.x) + 
         ray.direction.y * (ray.origin.y - self.center.y) + 
         ray.direction.z * (ray.origin.z - self.center.z))
        c = square(ray.origin.x - self.center.x) + square(ray.origin.y - self.center.y) + square(ray.origin.z - self.center.z) - self.square_radius
        discriminant = square(b) - 4 * c
        # The ray misses the sphere
        if discriminant < 0:
            return None
        # The square root of the discriminant is precomputed since
        # taking the square root often is an expensive operation.
        sqrt_discriminant = sqrt(discriminant)
        t0 = (-b -sqrt_discriminant) / 2
        # Intersection is not behind the origin of the ray
        if t0 >= 0:
            return Vector(ray.origin.x + ray.direction.x * t0,
                          ray.origin.y + ray.direction.y * t0,
                          ray.origin.z + ray.direction.z * t0)
        else:
            t1 = (-b +sqrt_discriminant) / 2
            return Vector(ray.origin.x + ray.direction.x * t1,
                          ray.origin.y + ray.direction.y * t1,
                          ray.origin.z + ray.direction.z * t1)