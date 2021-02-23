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
from pprint import pprint
import sys
from typing import Any, List, Tuple

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
        self.preview = []
        self.final_preview = [] 

    def add_slice(self, image: Image) -> None:
        self.preview.append(image)

    def remove_secondary_color(self, sprite: Image) -> Image:
        """Set the secondary color's alpha to 0."""
        color = self.colors.s_color
        pixeldata = list(sprite.getdata())
        for i, pixel in enumerate(pixeldata):
            if pixel[:3] == color:
                pixeldata[i] = (255,255,255,0)
        sprite.putdata(pixeldata)
        return sprite

    def slice(self) -> Image:
        #get sprite sheet origin
        scale = loop.spritesheet.sprite_sheet.scale

        #get sprite sheet ouline coords, translation adjusted
        sprite_a = loop.sprite_outline_a
        sprite_b = loop.sprite_outline_b

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

        #slice image and return
        return loop.reference_image.crop((left, bottom, right, top))

        

    def pixel(self) -> list:
        """Get coordinate and RGB data."""
        sheet = self.spritesheet.sprite_sheet
        pos = self.sprite_mouse_pos()
        coord = Point(pos.x // sheet.scale, pos.y // sheet.scale)
        x = int(coord[0])
        y = int(self.image.height - coord[1])
        try:
            rgb = self.reference_image.getpixel((x, y))
        except IndexError:
            rgb = (0, 0, 0)
        return coord, rgb

    def sprite_mouse_pos(self) -> Point:
        """Get the mouse position relative to the sprite sheet."""
        x = int(self.mouse_pos[0] - self.spritesheet.sprite_sheet.x)
        y = int(self.mouse_pos[1] - self.spritesheet.sprite_sheet.y)
        return Point(x, y)

    def sprite_outline_point_a(self) -> None:
        a = self.sprite_mouse_pos()
        self.sprite_outline_a = a

    def sprite_outline_point_b(self) -> None:
        b = self.sprite_mouse_pos()
        self.sprite_outline_b = b

    def ref_mouse_pos(self) -> Point:
        sheet = self.spritesheet.sprite_sheet
        x = int((self.mouse_pos[0] - sheet.x) // sheet.scale)
        y = int((self.mouse_pos[1] - sheet.y) // sheet.scale)
        return Point(x, y)

    def set_window_mouse_pos(self, x: int, y: int) -> None:
        self.mouse_pos = (x, y)

    def set_primary(self) -> None:
        coord, color = self.pixel()
        self.colors.set_p(coord, color)
        self.labels.set_p_label(color)

    def set_secondary(self) -> None:
        coord, color = self.pixel()
        self.colors.set_s(coord, color)
        self.labels.set_s_label(color)

    def crop_subsprite(self, mask) -> Image:
        top = loop._top_row(mask)
        bottom = loop._bottom_row(mask)
        left = loop._left_column(mask)
        right = loop._right_column(mask)
        return self.preview[0].crop((left, top, right, bottom))
        
    def _top_row(self, mask: List[List[bool]]) -> int:
        """Find top row index of sprite box."""
        for row in enumerate(mask):
            if any(row[1]):
                return row[0]

    def _bottom_row(self, mask: List[List[bool]]) -> int:
        """Find bottom row index of sprite box."""
        mask.reverse()
        for row in enumerate(mask):
            if any(row[1]):
                return len(mask) - row[0] - 1

    def _left_column(self, mask: List[List[bool]]) -> int:
        """Find left column index of sprite box."""
        row = self._top_row(mask)
        for pixel in mask[row]:
            if pixel == True:
                return mask[row].index(pixel)

    def _right_column(self, mask: List[List[bool]]) -> int:
        """Find right column index of sprite box."""
        row_index = self._top_row(mask)
        row = mask[row_index]
        row.reverse()
        for pixel in row:
            if pixel == True:
                return len(row) - row.index(pixel) - 1

    def update(self, dt) -> None:
        self.window.clear()
        self.spritesheet.update()
        self.outline.update()
        self.colors.update()
        self.labels.update(self.outline.a, self.outline.b)

    def reset(self) -> None:
        self.outline.reset()
        self.labels.reset()
        self.colors.reset()
        self.preview = []




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

    #save image
    elif symbol == key.S:   
        preview_image = loop.slice()
        preview_image.show()
        date = datetime.datetime.utcnow()
        preview_image.save(f"slices/{date}.png")
#         print(f"Saved as: {date}")

    #add to preview collection
    elif symbol == key.P:
        preview_image = loop.slice()
        loop.add_slice(preview_image)
#         print("preview:", loop.preview)
        print("Added to preview:", preview_image)

    elif symbol == key.V:
        if loop.preview:
            image = loop.preview[0]
#             image.show()

            #create mask for p_color        
            mask = []
            for row in range(image.height):
                mask.append([])
                for column in range(image.width):
                    mask[row].append([])
                    mask[row][column] = (image.getpixel((column, row)) != loop.colors.p_color)

            #crop the subsprite out of the main sheet
            subsprite = loop.crop_subsprite(mask)
            alpha_subsprite = subsprite.convert("RGBA")

            #remove secondary color if it's not white
            if not loop.colors.secondary_is_white():
                final_sprite = loop.remove_secondary_color(alpha_subsprite)
                final_sprite.show()
                










#         #Rows
#         #find the first row where a color is not the primary color
#         x_indices = []
#         x_longest_runs = []
#         for row in range(image.height):
#             x_start = 0
#             x_end = 0
#             for column in range(image.width):
#                 if image.getpixel((column, row)) != loop.colors.p_color:
#                     print(f"not p color: [{row}, {column}]")
#                     x_start = column
#                 else:
#                     print(f"is p color: [{row}, {column}]")
 
 


if __name__ == "__main__":
    frame_speed = 1/60
    keyboard = key.KeyStateHandler()
    window.push_handlers(keyboard)
    loop = App(window)
    pyglet.clock.schedule_interval(loop.update, frame_speed)
    pyglet.app.run()
