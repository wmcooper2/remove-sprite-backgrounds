"""Makes all pixels matching the reference pixel transparent.
    For use in removing the backgrounds of sprites.

    Run like this:
        `python3 removeBackground.py source.png 11 22`

        x = 11
        y = 22
        reference pixel becomes (11, 22)

    !!! overwrites original image

"""
#std lib
import sys

#3rd party
from PIL import Image

#get file name from args
file_ = sys.argv[1]

#choose ref pixel from args
ref_x = int(sys.argv[2])
ref_y = int(sys.argv[3])

#choose save to location from args
# save_to = sys.argv[4]

#load file 
img = Image.open(file_).convert("RGBA")
# ref = img.getpixel((0,0))
ref = img.getpixel((ref_x, ref_y))

count = 0
for i in range(img.width):
    for j in range(img.height):
        px = img.getpixel((i,j))
        if px == ref:
            img.putpixel((i,j), (0,0,0,0))
img.show()
img.save(file_, "PNG")

#save the image...
