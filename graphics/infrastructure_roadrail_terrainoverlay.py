#!/usr/bin/env python3

from PIL import Image
from PIL import ImageFilter
from random import randint
import numpy, blend_modes # For overlay blending
import glob, os, sys

if os.path.isdir("pygen") == False: os.mkdir("pygen")

verbose = True
scale = int(sys.argv[1])
mode = sys.argv[2]
tile_size = scale * 64

if mode == "rail":
  # Remapping of tile positions
  tile_positions = [
    [1, 1, 64, 32],
    [1, 1, 64, 32],
    [1, 1, 64, 32],
    [1, 1, 64, 32],
    [1, 1, 64, 32],
    [1, 1, 64, 32],
    [1, 1, 64, 32],
    [1, 1, 64, 32],
    [1, 1, 64, 32],
    [1, 1, 64, 32],
    [1, 1, 64, 32],
    [1, 1, 64, 32],
    [639, 1, 64, 41],
    [321, 1, 64, 32],
    [81, 1, 64, 32],
    [161, 1, 64, 24],
    [1119, 1, 64, 32],
    [559, 1, 64, 24],
    [879, 1, 64, 32],
    [1039, 1, 64, 41],
    [959, 1, 64, 41],
    [479, 1, 64, 24],
    [241, 1, 64, 24],
    [719, 1, 64, 41],
    [1, 1, 64, 32],
    [1, 1, 64, 32]
  ]
  # Infrastructure sprites to use
  infrastructure_list = {
    "rail": "rail",
    "monorail": "monorail",
    "maglev": "maglev"
  }
  # Terrain sprites to use
  terrain_list = {
    "arctic_grass": "arctic_groundtiles_32bpp.png",
    "arctic_snow": "arctic_groundtiles_snow_32bpp.png",
    "tropical_grass": "tropical_groundtiles_32bpp.png",
    "tropical_desert": "tropical_groundtiles_desert_32bpp.png",
    "temperate_grass": "temperate_groundtiles_32bpp.png",
    "general_concrete": "general_concretetiles_32bpp.png",
    "general_bridge": "general_bridgetiles_32bpp.png"
  }
elif mode == "road" or mode == "road_noline":
  tile_positions = [
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [959, 1, 65, 41],
    [479, 1, 65, 24],
    [241, 1, 65, 24],
    [719, 1, 65, 41]
  ]
  if mode == "road":
    # Infrastructure sprites to use
    infrastructure_list = {
      "road": "road",
    }
    # Terrain sprites to use
    terrain_list = {
      "arctic_grass": "arctic_groundtiles_32bpp.png",
      "arctic_snow": "arctic_groundtiles_snow_32bpp.png",
      "temperate_grass": "temperate_groundtiles_32bpp.png",
      "general_bridge": "general_bridgetiles_32bpp.png"
    }
  if mode == "road_noline":
    # Infrastructure sprites to use
    infrastructure_list = {
      "road": "road_noline",
    }
    # Terrain sprites to use
    terrain_list = {
      "tropical_grass": "tropical_groundtiles_32bpp.png",
      "tropical_desert": "tropical_groundtiles_desert_32bpp.png"
    }
elif mode == "road_town":
  # Includes bus stops
  tile_positions = [
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [959, 1, 65, 41],
    [479, 1, 65, 24],
    [241, 1, 65, 24],
    [719, 1, 65, 41],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32],
    [1, 1, 65, 32]
  ]
  infrastructure_list = {
    "road": "road_town"
  }
  terrain_list = {
    "general_concrete": "general_concretetiles_32bpp.png"
  }

def paste_to(input, ix, iy, iw, ih, output, ox, oy):
  crop = input.crop((ix * scale, iy * scale, (ix + iw) * scale, (iy + ih) * scale))
  output.paste(crop, (ox * scale, oy * scale))
  return output

