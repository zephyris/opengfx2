#!/usr/bin/env python3

from PIL import Image
import glob, os, sys

from tools import check_update_needed, blue_to

if os.path.isdir("pygen") == False: os.mkdir("pygen")

verbose = True
scale = int(sys.argv[1])

tile_width = 48
tile_height = 32

cursor_list = {
  "default": "classic_yellow",
  "opengfx_yellow": "opengfx_yellow"
}

xoffset_list = {
  "classic_yellow": 0,
  "opengfx_yellow": -8
}

print("Running in scale "+str(scale)+" mode")
for cursor_key in cursor_list:
  cursor_name = cursor_list[cursor_key]+"_cursor.png"
  icon_name = "cursor_icons.png"
  output_name = os.path.join("pygen", cursor_key+"_32bpp.png")
  if check_update_needed([cursor_name, icon_name], output_name):
    # open background icons and cursor to overlay
    icons_image = Image.open(icon_name).convert("RGB")
    cursor_image = Image.open(cursor_name)
    w, h = icons_image.size
    target_image = Image.new(mode="RGB", size=icons_image.size, color=(0, 0, 255))
    # for every icon in matrix of icons
    for x in range(int(w / ((tile_width + 1) * scale))):
      for y in range(int(h / ((tile_height + 1) * scale))):
        if x != 1 or y != 0: # not the special (1, 0) sleepy icon!
          r, g, b = icons_image.getpixel(((x * (tile_width + 1) + 1) * scale, (y * (tile_height + 1) + 1) * scale))
          if r != 255 or g != 255 or b != 255: # if not a white, ie. not an icon, pixel
            print(x, y)
            icons_image = blue_to(cursor_image, 0, 0, tile_width, tile_height, icons_image, x * (tile_width + 1) + 1, y * (tile_height + 1) + 1, scale)
    # Save 32bpp image
    icons_image.save(output_name)
