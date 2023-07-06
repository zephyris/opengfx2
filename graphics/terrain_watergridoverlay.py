#!/usr/bin/env python3

from PIL import Image
from PIL import ImageFilter
from random import randint
import numpy, blend_modes # For overlay blending
import glob, os, sys

from tools import check_update_needed, blue_to, paste_to

if os.path.isdir("pygen") == False: os.mkdir("pygen")

verbose = True
scale = int(sys.argv[1])
tile_size = scale * 64

mode = sys.argv[2]

# Terrain sprites to use
if mode == "shore":
  terrain_list = {
    "arctic_grass_gridline_shoretiles": os.path.join("pygen", "arctic_grass_gridline_shoretiles_32bpp.png"),
    "arctic_snow_gridline_shoretiles": os.path.join("pygen", "arctic_snow_gridline_shoretiles_32bpp.png"),
    "temperate_grass_gridline_shoretiles": os.path.join("pygen", "temperate_grass_gridline_shoretiles_32bpp.png"),
    "tropical_grass_gridline_shoretiles": os.path.join("pygen", "tropical_grass_gridline_shoretiles_32bpp.png"),
    "tropical_desert_gridline_shoretiles": os.path.join("pygen", "tropical_desert_gridline_shoretiles_32bpp.png")
  }
  palmask_path = "shorelines_overlaynormal.png"
  gridline_overlay_path = "shorelines_cornermarkers.png"
elif mode == "water":
  terrain_list = {
    "universal_watertile": "universal_watertile_32bpp.png",
    "universal_watertiles": "universal_watertiles_32bpp.png",
    "universal_rivertiles": "universal_rivertiles_32bpp.png",
  }
  palmask_paths = {
    "universal_watertile": "universal_watertile_palmask.png",
    "universal_watertiles": "universal_watertiles_palmask.png",
    "universal_rivertiles": "universal_rivertiles_palmask.png",
  }
  gridline_overlay_path = "watertiles_cornermarkers.png"
elif mode == "shoretoyland":
  terrain_list = {
    "toyland_grass_gridline_shoretiles": os.path.join("pygen", "toyland_grass_gridline_shoretiles_32bpp.png")
  }
  palmask_path = "shorelines_toyland_overlaynormal.png"
  gridline_overlay_path = "shorelines_toyland_cornermarkers.png"
elif mode == "watertoyland":
  terrain_list = {
    "toyland_watertile": "toyland_watertile_32bpp.png",
    "toyland_watertiles": "toyland_watertiles_32bpp.png",
    "toyland_rivertiles": "universal_rivertiles_32bpp.png",
  }
  palmask_paths = {
    "toyland_watertile": "toyland_watertile_palmask.png",
    "toyland_watertiles": "toyland_watertiles_palmask.png",
    "toyland_rivertiles": "universal_rivertiles_palmask.png",
  }
  gridline_overlay_path = "toyland_watertiles_cornermarkers.png"

print("Running in scale "+str(scale)+" (tile size "+str(tile_size)+")")
for terrain_key in terrain_list:
  print("  "+terrain_key)
  terrain_image_path = terrain_list[terrain_key]
  output_grid_path = os.path.join("pygen", terrain_key+"_gridline_32bpp.png")
  if mode != "shore" and mode != "shoretoyland":
    palmask_path = palmask_paths[terrain_key]
  output_gridpalmask_path = os.path.join("pygen", terrain_key+"_gridline_palmask.png")
  if check_update_needed([terrain_image_path, palmask_path, gridline_overlay_path], output_grid_path):
    terrain_image = Image.open(terrain_list[terrain_key]).convert("RGB")
    palmask_image = Image.open(palmask_path).convert("RGB")
    target_w, target_h = terrain_image.size
    target_image = terrain_image.crop((0, 0, target_w, target_h)).convert("RGB")
    target_palmask_image = palmask_image.crop((0, 0, target_w, target_h)).convert("RGB")
    # Overlay gridlines
    gridline_image = Image.open(gridline_overlay_path).convert("RGB")
    source_w, source_h = gridline_image.size
    source_h -= scale
    gridline_overlay = target_image.copy()
    for i in range(0, int(target_h / source_h) + 1):
      gridline_overlay = paste_to(gridline_image, 0, 0, target_w, source_h, gridline_overlay, 0, i * source_h, scale)
    target_image = blue_to(gridline_overlay, 0, 0, target_w, target_h, target_image, 0, 0, scale)
    target_palmask_image = blue_to(gridline_overlay, 0, 0, target_w, target_h, target_palmask_image, 0, 0, scale)
    # Save
    target_image.save(output_grid_path)
    target_palmask_image.save(output_gridpalmask_path)
