#!/usr/bin/env python3

# Bug: Why does tools openttd_palettise behave weird?

from PIL import Image
import glob, os, sys

from tools import openttd_palette, check_update_needed

def strict_convert(source):
  """
  Convert an image to an 8-bit palette image with the OpenTTD Windows palette. Converts non-matching pixels to index zero, does not do dithering.
  :param source: Input image, will be treated as RGB.
  :return: Image converted to the OpenTTD palette
  """

  r = openttd_palette["r"]
  g = openttd_palette["g"]
  b = openttd_palette["b"]

  source = source.convert("RGB")
  target = Image.new("P", source.size)
  palette_dict = {}
  palette = []
  for i in range(len(r)):
    key = str(hex(r[i])) + str(hex(g[i])) + str(hex(b[i]))
    palette_dict[key] = i
    palette.append(r[i])
    palette.append(g[i])
    palette.append(b[i])
  target.putpalette(palette)
  for x in range(source.size[0]):
    for y in range(source.size[1]):
      pr, pg, pb = source.getpixel((x, y))
      key = str(hex(pr)) + str(hex(pg)) + str(hex(pb))
      if key in palette_dict:
        target.putpixel((x, y), palette_dict[key])
      else:
        target.putpixel((x, y), 0)
  return target

def strict_convert_directory(base_path):
  suffix = "_32bpp.png";
  print("Converting to 8-bit")
  for input_file in glob.glob(os.path.join(base_path, "*"+suffix)):
    name = input_file[:-len(suffix)]
    if check_update_needed([name+"_32bpp.png"], name+"_8bpp.png") or os.path.getmtime(__file__) > os.path.getmtime(name+"_8bpp.png"):
      print(" "+name)
      with Image.open(input_file) as image:
        name = input_file[:-len(suffix)]
        image_8bpp = strict_convert(image);
        image_8bpp.save(os.path.join(base_path, name+"_8bpp.png"), "PNG")

if __name__ == '__main__':
  if len(sys.argv) < 2:
    strict_convert_directory(".")
  else:
    strict_convert_directory(sys.argv[1])
