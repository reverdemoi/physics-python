import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def subtract(vector1, vector2):
    return Vector(vector1.x - vector2.x, vector1.y - vector2.y)

def add(vector1, vector2):
    return Vector(vector1.x + vector2.x, vector1.y + vector2.y)

def normalize(vector):
    length = math.sqrt(vector.x ** 2 + vector.y ** 2)
    if length == 0:
        return Vector(0, 0)
    return Vector(vector.x / length, vector.y / length)

def multiply(vector, scalar):
    return Vector(vector.x * scalar, vector.y * scalar)

def magnitude(vector):
    return math.sqrt(vector.x ** 2 + vector.y ** 2)

def dotProduct(vector1, vector2):
    return vector1.x * vector2.x + vector1.y * vector2.y