#!/usr/bin/env python3

# building_shapeproc.py
# Generates output images used for dithering to 8bpp
# Inputs (should be of same dimensions for each group):
#   *_base_shape.png (8bpp, OpenTTD palette)
#    Encodes key ground textures with specific colours
#    Encodes wall/foliage/woodwork shape with specific colours for specific wall directions and materials
#    Encodes recolouring information (per column of sprites) in pixel colours on row 0
#   *_base_overlayshading.png (RGBA)
#    Overlay for shading, used as opacity 0.25 overlay mode overlay
#  *_base_overlaynormal.png (RGBA, should use only OpenTTD palette colours)
#    Overlay for overdrawn pixel art, used as opacity 1.0 normal mode overlay
# Resources:
#  textures
#    Images in ../textures relative to working directory
#    Should tile
# Outputs:
#  *_base_32bpp.png (RGB)
#    Recoloured and textured shape image, including overlays
#  *_base_palmask.png (8bpp, OpenTTD palette)
#    Recoloured shape image, overlaid with _overlaynormal
#    Used for restricting colour ranges during dithering

# Run in directory with images to process
# python3 building_shapeproc.py <scale>
#   scale: 1 or 4
#    64px or 256px tiles respective
#    Defines shading scheme and textures to use

# Dependencies
# pip3 install pillow
# pip3 install numpy
# pip3 install blend-modes

from PIL import Image
from PIL import ImageFilter
from random import randint
import numpy, blend_modes # For overlay blending
import glob, os, sys

from tools import openttd_palettise

if os.path.isdir("pygen") == False: os.mkdir("pygen")

verbose = True
scale = 1
scale = int(sys.argv[1])

snow = False
snowname = ""
if len(sys.argv) > 2:
  snow = True
  print("Using snow!")
  snowname = "snow_"
  

# OpenTTD DOS palette, RGB values
palette_r = [0,16,32,48,64,80,100,116,132,148,168,184,200,216,232,252,52,68,88,108,132,156,176,204,48,64,80,96,120,148,176,204,72,88,104,124,152,184,212,244,64,88,112,136,160,188,204,220,236,252,252,252,252,76,96,116,136,156,176,196,68,96,128,156,184,212,232,252,252,252,32,64,84,108,128,148,168,184,196,212,8,16,32,48,64,84,104,128,28,44,60,80,104,128,152,180,16,32,56,76,96,120,152,184,32,56,72,88,104,124,140,160,76,96,116,136,164,184,204,212,224,236,80,100,120,140,160,184,36,48,64,80,100,132,172,212,40,64,88,104,120,140,160,188,0,0,0,0,0,24,56,88,128,188,16,24,40,52,80,116,156,204,172,212,252,252,252,252,252,252,72,92,112,140,168,200,208,232,60,92,128,160,196,224,252,252,252,252,252,252,252,252,204,228,252,252,252,252,8,12,20,28,40,56,72,100,92,108,124,144,224,200,180,132,88,244,245,246,247,248,249,250,251,252,253,254,255,76,108,144,176,210,252,252,252,252,252,252,252,64,255,48,64,80,255,32,36,40,44,48,72,100,216,96,68,255]
palette_g = [0,16,32,48,64,80,100,116,132,148,168,184,200,216,232,252,60,76,96,116,140,160,184,208,44,60,76,92,120,148,176,204,44,60,80,104,132,160,188,220,0,4,16,32,56,84,104,132,156,188,208,232,252,40,60,88,116,136,156,180,24,44,68,96,120,156,184,212,248,252,4,20,28,44,56,72,92,108,128,148,52,64,80,96,112,132,148,168,52,68,88,104,124,148,176,204,52,72,96,116,136,164,192,220,24,28,40,52,64,84,108,128,40,52,68,84,96,112,128,148,168,188,28,40,56,76,100,136,40,52,64,80,100,132,172,212,20,44,64,76,88,104,136,168,24,36,52,72,96,120,144,168,196,224,64,80,96,112,140,172,204,240,52,52,52,100,144,184,216,244,20,44,68,100,136,176,184,208,0,0,0,0,0,0,0,80,108,136,164,192,220,252,136,144,156,176,196,216,24,36,52,68,92,120,152,172,156,176,200,224,244,236,220,188,152,0,0,0,0,0,0,0,0,0,0,0,0,24,44,72,108,146,60,84,104,124,148,172,196,0,0,48,64,80,255,68,72,76,80,84,100,132,244,128,96,255]
palette_b = [255,16,32,48,64,80,100,116,132,148,168,184,200,216,232,252,72,92,112,132,152,172,196,220,4,12,20,28,64,100,132,168,4,20,44,72,92,120,148,176,4,16,32,52,76,108,124,144,164,192,0,60,128,0,8,28,56,80,108,136,0,4,8,16,24,32,16,0,128,192,0,8,16,28,40,56,76,88,108,128,0,0,4,4,12,20,28,44,24,32,48,60,76,92,108,124,24,44,72,88,108,136,168,200,0,0,4,12,24,44,64,88,16,24,40,56,64,80,96,112,128,148,4,20,40,64,96,136,68,84,100,116,136,164,192,224,112,144,172,196,224,252,252,252,108,132,160,184,212,220,232,240,252,252,96,108,120,132,160,192,220,252,52,52,52,88,124,160,200,236,112,140,168,196,224,248,255,252,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,4,0,48,100,152,88,104,124,140,164,188,216,224,52,64,76,92,252,248,236,216,172,244,245,246,247,248,249,250,251,252,253,254,255,8,24,52,84,126,0,0,0,0,0,0,0,0,0,0,0,0,0,112,116,120,124,128,144,168,252,164,140,255]
# Setup palette image, used for applying palette quickly
def palette_image(r, g, b):
  palette = []
  for i in range(len(r)):
    palette.append(r[i])
    palette.append(g[i])
    palette.append(b[i])
  #if verbose == True:
    #print("Palette:")
    #print("%d entries" % len(palette))
    #print(palette)
  palimage = Image.new('P', (256, 1))
  for x in range(256):
    palimage.putpixel((x, 0), x)
  palimage.putpalette(palette)
  return palimage
