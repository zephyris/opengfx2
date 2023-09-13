#!/usr/bin/env python3

from PIL import Image
from PIL import ImageFilter
from random import randint
import numpy, blend_modes # For overlay blending
import glob, os, sys

from tools import check_update_needed, blend_overlay, paste_to, alpha_to, blue_to, colour_to, blue_to_alpha

if os.path.isdir("pygen") == False: os.mkdir("pygen")

verbose = True
scale = int(sys.argv[1])
mode = sys.argv[2]
tile_size = scale * 64

if mode == "rail":
  # Infrastructure sprites to use
  infrastructure_list = {
    "rail": "rail",
    "monorail": "monorail",
    "maglev": "maglev"
  }
elif mode == "rail_toyland":
  # Infrastructure sprites to use
  infrastructure_list = {
    "rail": "rail_toyland",
    "monorail": "monorail_toyland",
    "maglev": "maglev_toyland"
  }
elif mode == "road":
  # Infrastructure sprites to use
  infrastructure_list = {
    "road": "road"
  }
elif mode == "road_toyland":
  # Infrastructure sprites to use
  infrastructure_list = {
    "road": "road_toyland"
  }
elif mode == "terrain":
  # Infrastructure sprites to use
  infrastructure_list = {
    "none": "none"
  }
# Terrain sprites to use
terrain_tile_positions = [
  [719, 1, 64, 39],
  [959, 1, 64, 39],
  [479, 1, 64, 24],
  [241, 1, 64, 24]
]
# Terrain extra offset
terrain_tile_voffs = [0, 0, -7, -7]
if mode == "rail_toyland" or mode == "road_toyland":
  terrain_list = {
    "toyland_grass": os.path.join("pygen", "toyland_groundtiles_gridline_32bpp.png"),
    "toyland_grass_nogridline": os.path.join("pygen", "toyland_groundtiles_nogridline_32bpp.png")
  }
elif mode == "rail" or mode == "road":
  # Terrain list to process
  terrain_list = {
    "arctic_grass": os.path.join("pygen", "arctic_groundtiles_gridline_32bpp.png"),
    "arctic_snow": os.path.join("pygen", "arctic_groundtiles_snow_gridline_32bpp.png"),
    "tropical_grass": os.path.join("pygen", "tropical_groundtiles_gridline_32bpp.png"),
    "tropical_desert": os.path.join("pygen", "tropical_groundtiles_desert_gridline_32bpp.png"),
    "temperate_grass": os.path.join("pygen", "temperate_groundtiles_gridline_32bpp.png"),
    "arctic_grass_nogridline": os.path.join("pygen", "arctic_groundtiles_nogridline_32bpp.png"),
    "arctic_snow_nogridline": os.path.join("pygen", "arctic_groundtiles_snow_nogridline_32bpp.png"),
    "tropical_grass_nogridline": os.path.join("pygen", "tropical_groundtiles_nogridline_32bpp.png"),
    "tropical_desert_nogridline": os.path.join("pygen", "tropical_groundtiles_desert_nogridline_32bpp.png"),
    "temperate_grass_nogridline": os.path.join("pygen", "temperate_groundtiles_nogridline_32bpp.png")
  }
else:
  # Terrain list to process
  terrain_list = {
    "arctic_grass": os.path.join("pygen", "arctic_groundtiles_gridline_32bpp.png"),
    "arctic_snow": os.path.join("pygen", "arctic_groundtiles_snow_gridline_32bpp.png"),
    "tropical_grass": os.path.join("pygen", "tropical_groundtiles_gridline_32bpp.png"),
    "tropical_desert": os.path.join("pygen", "tropical_groundtiles_desert_gridline_32bpp.png"),
    "temperate_grass": os.path.join("pygen", "temperate_groundtiles_gridline_32bpp.png"),
    "toyland_grass": os.path.join("pygen", "toyland_groundtiles_gridline_32bpp.png"),
    "arctic_grass_nogridline": os.path.join("pygen", "arctic_groundtiles_nogridline_32bpp.png"),
    "arctic_snow_nogridline": os.path.join("pygen", "arctic_groundtiles_snow_nogridline_32bpp.png"),
    "tropical_grass_nogridline": os.path.join("pygen", "tropical_groundtiles_nogridline_32bpp.png"),
    "tropical_desert_nogridline": os.path.join("pygen", "tropical_groundtiles_desert_nogridline_32bpp.png"),
    "temperate_grass_nogridline": os.path.join("pygen", "temperate_groundtiles_nogridline_32bpp.png"),
    "toyland_grass_nogridline": os.path.join("pygen", "toyland_groundtiles_nogridline_32bpp.png")
  }
