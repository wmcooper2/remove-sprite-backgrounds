#std lib
import sys
from typing import List, Tuple

#3rd party
from PIL import Image
import pyglet

#custom
from constants import Box, Point, Pixel


class Outline():
    def __init__(self):
        self.primary_ref = 0
        self.secondary_ref = 0
        self.color = (255, 0, 0)
        self.line_width = 3

        #reference image
        self.a = Point(0, 0)
        self.b = Point(0, 0)
        self.width = 0
        self.height = 0

        #workspace spritesheet
        self.sheet_a = Point(0, 0)
        self.sheet_b = Point(0, 0)
        self.sheet_w = 0
        self.sheet_h = 0
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

    def __str__(self) -> None:
        return str(f"ref: A={self.a} B={self.b} w={self.width} h={self.height}, sheet: A={self.sheet_a} B={self.sheet_b} w={self.sheet_w} h={self.sheet_h}")

    def _dimensions(self) -> None:
        """Set the outline's width and height."""
        #reference image
        self.width = abs(self.a.x - self.b.x)
        self.height = abs(self.a.y - self.b.y)

        #workspace spritesheet
        self.sheet_w = abs(self.sheet_a.x - self.sheet_b.x)
        self.sheet_h = abs(self.sheet_a.y - self.sheet_b.y)

    def _box_coords(self) -> None:
        """Set the outline's perimeter"""
        #workspace spritesheet
        self.top_line.position = (
            self.sheet_a.x,
            self.sheet_a.y,
            self.sheet_b.x,
            self.sheet_a.y)

        self.bottom_line.position = (
            self.sheet_a.x,
            self.sheet_b.y,
            self.sheet_b.x,
            self.sheet_b.y)

        self.left_line.position = (
            self.sheet_a.x,
            self.sheet_a.y,
            self.sheet_a.x,
            self.sheet_b.y)

        self.right_line.position = (
            self.sheet_b.x,
            self.sheet_a.y,
            self.sheet_b.x,
            self.sheet_b.y)

    def _start(self, coord: Point)-> None:
        """Set the outline's starting point."""
        self.a = coord

    def _end(self, coord: Point) -> None:
        """Set the outline's ending point."""
        self.b = coord

    def _sheet_start(self, coord: Point)-> None:
        """Set the sheet's outline's starting point."""
        self.sheet_a = coord

    def _sheet_end(self, coord: Point) -> None:
        """Set the reference outline's ending point."""
        self.sheet_b = coord

    def _ref_coords(self) -> Tuple[Point, Point]:
        """Return coordinates for outline on actual reference image in memory."""
        return (self.a, self.b)

    def _outline_coords(self) -> Tuple[Point, Point]:
        """Return coordinates for outline drawn on screen."""
        return (self.sheet_a, self.sheet_b)

    def _move_down(self, amount: int) -> None:
        """Move the outline on the workspace spritesheet to the down by amount."""
        #current outline coords
        a, b = self._outline_coords()

        #adjust for the translation amount
        new_a = Point(a.x, a.y - amount)
        new_b = Point(b.x, b.y - amount)

        #change the outline's boundaries
        self._sheet_start(new_a)
        self._sheet_end(new_b)

    def _move_left(self, amount: int) -> None:
        """Move the outline on the workspace spritesheet to the left by amount."""
        #current outline coords
        a, b = self._outline_coords()

        #adjust for the translation amount
        new_a = Point(a.x - amount, a.y)
        new_b = Point(b.x - amount, b.y)

        #change the outline's boundaries
        self._sheet_start(new_a)
        self._sheet_end(new_b)

    def _move_right(self, amount: int) -> None:
        """Move the outline on the workspace spritesheet to the right by amount."""
        #current outline coords
        a, b = self._outline_coords()

        #adjust for the translation amount
        new_a = Point(a.x + amount, a.y)
        new_b = Point(b.x + amount, b.y)

        #change the outline's boundaries
        self._sheet_start(new_a)
        self._sheet_end(new_b)

    def _move_up(self, amount: int) -> None:
        """Move the outline on the workspace spritesheet to the up by amount."""
        #current outline coords
        a, b = self._outline_coords()

        #adjust for the translation amount
        new_a = Point(a.x, a.y + amount)
        new_b = Point(b.x, b.y + amount)

        #change the outline's boundaries
        self._sheet_start(new_a)
        self._sheet_end(new_b)

    def reset(self) -> None:
        self.a = Point(0, 0)
        self.b = Point(0, 0)
        self.sheet_a = Point(0, 0)
        self.sheet_b = Point(0, 0)

    def update(self) -> None:
        self._dimensions()
        self._box_coords()
        self.batch.draw()


