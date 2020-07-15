# This code and much of the comments are heavily inspired by the book "An Introduction to Raytracing" edited by Andrew S. Glassner
# It is provided under this license https://creativecommons.org/licenses/by/4.0/

#from PIL import Image
#from numpy import asarray
#img = Image.new(mode = "RGB", size = (3, 4), color = 'red')
#img2 = Image.fromarray(asarray(img), "RGB")
#print(asarray(img))
#img2.save("red3x4.png")

from numpy import array
from numpy import dot
from util import square
from util import normalize
from math import sqrt

### Datatypes ###

class Vector:
    def __init__(self, vec_array):
        self.__vec_array = vec_array
    
    @property
    def x(self):
        return self.__vec_array[0]
    
    @property
    def y(self):
        return self.__vec_array[1]

    @property
    def z(self):
        return self.__vec_array[2]
    
    @property
    def vec_array(self):
        return self.__vec_array

    def dot(self, other):
        return self.vec_array[0] * other.vec_array[0] + self.vec_array[1] * other.vec_array[1] + self.vec_array[2] * other.vec_array[2]

    def __add__(self, other):
        return Vector(self.vec_array + other.vec_array)

    def __sub__(self, other):
        return Vector(self.vec_array - other.vec_array)
    
    def __mul__(self, other):
        return Vector(self.vec_array * other)

    def __truediv__(self, other):
        return Vector(self.vec_array / other)

    def __str__(self):
        return "(" + str(self.vec_array[0]) + ", " + str(self.__vec_array[1]) + ", " + str(self.__vec_array[2]) + ")"

""" A ray is similar to a line except that it doesn't extend behind the origin.
    A ray is defined as the set of points described by these equations:

    x = origin.x + t * direction.x
    y = origin.y + t * direction.y
    z = origin.z + t * direction.z
    t > 0
 
    Where t is an independent parameter. """
class Ray:
    def __init__(self, origin : Vector, direction : Vector):
        self.origin = origin
        self.direction = normalize(direction)

### Components ###

class SphereComponent:
    def __init__(self, center : Vector, radius : float):
        self.center = center
        self.radius = radius
        # Used to make calculations faster since multiplication often is faster than division
        self.inv_radius = 1.0 / radius
        # Precomputed for performance reasons.
        self.square_radius = radius * radius 

    def unit_normal_at(self, surface_point : Vector):
        return (surface_point - self.center) * self.inv_radius 

class CameraComponent:
    def _init_(self, fov):
        self.fov = fov

class LightComponent:
    def __init__(self, intensity):
        self.intensity = intensity

### Systems ###

""" The "geometric" way of calculating the intersection between a sphere and a ray.
    Step 1: Check whether the ray origin is inside or outside the sphere
    Step 2: Determine the distance from the origin of the ray to the
    closest point to the center of the sphere that is still on the ray
    Step 3: If the ray is outside the sphere and faces away from it, the ray doesn't intersect the sphere
    Step 4: Check if the point closest to the sphere is inside the sphere 
    Step 5: Calculate instersection point """
def raySphereIntersection(sphere, ray):
    # Origin of ray to center of sphere vector (Origin to Center)
    oc = sphere.center - ray.origin
    # Length squared of oc
    l2oc = oc.dot(oc)
    outside = l2oc > sphere.square_radius
    # t-value of point on the ray that is closest to the center of the sphere
    # (t Closest Approach)
    tca = oc.dot(ray.direction)
    # Ray originates outside the sphere and is pointing away from it,
    # therefore it cannot intersect it
    if tca < 0 and outside:
        return None
    t2ca = square(tca)
    # Check if the closest point is within the sphere, otherwise the ray misses
    d2 = square(l2oc - t2ca)
    t2hc = sphere.square_radius - d2
    if t2hc < 0:
        return None
    t = tca + sqrt(t2hc)
    if outside:
        t = tca - sqrt(t2hc)
    return Vector(array([ray.origin.x + ray.direction.x * t, ray.origin.y + ray.direction.y * t, ray.origin.z + ray.direction.z * t])) 

""" The "algebraic" way of finding the intersection points.
    The equations for the ray and the sphere are combined and then solved to find up to two
    intersection points, than the closest one is selected (if it exists).
    t0 and t1 are the intersection points, t1 is only computed if t0 is found to be negative (and therefore invalid).
    For a more in-depth look at the math see p. 35 of An Introduction to Ray Tracing by Morgan Kaufmann """
def algRaySphereIntersection(sphere, ray):
    b = 2 * (ray.direction.x * (ray.origin.x - sphere.center.x) + 
        ray.direction.y * (ray.origin.y - sphere.center.y) + 
        ray.direction.z * (ray.origin.z - sphere.center.z))
    c = square(ray.origin.x - sphere.center.x) + square(ray.origin.y - sphere.center.y) + square(ray.origin.z - sphere.center.z) - sphere.square_radius
    discriminant = square(b) - 4 * c
    # The ray misses the sphere
    if discriminant < 0:
        return None
    # The square root of the discriminant is precomputed since
    # taking the square root is often an expensive operation.
    sqrt_discriminant = sqrt(discriminant)
    t0 = (-b -sqrt_discriminant) / 2
    # Intersection is not behind the origin of the ray
    if t0 >= 0:
        return Vector(array([ray.origin.x + ray.direction.x * t0,
                        ray.origin.y + ray.direction.y * t0,
                        ray.origin.z + ray.direction.z * t0]))
    else:
        t1 = (-b +sqrt_discriminant) / 2
        return Vector(array([ray.origin.x + ray.direction.x * t1,
                        ray.origin.y + ray.direction.y * t1,
                        ray.origin.z + ray.direction.z * t1]))

#r = Ray(Vector(array([1, -2, -1])), Vector(array([1, 2, 4])))
#s = Sphere(Vector(array([3, 0, 5])), 3)

#print(s.intersect(r))
#print(s.unit_normal_at(s.intersect(r)))
