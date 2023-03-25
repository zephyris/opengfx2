#!/usr/bin/env python3

from PIL import Image
from PIL import ImageFilter
from random import randint
import numpy, blend_modes # For overlay blending
import glob, os, sys

from tools import openttd_palettise

verbose = True

# Define the working palette
palette_r = [0, 16, 32, 48, 64, 80, 100, 116, 132, 148, 168, 184, 200, 216, 232, 252, 52, 68, 88, 108, 132, 156, 176, 204, 48, 64, 80, 96, 120, 148, 176, 204, 72, 88, 104, 124, 152, 184, 212, 244, 64, 88, 112, 136, 160, 188, 204, 220, 236, 252, 252, 252, 252, 76, 96, 116, 136, 156, 176, 196, 68, 96, 128, 156, 184, 212, 232, 252, 252, 252, 32, 64, 84, 108, 128, 148, 168, 184, 196, 212, 8, 16, 32, 48, 64, 84, 104, 128, 28, 44, 60, 80, 104, 128, 152, 180, 16, 32, 56, 76, 96, 120, 152, 184, 32, 56, 72, 88, 104, 124, 140, 160, 76, 96, 116, 136, 164, 184, 204, 212, 224, 236, 80, 100, 120, 140, 160, 184, 36, 48, 64, 80, 100, 132, 172, 212, 40, 64, 88, 104, 120, 140, 160, 188, 0, 0, 0, 0, 0, 24, 56, 88, 128, 188, 16, 24, 40, 52, 80, 116, 156, 204, 172, 212, 252, 252, 252, 252, 252, 252, 72, 92, 112, 140, 168, 200, 208, 232, 60, 92, 128, 160, 196, 224, 252, 252, 252, 252, 252, 252, 252, 252, 204, 228, 252, 252, 252, 252, 8, 12, 20, 28, 40, 56, 72, 100, 92, 108, 124, 144, 224, 200, 180, 132, 88, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 76, 108, 144, 176, 210, 252, 252, 252, 252, 252, 252, 252, 64, 255, 48, 64, 80, 255, 32, 36, 40, 44, 48, 72, 100, 216, 96, 68, 255]
palette_g = [0, 16, 32, 48, 64, 80, 100, 116, 132, 148, 168, 184, 200, 216, 232, 252, 60, 76, 96, 116, 140, 160, 184, 208, 44, 60, 76, 92, 120, 148, 176, 204, 44, 60, 80, 104, 132, 160, 188, 220, 0, 4, 16, 32, 56, 84, 104, 132, 156, 188, 208, 232, 252, 40, 60, 88, 116, 136, 156, 180, 24, 44, 68, 96, 120, 156, 184, 212, 248, 252, 4, 20, 28, 44, 56, 72, 92, 108, 128, 148, 52, 64, 80, 96, 112, 132, 148, 168, 52, 68, 88, 104, 124, 148, 176, 204, 52, 72, 96, 116, 136, 164, 192, 220, 24, 28, 40, 52, 64, 84, 108, 128, 40, 52, 68, 84, 96, 112, 128, 148, 168, 188, 28, 40, 56, 76, 100, 136, 40, 52, 64, 80, 100, 132, 172, 212, 20, 44, 64, 76, 88, 104, 136, 168, 24, 36, 52, 72, 96, 120, 144, 168, 196, 224, 64, 80, 96, 112, 140, 172, 204, 240, 52, 52, 52, 100, 144, 184, 216, 244, 20, 44, 68, 100, 136, 176, 184, 208, 0, 0, 0, 0, 0, 0, 0, 80, 108, 136, 164, 192, 220, 252, 136, 144, 156, 176, 196, 216, 24, 36, 52, 68, 92, 120, 152, 172, 156, 176, 200, 224, 244, 236, 220, 188, 152, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 24, 44, 72, 108, 146, 60, 84, 104, 124, 148, 172, 196, 0, 0, 48, 64, 80, 255, 68, 72, 76, 80, 84, 100, 132, 244, 128, 96, 255]
palette_b = [255, 16, 32, 48, 64, 80, 100, 116, 132, 148, 168, 184, 200, 216, 232, 252, 72, 92, 112, 132, 152, 172, 196, 220, 4, 12, 20, 28, 64, 100, 132, 168, 4, 20, 44, 72, 92, 120, 148, 176, 4, 16, 32, 52, 76, 108, 124, 144, 164, 192, 0, 60, 128, 0, 8, 28, 56, 80, 108, 136, 0, 4, 8, 16, 24, 32, 16, 0, 128, 192, 0, 8, 16, 28, 40, 56, 76, 88, 108, 128, 0, 0, 4, 4, 12, 20, 28, 44, 24, 32, 48, 60, 76, 92, 108, 124, 24, 44, 72, 88, 108, 136, 168, 200, 0, 0, 4, 12, 24, 44, 64, 88, 16, 24, 40, 56, 64, 80, 96, 112, 128, 148, 4, 20, 40, 64, 96, 136, 68, 84, 100, 116, 136, 164, 192, 224, 112, 144, 172, 196, 224, 252, 252, 252, 108, 132, 160, 184, 212, 220, 232, 240, 252, 252, 96, 108, 120, 132, 160, 192, 220, 252, 52, 52, 52, 88, 124, 160, 200, 236, 112, 140, 168, 196, 224, 248, 255, 252, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 4, 0, 48, 100, 152, 88, 104, 124, 140, 164, 188, 216, 224, 52, 64, 76, 92, 252, 248, 236, 216, 172, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 8, 24, 52, 84, 126, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 112, 116, 120, 124, 128, 144, 168, 252, 164, 140, 255]
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
def palette_dict(indices, r, g, b):
  palette_dict = {}
  for i in indices:
    key = str(hex(r[i])) + str(hex(g[i])) + str(hex(b[i]))
    palette_dict[key] = i
  return palette_dict
