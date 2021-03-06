import raytracer.base as rt

from typing import NamedTuple


class World(NamedTuple):
    gravity: rt.Vector
    wind: rt.Vector


class Projectile(NamedTuple):
    position: rt.Point
    velocity: rt.Vector


def tick(world: World, p: Projectile) -> Projectile:
    pos = p.position + p.velocity
    velocity = p.velocity + world.gravity + world.wind
    return Projectile(pos, velocity)


start = rt.Point(0, 1, 0)
vel = rt.Vector(1, 1.8, 0).normalize() * 11.25
p = Projectile(start, vel)
gravity = rt.Vector(0, -0.1, 0)
wind = rt.Vector(-0.01, 0, 0)
w = World(gravity, wind)
c = rt.Canvas(900, 550)
c1 = rt.Color(1, 0, 0)
t = 0

while p.position.y > 0:
    print(f"Tick {t}: Position {p.position}")

    c.write_pixel(int(p.position.x), int(550 - p.position.y), c1)
    p = tick(w, p)
    t = t + 1

print(f"\nTook {t} ticks to hit ground")

with open("foo.ppm", "w") as ppm_file:
    ppm_file.write(c.to_ppm())
