#3rd party
import pyglet

#custom
from constants import Color, Point

class Colors():
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        #primary color
        self.p_pos = None
        self.p_color = (255, 255, 255)
        self._p_color_box = {"x": 980, "y": 775, "w": 20, "h": 20}
        self.p_color_box = pyglet.shapes.Rectangle(
            self._p_color_box["x"],
            self._p_color_box["y"],
            self._p_color_box["w"],
            self._p_color_box["h"],
            color=self.p_color,
            batch=self.batch)

        #secondary color
        self.s_pos = None
        self.s_color = (255, 255, 255)
        self._s_color_box = {"x": 980, "y": 755, "w": 20, "h": 20}
        self.s_color_box = pyglet.shapes.Rectangle(
            self._s_color_box["x"],
            self._s_color_box["y"],
            self._s_color_box["w"],
            self._s_color_box["h"],
            color=self.s_color,
            batch=self.batch)

    def update(self) -> None:
        self.p_color_box.color = self.p_color
        self.s_color_box.color = self.s_color
        self.batch.draw()

    def set_p(self, coord: Point, rgb: Color) -> None:
        self.p_color = (rgb[0], rgb[1], rgb[2])
        self.p_color_box.color = self.p_color
        self.p_pos = coord

    def set_s(self, coord: Point, rgb: Color) -> None:
        self.s_color = (rgb[0], rgb[1], rgb[2])
        self.s_color_box.color = self.s_color
        self.s_pos = coord

    def reset(self) -> None:
        self.p_pos = None
        self.s_pos = None
        self.p_color = (255, 255, 255)
        self.s_color = (255, 255, 255)
        self.update()

class Labels():
    def __init__(self, window):
        #label box
        self.background = pyglet.graphics.Batch()
        self.box_height = window.height
        self.box_width = 200
        self.box_color = (255, 255, 255) #White
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
        self.label_color = (0, 0, 0, 255) #Black
        self.primary = pyglet.text.Label(
            self.p_label,
            color=self.label_color,
            x=window.width - self.box_width + self.label_x_offset,
            y=780,
            batch=self.labels)
        self.secondary = pyglet.text.Label(
            self.s_label,
            color=self.label_color,
            x=window.width - self.box_width + self.label_x_offset,
            y=760,
            batch=self.labels)

#         self.start = pyglet.text.Label(
#             self.start_label,
#             color=self.label_color,
#             x=window.width - self.box_width + self.label_x_offset,
#             y=740,
#             batch=self.labels)
#         self.end = pyglet.text.Label(
#             self.end_label,
#             color=self.label_color,
#             x=window.width - self.box_width + self.label_x_offset,
#             y=720,
#             batch=self.labels)

    def update(self, a: Point, b: Point) -> None:
#         self.primary.text = f"{self.p_label} {str(self.p_color)}"
#         self.secondary.text = f"{self.s_label} {str(self.s_color)}"
#         self.start.text = f"{self.start_label} [{a.x}, {a.y}]"
#         self.end.text = f"{self.end_label} [{b.x}, {b.y}]"
        self.background.draw()
        self.labels.draw()

    def reset(self) -> None:
        self.p_label = "Pri:"
        self.s_label = "Sec:"
#         self.start_label = "Start:"
#         self.end_label = "End:"