palimage=palette_image(palette_r, palette_g, palette_b)

# Special palette details
# Values to exclude during dithering
palette_exclude = [0,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,245,246,247,248,249,250,251,252,253,254,254,255]
palette_generalmask = [0, 255]


# ==Insets or outsets a blurred version masked indices==
#image_32bit: RGB image to modify
#image_shape, indices: indexed shape reference image
#indices: indices in shape image to modify, either inset within these indices or outset around these indices
#offset_x, offset_y: distance to shift blurred inset in x and y
#blur, value, opacity: blur radius, value (colour) and opacity of blurred inset
#blend: "normal" or "overlay"
#mode: "inset" or "outset"
def inout_blur(image_32bit, image_shape, indices, offset_x, offset_y, blur, value, opacity, blend, mode):
  # Make black image for merging channels
  image_black = Image.new("L", (image_32bit.size), 0)
  image_white = Image.new("L", (image_32bit.size), 255)
  image_value_r = Image.new("L", (image_32bit.size), value[0])
  image_value_g = Image.new("L", (image_32bit.size), value[1])
  image_value_b = Image.new("L", (image_32bit.size), value[2])
  # Make sharp mask from indices (white = in indices)
  if mode == "inset":
    v = [255] * 256
    for i in range(len(indices)):
      v[indices[i]] = 0
  elif mode == "outset":
    v = [0] * 256
    index_exclude = palette_exclude + indices
    for i in range(len(index_exclude)):
      v[index_exclude[i]] = 255
  mask_palimg = palette_image(v, v, v)
  image_shape.putpalette(mask_palimg.getpalette())
  image_mask = image_shape.convert("L")
  # Make blurred overlay (black = in indices, with spatial offset)
  if mode == "inset":
    v = [255] * 256
    for i in range(len(indices)):
      v[indices[i]] = 0
  elif mode == "outset":
    v = [0] * 256
    for i in range(len(indices)):
      v[indices[i]] = 255
  mask_palimg = palette_image(v, v, v)
  image_shape.putpalette(mask_palimg.getpalette())
  image_overlay = Image.new("L", (image_mask.size))
  image_overlay.paste(image_shape, (offset_x, offset_y))
  image_overlay = image_overlay.filter(ImageFilter.GaussianBlur(radius=blur))
  image_overlay = Image.merge("RGBA", (image_value_r, image_value_g, image_value_b, image_overlay))
  # Mask blurred overlay with sharp mask
  image_transparent = Image.merge("RGBA", (image_black, image_black, image_black, image_black))
  image_overlay.paste(image_transparent, (0, 0), image_mask)
  # Overlay blurred image
  r, g, b = image_32bit.convert("RGB").split()
  image_32bit = Image.merge("RGBA", (r, g, b, image_white))
  image_bg_arr = numpy.array(image_32bit).astype(float)
  image_fg_arr = numpy.array(image_overlay).astype(float)
  if blend == "overlay":
    image_blended_arr_float = blend_modes.overlay(image_bg_arr, image_fg_arr, opacity)
  elif blend == "normal":
    image_blended_arr_float = blend_modes.normal(image_bg_arr, image_fg_arr, opacity)
  image_blended_arr = numpy.uint8(image_blended_arr_float)
  image_out = Image.fromarray(image_blended_arr)
  return image_out

