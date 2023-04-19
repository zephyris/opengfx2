#!/usr/bin/env python3

from PIL import Image
from PIL import ImageFilter
from random import randint
import numpy, blend_modes # For overlay blending
import glob, os, sys

from tools import openttd_palettise, check_update_needed, openttd_palette, openttd_palette_animated, openttd_palette_generalmask

verbose = True

# Define the working palette
palette_r = openttd_palette["r"]
palette_g = openttd_palette["g"]
palette_b = openttd_palette["b"]
# Setup palette image, used for applying palette quickly
def palette_image(r, g, b):
  palette = []
  for i in range(len(r)):
    palette.append(r[i])
    palette.append(g[i])
    palette.append(b[i])
  palimage = Image.new('P', (256, 1))
  for x in range(256):
    palimage.putpixel((x, 0), x)
  palimage.putpalette(palette)
  return palimage
palimage=palette_image(palette_r, palette_g, palette_b)

# Setup palette dict for quick lookup


# Define special palette index sets
# 'Normal' palette entries
colors_normal = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 255]
# Action colours (animated palette indices)
colors_action = openttd_palette_animated
# Special colours, do not propagate errors through these indices
colors_special = openttd_palette_generalmask

# Palette colour sets
# Color set start indices
color_set_start = [1, 16, 24, 32, 40, 50, 53, 60, 70, 80, 88, 96, 104, 112, 122, 128, 136, 144, 154, 162, 170, 178, 192, 198, 206]
# Color set length
color_set_length = [15, 8, 8, 8, 10, 3, 7, 10, 10, 8, 8, 8, 8, 10, 6, 8, 8, 10, 8, 8, 8, 14, 6, 8, 4]

# Primary conversion function
# dither_factor is the additional multiplicative factor on error diffusion, use between 0 and 1
# src and pal are the image to dither and an image defining palette restrictions
def make_8bpp(src, pal, dither_factor):
  width, height = src.size
  # Start by making sure the images are the correct mode
  # Source must be RGB (no alpha)
  src = src.convert("RGB")
  # Palette must be 8-bit with OpenTTD palette
  pal = openttd_palettise(pal)
  
  # Convert src to 8-bit with OpenTTD palette using custom dithering
  # Dithers in HSV space, restricting colour sets when specified in pal
  dithered = make_dithered(src, pal, dither_factor)
  
  # Overlay pixels in pal exactly matching indices in colors_action over dithered image
  # Mask from indices
  v = [0] * 255
  for i in range(len(colors_action)):
    v[colors_action[i]] = 255
  mask_palimg = palette_image(v, v, v)
  mask = pal.copy()
  mask.putpalette(mask_palimg.getpalette())
  mask = mask.convert("L")
  # Paste using mask
  dithered.paste(pal, (0, 0), mask)
  
  # Return result
  return dithered

def most_similar_in_palette(pr, pg, pb):
  dist = 255 * 255 * 255
  index = 0
  for i in colors_normal:
    cd = (pr - palette_r[i]) * (pr - palette_r[i]) + (pg - palette_g[i]) * (pg - palette_g[i]) + (pb - palette_b[i]) * (pb - palette_b[i])
    if cd < dist:
      dist = cd
      index = i
  return index

def most_similar_in_color_set(pr, pg, pb, color_set):
  dist = 255 * 255 * 255
  index = 0
  start_index = color_set_start[color_set]
  end_index = start_index + color_set_length[color_set]
  for i in range(start_index, end_index):
    cd = (pr - palette_r[i]) * (pr - palette_r[i]) + (pg - palette_g[i]) * (pg - palette_g[i]) + (pb - palette_b[i]) * (pb - palette_b[i])
    if cd < dist:
      dist = cd
      index = i
  return index

