#!/usr/bin/env python3

# tree_shapeproc.py
# Generates output images used for dithering to 8bpp
# Inputs (should be of same dimensions for each group):
#   *_shape.png (8bpp, OpenTTD palette)
#    Encodes tree shape with a single colour series for leaves and trunk
#    Encodes recolouring information (per column of sprites) in pixel colours on row 0
# Outputs:
#  *_32bpp.png (RGB)
#    Recoloured and textured shape image, including overlays
#  *_palmask.png (8bpp, OpenTTD palette)
#    Recoloured shape image, overlaid with _overlaynormal
#    Used for restricting colour ranges during dithering

# Run in directory with images to process
# python3 tree_shapeproc.py <scale>
#   scale: 1 or 4
#    64px or 256px tiles respective
#    Defines shading scheme and textures to use

# Dependencies
# pip3 install pillow
# pip3 install numpy
# pip3 install blend-modes

from tools import palette_image

from PIL import Image
from PIL import ImageFilter
from PIL import ImageDraw
from random import randint, seed
import math
import numpy, blend_modes # For overlay blending
import glob, os, sys

from tools import check_update_needed, openttd_palette, openttd_palettise, paste_to, blue_to

if os.path.isdir("pygen") == False: os.mkdir("pygen")

verbose = True
scale = 1
scale = int(sys.argv[1])

snow = False
namesuffix = ""
if len(sys.argv) > 2:
  snow = True
  print("Using snow!")
  namesuffix = "snow_"

# OpenTTD DOS palette, RGB values
palette_r = openttd_palette["r"]
palette_g = openttd_palette["g"]
palette_b = openttd_palette["b"]

# ==Adds value noise to masked indices==
#image_32bit: RGB image to modify
#image_shape, indices: indexed shape reference image and indices to use
#power: +/- value range to add to value channel
def add_value_noise(image_32bit, image_shape, indices, power):
  image_hsv = image_32bit.convert("HSV");
  h, s, v = image_hsv.split()
  width, height = image_32bit.size
  for x in range(width):
    for y in range(height):
      if image_shape.getpixel((x, y)) in indices:
        v.putpixel((x, y), v.getpixel((x, y)) + randint(-power, power))
  image_hsv = Image.merge("HSV", (h, s, v))
  image_32bit = image_hsv.convert("RGB")
  return image_32bit

suffix = "_leaf_shape.png";
# Input image must be forrectly formatted:
# Sprites must be organised in with a 1px white (index index_frame) border
# Sprites must be organised in columns, each column defines a tree
# Sprites must be the exact sprite_width/height
# Source indices for remapping:
index_leaf_remaps = [80, 81, 82, 83, 84, 85, 86, 87]
index_trunk_remaps = [104, 105, 106, 107, 108, 109, 110, 111]
index_remaps_snow = [-1, -1, -1, 213, 212, 211, 210, 210]
#index_remaps_snow = index_leaf_remaps[4:] + index_trunk_remaps[4:]
# Tree sprite sizes
w = 45
h = 80
# Growth/death parameters
cy = 6 # y position of centre of base of trunk relative to bottom of sprite
resize = [0.45, 0.65, 0.85, 1, 1, 1, 1] # scale factor
density = [1, 1, 1, 1, 0.8, 0.5, 0] # leaf density, random pixel removal
for input_file in glob.glob("*"+suffix):
  outfile = os.path.join("pygen", input_file[:-len(suffix)]+"_"+namesuffix+"32bpp.png")
  if check_update_needed([input_file], outfile):
    with Image.open(input_file) as image:
      # Open shape image
      width, height = image.size
      columns = int(math.floor(width / w) / scale)
      print("%s in scale %d mode" % (input_file, scale))
      # Convert shape image to OpenTTD 8 bit
      image_shape = openttd_palettise(image)
      # Apply colouring specified by pixel above each sprite
      image_colorised = Image.new("P", (image_shape.size))
      image_colorised.paste(image_shape, (0,0))
      image_colorised.putpalette(image_shape.getpalette())
      for column in range(columns):
        x = column * (w + 1) + 1
        for row in range(2):
          y = row * (h + 1) + 1
          print("  bounds "+", ".join([str(x) for x in [x, y, w, h]]))
          index_target = []
          if row == 0:
            print("  leaf")
            index_remaps = index_leaf_remaps
          else:
            print("  trunk")
            index_remaps = index_trunk_remaps
          for i in range(len(index_remaps)):
            index_target.append(image_shape.getpixel(((x + i) * scale, (y - 1) * scale)))
          if verbose == True:
            print("  Source indices: "+",".join(map(str, index_remaps)))
            print("  Target indices: "+",".join(map(str, index_target)))
          # Apply new colours
          current_r = palette_r.copy()
          current_g = palette_g.copy()
          current_b = palette_b.copy()
          for i in range(len(index_remaps)):
            current_r[index_remaps[i]] = palette_r[index_target[i]]
            current_g[index_remaps[i]] = palette_g[index_target[i]]
            current_b[index_remaps[i]] = palette_b[index_target[i]]
          # Override with snow colors, if in snow mode 
          if snow == True:
            for i in range(len(index_remaps_snow)):
              if index_remaps_snow[i] != -1:
                current_r[index_remaps[i]] = palette_r[index_remaps_snow[i]]
                current_g[index_remaps[i]] = palette_g[index_remaps_snow[i]]
                current_b[index_remaps[i]] = palette_b[index_remaps_snow[i]]
          current_palimg = palette_image(current_r, current_g, current_b)
          current_spriteset = image_colorised.crop((x * scale, (y - 1) * scale, (x + w) * scale, (y + h) * scale))
          current_spriteset.putpalette(current_palimg.getpalette())
          current_spriteset = openttd_palettise(current_spriteset)
          image_colorised.paste(current_spriteset, (x * scale, (y - 1) * scale))
      # Generate tree growth and death sprites
      current_palimg = palette_image(current_r, current_g, current_b)
      image_out = Image.new("RGBA", (((w + 1) * 7 + 1) * scale, ((h + 1) * columns + 1) * scale), (0, 0, 255))
      draw = ImageDraw.Draw(image_out)
      for column in range(columns):
        x = column * (w + 1) + 1
        for outcolumn in range(7):
          for row in [0, 1, 0]:
            y = row * (h + 1) + 1
            current_spriteset = image_colorised.crop((x * scale, y * scale, (x + w) * scale, (y + h) * scale))
            ow = int(w * resize[outcolumn] * scale)
            oh = int(h * resize[outcolumn] * scale)
            xoffs = int(w / 2 - w * resize[outcolumn] / 2)
            yoffs = int(h - h * resize[outcolumn] + cy * resize[outcolumn] - cy)
            current_spriteset=current_spriteset.resize((ow, oh), resample=Image.NEAREST)
            if row == 0:
              seed(0)
              for tx in range(1, ow - 1):
                for ty in range(1, oh - 1):
                  if randint(0, 100) > density[outcolumn] * 100:
                    current_spriteset.putpixel((tx, ty), 0)
            image_out = blue_to(current_spriteset, 0, 0, ow, oh, image_out, ((w + 1) * outcolumn + 1 + xoffs), ((h + 1) * column + 1 + yoffs), scale)
      # Save a copy of the unshaded image, as palmask
      image_out.save(outfile, "PNG")