def overlay_simple(image_32bit, image_texture, opacity):
  image_width, image_height = image_32bit.size
  # Make black image for merging channels
  image_black = Image.new("L", (image_width, image_height), 0)
  image_white = Image.new("L", (image_width, image_height), 255)
  # Make sharp mask from blue and white pixels in image_32bit (only ones with b == 255)
  image_mask = Image.new("L", (image_width, image_height), 0)
  for x in range(image_width):
    for y in range(image_height):
      r, g, b, a = image_32bit.getpixel((x, y))
      if b == 255:
        image_mask.putpixel((x, y), 255)
  # Mask overlay with image_mask
  image_transparent = Image.merge("RGBA", (image_black, image_black, image_black, image_black))
  image_texture.paste(image_transparent, (0, 0), image_mask)
  # Overlay texture image
  r, g, b = image_32bit.convert("RGB").split()
  image_32bit = Image.merge("RGBA", (r, g, b, image_white))
  image_bg_arr = numpy.array(image_32bit).astype(float)
  image_fg_arr = numpy.array(image_texture).astype(float)
  image_blended_arr_float = blend_modes.overlay(image_bg_arr, image_fg_arr, opacity)
  image_blended_arr = numpy.uint8(image_blended_arr_float)
  image_out = Image.fromarray(image_blended_arr)
  return image_out

# Output image properties
output_width = (scale + (tile_size + scale) * len(tile_positions))
output_height = 0
for i in range(len(tile_positions)):
  if tile_positions[i][3] * scale + scale > output_height:
    output_height = tile_positions[i][3] * scale + scale

print("Running in scale "+str(scale)+" (tile size "+str(tile_size)+") "+mode+" mode")
for terrain_key in terrain_list:
  print(" "+terrain_key)
  # Make image containing arranged terrain backgrounds
  terrain_image = Image.open(os.path.join("..", "..", "terrain", str(tile_size), terrain_list[terrain_key]))
  target_image = Image.new("RGBA", (output_width, output_height), (255, 255, 255, 255))
  for i in range(len(tile_positions)):
    target_image = paste_to(terrain_image, tile_positions[i][0], tile_positions[i][1], tile_positions[i][2], tile_positions[i][3], target_image, i * (tile_size // scale + 1) + 1, 1)
  # Make a palmask image from terrain background palmask images, if they exists
  terrain_palmask_path = os.path.join("..", "..", "terrain", str(tile_size), terrain_list[terrain_key][:len("_32bpp.png")]+"_palmask.png")
  if os.path.isfile(terrain_palmask_path):
    terrain_image_palmask = Image.open()
    target_image_palmask = Image.new("P", (output_width, output_height), 255)
    target_image_palmask.putpalette(palimg.getpalette())
    for i in range(len(tile_positions)):
      target_image_palmask = paste_to(terrain_image_palmask, tile_positions[i][0], tile_positions[i][1], tile_positions[i][2], tile_positions[i][3], target_image_palmask,i * (tile_size // scale + 1) + 1, 1)
  for infrastructure_key in infrastructure_list:
    # Overlay each infrastructure set
    print("  "+infrastructure_key)
    output_image = target_image.copy()
    # Overlay overlay_alpha, if it exists
    name_overlayalpha = infrastructure_list[infrastructure_key]+"_overlayalpha.png"
    if os.path.isfile(name_overlayalpha):
      print(name_overlayalpha)
      infrastructure_image = Image.open(name_overlayalpha).convert("RGBA")
      output_image = Image.alpha_composite(output_image, infrastructure_image)
    # Overlay additional overlay, if it exists
    name_overlayalpha2 = infrastructure_list[infrastructure_key]+"_overlayalpha2.png"
    if os.path.isfile(name_overlayalpha2):
      print(name_overlayalpha2)
      infrastructure_image = Image.open(name_overlayalpha2).convert("RGBA")
      output_image = Image.alpha_composite(output_image, infrastructure_image)
    # Overlay overlayshading, if it exists
    name_overlayshading = infrastructure_list[infrastructure_key]+"_overlayshading.png"
    if os.path.isfile(name_overlayshading):
      print(name_overlayshading)
      infrastructure_image = Image.open(name_overlayshading).convert("RGBA")
      output_image = overlay_simple(output_image, infrastructure_image, 192/255)
    # Save 32bpp image
    output_image.save(os.path.join("pygen", infrastructure_key+"_"+terrain_key+"_32bpp.png"))
    # Save palmask image
    if os.path.isfile(terrain_palmask_path):
      target_image_palmask.save(os.path.join("pygen", infrastructure_key+"_"+terrain_key+"_palmask.png"))
