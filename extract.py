"""Let user decide which sprites to include in a spritesheet and automatically remove the background color.

    Make sure the image is in PNG format.

    - scale and translate the image where you want it.

    Controls:
        arrows: up down left right
        1: set the primary reference color.
        2: set the secondary reference color.
        e: preview single, cleaned slice.
        s: save single, uncleaned slice.
        v: extract the secondary color and put in final sprite list.
        w: save the extracted sprites to their own sheet.
        r: reset everything.
        esc/q: quit.


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
from constants import Color, Point, Pixel
from control_panel import ControlPanel
from workspace import Workspace

#Make a window
window = pyglet.window.Window(1000, 800)

#set mouse cursor to crosshairs
cursor = window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
window.set_mouse_cursor(cursor)


class App():
    def __init__(self, window, img):
        self.window = window
        self.control_panel = ControlPanel(self.window)
        self.workspace = Workspace(img)
        self.mouse_pos = Point(0, 0)
        self.sprite_outline_b = Point(0, 0)

    def add_slice(self, image: Image) -> None:
        """Add rough image slice to the image list."""
        self.control_panel.add_image(image)

    def add_final_subsprite(self, image:Image) -> None:
        """Add extracted sprite to final collection."""
        self.control_panel.add_final_subsprite(image)

    def change_mouse_pos(self, x: int, y: int) -> None:
        """Change the current mouse position."""
        self.mouse_pos = (x, y)

    def change_outline_end(self) -> None:
        """Change the outline's ending point."""
        self.workspace.change_outline_end(self.sheet_mouse_pos())

    def change_outline_start(self) -> None:
        """Change the outline's starting point."""
        self.workspace.change_outline_start(self.sheet_mouse_pos())

    def crop_subsprite(self, img, mask) -> Image:
        box = self.workspace.crop_subsprite(mask)
        return img.crop(box)

    def first_preview_image(self) -> Image:
        """Return the first preview image."""
        return self.control_panel.preview_image(0)

    def get_pixel(self) -> Pixel:
        """Get single pixel's information."""
        return self.workspace.pixel(self.sheet_mouse_pos())

    def is_secondary_white(self) -> bool:
        return self.control_panel.is_secondary_white()

    def last_preview_image(self) -> Image:
        """Return the last preview image."""
        return self.control_panel.preview_image(-1)

    def p_color(self) -> Color:
        """Return the primary color choice."""
        return self.control_panel.get_primary_color()

    def pan_down(self) -> None:
        """Pan down on the workspace."""
        self.workspace.pan_down()

    def pan_left(self) -> None:
        """Pan left on the workspace."""
        self.workspace.pan_left()

    def pan_right(self) -> None:
        """Pan right on the workspace."""
        self.workspace.pan_right()

    def pan_up(self) -> None:
        """Pan up on the workspace."""
        self.workspace.pan_up()

    def ref_img_coords(self) -> Tuple[Point, Point]:
        """Return outline's A and B coordinates."""
        return self.workspace.ref_img_coords()

    def remove_secondary_color(self, sprite: Image) -> Image:
        """Set the secondary color's alpha to 0."""
        color = self.s_color()
        #KUDOS
        #https://stackoverflow.com/questions/28754852/how-to-set-alpha-value-of-a-pixel-in-python/28758075
        pixeldata = list(sprite.getdata())
        for i, pixel in enumerate(pixeldata):
            if pixel[:3] == color:
                pixeldata[i] = (255,255,255,0)
        sprite.putdata(pixeldata)
        return sprite

    def s_color(self) -> Color:
        """Return the secondary color choice."""
        return self.control_panel.get_secondary_color()

    def sheet_scale(self) -> int:
        """Return sprite sheet scale size."""
        return self.workspace.sheet_scale()

    def slice(self) -> Image:
        """Return a slice of the spritesheet."""
        #TODO, separate the reference outline and the sheet outline
        coords = self.ref_img_coords()
        return self.workspace.slice(coords)

    def sliced_image(self) -> Image:
        """Returns the recently sliced image."""
        return self.control_panel.sliced_image()

    def sheet_coords(self) -> Tuple[int, int]:
        """Get sprite sheet's origin coordinates."""
        return self.workspace.sheet_coords()

    def sheet_mouse_pos(self) -> Point:
        """Get the mouse position relative to the sprite sheet."""
        x, y = self.sheet_coords()
        pos = self.mouse_pos
        return Point(int(pos[0] - x), int(pos[1] - y))

    def show_all_final_subsprites(self) -> None:
        self.control_panel.show_all_final_subsprites()

    def ref_mouse_pos(self) -> Point:
        """Get mouse position relative to the reference image."""
        x, y = self.sheet_coords()
        scale = self.sheet_scale()
        pos = self.mouse_pos
        return Point(int((pos[0] - x) // scale), int((pos[1] - y) // scale))

    def set_primary(self) -> None:
        """Set the primary color."""
        coord, color = self.get_pixel()
        self.control_panel.primary_color(coord, color)

    def set_secondary(self) -> None:
        """Set the secondary color."""
        coord, color = self.get_pixel()
        self.control_panel.secondary_color(coord, color)

    def zoom_in(self) -> None:
        """Zoom in on the workspace."""
        self.workspace.zoom_in()

    def zoom_out(self) -> None:
        """Zoom out on the workspace."""
        self.workspace.zoom_out()

    def reset(self) -> None:
        self.control_panel.reset()
        self.workspace.reset()

    def update(self, dt) -> None:
        self.window.clear()
        self.workspace.update()
        self.control_panel.update()

@window.event
def on_mouse_motion(x, y, dx, dy):
    """Save the mouse position."""
    app.change_mouse_pos(x, y)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    """Draw the outline as the mouse is dragged."""
    app.change_mouse_pos(x, y)
    app.change_outline_end()
    app.workspace.outline.update()

@window.event
def on_mouse_press(x, y, button, modifiers):
    """Set the starting point."""
    app.change_mouse_pos(x, y)
    app.change_outline_start()

@window.event
def on_mouse_release(x, y, button, modifiers):
    """When you release the mouse button..."""
    app.change_mouse_pos(x, y)
    app.change_outline_end()

@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.ESCAPE or symbol == key.Q:
        quit()

    #transformations
    elif symbol == key.U:
        app.zoom_in()
    elif symbol == key.D:
        app.zoom_out()
    elif symbol == key.UP:
        app.pan_up()
    elif symbol == key.DOWN:
        app.pan_down()
    elif symbol == key.LEFT:
        app.pan_left()
    elif symbol == key.RIGHT:
        app.pan_right()

    #set colors     
    elif symbol == key._1:
        app.set_primary()
    elif symbol == key._2:
        app.set_secondary()

    #reset values
    elif symbol == key.R:
        app.reset()

    #save image
    elif symbol == key.S:   
        preview_image = app.slice()
        date = datetime.datetime.utcnow()
        preview_image.save(f"slices/{date}.png")

    #add to preview collection
    elif symbol == key.E:
        #combine/refactor
        app.add_slice(app.slice())

    elif symbol == key.V:
        image = app.sliced_image()
        if image:

            #create mask for p_color        
            mask = []
            for row in range(image.height):
                mask.append([])
                for column in range(image.width):
                    mask[row].append([])
                    mask[row][column] = (image.getpixel((column, row)) != app.p_color())

            #crop the subsprite out of the main sheet
            cropped_subsprite = app.crop_subsprite(image, mask)
            alpha_subsprite = cropped_subsprite.convert("RGBA")

            #remove secondary color if it's not white
            if not app.is_secondary_white():
                extracted_sprite = app.remove_secondary_color(alpha_subsprite)

                #add 1px clear border
                dimensions = (extracted_sprite.width + 2, extracted_sprite.height + 2)
                color = (0,0,0,0) #transparent
                final_image = Image.new("RGBA", dimensions, color)
                final_image.paste(extracted_sprite, (1, 1))
#                 final_image.show()
#                 app.add_final_subsprite(extracted_sprite)
                app.add_final_subsprite(final_image)

    elif symbol == key.W:
        #these images already have the 1px border around them
        all_images = app.control_panel.preview.preview

        if not all_images:
            print("There are no images to save.")
        else:
            #check heights
            maxheight = max([image.height for image in all_images])
            minheight = min([image.height for image in all_images])
            if maxheight != minheight:
                for image in enumerate(all_images):
                    print(image[0], image[1].height)
                raise Exception("The heights are not the same.")

            #check widths
            maxwidth = max([image.width for image in all_images])
            minwidth = min([image.width for image in all_images])
            if maxwidth != minwidth:
                for image in enumerate(all_images):
                    print(image[0], image[1].width)
                raise Exception("The widths are not the same.")

            #paste into new blank image
            height = maxheight
            width = len(all_images * maxwidth)
            color = (0,0,0,0) #transparent
            final_image = Image.new("RGBA", (width, height), color)
            for image in enumerate(all_images):
                final_image.paste(image[1], (image[0]*image[1].width, 0))
            final_image.show()
            date = datetime.datetime.utcnow()
            final_image.save(f"sprite_sheets/{date}.png")


if __name__ == "__main__":
    frame_speed = 1/60
    keyboard = key.KeyStateHandler()
    window.push_handlers(keyboard)
    img = sys.argv[1]
    app = App(window, img)
    pyglet.clock.schedule_interval(app.update, frame_speed)
    pyglet.app.run()