def overlay_texture(image_32bit, image_shape, image_texture, indices, opacity, blend):
  # Make black image for merging channels
  image_black = Image.new("L", (image_32bit.size), 0)
  image_white = Image.new("L", (image_32bit.size), 255)
  # Make sharp mask from indices (white = in indices)
  v = [255] * 256
  for i in range(len(indices)):
    v[indices[i]] = 0
  mask_palimg = palette_image(v, v, v)
  image_shape.putpalette(mask_palimg.getpalette())
  image_mask = image_shape.convert("L")
  image_width, image_height = image_32bit.size
  # Make texture large enough for overlay
  image_overlay = Image.new("RGBA", (image_32bit.size))
  texture_width, texture_height = image_texture.size
  for x in range(int(image_width/texture_width)+1):
    for y in range(int(image_height/texture_height)+1):
      image_overlay.paste(image_texture, (x * texture_width, y * texture_height))
  # Mask blurred overlay with sharp mask
  image_transparent = Image.merge("RGBA", (image_black, image_black, image_black, image_black))
  image_overlay.paste(image_transparent, (0, 0), image_mask)
  # Overlay texture image
  r, g, b = image_32bit.convert("RGB").split()
  image_32bit = Image.merge("RGBA", (r, g, b, image_white))
  image_bg_arr = numpy.array(image_32bit).astype(float)
  image_fg_arr = numpy.array(image_overlay).astype(float)
  if blend == "overlay":
    image_blended_arr_float = blend_modes.overlay(image_bg_arr, image_fg_arr, opacity)
  elif blend == "normal":
    image_blended_arr_float = blend_modes.normal(image_bg_arr, image_fg_arr, opacity)
  image_blended_arr = numpy.uint8(image_blended_arr_float)
  image_out = Image.fromarray(image_blended_arr)
  return image_out

def simple_overlay_texture(image_32bit, image_shape, image_texture, indices):
  # Make black image for merging channels
  image_black = Image.new("L", (image_32bit.size), 0)
  image_white = Image.new("L", (image_32bit.size), 255)
  # Make sharp mask from indices (white = in indices)
  v = [0] * 255
  for i in range(len(indices)):
    v[indices[i]] = 255
  mask_palimg = palette_image(v, v, v)
  image_shape.putpalette(mask_palimg.getpalette())
  image_mask = image_shape.convert("L")
  image_width, image_height = image_32bit.size
  # Make texture large enough for overlay
  image_texture = image_texture.convert("RGBA")
  image_overlay = Image.new("RGBA", (image_32bit.size))
  texture_width, texture_height = image_texture.size
  for x in range(int(image_width/texture_width)+1):
    for y in range(int(image_height/texture_height)+1):
      image_overlay.paste(image_texture, (x * texture_width, y * texture_height))
  # Mask texture overlay with sharp mask
  # Overlay texture image
  image_32bit.paste(image_overlay, (0, 0), image_mask)
  return image_32bit

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

