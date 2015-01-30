#!env python
'''
Created on 30 janv. 2015

@author: Christophe Calvès

Very simple image transformation script.
It requires python 3 and the pillow module to run.  

Copyright (C) 2015 Christophe Calvès

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
 
'''
from __future__ import print_function
from PIL import Image, ImageFont, ImageDraw

# CONFIGURATION ZONE: EDIT THESE VARIABLES TO FIT YOUR TASTE.

# File path of the input image.
# It has to be a RGBA image!!
filesrc = "/home/tof/Perso/admin/identites/bind_nuage.png"

# File path of the output image
filedst = "/tmp/test.png"

# Font to use: file path to the font and font size
font = ImageFont.truetype('/usr/share/fonts/TTF/timesbd.ttf', 20)

# Horizontal space to let between characters
padding_width  = 0

# Vertical space to let between characters
padding_height = 0

# For every region of the input image: if the mean value is less than threshold,
# replace that region by "0" (lessthanthreshold) in the output image.
# Otherwise, replace it by "1" (greaterorequaltothreashold).
threshold= 0.3
lessthanthreshold = "0"
greaterorequaltothreshold="1"

# END OF CONFIGUTATION ZONE. DO NOT EDIT PAST THIS LINE
# UNLESS YOU KNOW WHAT YOU'RE DOING.

imsrc = Image.open(filesrc)
size  = imsrc.size

im_width  = size[0]
im_height = size[1]

# Calculating font width and height
drawsrc = ImageDraw.Draw(imsrc)

one_size = drawsrc.textsize(greaterorequaltothreshold, font)
zero_size= drawsrc.textsize(lessthanthreshold, font)

# Size of the boxes that contain either greaterorequaltothreshold or lessthanthreshold
# It has to be big enough for greaterorequaltothreshold or lessthanthreshold
# and the padding.
box_width  = max(one_size[0], zero_size[0]) + padding_width
box_height = max(one_size[1], zero_size[1]) + padding_height

del one_size, zero_size, drawsrc

# Computes the mean value (taking alpha into account) of the
# rectangular region from (x,y) to (x+box_width, y+box_height)
# of the input image.
def mean(x , y):
    res = 0
    
    width  = min(box_width , im_width  - x)
    height = min(box_height, im_height - y)
    
    for row in range(height):
        for col in range(width):
            pixel = imsrc.getpixel((x+col, y+row))
            res += pixel[3] * (pixel[0] + pixel[1] + pixel[2]) / (255 * 255 * 3)
            
    
    return res / (height * width)

# Horizontal number of boxes 
boxes_width  = int(im_width  / box_width )

# Vertical number of boxes
boxes_height = int(im_height / box_height)

# Size of the output image
imdst_width  = box_width  * boxes_width
imdst_height = box_height * boxes_height

# Output image
imdst = Image.new(imsrc.mode, (imdst_width,imdst_height) , 0xffffffff)
draw  = ImageDraw.Draw(imdst)

for row in range(boxes_height):
    for col in range(boxes_width):
        x = col * box_width
        y = row * box_height 
        m = mean(x,y)
        
        if(m >= threshold):
            txt = greaterorequaltothreshold
        else:
            txt = lessthanthreshold
    
        draw.text((x,y),txt, font = font, fill=(0,0,0,255))
    
imdst.save(filedst)
