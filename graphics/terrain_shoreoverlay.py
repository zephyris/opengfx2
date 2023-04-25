#!/usr/bin/env python3

from PIL import Image
from PIL import ImageFilter
from random import randint
import numpy, blend_modes # For overlay blending
import glob, os, sys

from tools import openttd_palettise, openttd_palette_image, check_update_needed

if os.path.isdir("pygen") == False: os.mkdir("pygen")

verbose = True
scale = int(sys.argv[1])
tile_size = scale * 64

palimage=openttd_palette_image()

# Terrain sprites to use
terrain_list = {
  "arctic_grass": "arctic_groundtiles_32bpp.png",
  "arctic_snow": "arctic_groundtiles_snow_32bpp.png",
  "tropical_grass": "tropical_groundtiles_32bpp.png",
  "tropical_desert": "tropical_groundtiles_desert_32bpp.png",
  "temperate_grass": "temperate_groundtiles_32bpp.png",
  "general_concrete": "general_concretetiles_32bpp.png"
}

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

print("Running in scale "+str(scale)+" (tile size "+str(tile_size)+")")
for terrain_key in terrain_list:
  print(" "+terrain_key)
  terrain_image_path = terrain_list[terrain_key]
  shoreline_overlay_path = "shorelines_overlaynormal.png"
  shoreline_shading_path = "shorelines_overlayshading.png"
  output_main_path = os.path.join("pygen", terrain_key+"_shoretiles_palmask.png")
  output_palmask_path = os.path.join("pygen", terrain_key+"_shoretiles_32bpp.png")
  if check_update_needed([terrain_image_path, shoreline_overlay_path, shoreline_shading_path], output_main_path):
    terrain_image = Image.open(terrain_image_path).convert("RGB")
    shore_image = Image.open(shoreline_overlay_path)
    shore_image = openttd_palettise(shore_image)
    width, height = shore_image.size
    target_image = terrain_image.crop((0, 0, width, height))
    # Save shore_image as palmask image
    shore_image.save(output_main_path)
    # Overlay shading, if it exists
    target_image = target_image.convert("RGBA")
    if os.path.isfile(shoreline_shading_path):
      shoreline_shading = Image.open(shoreline_shading_path).convert("RGBA")
      target_image = overlay_simple(target_image, shoreline_shading, 192/255)
    # Overlay shore_image onto target_image using blue as transparent
    v = [255] * 256
    v[0] = 0
    mask_palimg = palette_image(v, v, v)
    shore_mask = shore_image.copy()
    shore_mask.putpalette(mask_palimg.getpalette())
    shore_mask = shore_mask.convert("L")
    target_image.paste(shore_image, (0, 0), shore_mask)
    # Save
    target_image.save(output_palmask_path)