suffix = "_base_shape.png";
index_frame = [15, 255] #### HACKED!!! Why does index conversion of input sprite not use index 255/white? ####
# Input image must be forrectly formatted:
# Sprites must be organised in with a 1px white (index index_frame) border
# Sprites must be organised in columns, each column will be recoloured together
# Pixels on the first row, aligned with the start of the sprite column, indicate remapping
# Source indices for remapping:
# Base area (1 entry), walls main (3 entries), walls alt (3), roof (3), windows (3), woodwork (3), metalwork (3)
index_groundtextures = [82, 107, 8, 3]
index_remaps = [1, 41, 42, 43, 90, 91, 92, 115, 116, 117]
index_remaps_snow = [-1, -1, -1, 211, -1, -1, 211, -1, -1, 211]
index_base = [1]
index_walls = [41, 42, 43]
index_greenery = [90, 91, 92]
index_woodwork = [115, 116, 117]
for input_file in glob.glob("*"+suffix):
  with Image.open(input_file) as image:
    # Open shape image
    width, height = image.size
    print("%s in scale %d mode" % (input_file, scale))
    # Convert shape image to OpenTTD 8 bit
    image_shape = openttd_palettise(image)
    # Apply colouring specified by pixel above each column of sprites
    # Loop through _second_ row of pixels (multiplied by scale)
    image_colorised = Image.new("P", (image_shape.size))
    image_colorised.paste(image_shape, (0,0))
    image_colorised.putpalette(image_shape.getpalette())
    x = 0
    while x < width - scale:
      # Find start of a sprite
      while x < width - scale and image_shape.getpixel((x, 2 * scale)) in index_frame:
        x += 1
      # Find sprite width
      w = 0
      while x + w < width - scale and image_shape.getpixel((x + w, 2 * scale)) not in index_frame:
        w += 1
      if verbose == True:
        print(" Sprite column, x: %d, w: %d" % (x, w))
      # Lookup color remapping
      if w > len(index_remaps):
        # Only process if sprite column is wide enough to have all remapping info in row 1
        index_target = []
        for i in range(len(index_remaps)):
          index_target.append(image_shape.getpixel((x + i * scale, 0 * scale)))
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
          #Replace horizontal and roofs with snow colours
          for i in range(len(index_remaps_snow)):
            if index_remaps_snow[i] != -1:
              current_r[index_remaps[i]] = palette_r[index_remaps_snow[i]]
              current_g[index_remaps[i]] = palette_g[index_remaps_snow[i]]
              current_b[index_remaps[i]] = palette_b[index_remaps_snow[i]]
        current_palimg = palette_image(current_r, current_g, current_b)
        current_spriteset = image_colorised.crop((x, 0, x + w, height))
        current_spriteset.putpalette(current_palimg.getpalette())
        current_spriteset = openttd_palettise(current_spriteset)
        image_colorised.paste(current_spriteset, (x, 0))
        # Increment x position by width for the next sprite set
        x += w
    # Make copy of the image for shading
    image_32bit = Image.new("RGB", (image_colorised.size))
    image_32bit.paste(image_colorised, (0, 0))
    # Save a copy of the unshaded image, with the pixel art overlay if it exists, as the palette mask
    image_unshaded = Image.new("P", (image_colorised.size))
    image_unshaded.paste(image_colorised, (0, 0))
    image_unshaded.putpalette(image_colorised.getpalette())
    # Set pixels in ground texture to background colour (ie. allow all colours for dithering)
    for x in range(width):
      for y in range(height):
        if image_shape.getpixel((x, y)) in index_groundtextures:
          image_unshaded.putpixel((x, y), 0)
    normal_overlay_name = input_file[:-len(suffix)]+"_base_overlaynormal.png"
    if os.path.isfile(normal_overlay_name):
      image_unshaded = overlay_texture(image_32bit, image_shape, Image.open(normal_overlay_name), range(256), 255/255, "normal")
    image_unshaded.save(os.path.join("pygen", input_file[:-len(suffix)]+"_"+snowname+"base_palmask.png"), "PNG")
    # Shade using standard rules
    # Ground textures
    texture_opacity = 255
    if snow == True:
      image_32bit = simple_overlay_texture(image_32bit, image_shape, Image.open("../../textures/ground_snow.png"), [index_groundtextures[0]])
    else:
      image_32bit = simple_overlay_texture(image_32bit, image_shape, Image.open("../../textures/ground_grass_temperate.png"), [index_groundtextures[0]])
    image_32bit = simple_overlay_texture(image_32bit, image_shape, Image.open("../../textures/ground_bare.png"), [index_groundtextures[1]])
    image_32bit = simple_overlay_texture(image_32bit, image_shape, Image.open("../../textures/ground_concrete.png"), [index_groundtextures[2]])
    image_32bit = simple_overlay_texture(image_32bit, image_shape, Image.open("../../textures/ground_tarmac.png"), [index_groundtextures[3]])
    # Greenery noise and shading
    if scale == 1:
      image_32bit = add_value_noise(image_32bit, image_shape, index_greenery, 27)
    elif scale == 4:
      image_32bit = overlay_texture(image_32bit, image_shape, Image.open("../../textures/foliage.png"), index_greenery, 92/255, "overlay")
    image_32bit = inout_blur(image_32bit, image_shape, index_greenery, 1, -1, 2, (0, 0, 0), 191/255, "overlay", "inset")
    image_32bit = inout_blur(image_32bit, image_shape, index_greenery, -1, 1, 2, (255, 255, 255), 191/255, "overlay", "inset")
    # Wall noise and shading
    image_32bit = add_value_noise(image_32bit, image_shape, index_walls, 15)
    image_32bit = inout_blur(image_32bit, image_shape, index_walls, 1, -1, 1, (0, 0, 0), 191/255, "overlay", "inset")
    image_32bit = inout_blur(image_32bit, image_shape, index_walls, -1, 1, 1, (255, 255, 255), 191/255, "overlay", "inset")
    # Blurred ground overlay
    image_32bit = inout_blur(image_32bit, image_shape, [index_groundtextures[0], 0, 255], -2, 0, 1.5, (255, 255, 255), 159/255, "overlay", "inset")
    image_32bit = inout_blur(image_32bit, image_shape, [index_groundtextures[0], index_groundtextures[1], 0, 255], 0, 0, 1.5, (0, 0, 0), 159/255, "overlay", "inset")
    image_32bit = inout_blur(image_32bit, image_shape, [index_groundtextures[3], 0, 255], 2, 0, 1.5, (0, 0, 0), 159/255, "overlay", "inset")
    # Building base shadow
    image_32bit = inout_blur(image_32bit, image_shape, index_base, -2, 0, 1.5, (0, 0, 0), 191/255, "normal", "outset")
    # Add manual overlays, if the files exist
    # Overlay overlay_alpha, if it exists
    alpha_overlay_name = input_file[:-len(suffix)]+"_base_overlayalpha.png"
    if os.path.isfile(alpha_overlay_name):
      print(alpha_overlay_name)
      image_32bit = image_32bit.convert("RGBA")
      image_32bit = Image.alpha_composite(image_32bit, Image.open(alpha_overlay_name).convert("RGBA"))
    # Shading/overlay mode overlay
    shading_overlay_name = input_file[:-len(suffix)]+"_base_overlayshading.png"
    if os.path.isfile(shading_overlay_name):
      image_32bit = overlay_texture(image_32bit, image_shape, Image.open(shading_overlay_name), range(256), 63/255, "overlay")
    # Pixel art/normal mode overlay
    normal_overlay_name = input_file[:-len(suffix)]+"_base_overlaynormal.png"
    if os.path.isfile(normal_overlay_name):
      image_32bit = overlay_texture(image_32bit, image_shape, Image.open(normal_overlay_name), range(256), 255/255, "normal")
    # Save shaded image
    image_32bit.save(os.path.join("pygen", input_file[:-len(suffix)]+"_"+snowname+"base_32bpp.png"), "PNG")