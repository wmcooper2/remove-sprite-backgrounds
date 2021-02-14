"""Let user decide which sprites to include in a spritesheet and automatically remove the background color.

    1. scale and translate the image where you want it.
    2. press "p" to set the primary reference color.
    3. press "s" to set the secondary reference color.
    4. press "r" to reset everything.

"""

#std lib
from collections import namedtuple
import sys
from typing import Tuple

#3rd party
from PIL import Image
import pyglet
from pyglet.window import key

#Make a window
window = pyglet.window.Window(800, 600)

#set mouse cursor to crosshairs
cursor = window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
window.set_mouse_cursor(cursor)


Point = namedtuple("Point", ["x", "y"])
Color = namedtuple("Color", ["red", "green", "blue"])

class Colors():
    def __init__(self):
        self.primary = None
        self.secondary = None

    def primary(red: int, green: int, blue: int) -> None:
        self.primary = (red, green, blue)

    def secondary(red: int, green: int, blue: int) -> None:
        self.secondary = (red, green, blue)

    def reset(self) -> None:
        self.primary = None
        self.secondary = None

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
        self.top_line = pyglet.shapes.Line(self.a.x, self.a.y, self.b.x, self.b.y, width=self.line_width, color=self.color, batch=self.batch)
        self.bottom_line = pyglet.shapes.Line(self.a.x, self.a.y, self.b.x, self.b.y, width=self.line_width, color=self.color, batch=self.batch)
        self.right_line = pyglet.shapes.Line(self.a.x, self.a.y, self.b.x, self.b.y, width=self.line_width, color=self.color, batch=self.batch)
        self.left_line = pyglet.shapes.Line(self.a.x, self.a.y, self.b.x, self.b.y, width=self.line_width, color=self.color, batch=self.batch)

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

class Labels():
    def __init__(self):
        #label box
        self.background = pyglet.graphics.Batch()
        self.box_height = 30
        self.box_width = 800
        self.box_color = (0, 0, 0)
        self.rectangle = pyglet.shapes.Rectangle(0, 0, self.box_width, self.box_height, color=self.box_color, batch=self.background)
        self.p_label = "Pri:"
        self.s_label = "Sec:"
        self.start_label = "Start:"
        self.end_label = "End:"

        #labels
        self.label_y_offset = 10
        self.labels = pyglet.graphics.Batch()
        self.label_color = (255, 0, 0, 255)
        self.primary = pyglet.text.Label(self.p_label, color=self.label_color, x=0, y=0+self.label_y_offset, batch=self.labels)
        self.secondary = pyglet.text.Label(self.s_label, color=self.label_color, x=150, y=0+self.label_y_offset, batch=self.labels)
        self.start = pyglet.text.Label(self.start_label, color=self.label_color, x=300, y=0+self.label_y_offset, batch=self.labels)
        self.end = pyglet.text.Label(self.end_label, color=self.label_color, x=450, y=0+self.label_y_offset, batch=self.labels)

    def update(self, a: Point, b: Point, primary: Color, secondary: Color) -> None:
        self.primary.text = f"{self.p_label} {str(primary)}"
        self.secondary.text = f"{self.s_label} {str(secondary)}"
        self.start.text = f"{self.start_label} [{a.x}, {a.y}]"
        self.end.text = f"{self.end_label} [{b.x}, {b.y}]"
        self.background.draw()
        self.labels.draw()

    def reset(self) -> None:
        self.p_label = "Pri:"
        self.s_label = "Sec:"
        self.start_label = "Start:"
        self.end_label = "End:"

class SpriteSheet():
    def __init__(self):
        self.y_offset = 30
        self.speed = 40
        self.rate = 1.5
        self.zoom = 1
        self.sheet = pyglet.resource.image(sys.argv[1])
        self.seq = pyglet.image.ImageGrid(self.sheet, 1, 1)
        self.anim = pyglet.image.Animation.from_image_sequence(self.seq, 0.2, True)
        self.batch = pyglet.graphics.Batch()
        self.sprite_sheet = pyglet.sprite.Sprite(self.anim, y=self.y_offset, batch=self.batch)

    def update(self) -> None:
        self.batch.draw()

    def scale_up(self) -> None:
        self.sprite_sheet.scale *= self.rate
        self.zoom *= self.rate

    def scale_down(self) -> None:
        self.sprite_sheet.scale /= self.rate
        self.zoom /= self.rate

    def move_up(self) -> None:
        self.sprite_sheet.y += self.speed * self.rate

    def move_down(self) -> None:
        self.sprite_sheet.y -= self.speed * self.rate

    def move_left(self) -> None:
        self.sprite_sheet.x -= self.speed * self.rate

    def move_right(self) -> None:
        self.sprite_sheet.x += self.speed * self.rate

