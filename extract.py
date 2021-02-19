"""Let user decide which sprites to include in a spritesheet and automatically remove the background color.

    Make sure the image is in PNG format.

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

#custom
from constants import Color, Point
from control_panel import Colors, Labels
from workspace import OutLine, SpriteSheet

#Make a window
window = pyglet.window.Window(1000, 800)

#set mouse cursor to crosshairs
cursor = window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
window.set_mouse_cursor(cursor)




class App():
    def __init__(self, window):
        self.window = window
        self.spritesheet = SpriteSheet()
        self.outline = OutLine()
        self.labels = Labels(self.window)
        self.colors = Colors()
        self.reference_image = Image.open(sys.argv[1])
        self.image = pyglet.image.load(sys.argv[1])
        self.mouse_pos = Point(0, 0)

    def _debug_coord(self) -> None:
        """Print mouse coordinates for debugging."""
        sprite = self.sprite_mouse_pos()
        scaled_2_ref = Point(sprite.x // self.spritesheet.sprite_sheet.scale, sprite.y // self.spritesheet.sprite_sheet.scale)

        x = int(scaled_2_ref[0])
        y = int(self.image.height - scaled_2_ref[1])
        pixel = self.reference_image.getpixel((x, y))
#         print(f"Scaled: {scaled_2_ref}, RGB: {pixel}")

    def sprite_mouse_pos(self) -> Point:
        """Get the mouse position relative to the sprite sheet."""
        x = int(self.mouse_pos[0] - self.spritesheet.sprite_sheet.x)
        y = int(self.mouse_pos[1] - self.spritesheet.sprite_sheet.y)
        return Point(x, y)

    def ref_mouse(self) -> Point:
        """Get the mouse position relative to the original image."""
        y = (self.reference_image.height - self.mouse_pos[1]) + (self.spritesheet.sprite_sheet.y // self.spritesheet.sprite_sheet.scale)
        x = (self.mouse_pos[0] - self.spritesheet.sprite_sheet.x) // self.spritesheet.sprite_sheet.scale

        return Point(x, y)

    def points_chosen(self) -> bool:
        return loop.colors.primary is not None \
                and loop.colors.secondary is not None \
                and loop.outline.start[0] != 0 \
                and loop.outline.start[1] != 0

    def set_mouse_pos(self, x: int, y: int) -> None:
        self.mouse_pos = (x, y)

    def set_primary_pixel(self) -> None:
        self.colors.primary_pixel(self.mouse_pos)
        self.colors.primary = (0,0,0)
        #update label of p color

    def set_secondary_pixel(self) -> None:
        self.colors.secondary_pixel(self.mouse_pos)
        self.colors.secondary = (0,0,0)
        #update label of s color

    def set_primary_color(self, x: int , y: int) -> None:
        y = self.ref_mouse().y

        #access the pixel colors 
        pixel = self.reference_image.getpixel((x, y))
        self.colors.set_primary(pixel[0], pixel[1], pixel[2])

    def set_secondary_color(self, x: int, y: int) -> None:
        y = self.ref_mouse().y

        #access the pixel colors 
        pixel = self.reference_image.getpixel((x, y))
        self.colors.set_secondary(pixel[0], pixel[1], pixel[2])

    def update(self, dt) -> None:
        self.window.clear()
        self.spritesheet.update()
        self.outline.update()
        self.colors.update()
        self.labels.update(self.outline.a, self.outline.b, self.colors.primary, self.colors.secondary)
#         print(self.mouse_pos)

    def reset(self) -> None:
        self.outline.reset()
        self.labels.reset()
        self.colors.reset()




@window.event
def on_mouse_motion(x, y, dx, dy):
    loop.set_mouse_pos(x, y)
    loop._debug_coord()


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    """Draw the outline as the mouse is dragged."""
    loop.outline.end(x, y)

@window.event
def on_mouse_press(x, y, button, modifiers):
    """Set the starting point."""
    loop.outline.start(x, y)
    loop.outline.end(x, y)

@window.event
def on_mouse_release(x, y, button, modifiers):
    if loop.colors.primary is not None and loop.colors.secondary is not None:
        loop.outline.end(x, y)

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

    elif symbol == key._1:
        loop.set_primary_pixel()

    elif symbol == key._2:
        loop.set_secondary_pixel()

    elif symbol == key.R:
        loop.reset()

    #save image
    elif symbol == key.S:   
        pointA = loop.outline.a
        pointB = loop.outline.b
        label_offset = loop.labels.box_height
        image_height = loop.reference_image.height
        image_width = loop.reference_image.width
        scale = loop.spritesheet.sprite_sheet.scale
#         translation_x = loop.spritesheet.sprite_sheet.x
#         translation_y = loop.spritesheet.sprite_sheet.y
        image_x = loop.spritesheet.sprite_sheet.x
        image_y = loop.spritesheet.sprite_sheet.y

#         print("translation x, y:", translation_x, translation_y)

        #PIL inverts y-axis
        #account for scaling
        left = min(pointA.x, pointB.x) // scale
        right = max(pointA.x, pointB.x) // scale
        top = (min(pointA.y, pointB.y) - label_offset) // scale 
        bottom = (max(pointA.y, pointB.y) - label_offset) // scale 

        #TODO
        #account for image translation
#         image_x_offset = int(image_width * scale)
#         image_y_offset = int(image_height * scale)
#         print("after scale and translation:", image_x_offset, image_y_offset)

        bottom_line = loop.reference_image.height - bottom
        top_line = loop.reference_image.height - top
        preview_image = loop.reference_image.crop((left, bottom_line, right, top_line))
        preview_image.show()
        file_name = input("Give the image a name (no extension) or x to cancel: ").strip()
        if file_name != "x":
            preview_image.save(f"slices/{file_name}.png")


if __name__ == "__main__":
    frame_speed = 1/60
    keyboard = key.KeyStateHandler()
    window.push_handlers(keyboard)
#     image = pyglet.image.load(sys.argv[1])
    loop = App(window)

    #TODO
#     reference_image = Image.open(sys.argv[1])

    pyglet.clock.schedule_interval(loop.update, frame_speed)
    pyglet.app.run()
