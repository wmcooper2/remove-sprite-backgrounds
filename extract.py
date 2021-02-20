"""Let user decide which sprites to include in a spritesheet and automatically remove the background color.

    Make sure the image is in PNG format.

    1. scale and translate the image where you want it.
    2. press "p" to set the primary reference color.
    3. press "s" to set the secondary reference color.
    4. press "r" to reset everything.

"""

#std lib
from collections import namedtuple
import datetime
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
        self.sprite_outline_a = Point(0, 0)
        self.sprite_outline_b = Point(0, 0)

    def pixel(self) -> list:
        """Get coordinate and RGB data."""
        sprite = self.sprite_mouse_pos()
        coord = Point(sprite.x // self.spritesheet.sprite_sheet.scale,
                      sprite.y // self.spritesheet.sprite_sheet.scale)
        x = int(coord[0])
        y = int(self.image.height - coord[1])
        try:
            rgb = self.reference_image.getpixel((x, y))
        except IndexError:
            rgb = (0, 0, 0)
#         print(f"Scaled: {coord}, RGB: {rgb}")
        return coord, rgb

    def sprite_mouse_pos(self) -> Point:
        """Get the mouse position relative to the sprite sheet."""
        x = int(self.mouse_pos[0] - self.spritesheet.sprite_sheet.x)
        y = int(self.mouse_pos[1] - self.spritesheet.sprite_sheet.y)
        return Point(x, y)

    def sprite_outline_point_a(self) -> None:
        a = self.sprite_mouse_pos()
        self.sprite_outline_a = a
#         print(a)

    def sprite_outline_point_b(self) -> None:
        b = self.sprite_mouse_pos()
        self.sprite_outline_b = b
#         print(b)

    def ref_mouse_pos(self) -> Point:
        x = int((
                self.mouse_pos[0] - self.spritesheet.sprite_sheet.x)
                // self.spritesheet.sprite_sheet.scale)
        y = int((
                self.mouse_pos[1] - self.spritesheet.sprite_sheet.y)
                // self.spritesheet.sprite_sheet.scale)
        return Point(x, y)

    def set_window_mouse_pos(self, x: int, y: int) -> None:
        self.mouse_pos = (x, y)

    def set_primary(self) -> None:
        coord, color = self.pixel()
        self.colors.set_p(coord, color)
        #update label of p color

    def set_secondary(self) -> None:
        coord, color = self.pixel()
        self.colors.set_s(coord, color)
        #update label of s color

    def update(self, dt) -> None:
        self.window.clear()
        self.spritesheet.update()
        self.outline.update()
        self.labels.update(self.outline.a, self.outline.b)
        self.colors.update()

    def reset(self) -> None:
        self.outline.reset()
        self.labels.reset()
        self.colors.reset()




@window.event
def on_mouse_motion(x, y, dx, dy):
    """Whenever the mouse is moved..."""
    loop.set_window_mouse_pos(x, y)
    loop.pixel()

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    """Draw the outline as the mouse is dragged."""
    loop.outline.end(x, y)

@window.event
def on_mouse_press(x, y, button, modifiers):
    """Set the starting point."""
    loop.set_window_mouse_pos(x, y)
    loop.sprite_outline_point_a()
    loop.outline.start(x, y)
    loop.outline.end(x, y)

@window.event
def on_mouse_release(x, y, button, modifiers):
    """When you release the mouse button..."""
    loop.set_window_mouse_pos(x, y)
    loop.sprite_outline_point_b()
    loop.outline.end(x, y)

@window.event
def on_key_press(symbol, modifiers):
    
    #transformations
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

    #set colors     
    elif symbol == key._1:
        loop.set_primary()
    elif symbol == key._2:
        loop.set_secondary()

    #reset values
    elif symbol == key.R:
        loop.reset()

    #TODO
    #save image
    elif symbol == key.S:   
        a = loop.outline.a
        b = loop.outline.b
        label_offset = loop.labels.box_height
#         print("a, b:", a, b)

        ref_h = loop.reference_image.height
        ref_w = loop.reference_image.width
#         print("ref h,w: ", ref_h, ref_w)

        #get sprite sheet origin
        scale = loop.spritesheet.sprite_sheet.scale
        sprite_x = loop.spritesheet.sprite_sheet.x
        sprite_y = loop.spritesheet.sprite_sheet.y
#         print("scale sprite_x,y", scale, sprite_x, sprite_y)

        #get sprite sheet ouline coords, translation adjusted
        sprite_a = loop.sprite_outline_a
        sprite_b = loop.sprite_outline_b
#         print("Pyglet sprite [a, b]:", sprite_a, sprite_b)

        #set outline boundaries
        left = min(sprite_a.x, sprite_b.x)
        right = max(sprite_a.x, sprite_b.x)
        top = min(sprite_a.y, sprite_b.y)
        bottom = max(sprite_a.y, sprite_b.y)

        #adjust for scaling
        left /= scale
        right /= scale
        top /= scale
        bottom /= scale

        #invert the y-axis for PIL's coordinate system
        top = loop.reference_image.height - top
        bottom = loop.reference_image.height - bottom
        print(f"PIL lbrt: {left} {bottom} {right} {top}")

        #show preview and save
        preview_image = loop.reference_image.crop((left, bottom, right, top))
        preview_image.show()
#         date = datetime.datetime.utcnow()
#         preview_image.save(f"slices/{date}.png")
#         print(f"Saved as: {date}")


if __name__ == "__main__":
    frame_speed = 1/60
    keyboard = key.KeyStateHandler()
    window.push_handlers(keyboard)
    loop = App(window)
    pyglet.clock.schedule_interval(loop.update, frame_speed)
    pyglet.app.run()