class Loop():
    def __init__(self, window):
        self.window = window
        self.spritesheet = SpriteSheet()
        self.outline = OutLine()
        self.labels = Labels()
        self.colors = Colors()
        self.reference_image = Image.open(sys.argv[1])

    def points_chosen(self) -> bool:
        return loop.colors.primary is not None \
                and loop.colors.secondary is not None \
                and loop.outline.start[0] != 0 \
                and loop.outline.start[1] != 0

    def set_primary_color(self) -> None:
        #print pixel location, compare to the screen
        #get pixel data from Point; self.outline.a
        #mouse location + image location * zoom; self.outline.a.x + self.spritesheet.sprite_sheet.x * self.spritesheet.sprite_sheet.rate
        #mouse location, adjust for image location and zoom
        self.colors.primary = "test"

    def set_secondary_color(self) -> None:
        self.colors.secondary = "test"

    def update(self, dt) -> None:
        self.window.clear()
        self.spritesheet.update()
        self.outline.update()
        self.labels.update(self.outline.a, self.outline.b, self.colors.primary, self.colors.secondary)

    def reset(self) -> None:
        self.outline.reset()
        self.labels.reset()
        self.colors.reset()





@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    loop.outline.end(x, y)

@window.event
def on_mouse_press(x, y, button, modifiers):
    """Set the starting point."""
    if loop.colors.primary is None:
        loop.set_primary_color()
    elif loop.colors.secondary is None:
        loop.set_secondary_color()
    else:
        loop.outline.start(x, y)
        loop.outline.end(x, y)

@window.event
def on_mouse_release(x, y, button, modifiers):
    if loop.colors.primary is not None and loop.colors.secondary is not None:
        loop.outline.end(x, y)
        print(loop.outline)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.U:
        loop.spritesheet.scale_up()
    elif symbol == key.D:
        loop.spritesheet.scale_down()
    elif symbol == key.UP:
        loop.spritesheet.move_up()
    elif symbol == key.DOWN:
        loop.spritesheet.move_down()
    elif symbol == key.LEFT:
        loop.spritesheet.move_left()
    elif symbol == key.RIGHT:
        loop.spritesheet.move_right()
    elif symbol == key.R:
        loop.reset()
    elif symbol == key.P:
        print("pixel choice")

    elif symbol == key.S:
        pointA = loop.outline.a
        pointB = loop.outline.b
        offset = loop.labels.box_height
#         print("offset", offset)

        height = loop.reference_image.height
#         print("height:", height)

        #PIL inverts y-axis
        left = min(pointA.x, pointB.x)
        right = max(pointA.x, pointB.x)
        top = min(pointA.y, pointB.y) - offset
        bottom = max(pointA.y, pointB.y) - offset
#         print(f"LTRB: {left}, {top}, {right}, {bottom}")

        bottom_line = loop.reference_image.height - bottom
        top_line = loop.reference_image.height - top
#         print(f"bottom_line {bottom_line}, top_line {top_line}")
#         print(f"pointA {pointA}, pointB {pointB}")
        preview_image = loop.reference_image.crop((left, bottom_line, right, top_line))
#         print(preview_image)
        preview_image.show()

if __name__ == "__main__":
    frame_speed = 1/60
    keyboard = key.KeyStateHandler()
    window.push_handlers(keyboard)
    loop = Loop(window)

    pyglet.clock.schedule_interval(loop.update, frame_speed)
    pyglet.app.run()


#load file in Pillow for easy pixel access
# img = Image.open(file_).convert("RGBA")
# ref = img.getpixel((0,0))
# ref = img.getpixel((ref_x, ref_y))
