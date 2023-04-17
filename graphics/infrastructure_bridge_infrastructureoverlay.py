#!/usr/bin/env python3

from PIL import Image
from PIL import ImageFilter
from random import randint
import numpy, blend_modes # For overlay blending
import glob, os, sys

from tools import check_update_needed, paste_to, overlay_bluetransp, bluewhite_to_transp, mask_image

if os.path.isdir("pygen") == False: os.mkdir("pygen")

verbose = True
scale = int(sys.argv[1])
mode = sys.argv[2]
tile_size = scale * 64

if mode == "bridges":
  # Source tile positions in infrastructure
  tile_positions = [
    [1, 1, 64, 32],
    [66, 1, 64, 32],
  ]
  # vertical offset for infrastructure tiles
  v_offs = [81, 81]
  # Infrastructure sprites to use
  infrastructure_list = {
    "road": "road_general_bridge_32bpp.png",
    "rail": "rail_general_bridge_32bpp.png",
    "monorail": "monorail_general_bridge_32bpp.png",
    "maglev": "maglev_general_bridge_32bpp.png"
  }
  # Terrain sprites to use
  bridge_list = {
    "template": "bridge_template_32bpp.png",
    "deckonly": "bridge_deckonly_32bpp.png",
    "steelfast": "bridge_steelfast_32bpp.png",
    "steelslow": "bridge_steelslow_32bpp.png",
    "wood": "bridge_wood_32bpp.png",
    "girder": "bridge_girder_32bpp.png",
    "suspension": "bridge_suspension_32bpp.png",
    "tubular": "bridge_tubular_32bpp.png"
  }
  bridgemask = "bridge_deckmask.png"
  composite_over = True
elif mode == "railramps" or mode == "roadramps":
  # Source tile positions in infrastructure
  if mode == "railramps":
    tile_positions = [
      [66, 1, 64, 32],
      [66, 1, 64, 32],
      [1, 1, 64, 32],
      [1, 1, 64, 32],
      [1301, 1, 64, 39],
      [1431, 1, 64, 23],
      [1496, 1, 64, 39],
      [1366, 1, 64, 23]
    ]
    # Infrastructure sprites to use
    infrastructure_list = {
      "rail": "rail_general_bridge_32bpp.png",
      "monorail": "monorail_general_bridge_32bpp.png",
      "maglev": "maglev_general_bridge_32bpp.png"
    }
  elif mode == "roadramps":
    # Tile poisitions
    tile_positions = [
      [66, 1, 64, 32],
      [66, 1, 64, 32],
      [1, 1, 64, 32],
      [1, 1, 64, 32],
      [976, 1, 64, 39],
      [1106, 1, 64, 23],
      [1171, 1, 64, 39],
      [1041, 1, 64, 23]
    ]
    # Infrastructure sprites to use
    infrastructure_list = {
      "road": "road_general_bridge_32bpp.png"
    }
  # vertical offset for infrastructure tiles
  v_offs = [16, 24, 16, 24, 16, 24, 16, 24]
  # Terrain sprites to use
  bridge_list = {
    "ramps_general": "bridgeramps_general_32bpp.png",
    "ramps_wood": "bridgeramps_wood_32bpp.png",
  }
  bridgemask = "bridgeramps_deckmask.png"
  composite_over = False

print("Running in scale "+str(scale)+" (tile size "+str(tile_size)+") "+mode+" mode")
for bridge_key in bridge_list:
  print(" "+bridge_key)
  for infrastructure_key in infrastructure_list:
    print("  "+infrastructure_key)
    # Open bridge image
    bridge_image = Image.open(bridge_list[bridge_key])
    # Open bridge image
    bridgemask_image = Image.open(bridgemask)
    # Make images containing arranged infrastructure sprites and arranged mask sprites
    infrastructure_image = Image.open(os.path.join("..", "..", "infrastructure", str(tile_size), "pygen", infrastructure_list[infrastructure_key]))
    infrastructure_target_image = Image.new("RGBA", bridge_image.size, (255, 255, 255, 255))
    mask_target_image = Image.new("RGBA", bridge_image.size, (255, 255, 255, 255))
    for i in range(int((bridge_image.size[0] - 1) / (tile_size + 1))):
      infrastructure_target_image = paste_to(infrastructure_image, tile_positions[i % len(tile_positions)][0], tile_positions[i % len(tile_positions)][1], tile_positions[i % len(tile_positions)][2], tile_positions[i % len(tile_positions)][3], infrastructure_target_image, i * (tile_size // scale + 1) + 1, 1 + v_offs[i % len(tile_positions)], scale)
      mask_target_image = paste_to(bridgemask_image, 1 + (i % len(tile_positions)) * (tile_size + 1), 0, tile_size, bridge_image.size[1], mask_target_image, i * (tile_size // scale + 1) + 1, 0, scale)
    target_image = mask_image(infrastructure_target_image, mask_target_image)
    # Overlay for 32bpp image
    if composite_over:
      target_image = overlay_bluetransp(bridge_image, target_image)
    else:
      target_image = overlay_bluetransp(target_image, bridge_image)
    # Save 32bpp image
    target_image.save(os.path.join("pygen", bridge_key+"_"+infrastructure_key+"_32bpp.png"))
    # Load palmask image, if it exists
    bridge_palmask_path = os.path.join(infrastructure_list[infrastructure_key][:len("_32bpp.png")]+"_palmask.png")
    if os.path.isfile(bridge_palmask_path):
      bridge_image_palmask = Image.open()
      target_image_palmask.putpalette(palimg.getpalette())
      target_image_palmask.save(os.path.join("pygen", bridge_key+"_"+infrastructure_key+"_palmask.png"))
