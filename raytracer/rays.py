import math
from raytracer.base import *
from typing import NamedTuple, Any


class Ray:
    def __init__(self, origin: Point, direction: Vector):
        self.origin = origin
        self.direction = direction

    def position(self, time: float):
        return self.origin + self.direction * time

    def transform(self, m: Matrix):
        return Ray(m * self.origin, m * self.direction)

    def __str__(self):
        return f"Ray: Origin: {self.origin}, Direction: {self.direction}"


class Comps(NamedTuple):
    t: float
    object: Any
    point: Point
    eyev: Vector
    normalv: Vector
    inside: bool
    over_point: Point


class Intersection:
    def __init__(self, t: float, object):
        self.object = object
        self.t = t

    def __lt__(self, other):
        return self.t < other.t

    def prepare_computations(self, ray: Ray):
        point = ray.position(self.t)
        normalv = self.object.normal_at(point)
        eyev = -ray.direction
        inside = False

        if normalv.dot(eyev) < 0:
            inside = True
            normalv = -normalv
        over_point = point + (normalv * EPSILON)
        return Comps(
            self.t, self.object, point, -ray.direction, normalv, inside, over_point
        )

    def __str__(self):
        return f"Intersection\nt:{self.t}\nobject: {self.object}"


class Intersections(list):
    def __init__(self, *args):
        super(Intersections, self).__init__(args)

    def hit(self) -> Intersection:
        hit = None
        for i in self:
            if i.t > 0 and (hit is None or i.t < hit.t):
                hit = i
        return hit