paldict = palette_dict(range(256), palette_r, palette_g, palette_b)

# Palette colour sets
# Color set start indices
color_set_start = [1, 16, 24, 32, 40, 50, 53, 60, 70, 80, 88, 96, 104, 112, 122, 128, 136, 144, 154, 162, 170, 178, 192, 198, 206]
# Color set length
color_set_length = [15, 8, 8, 8, 10, 3, 7, 10, 10, 8, 8, 8, 8, 10, 6, 8, 8, 10, 8, 8, 8, 14, 6, 8, 4]
color_set_dicts = []
for i in range(len(color_set_start)):
  curdict = palette_dict(range(color_set_start[i], color_set_start[i] + color_set_length[i]), palette_r, palette_g, palette_b)
  color_set_dicts.append(curdict)


# Define special palette index sets
def match_dict(indices, r, g, b):
  match_dict = {}
  for i in range(256):
    key = str(hex(r[i])) + str(hex(g[i])) + str(hex(b[i]))
    if i in indices:
      match_dict[key] = True
    else:
      match_dict[key] = False
  return match_dict
def matched_dict(match_dict, r, g, b):
  key = str(hex(r)) + str(hex(g)) + str(hex(b))
  return match_dict[key]
# 'Normal' palette entries
colors_normal = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 255]
colors_normal_matchdict = match_dict(colors_normal, palette_r, palette_g, palette_b)
# Action colours (animated palette indices)
colors_action = [227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 254]
colors_action_matchdict = match_dict(colors_action, palette_r, palette_g, palette_b)
# Special colours, do not propagate errors through these indices
colors_special = [0, 255]
colors_special_matchdict = match_dict(colors_special, palette_r, palette_g, palette_b)

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
  key = str(hex(pr)) + str(hex(pg)) + str(hex(pb))
  if (key in paldict):
    index = paldict[key]
  else :
    dist = 255 * 255 * 255
    index = 0
    for i in colors_normal:
      cd = (pr - palette_r[i]) * (pr - palette_r[i]) + (pg - palette_g[i]) * (pg - palette_g[i]) + (pb - palette_b[i]) * (pb - palette_b[i])
      if cd < dist:
        dist = cd
        index = i
  return index

def most_similar_in_color_set(pr, pg, pb, color_set):
  key = str(hex(pr)) + str(hex(pg)) + str(hex(pb))
  if (key in color_set_dicts[color_set]):
    index = color_set_dicts[color_set][key]
  else:
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
      if matched_dict(colors_special_matchdict, pr, pg, pb) == True:
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
      if donotdither.getpixel((x, y)) == 255:
        # Do not dither this pixel, just set nearest value
        res.putpixel((x, y), most_similar_in_palette(pr, pg, pb))
      else:
        pr, pg, pb = src.getpixel((x, y))
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
  if os.path.isfile(name+"_8bpp.png"):
    if os.path.getmtime(name+"_8bpp.png") > os.path.getmtime(input_file):
      do_processing = False
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