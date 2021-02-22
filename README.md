# Game Sprite Background Remover
Removes the background color from spritesheets.

### Operation
Acts on a single color found in the first pixel coordinate (0, 0).  
Changes each pixel's Alpha value to be transparent that matches the reference pixel.  
Overwrites the original image.  
Saves new image as PNG.
* Run: `python3 removeBackground.py <image>`


### Notes
* Work on one sprite image at a time.
* Program assumes there is a primary and secondary color.
    * (give example screen shots here)