# Dither function
# Do dithering in RGB space
# Do not dither (propagate pixel value errors) to indices in colors_action or colors_special
# If pal pixel index is in one of the color sets, restrict dithering to only indices in that set
def make_dithered(src, pal, dither_factor):
  # Find colour groups in pal image and make an image recording the color set per pixel
  # If sets pixel is not 255 then dithering is restricted to indices in color_set[pixel value]
  v = [255] * 256
  for i in range(len(color_set_start)):
    for j in range(color_set_length[i]):
      v[color_set_start[i] + j] = i
  sets_palimg = palette_image(v, v, v)
  sets = pal.copy()
  sets.putpalette(sets_palimg.getpalette())
  sets = sets.convert("L")
  
  # Find pixels in src exactly matching colors_special and make an image with this mask
  # Do not propagate pixel value errors through donotdither pixels with value 255
  width, height = src.size
  donotdither = Image.new("L", (width, height), 0)
  for x in range(width):
    for y in range(height):
      pr, pg, pb = src.getpixel((x, y))
      for i in range(len(colors_special)):
        if palette_r[colors_special[i]] == pr and palette_g[colors_special[i]] == pg and palette_b[colors_special[i]] == pb:
          donotdither.putpixel((x, y), 255)
          break
  
  # Dither settings
  # Sierra http://www.tannerhelland.com/4660/dithering-eleven-algorithms-source-code/
  #dox = 2
  #doy = 0
  #df = 32
  #da = [
  #  [-1, -1, -1,  5,  3],
  #  [ 2,  4,  5,  4,  2],
  #  [ 0,  2,  3,  2,  0]
  #]
  
  # Sierra lite http://www.tannerhelland.com/4660/dithering-eleven-algorithms-source-code/
  dox = 1
  doy = 0
  df = 4
  da = [
    [-1, -1,  2],
    [ 1,  1,  0]
  ]
  
  # Do dithering
  # TODO: Change to dithering in HSV space, with error propogation factors of h, s, v = 0, 0.8, 1.0
  res = Image.new("P", (src.size))
  res.putpalette(palimage.getpalette())
  for y in range(height):
    for x in range(width):
      pr, pg, pb = src.getpixel((x, y))
      if donotdither.getpixel((x, y)) == 255:
        # Do not dither this pixel, just set nearest value
        res.putpixel((x, y), most_similar_in_palette(pr, pg, pb))
      else:
        # Dither this pixel
        if sets.getpixel((x, y)) != 255:
          # Dither this pixel within a color set
          res.putpixel((x, y), most_similar_in_color_set(pr, pg, pb, sets.getpixel((x, y))))
        else:
          # Dither this pixel to any color
          res.putpixel((x, y), most_similar_in_palette(pr, pg, pb))
        # Diffuse errors according to the dithering matrix
        error = [0, 0, 0]
        error[0] = pr - palette_r[res.getpixel((x, y))]
        error[1] = pg - palette_g[res.getpixel((x, y))]
        error[2] = pb - palette_b[res.getpixel((x, y))]
        # Do error propagation
        for b in range(len(da)):
          for a in range(len(da[0])):
            # For each x and y offset a and b in dither array
            if da[b][a] != -1 and x + a < width - 1 and y + b < height - 1:
              # If a valid dither value and within image bounds
              if donotdither.getpixel((x, y)) != 255:
                # Do not propagate errors through pixels identified as donotdither
                # Alter pixel value to propagate errors
                pcr, pcg, pcb = src.getpixel((x + a - dox, y + b - doy))
                pcr = int(pcr + error[0] * dither_factor * da[b][a] / df)
                pcg = int(pcg + error[1] * dither_factor * da[b][a] / df)
                pcb = int(pcb + error[2] * dither_factor * da[b][a] / df)
                src.putpixel((x + a - dox, y + b - doy), (pcr, pcg, pcb))

  # Return result
  return res

suffix = "_32bpp.png";
print("Converting to 8-bit")
for input_file in glob.glob("*"+suffix):
  # Only process images lacking a *_8bpp output _or_ modified more recently than the *_8bpp output
  do_processing = True
  name = input_file[:-len(suffix)]
  if verbose == True:
    print(" "+name)
  do_processing = check_update_needed([input_file], name+"_8bpp.png")
  if do_processing:
    with Image.open(input_file) as image:
      name = input_file[:-len(suffix)]
      width, height = image.size
      if os.path.isfile(name+"_palmask.png"):
        palmask = Image.open(name+"_palmask.png")
      else:
        palmask = Image.new("P", (width, height), 0)
        palmask.putpalette(palimage.getpalette())
      image_8bpp = make_8bpp(image, palmask, 1);
      image_8bpp.save(name+"_8bpp.png", "PNG")
  else:
    print("  Skipped, output exists and is up-to-date")