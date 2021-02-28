#std lib
from time import sleep
from pathlib import Path

#3rd party
from PIL import Image
import pyglet

#custom
from constants import Color, Point


#setup image directory
# root = "." 
# tempdir = "./temp"
# pyglet.resource.path = [root, tempdir]
# pyglet.resource.reindex()

class Details():
    def __init__(self, window, box_width):
        self.batch = pyglet.graphics.Batch()
        self.label_color = (0, 0, 0, 255) #Black
        self.label_x_offset = 10

        #primary color
        self.p_color = (255, 255, 255)
        self.p_label = "Pri:"
        self._p_color_box = {"x": 980, "y": 775, "w": 20, "h": 20}
        self.p_pos = None

        self.primary = pyglet.text.Label(
            self.p_label,
            color=self.label_color,
            x=window.width - box_width + self.label_x_offset,
            y=780,
            batch=self.batch)

        self.p_color_box = pyglet.shapes.Rectangle(
            self._p_color_box["x"],
            self._p_color_box["y"],
            self._p_color_box["w"],
            self._p_color_box["h"],
            color=self.p_color,
            batch=self.batch)

        #secondary color
        self.s_color = (255, 255, 255)
        self.s_label = "Sec:"
        self._s_color_box = {"x": 980, "y": 755, "w": 20, "h": 20}
        self.s_pos = None

        self.secondary = pyglet.text.Label(
            self.s_label,
            color=self.label_color,
            x=window.width - box_width + self.label_x_offset,
            y=760,
            batch=self.batch)

        self.s_color_box = pyglet.shapes.Rectangle(
            self._s_color_box["x"],
            self._s_color_box["y"],
            self._s_color_box["w"],
            self._s_color_box["h"],
            color=self.s_color,
            batch=self.batch)

    def is_secondary_white(self) -> bool:
        """Checks if secondary color is white."""
        return self.s_color == (255, 255, 255)

    def set_p(self, coord: Point, rgb: Color) -> None:
        """Set the primary color."""
        self.p_color = (rgb[0], rgb[1], rgb[2])
        self.p_color_box.color = self.p_color
        self.p_pos = coord

    def set_s(self, coord: Point, rgb: Color) -> None:
        """Set the secondary color."""
        self.s_color = (rgb[0], rgb[1], rgb[2])
        self.s_color_box.color = self.s_color
        self.s_pos = coord

    def set_p_label(self, color) -> None:
        """Change the primary color label's text."""
        self.primary.text = f"{self.p_label} {color}"

    def set_s_label(self, color) -> None:
        """Change the secondary color label's text."""
        self.secondary.text = f"{self.s_label} {color}"

    def reset(self) -> None:
        self.p_pos = None
        self.s_pos = None
        self.p_color = (255, 255, 255)
        self.s_color = (255, 255, 255)
        self.primary.text = "Pri:"
        self.secondary.text = "Sec:"
        self.update()

    def update(self) -> None:
        self.p_color_box.color = self.p_color
        self.s_color_box.color = self.s_color
        self.batch.draw()


class Controls():
    def __init__(self, window, box_width):
        self.start_label = "Start:"
        self.end_label = "End:"

        #labels
        self.label_y_offset = 10
        self.label_x_offset = 10
        self.batch = pyglet.graphics.Batch()
        self.label_color = (0, 0, 0, 255) #Black
        self.labels_top = 220
        self.vertical_spacing = 20

        self._arrows = pyglet.text.Label(
            "Arrows: UDLR",
            color=self.label_color,
            x=window.width - box_width + self.label_x_offset,
            y=0,
            batch=self.batch)

        self._one = pyglet.text.Label(
            "1:   set primary color",
            color=self.label_color,
            x=window.width - box_width + self.label_x_offset,
            y=0,
            batch=self.batch)

        self._two = pyglet.text.Label(
            "2:   set secondary color",
            color=self.label_color,
            x=window.width - box_width + self.label_x_offset,
            batch=self.batch)

        self._extract = pyglet.text.Label(
            "e:   extract",
            color=self.label_color,
            x=window.width - box_width + self.label_x_offset,
            y=0,
            batch=self.batch)

        self._save = pyglet.text.Label(
            "s:   save (uncleaned)",
            color=self.label_color,
            x=window.width - box_width + self.label_x_offset,
            y=0,
            batch=self.batch)

        self._view = pyglet.text.Label(
            "v:   view",
            color=self.label_color,
            x=window.width - box_width + self.label_x_offset,
            y=0,
            batch=self.batch)

        self._save_to_sheet = pyglet.text.Label(
            "w:  save to sheet",
            color=self.label_color,
            x=window.width - box_width + self.label_x_offset,
            y=0,
            batch=self.batch)

        self._scaleup = pyglet.text.Label(
            "u:   scale up",
            color=self.label_color,
            x=window.width - box_width + self.label_x_offset,
            y=0,
            batch=self.batch)

        self._scaledown = pyglet.text.Label(
            "d:   scale down",
            color=self.label_color,
            x=window.width - box_width + self.label_x_offset,
            y=0,
            batch=self.batch)

        self._reset = pyglet.text.Label(
            "r:    reset",
            color=self.label_color,
            x=window.width - box_width + self.label_x_offset,
            y=0,
            batch=self.batch)

        self._escape = pyglet.text.Label(
            "esc/q:   Quit",
            color=self.label_color,
            x=window.width - box_width + self.label_x_offset,
            y=0,
            batch=self.batch)

        self._label_list = [
            self._arrows,
            self._one,
            self._two,
            self._extract,
            self._save,
            self._view,
            self._scaledown,
            self._scaleup,
            self._reset,
            self._save_to_sheet,
            self._escape]

        for index, label in enumerate(self._label_list):
            label.y = self.labels_top - index * self.vertical_spacing

    def update(self) -> None:
        self.batch.draw()