# Infrastructure sprites to use
if mode == "terrain":
  infrastructure_tile_positions = [
    [1, 1, 64, 31],
    [1, 1, 64, 31],
    [1, 1, 64, 31],
    [1, 1, 64, 31]
  ]
else:
  infrastructure_tile_positions = [
    [1, 1, 64, 31],
    [66, 1, 64, 31],
    [1, 1, 64, 31],
    [66, 1, 64, 31]
  ]
col_width = 64
row_height = 64

# Output image properties
output_width = ((col_width + 1) * 2 + 1) * scale
output_height = ((row_height + 1) * len(infrastructure_tile_positions) + 1) * scale 

print("Running in scale "+str(scale)+" (tile size "+str(tile_size)+") "+mode+" mode")
for terrain_key in terrain_list:
  print(" "+terrain_key)
  for infrastructure_key in infrastructure_list:
    terrain_image_path = os.path.join("..", "..", "..", "terrain", str(tile_size), terrain_list[terrain_key])
    if mode == "terrain":
      infrastructure_image_path = terrain_image_path
    else:
      infrastructure_image_path = os.path.join("..", "..", "..", "infrastructure", str(tile_size), infrastructure_list[infrastructure_key]+"_overlayalpha.png")
    if terrain_key == "arctic_snow":
      name_overlay = os.path.join("pygen", infrastructure_key+"tunnels_snow_regions_32bpp.png")
    else:
      name_overlay = os.path.join("pygen", infrastructure_key+"tunnels_regions_32bpp.png")
    name_overlayshading = infrastructure_list[infrastructure_key]+"tunnels_regions_overlayshading.png"
    output_normal_path = os.path.join("pygen", "tunnels_"+infrastructure_key+"_"+terrain_key+"_32bpp.png")
    # Check if update needed
    if check_update_needed([terrain_image_path, infrastructure_image_path, name_overlay, name_overlayshading], output_normal_path):
      # Make image containing arranged infrastructure on and slope backgrounds
      terrain_image = Image.open(terrain_image_path)
      infrastructure_image = blue_to_alpha(Image.open(infrastructure_image_path))
      target_image = Image.new("RGBA", (output_width, output_height), (255, 255, 255, 255))
      for i in range(len(infrastructure_tile_positions)):
        target_image = paste_to(terrain_image, terrain_tile_positions[i][0], terrain_tile_positions[i][1], terrain_tile_positions[i][2], terrain_tile_positions[i][3], target_image, 0 * (tile_size // scale + 1) + 1, i * (tile_size // scale + 1) + (tile_size - terrain_tile_positions[i][3] + terrain_tile_voffs[i]) * scale, scale)
        target_image = paste_to(terrain_image, terrain_tile_positions[i][0], terrain_tile_positions[i][1], terrain_tile_positions[i][2], terrain_tile_positions[i][3], target_image, 1 * (tile_size // scale + 1) + 1, i * (tile_size // scale + 1) + (tile_size - terrain_tile_positions[i][3] + terrain_tile_voffs[i]) * scale, scale)
        target_image = alpha_to(infrastructure_image, infrastructure_tile_positions[i][0], infrastructure_tile_positions[i][1], infrastructure_tile_positions[i][2], infrastructure_tile_positions[i][3], target_image, 1 * (tile_size // scale + 1) + 1, i * (tile_size // scale + 1) + (tile_size - infrastructure_tile_positions[i][3]) * scale, scale)
        # Overlay each infrastructure set
        print("  "+infrastructure_key)
        # Overlay overlay_alpha
        print(name_overlay)
        overlay_image = Image.open(name_overlay).convert("RGBA")
        target_image = colour_to(overlay_image, 0, 0, output_width, output_height, target_image, 0, 0, scale, 252, 0, 255) # Warning magenta (255, 0, 255) gets change to 252, 0, 255 by building_shapeproc
        # Overlay overlayshading, if it exists
        if os.path.isfile(name_overlayshading):
          print(name_overlayshading)
          overlay_image = Image.open(name_overlayshading).convert("RGBA")
          target_image = blend_overlay(target_image, overlay_image, 1.0)
        # Save 32bpp image
        target_image.save(output_normal_path)
