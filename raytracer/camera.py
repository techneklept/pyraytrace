import math
import raytracer.base as rt
import raytracer.rays as rays
from raytracer.world import World


class Camera:
    def __init__(self, hsize: int, vsize: int, fov: float, transform: rt.Matrix = None):
        self.hsize = hsize
        self.vsize = vsize
        self.fov = fov
        if transform is None:
            transform = rt.Identity()

        self.transform = transform
        half_view = math.tan(self.fov / 2)
        aspect = self.hsize / self.vsize
        if aspect >= 1:
            self.half_width = half_view
            self.half_height = half_view / aspect
        else:
            self.half_width = half_view * aspect
            self.half_height = half_view

        self.pixel_size = (self.half_width * 2) / self.hsize

    def ray_for_pixel(self, x: int, y: int) -> rays.Ray:
        xoffset = (x + 0.5) * self.pixel_size
        yoffset = (y + 0.5) * self.pixel_size

        world_x = self.half_width - xoffset
        world_y = self.half_height - yoffset
        pixel = self.transform.inverse() * rt.Point(world_x, world_y, -1)
        origin = self.transform.inverse() * rt.Point(0, 0, 0)
        direction = (pixel - origin).normalize()
        return rays.Ray(origin, direction)

    def render(self, world: World):
        image = rt.Canvas(self.hsize, self.vsize)
        for y in range(0, self.vsize):
            for x in range(0, self.hsize):
                ray = self.ray_for_pixel(x, y)
                color = world.color_at(ray)
                image.write_pixel(x, y, color)

        return image
