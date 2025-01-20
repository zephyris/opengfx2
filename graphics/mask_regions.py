#!/usr/bin/env python3

from PIL import Image, ImageDraw
import os, sys

from tools import openttd_palettise, check_update_needed

def mask_regions(base_name, region_mask_path, scale, verbose=True):
  print("Masking regions in", base_name)
  base_path = os.path.dirname(base_name)
  if os.path.isdir(os.path.join(base_path, "pygen")) == False: os.mkdir(os.path.join(base_path, "pygen"))

  # splits [base_name]_32bpp and [base_name]_palmask images into tiles using mapping in [region_mask_path] image
  # for example, splitting back wall from depot sprites or splitting far side from tunnel sprites

  # RGB image
  source_suffices = ["_32bpp.png"]
  if os.path.isfile(base_name+"_palmask.png"):
    source_suffices.append("_palmask.png")
  for image_index in range(len(source_suffices)):
    # check if update needed
    source_path = base_name + source_suffices[image_index]
    out_path = base_name+"_regions"+source_suffices[image_index]
    if check_update_needed([__file__, source_path, region_mask_path], out_path):
      print("Generating", os.path.basename(out_path))
      source_image = Image.open(source_path).convert("RGB")
      # 8-bit indexed or grayscale image, each value indicates a region
      # Must be sequentially numbered, indices 1..255 represent subtiles, 0 indicates background
      region_mask = openttd_palettise(Image.open(region_mask_path))
      # infer tile width from source image, 1 column with scale-wide white border on left and right
      tile_size = source_image.width - scale * 2
      # infer tile height from non-white pixels in second pixel column
      tile_height = 0
      while tile_height < source_image.height:
        if source_image.getpixel((scale, tile_height + scale)) == (255, 255, 255):
          break
        tile_height += 1
      # round height to multiple of scale
      tile_height = (tile_height // scale) * scale
      print("  ", "Tile size", tile_size, ",", tile_height)

      # Pre-process masks to set index 255 pixels to index 0
      region_mask_width, region_mask_height = region_mask.size
      for x in range(region_mask_width):
        for y in range(region_mask_height):
          if region_mask.getpixel((x, y)) == 255:
            region_mask.putpixel((x, y), 0)

      # Find number of subregions from brightest region_mask, this will define number of colums in the output spritesheet
      tmp, region_number = region_mask.getextrema()
      print("  ", "Number of regions in region mask:", region_number)

      # Setup output image
      source_image_width, source_image_height = source_image.size
      output_rows = (source_image_height - scale) // tile_height
      print("  ", "Output columns and rows", region_number, ",", output_rows)
      output_image = Image.new("RGB", ((region_number * (tile_size + scale) + scale), (tile_height + scale) * output_rows + scale), (255, 255, 255))

      for tile in range(region_number):
        print("  Region index "+str(tile))
        # Make a mask of the current index
        values = [0] * 256
        values[tile + 1] = 255
        palette = []
        for i in range(len(values)):
          palette.append(values[i])
          palette.append(values[i])
          palette.append(values[i])
        current_mask = region_mask.copy()
        current_mask.putpalette(palette)
        current_mask = current_mask.convert("L")
        # Fill background of sprite blue
        drawing = ImageDraw.Draw(output_image)
        for row in range(output_rows):
          blue_x = scale + tile * (tile_size + scale)
          blue_y = scale + row * (tile_height + scale)
          blue_w = tile_size
          blue_h = tile_height + scale - 1
          drawing.rectangle((blue_x, blue_y, blue_x + blue_w - 1, blue_y + blue_h - 1), fill="#0000ff", outline=None)
          # Paste sprite into output using mask
          bounds = scale, scale + row * (tile_height + scale), scale + tile_size, scale + row * (tile_height + scale) + tile_height + scale
          print("   ", "Mask position  ", tile, bounds)
          target_bounds = bounds[0] + tile * (tile_size + scale), bounds[1], bounds[2] + tile * (tile_size + scale), bounds[3]
          print("   ", "Target position", tile, target_bounds)
          output_image.paste(source_image.crop(bounds), target_bounds, current_mask.crop(bounds))
      output_image.save(out_path)
    else:
      print("Skipping", os.path.basename(out_path))

if __name__ == "__main__":
  mask_regions(sys.argv[1], sys.argv[2], int(sys.argv[3]))
