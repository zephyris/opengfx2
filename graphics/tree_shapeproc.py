#!/usr/bin/env python3

# tree_shapeproc.py
# Generates output images used for dithering to 8bpp
# Inputs (should be of same dimensions for each group):
#   *_shape.png (8bpp, OpenTTD palette)
#    Encodes tree shape with a single colour series for leaves and trunk
#    Encodes recolouring information (per column of sprites) in pixel colours on row 0
# Outputs:
#  *_32bpp.png (RGB)
#    Recoloured shape image

# Run in directory with images to process
# python3 tree_shapeproc.py <scale>
#   scale: 1 or 4
#    64px or 256px tiles respective
#    Defines generation of 'dying' stages

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

suffices = {
  "_leaf_shape.png": {
    "name": "",
    "resize": [0.45, 0.65, 0.85, 1, 1, 1, 1], # scale factor
    "density": [1, 1, 1, 1, 1, 1, 1], # leaf density, random pixel removal
    "browning": [1, 1, 1, 1, 1, 1, 1], # leaf browning, random pixel brownout
    "trunkshift": [0, 0, 0, 0, 0, 0, 0], # trunk index darkening shift
    "rearleafrem": [0, 0, 0, 0, 1, 3, 8], # leaf indices (from lowest) to remove (rear layer)
    "frontleafrem": [0, 0, 0, 0, 4, 6, 8], # leaf indices (from lowest) to remove (rear layer)
  },
  "_nonleaf_shape.png": {
    "name": "nonleaf_",
    "resize": [0.45, 0.65, 0.85, 1, 0.92, 0.82, 0.67], # scale factor
    "density": [1, 1, 1, 1, 1, 1, 1], # leaf density, random pixel removal
    "browning": [1, 1, 1, 1, 0.75, 0.5, 0], # leaf browning, random pixel brownout
    "trunkshift": [0, 0, 0, 0, 0, 2, 4], # trunk index darkening shift
    "rearleafrem": [0, 0, 0, 0, 0, 0, 0], # leaf indices (from lowest) to remove (rear layer)
    "frontleafrem": [0, 0, 0, 0, 0, 0, 0], # leaf indices (from lowest) to remove (rear layer)
  },
  "_pineleaf_shape.png": {
    "name": "nonleaf_",
    "resize": [0.45, 0.65, 0.85, 1, 1, 1, 1], # scale factor
    "density": [1, 1, 1, 1, 1, 1, 0], # leaf density, random pixel removal
    "browning": [1, 1, 1, 1, 0.5, 0, 0], # leaf browning, random pixel brownout
    "trunkshift": [0, 0, 0, 0, 0, 0, 0], # trunk index darkening shift
    "rearleafrem": [0, 0, 0, 0, 0, 0, 0], # leaf indices (from lowest) to remove (rear layer)
    "frontleafrem": [0, 0, 0, 0, 0, 0, 0], # leaf indices (from lowest) to remove (rear layer)
  }
}
for suffix in suffices:
  # Input image must be forrectly formatted:
  # Sprites must be organised in with a 1px white (index index_frame) border
  # Sprites must be organised in columns, each column defines a tree
  # Sprites must be the exact sprite_width/height
  # Source indices for remapping:
  index_leaf_remaps = [80, 81, 82, 83, 84, 85, 86, 87]
  index_trunk_remaps = [104, 105, 106, 107, 108, 109, 110, 111]
  index_remaps_snow = [-1, -1, -1, 214, 213, 212, 211, 210]
  index_browning = [104, 105, 106, 107, 108, 109, 110, 111]
  #index_remaps_snow = index_leaf_remaps[4:] + index_trunk_remaps[4:]
  # Tree sprite sizes
  w = 45
  h = 80
  # Growth/death parameters
  cy = 6 # y position of centre of base of trunk relative to bottom of sprite
  resize = suffices[suffix]["resize"] # scale factor
  density = suffices[suffix]["density"] # leaf density, random pixel removal
  browning = suffices[suffix]["browning"] # leaf browning, random pixel brownout
  trunkshift = suffices[suffix]["trunkshift"] # trunk index darkening shift
  rearleafrem = suffices[suffix]["rearleafrem"]
  frontleafrem = suffices[suffix]["frontleafrem"]
  for input_file in glob.glob("*"+suffix):
    outfile = os.path.join("pygen", input_file[:-len(suffix)]+"_"+suffices[suffix]["name"]+namesuffix+"32bpp.png")
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
        # Output image
        image_out = Image.new("RGBA", (((w + 1) * 7 + 1) * scale, ((h + 1) * columns + 1) * scale), (0, 0, 255))
        draw = ImageDraw.Draw(image_out)
        for column in range(columns):
          seed(0)
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
            if row == 0:
              index_target_leaf = index_target.copy()
            if row == 1:
              index_target_trunk = index_target.copy()
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
          x = column * (w + 1) + 1
          for outcolumn in range(7):
            for rowindex, row in enumerate([0, 1, 0, 2]):
              if height >= (h + 1) * (row + 1) * scale:
                y = row * (h + 1) + 1
                current_spriteset = image_colorised.crop((x * scale, y * scale, (x + w) * scale, (y + h) * scale))
                if row == 0 or row == 1: # leaves and trunk, require growth scaling
                  ow = int(w * resize[outcolumn] * scale)
                  oh = int(h * resize[outcolumn] * scale)
                  xoffs = int(w / 2 - w * resize[outcolumn] / 2)
                  yoffs = int(h - h * resize[outcolumn] + cy * resize[outcolumn] - cy)
                  current_spriteset=current_spriteset.resize((ow, oh), resample=Image.NEAREST)
                else: # terrain integration, no scaling
                  ow = w
                  oh = h
                  xoffs = 0
                  yoffs = 0
                if row == 0: # erase some leaf pixels for patchy apperance
                  if density[outcolumn] < 1: # if pixels should be erased
                    for tx in range(scale, ow - scale): # for all pixels, with padding of scale
                      for ty in range(scale, oh - scale):
                        if randint(0, 100) > density[outcolumn] * 100: # remove pixels to target density
                          if randint(1, scale ** 2) == 1: # removing in clumps, so 1 per scale^2
                            for oa in range(-int(scale / 2) - 1, int(scale / 2) + 1): # for offsets in clump size
                              for ob in range(-int(scale / 2) - 1, int(scale / 2) + 1):
                                if (oa ** 2 + ob ** 2) ** 0.5 < (scale / 2) * 1.3 or randint(0, 1) == 0: # circle + random pixels, not square
                                  current_spriteset.putpixel((tx + oa, ty + ob), 0)
                if row == 0: # erase some leaf indices for dying effect
                  if rowindex == 0:
                    leafrem = rearleafrem
                  elif rowindex == 2:
                    leafrem = frontleafrem
                  #print(row, rowindex, column, leafrem[outcolumn], index_target_leaf)
                  if leafrem[outcolumn] > 0:
                    for tx in range(0, ow): # for all pixels
                      for ty in range(0, oh):
                        cpv = current_spriteset.getpixel((tx, ty))
                        if cpv in index_target_leaf: # if a leaf pixel
                          if index_target_leaf.index(cpv) < leafrem[outcolumn]:
                            current_spriteset.putpixel((tx, ty), 0)
                        if cpv in index_remaps_snow: # if a snowy leaf pixel
                          if index_remaps_snow.index(cpv) <= leafrem[outcolumn]:
                            current_spriteset.putpixel((tx, ty), 0)
                if row == 0: # brown-out some leaf pixels for dead appearance
                  if browning[outcolumn] < 1: # if pixels should be browned
                    for tx in range(0, ow): # for all pixels
                      for ty in range(0, oh):
                        cpv = current_spriteset.getpixel((tx, ty))
                        if randint(0, 100) > browning[outcolumn] * 100 and cpv != 0: # brown pixels to target density
                          for i in range(len(index_target_leaf)):
                            if cpv == index_target_leaf[i]:
                              current_spriteset.putpixel((tx, ty), index_browning[i])
                if row == 1: # index-shift darker some trunk pixels
                  if trunkshift[outcolumn] != 0: # if pixel indices should be shifted
                    for tx in range(0, ow): # for all pixels
                      for ty in range(0, oh):
                        cpv = current_spriteset.getpixel((tx, ty))
                        if cpv in index_target_trunk: # trunk pixels to value shift
                          if index_target_trunk.index(cpv) > trunkshift[outcolumn]:
                            current_spriteset.putpixel((tx, ty), index_target_trunk[index_target_trunk.index(cpv) - trunkshift[outcolumn]])
                          else:
                            current_spriteset.putpixel((tx, ty), index_target_trunk[0])
                if row !=0 or density[outcolumn] > 0: # only draw if the trunk (row 1) or density is non-zero
                  image_out = blue_to(current_spriteset, 0, 0, ow, oh, image_out, ((w + 1) * outcolumn + 1 + xoffs), ((h + 1) * column + 1 + yoffs), scale)
            draw.rectangle((((w + 1) * outcolumn) * scale, ((h + 1) * column) * scale, ((w + 1) * outcolumn) * scale + (w + 2) * scale - 1, ((h + 1) * column) * scale + (h + 2) * scale - 1), fill=None, outline=(255, 255, 255), width=scale)
        # Save the image
        image_out.save(outfile, "PNG")
