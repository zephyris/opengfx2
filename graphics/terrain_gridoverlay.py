#!/usr/bin/env python3

from PIL import Image
from PIL import ImageFilter
from random import randint
import numpy, blend_modes # For overlay blending
import glob, os, sys

from tools import check_update_needed, blend_overlay, paste_to

if os.path.isdir("pygen") == False: os.mkdir("pygen")

verbose = True
scale = int(sys.argv[1])
tile_size = scale * 64

# Terrain sprites to use
terrain_list = {
	"arctic_groundtiles": "arctic_groundtiles_32bpp.png",
  "arctic_groundtiles_rocks": "arctic_groundtiles_rocks_32bpp.png",
  "arctic_groundtiles_rough": "arctic_groundtiles_rough_32bpp.png",
	"arctic_groundtiles_snow": "arctic_groundtiles_snow_32bpp.png",
  "arctic_groundtiles_snowtransition": "arctic_groundtiles_snowtransition_32bpp.png",
	"tropical_groundtiles": "tropical_groundtiles_32bpp.png",
  "tropical_groundtiles_rocks": "tropical_groundtiles_rocks_32bpp.png",
  "tropical_groundtiles_rough": "tropical_groundtiles_rough_32bpp.png",
	"tropical_groundtiles_desert": "tropical_groundtiles_desert_32bpp.png",
  "tropical_groundtiles_deserttransition": "tropical_groundtiles_deserttransition_32bpp.png",
  "tropical_groundtiles_snowtransition": "tropical_groundtiles_snowtransition_32bpp.png",
	"temperate_groundtiles": "temperate_groundtiles_32bpp.png",
  "temperate_groundtiles_rocks": "temperate_groundtiles_rocks_32bpp.png",
  "temperate_groundtiles_rough": "temperate_groundtiles_rough_32bpp.png",
  "temperate_groundtiles_snowtransition": "temperate_groundtiles_snowtransition_32bpp.png",
  "toyland_groundtiles": "toyland_groundtiles_32bpp.png",
  "toyland_groundtiles_rocks": "toyland_groundtiles_rocks_32bpp.png",
  "toyland_groundtiles_rough": "toyland_groundtiles_rough_32bpp.png",
  "toyland_shoretiles": "toyland_shoretiles_32bpp.png",
  "toyland_yellowtiles": "toyland_yellowtiles_32bpp.png"
}

gridline_opacity = 40/255

print("Running in scale "+str(scale)+" (tile size "+str(tile_size)+")")
for terrain_key in terrain_list:
  print("  "+terrain_key)
  terrain_image_path = terrain_list[terrain_key]
  gridline_overlay_path = "groundtiles_gridlines.png"
  output_grid_path = os.path.join("pygen", terrain_key+"_gridline_32bpp.png")
  output_nogrid_path = os.path.join("pygen", terrain_key+"_nogridline_32bpp.png")
  if check_update_needed([terrain_image_path, gridline_overlay_path], output_grid_path):
    terrain_image = Image.open(terrain_list[terrain_key]).convert("RGB")
    terrain_image.save(output_nogrid_path)
    target_w, target_h = terrain_image.size
    target_image = terrain_image.crop((0, 0, target_w, target_h)).convert("RGBA")
    # Overlay gridlines
    gridline_image = Image.open(gridline_overlay_path).convert("RGBA")
    source_w, source_h = gridline_image.size
    source_h -= scale
    gridline_overlay = target_image.copy()
    for i in range(0, int(target_h / source_h) + 1):
      gridline_overlay = paste_to(gridline_image, 0, 0, target_w, source_h, gridline_overlay, 0, i * source_h, scale)
    target_image = blend_overlay(target_image, gridline_overlay, gridline_opacity)
    # Save
    target_image.save(output_grid_path)
