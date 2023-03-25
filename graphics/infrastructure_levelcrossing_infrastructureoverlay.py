#!/usr/bin/env python3

from PIL import Image
from PIL import ImageFilter
from random import randint
import numpy, blend_modes # For overlay blending
import glob, os, sys

if os.path.isdir("pygen") == False: os.mkdir("pygen")

verbose = True
scale = int(sys.argv[1])
tile_size = scale * 64

# Road tiles to use
road_tile_positions = [
  [66, 1, 64, 32],
  [1, 1, 64, 32],
  [66, 1, 64, 32],
  [1, 1, 64, 32]
]
# Rail tiles to use
rail_tile_positions = [
  [1, 1, 64, 32],
  [66, 1, 64, 32],
  [1, 1, 64, 32],
  [66, 1, 64, 32]
]
# Rail types to use
infrastructure_list = {
  "rail": "rail",
  "monorail": "monorail",
  "maglev": "maglev"
}
# Terrain types to use
terrain_list = {
  "arctic_grass": "arctic_grass",
  "arctic_snow": "arctic_grass",
  "tropical_grass": "tropical_grass",
  "tropical_desert": "tropical_desert",
  "temperate_grass": "temperate_grass",
  "concrete": "general_concrete"
}

def paste_to(input, ix, iy, iw, ih, output, ox, oy):
  crop = input.crop((ix * scale, iy * scale, (ix + iw) * scale, (iy + ih) * scale))
  output.paste(crop, (ox * scale, oy * scale))
  return output

def alpha_to(input1, ix1, iy1, w, h, input2, ix2, iy2):
  crop1 = input1.crop((ix1 * scale, iy1 * scale, (ix1 + w) * scale, (iy1 + h) * scale))  
  crop2 = input2.crop((ix2 * scale, iy2 * scale, (ix2 + w) * scale, (iy2 + h) * scale))
  crop = Image.alpha_composite(crop2, crop1)
  output = paste_to(crop, 0, 0, w, h, input2, ix2, iy2)
  return output  

# Output image properties
output_width = (scale + (tile_size + scale) * len(rail_tile_positions))
output_height = 0
for i in range(len(rail_tile_positions)):
  if rail_tile_positions[i][3] + 1 > output_height:
    output_height = rail_tile_positions[i][3] + 1
output_height += 1
output_height *= scale

print("Running in scale "+str(scale)+" (tile size "+str(tile_size)+")")
for terrain_key in terrain_list:
  print(" "+terrain_key)
  for infrastructure_key in infrastructure_list:
    print("  "+infrastructure_key)
    # Make image containing arranged rail background tiles
    terrain_image = Image.open(os.path.join("pygen", infrastructure_list[infrastructure_key]+"_"+terrain_list[terrain_key]+"_32bpp.png")).convert("RGBA")
    target_image = Image.new("RGBA", (output_width, output_height))
    for i in range(len(rail_tile_positions)):
      target_image = paste_to(terrain_image, rail_tile_positions[i][0], rail_tile_positions[i][1], rail_tile_positions[i][2], rail_tile_positions[i][3], target_image, i * (tile_size // scale + 1) + 1, 1)
    # Overlay road overlayalpha
    road_image = Image.open("road_overlayalpha.png").convert("RGBA")
    for i in range(len(road_tile_positions)):
      target_image = alpha_to(road_image, road_tile_positions[i][0], road_tile_positions[i][1], road_tile_positions[i][2], road_tile_positions[i][3], target_image, i * (tile_size // scale + 1) + 1, 1)
    # Overlay overlayalpha
    name_overlayalpha = infrastructure_list[infrastructure_key]+"_levelcrossing_overlayalpha.png"
    print(name_overlayalpha)
    infrastructure_alpha = Image.open(name_overlayalpha).convert("RGBA")
    target_image = Image.alpha_composite(target_image, infrastructure_alpha)
    # Overlay crossing lights
    name_overlaynormal = "levelcrossing_overlaynormal.png"
    print(name_overlaynormal)
    infrastructure_normal = Image.open(name_overlaynormal).convert("RGBA")
    target_image = Image.alpha_composite(target_image, infrastructure_normal)
    target_image.save(os.path.join("pygen", "levelcrossing_road_"+infrastructure_key+"_"+terrain_key+"_32bpp.png"))
    # Save palmask image
    blank_palmask = Image.new("RGBA", (output_width, output_height), (0, 0, 255))
    infrastructure_normal = Image.alpha_composite(blank_palmask, infrastructure_normal)
    infrastructure_normal.save(os.path.join("pygen", "levelcrossing_road_"+infrastructure_key+"_"+terrain_key+"_palmask.png"))