class SpriteSheet():
    def __init__(self, img):
        self.image = pyglet.image.load(img) #for ease of coordinate system use, redundant?
        self.reference_image = Image.open(img)
        self.sheet = pyglet.resource.image(img)
        self.seq = pyglet.image.ImageGrid(self.sheet, 1, 1)
        self.anim = pyglet.image.Animation.from_image_sequence(self.seq, 0.2, True)
        self.batch = pyglet.graphics.Batch()
        self.sprite_sheet = pyglet.sprite.Sprite(self.anim, batch=self.batch)
        self.translation_speed = 100

    def _coords(self) -> Tuple[int, int]:
        """Return sprite sheet's origin coordinates."""
        return (self.sprite_sheet.x, self.sprite_sheet.y)

    def _crop_boundaries(self, mask) -> Box:
        """Return the boundaries for the crop box."""
        top = self._top_row(mask)
        bottom = self._bottom_row(mask)
        left = self._left_column(mask)
        right = self._right_column(mask)
        return Box(left, top, right, bottom)

    def _move_up(self) -> None:
        """Translate the sprite sheet up."""
        self.sprite_sheet.y +=  self.translation_speed

    def _move_down(self) -> None:
        """Translate the sprite sheet down."""
        self.sprite_sheet.y -= self.translation_speed

    def _move_left(self) -> None:
        """Translate the sprite sheet left."""
        self.sprite_sheet.x -= self.translation_speed

    def _move_right(self) -> None:
        """Translate the sprite sheet right."""
        self.sprite_sheet.x += self.translation_speed

    def _pixel(self, pos: Point) -> Pixel:
        """Get pixel's coordinate and RGB data."""
        scale = self._scale()
        coord = Point(pos.x // scale, pos.y // scale)
        x = int(coord[0])
        y = int(self.image.height - coord[1])
        try:
            rgb = self.reference_image.getpixel((x, y))
        except IndexError:
            rgb = (0, 0, 0)
        return coord, rgb

    def _scale(self) -> int:
        """Return sprite sheet scale."""
        return self.sprite_sheet.scale

    def _scale_down(self) -> None:
        """Decrement the sprite sheet scale by 1."""
        self.sprite_sheet.scale -= 1
        if self.sprite_sheet.scale <= 1:
            self.sprite_sheet.scale = 1

    def _scale_up(self) -> None:
        """Increment the sprite sheet scale by 1."""
        self.sprite_sheet.scale += 1
        if self.sprite_sheet.scale >= 6:
            self.sprite_sheet.scale = 6

    def _slice(self, coords: Tuple[Point, Point]) -> Image:
        """Returns slice of the reference image."""
        image = self.reference_image
        scale = self._scale()
        sprite_a, sprite_b = coords[0], coords[1]

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

        #flip the y-axis because of PIL's coordinate system
        top = image.height - top
        bottom = image.height - bottom
        return image.crop((left, bottom, right, top))

    def _translation_speed(self) -> int:
        """Returns spritesheet translation speed."""
        return self.translation_speed

    #BOUNDARIES
    def _bottom_row(self, mask: List[List[bool]]) -> int:
        """Find bottom row index of sprite box."""
        mask.reverse()
        for row in enumerate(mask):
            if any(row[1]):
                return len(mask) - row[0]

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
                return len(row) - row.index(pixel)

    def _top_row(self, mask: List[List[bool]]) -> int:
        """Find top row index of sprite box."""
        for row in enumerate(mask):
            if any(row[1]):
                return row[0]

    def reset(self) -> None:
        self.sprite_sheet.scale = 1
        self.sprite_sheet.x = 0
        self.sprite_sheet.y = 0

    def update(self) -> None:
        self.batch.draw()


class Workspace():
    def __init__(self, img):
        self.outline = Outline()
        self.sprites = SpriteSheet(img)

    def change_outline_end(self, ref_coord: Point) -> None:
        """Change the outline's ending point."""
        self.outline._end(ref_coord)

        #adjust outline as sprite sheet is transformed
        scale = self.sprites._scale()
        translation = self.sprites._coords()
        sheet_coord = Point(ref_coord[0] + translation[0], ref_coord[1] + translation[1])
        self.outline._sheet_end(sheet_coord)

    def change_outline_start(self, ref_coord: Point) -> None:
        """Change the outline's starting point."""
        self.outline._start(ref_coord)

        #adjust outline as sprite sheet is transformed
        scale = self.sprites._scale()
        translation = self.sprites._coords()
        sheet_coord = Point(ref_coord[0] + translation[0], ref_coord[1] + translation[1])
        self.outline._sheet_start(sheet_coord)

    def crop_subsprite(self, mask) -> Box:
        """Return a cropped image."""
        return self.sprites._crop_boundaries(mask)

    def ref_img_coords(self) -> Tuple[Point, Point]:
        """Return the outline's A and B coordinates."""
        return self.outline._ref_coords()

    def pan_up(self) -> None:
        """Pan up on the workspace."""
        speed = self.sprites._translation_speed()
        self.outline._move_up(speed)
        self.sprites._move_up()

    def pan_down(self) -> None:
        """Pan down on the workspace."""
        speed = self.sprites._translation_speed()
        self.outline._move_down(speed)
        self.sprites._move_down()

    def pan_left(self) -> None:
        """Pan left on the workspace."""
        speed = self.sprites._translation_speed()
        self.outline._move_left(speed)
        self.sprites._move_left()

    def pan_right(self) -> None:
        """Pan right on the workspace."""
        speed = self.sprites._translation_speed()
        self.outline._move_right(speed)
        self.sprites._move_right()

    def pixel(self, pos: Point) -> Pixel:
        """Get pixel information."""
        return self.sprites._pixel(pos)

    def sheet_coords(self) -> Tuple[int, int]:
        """Return sprite sheet coordinates."""
        return self.sprites._coords()

    def sheet_scale(self) -> int:
        """Return sprite sheet scale."""
        return self.sprites._scale()

    def slice(self, coords: Tuple[Point, Point]) -> Image:
        """Return a slice of the spritesheet."""
        return self.sprites._slice(coords)

    def zoom_in(self) -> None:
        """Zoom in on the sprite sheet."""
        self.sprites._scale_up()

    def zoom_out(self) -> None:
        """Zoom out on the sprite sheet."""
        self.sprites._scale_down()

    def reset(self) -> None:
        """Reset everything."""
        self.outline.reset()
        self.sprites.reset()

    def update(self) -> None:
        self.sprites.update()
        self.outline.update()
