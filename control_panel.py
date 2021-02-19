#3rd party
import pyglet

#custom
from constants import Color, Point
# from constants import Constants as c

class Colors():
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.primary = None
        self.secondary = None
#         self.p_color = shape
#         self.rectangle = pyglet.shapes.Rectangle(
#             600,
#             600,
#             100,
#             100,
#             color=self.primary,
#             batch=self.batch)
#         self.s_color = shape

    def update(self) -> None:
        self.batch.draw()

    def set_primary(self, red: int, green: int, blue: int) -> None:
        self.primary = (red, green, blue)

    def set_secondary(self, red: int, green: int, blue: int) -> None:
        self.secondary = (red, green, blue)

    def primary_pixel(self, coord) -> None:
        self.p_pixel = coord
        print(self.p_pixel)

    def secondary_pixel(self, coord) -> None:
        self.s_pixel = coord
        print(self.s_pixel)

    def reset(self) -> None:
        self.primary = None
        self.secondary = None


class Labels():
    def __init__(self, window):
        #label box
        self.background = pyglet.graphics.Batch()
        self.box_height = window.height
        self.box_width = 200
        self.box_color = (0, 255, 0) #Green
        self.rectangle = pyglet.shapes.Rectangle(
            window.width - self.box_width,
            0,
            self.box_width,
            self.box_height,
            color=self.box_color,
            batch=self.background)
        self.p_label = "Pri:"
        self.s_label = "Sec:"
        self.start_label = "Start:"
        self.end_label = "End:"

        #labels
        self.label_y_offset = 10
        self.label_x_offset = 10
        self.labels = pyglet.graphics.Batch()
        self.label_color = (255, 0, 0, 255) #Red
        self.primary = pyglet.text.Label(self.p_label,
            color=self.label_color,
            x=window.width - self.box_width + self.label_x_offset,
            y=780,
            batch=self.labels)
        self.secondary = pyglet.text.Label(self.s_label,
            color=self.label_color,
            x=window.width - self.box_width + self.label_x_offset,
            y=760,
            batch=self.labels)
        self.start = pyglet.text.Label(self.start_label,
            color=self.label_color,
            x=window.width - self.box_width + self.label_x_offset,
            y=740,
            batch=self.labels)
        self.end = pyglet.text.Label(self.end_label,
            color=self.label_color,
            x=window.width - self.box_width + self.label_x_offset,
            y=720,
            batch=self.labels)

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

