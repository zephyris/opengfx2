#!/usr/bin/env python3

from PIL import Image, ImageDraw
import os, sys

from tools import openttd_palettise, check_update_needed

if os.path.isdir("pygen") == False: os.mkdir("pygen")

# splits [base_name]_32bpp and [base_name]_palmask images into tiles using mapping in [tile_mask_path] image
# for example, splitting temperate iron ore mine into 16 tiles or splitting banks into 2 tiles
base_name = sys.argv[1]
tile_mask_path = sys.argv[2]

# RGB image
source_suffices = ["_32bpp.png"]
if os.path.isfile(base_name+"_palmask.png"):
  source_suffices.append("_palmask.png")
for image_index in range(len(source_suffices)):
  # check if update needed
  source_path = base_name + source_suffices[image_index]
  out_path = base_name+"_tiles"+source_suffices[image_index]
  if check_update_needed([source_path, tile_mask_path], out_path):
    source_image = Image.open(source_path).convert("RGB")
    # 8-bit indexed or grayscale image, each value indicates a subtile
    # Must be sequentially numbered, indices 1..255 represent subtiles, 0 indicates background
    # Regions should be tile_size in width, otherwise poorly defined behaviour
    tile_mask = openttd_palettise(Image.open(tile_mask_path))
    scale = int(sys.argv[3])
    tile_size = 64 * scale

    # Process source_image in rows of tile_mask height (plus scale px border)
    tile_mask_width, tile_mask_height = tile_mask.size
    for x in range(tile_mask_width):
      for y in range(tile_mask_height):
        if tile_mask.getpixel((x, y)) == 255:
          tile_mask.putpixel((x, y), 0)
    tile_mask_height = tile_mask_height - scale # Remove lower border from height

    # Find number of subtiles from brightest tile_Mask 
    tmp, tile_number = tile_mask.getextrema()
    print("Number of tiles in tile mask:", tile_number)

    # Setup output image
    source_image_width, source_image_height = source_image.size
    output_rows = (source_image_height - 1) // (tile_mask_height - 1)
    output_image = Image.new("RGB", ((tile_number * (64 + 1) + 1) * scale, tile_mask_height * output_rows + scale), (255, 255, 255))

    # Loop through rows
    for row in range(output_rows):
      # Loop through tiles
      print(" Row "+str(row))
      for tile in range(tile_number):
        print("  Tile index "+str(tile))
        # Make a mask of the current index
        values = [0] * 256
        values[tile + 1] = 255
        palette = []
        for i in range(len(values)):
          palette.append(values[i])
          palette.append(values[i])
          palette.append(values[i])
        current_mask = tile_mask.copy()
        current_mask.putpalette(palette)
        current_mask = current_mask.convert("L")
        # Find top/right coordinate of mask (value 255) region
        bounds = current_mask.getbbox()
        print("   ", "Mask position  ", tile, bounds)
        # Fill background of sprite blue
        sprite_x = scale + tile * (tile_size + scale)
        sprite_y = scale + row * (tile_mask_height)
        drawing = ImageDraw.Draw(output_image)
        drawing.rectangle((sprite_x, sprite_y, sprite_x + tile_size + 1, sprite_y + tile_mask_height - 2), fill="#0000ff", outline=None)
        # Paste into output using mask
        source_x = bounds[0]
        source_y = bounds[1] + row * tile_mask_height
        print("   ", "Source position", tile, (source_x, source_y, source_x + bounds[2], source_y + bounds[3]))
        output_image.paste(source_image.crop((source_x, source_y, source_x + bounds[2] - bounds[0], source_y + bounds[3] - bounds[1])), (sprite_x, sprite_y - (bounds[3] - bounds[1]) + tile_mask_height - 1), current_mask.crop(bounds))
    output_image.save(out_path)
