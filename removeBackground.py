"""Makes all pixels matching the reference pixel transparent.
    For use in removing the backgrounds of sprites.
"""
#std lib
import sys

#3rd party
from PIL import Image

#get file name from args
file_ = sys.argv[1]

#load file 
img = Image.open(file_).convert("RGBA")
ref = img.getpixel((0,0))

count = 0
for i in range(img.width):
    for j in range(img.height):
        px = img.getpixel((i,j))
        if px == ref:
            img.putpixel((i,j), (0,0,0,0))
img.show()

#save the image...
