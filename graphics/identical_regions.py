#!/usr/bin/env python3

from PIL import Image
import numpy
import skimage
import os, sys

from tools import openttd_palettise, check_update_needed

# makes marked rectangular regions of a sprite sheet identical, one mask image for all _output_ images for a base name
# for example, preventing dither jitter in animation series, or making near-identical regions identical in ground tiles and similar
base_path = sys.argv[1]
suffices = ["_8bpp.png", "_bt32bpp.png", "_rm32bpp.png", "_palmask.png"]
mask_path = sys.argv[2]

# check if update needed
for suffix in suffices:
  source_path = base_path + suffix
  out_path = base_path + "_idmap" + suffix
  if os.path.isfile(source_path):
    if check_update_needed([source_path, mask_path], out_path):
      source_image = Image.open(source_path)
      # 8-bit indexed or grayscale image, each value indicates a rectangular region
      # Must be sequentially numbered, indices 1..255 represent regions to make identical, 0 indicates background
      region_mask = openttd_palettise(Image.open(mask_path))
      
      # Work in numpy/skimage
      region_mask = numpy.array(region_mask)
      region_number = numpy.max(region_mask) 
      print("Number of regions in identical region mask:", region_number)
      for i in range(region_number):
        # make mask equal to current index value
        current_mask = numpy.where(region_mask == i + 1, 255, 0)
        current_labels = skimage.measure.label(current_mask)
        mask_props = skimage.measure.regionprops_table(current_labels, properties=["bbox"])
        # master region
        refx1, refy1, refx2, refy2 = mask_props["bbox-0"][0], mask_props["bbox-1"][0], mask_props["bbox-2"][0], mask_props["bbox-3"][0]
        print("Master region:", refy1, refx1, refy2, refx2) # x/y swapped in numpy representation
        count = len(mask_props["bbox-0"])
        mask = Image.fromarray(numpy.uint8(current_mask)).crop((refy1, refx1, refy2, refx2))
        # take first entry as master copy, and do masked copy to all other positions
        for i in range(1, count):
          print("  Pasting to:", mask_props["bbox-1"][i], mask_props["bbox-0"][i], mask_props["bbox-3"][i], mask_props["bbox-2"][i])
          source_image.paste(source_image.crop((refy1, refx1, refy2, refx2)), (mask_props["bbox-1"][i], mask_props["bbox-0"][i]), mask)
      # save modified source_image as output
      source_image.save(out_path)
