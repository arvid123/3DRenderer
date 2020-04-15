import math

def normalize(vec):
    length = math.sqrt(vec.x * vec.x + vec.y * vec.y + vec.z * vec.z)
    if length == 0:
        return vec
    else:
        return vec / length 