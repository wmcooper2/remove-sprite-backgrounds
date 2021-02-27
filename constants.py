#std lib
from collections import namedtuple
import sys

#3rd party
from PIL import Image

Color = namedtuple("Color", ["red", "green", "blue"])
Point = namedtuple("Point", ["x", "y"])
Box = namedtuple("Box", ["x1", "y1", "x2", "y2"])

class Pixel:
    def __init__(self, point: Point, color: Color):
        self.point = point
        self.color = color

# Pixel = namedtuple("Pixel", [("Point", Point), ("Color", Color)])
