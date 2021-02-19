#std lib
import sys

#3rd party
import pyglet

#custom
from constants import Point

class OutLine():
    def __init__(self):
        self.primary_ref = 0
        self.secondary_ref = 0
        self.color = (255, 0, 0)
        self.line_width = 3
        self.a = Point(0, 0)
        self.b = Point(0, 0)
        self.width = 0
        self.height = 0
        self.batch = pyglet.graphics.Batch()
        self.top_line = pyglet.shapes.Line(
            self.a.x,
            self.a.y,
            self.b.x,
            self.b.y,
            width=self.line_width,
            color=self.color,
            batch=self.batch)
        self.bottom_line = pyglet.shapes.Line(
            self.a.x,
            self.a.y,
            self.b.x,
            self.b.y,
            width=self.line_width,
            color=self.color,
            batch=self.batch)
        self.right_line = pyglet.shapes.Line(
            self.a.x,
            self.a.y,
            self.b.x,
            self.b.y,
            width=self.line_width,
            color=self.color,
            batch=self.batch)
        self.left_line = pyglet.shapes.Line(
            self.a.x,
            self.a.y,
            self.b.x,
            self.b.y,
            width=self.line_width,
            color=self.color,
            batch=self.batch)

    def update(self) -> None:
        self.dimensions()
        self.box_coords()
        self.batch.draw()

    def dimensions(self) -> None:
        """Set the outline's width and height."""
        self.width = abs(self.a.x - self.b.x)
        self.height = abs(self.a.y - self.b.y)

    def box_coords(self) -> None:
        """Set the outline's perimeter"""
        self.top_line.position = (self.a.x, self.a.y, self.b.x, self.a.y)
        self.bottom_line.position = (self.a.x, self.b.y, self.b.x, self.b.y)
        self.left_line.position = (self.a.x, self.a.y, self.a.x, self.b.y)
        self.right_line.position = (self.b.x, self.a.y, self.b.x, self.b.y)

    def start(self, x: int, y: int)-> None:
        self.a = Point(x, y)

    def end(self, x: int, y: int) -> None:
        self.b = Point(x, y)

    def reset(self) -> None:
        self.a = Point(0, 0)
        self.b = Point(0, 0)

    def __str__(self) -> None:
        return str(f"A={self.a} B={self.b} w={self.width} h={self.height}")


class SpriteSheet():
    def __init__(self):
        self.rate = 1.5
        self.sheet = pyglet.resource.image(sys.argv[1])
        self.seq = pyglet.image.ImageGrid(self.sheet, 1, 1)
        self.anim = pyglet.image.Animation.from_image_sequence(self.seq, 0.2, True)
        self.batch = pyglet.graphics.Batch()
        self.sprite_sheet = pyglet.sprite.Sprite(self.anim, batch=self.batch)
        self.translation_x = 0
        self.translation_y = 0
        self.translation_speed = 40

    def update(self) -> None:
        self.batch.draw()

    def scale_up(self) -> None:
        self.sprite_sheet.scale += 1
        if self.sprite_sheet.scale >= 6:
            self.sprite_sheet.scale = 6

    def scale_down(self) -> None:
        self.sprite_sheet.scale -= 1
        if self.sprite_sheet.scale <= 1:
            self.sprite_sheet.scale = 1

    def move_up(self) -> None:
        self.sprite_sheet.y +=  self.translation_speed
#         self.sprite_sheet.y += self.speed // self.sprite_sheet.scale

    def move_down(self) -> None:
        self.sprite_sheet.y -= self.translation_speed
#         self.sprite_sheet.y -= self.speed // self.sprite_sheet.scale

    def move_left(self) -> None:
        self.sprite_sheet.x -= self.translation_speed
#         self.sprite_sheet.x -= self.speed // self.sprite_sheet.scale

    def move_right(self) -> None:
        self.sprite_sheet.x += self.translation_speed
#         self.sprite_sheet.x += self.speed // self.sprite_sheet.scale