class Preview():
    def __init__(self, window, box_width):
        self.window = window
        self.box_width = box_width
        self.batch = pyglet.graphics.Batch()
        self.box_height = 200
        self.box_y = 550
        self.box_color = (100, 100, 100) #purple
        self.box = pyglet.shapes.Rectangle(
            self.window.width - self.box_width,
            self.box_y,
            self.box_width,
            self.box_height,
            color=self.box_color,
            batch=self.batch)
        self.images = []
        self.preview = []
        self.sprites = []

    def add(self, image: Image) -> None:
        """Add image to list."""
        self.images.append(image)

    def add_final_subsprite(self, image:Image) -> None:
        """Add image to preview list."""
        self.preview.append(image)
        self.sprites.append(self._new_sprite(image))

    def get(self, index: int) -> Image:
        """Return image from list at index."""
        return self.images[index]

    def get_image(self) -> Image:
        """Returns recently sliced image."""
        return self.images.pop()

    def _new_sprite(self, image) -> pyglet.sprite.Sprite:
        #save the image in temp dir
#         temp = "./temp/image.png"
        temp = "./tempimage.png"
        image.save(temp)

        #wait for the OS to save the image?
        while not Path(temp).exists():
            sleep(0.25)
        #reload the image in pyglet's format
        img = pyglet.image.load(temp)
        sprite = pyglet.sprite.Sprite(
            img,
            x=self.window.width - self.box_width,
            y=self.box_y)
        sprite.scale = 5
        return sprite

    def show_all_final_subsprites(self) -> None:
        for sprite in self.preview:
            sprite.show()

    def reset(self) -> None:
        self.image = []
        self.preview = []
        self.sprites = []

    def update(self) -> None:
        self.batch.draw()
        
        #draw the most recent sprite
        if self.sprites:
            self.sprites[-1].draw()

class ControlPanel():
    def __init__(self, window):
        self.window = window
        self.box_height = window.height
        self.box_width = 200

        #Components
        self.controls = Controls(self.window, self.box_width)
        self.preview = Preview(self.window, self.box_width)
        self.details = Details(self.window, self.box_width)

        #Background
        self.box_color = (255, 255, 255) #White
        self.background = pyglet.graphics.Batch()
        self.rectangle = pyglet.shapes.Rectangle(
            window.width - self.box_width,
            0,
            self.box_width,
            self.box_height,
            color=self.box_color,
            batch=self.background)

    def add_image(self, image: Image) -> None:
        """Add image to image list."""
        self.preview.add(image)

    def add_final_subsprite(self, image:Image) -> None:
        """Add extracted sprite to final collection."""
        self.preview.add_final_subsprite(image)

    def get_primary_color(self) -> Color:
        """Return the primary color choice."""
        return self.details.p_color

    def get_secondary_color(self) -> Color:
        """Return the secondary color choice."""
        return self.details.s_color

    def is_secondary_white(self) -> bool:
        """Returns True is secondary color is white."""
        return self.details.is_secondary_white()

    def preview_image(self, index: int) -> Image:
        """Get preview image at index."""
        return self.preview.get(index)

    def primary_color(self, coord, color) -> None:
        """Set the primary color."""
        self.details.set_p_label(color)
        self.details.set_p(coord, color)

    def secondary_color(self, coord, color) -> None:
        """Set the secondary color."""
        self.details.set_s_label(color)
        self.details.set_s(coord, color)
    
    def sliced_image(self) -> Image:
        """Returns the recently sliced image."""
        return self.preview.get_image()

    def show_all_final_subsprites(self) -> None:
        self.preview.show_all_final_subsprites()

    def update(self) -> None:
        self.background.draw()
        self.controls.update()
        self.details.update()
        self.preview.update()

    def reset(self) -> None:
        self.details.reset()
        self.preview.reset()
