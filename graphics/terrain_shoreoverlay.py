#!/usr/bin/env python3

from PIL import Image
from PIL import ImageFilter
from random import randint
import numpy, blend_modes # For overlay blending
import glob, os, sys

from tools import openttd_palettise

if os.path.isdir("pygen") == False: os.mkdir("pygen")

verbose = True
scale = int(sys.argv[1])
tile_size = scale * 64

# OpenTTD DOS palette, RGB values
palette_r = [0,16,32,48,64,80,100,116,132,148,168,184,200,216,232,252,52,68,88,108,132,156,176,204,48,64,80,96,120,148,176,204,72,88,104,124,152,184,212,244,64,88,112,136,160,188,204,220,236,252,252,252,252,76,96,116,136,156,176,196,68,96,128,156,184,212,232,252,252,252,32,64,84,108,128,148,168,184,196,212,8,16,32,48,64,84,104,128,28,44,60,80,104,128,152,180,16,32,56,76,96,120,152,184,32,56,72,88,104,124,140,160,76,96,116,136,164,184,204,212,224,236,80,100,120,140,160,184,36,48,64,80,100,132,172,212,40,64,88,104,120,140,160,188,0,0,0,0,0,24,56,88,128,188,16,24,40,52,80,116,156,204,172,212,252,252,252,252,252,252,72,92,112,140,168,200,208,232,60,92,128,160,196,224,252,252,252,252,252,252,252,252,204,228,252,252,252,252,8,12,20,28,40,56,72,100,92,108,124,144,224,200,180,132,88,244,245,246,247,248,249,250,251,252,253,254,255,76,108,144,176,210,252,252,252,252,252,252,252,64,255,48,64,80,255,32,36,40,44,48,72,100,216,96,68,255]
palette_g = [0,16,32,48,64,80,100,116,132,148,168,184,200,216,232,252,60,76,96,116,140,160,184,208,44,60,76,92,120,148,176,204,44,60,80,104,132,160,188,220,0,4,16,32,56,84,104,132,156,188,208,232,252,40,60,88,116,136,156,180,24,44,68,96,120,156,184,212,248,252,4,20,28,44,56,72,92,108,128,148,52,64,80,96,112,132,148,168,52,68,88,104,124,148,176,204,52,72,96,116,136,164,192,220,24,28,40,52,64,84,108,128,40,52,68,84,96,112,128,148,168,188,28,40,56,76,100,136,40,52,64,80,100,132,172,212,20,44,64,76,88,104,136,168,24,36,52,72,96,120,144,168,196,224,64,80,96,112,140,172,204,240,52,52,52,100,144,184,216,244,20,44,68,100,136,176,184,208,0,0,0,0,0,0,0,80,108,136,164,192,220,252,136,144,156,176,196,216,24,36,52,68,92,120,152,172,156,176,200,224,244,236,220,188,152,0,0,0,0,0,0,0,0,0,0,0,0,24,44,72,108,146,60,84,104,124,148,172,196,0,0,48,64,80,255,68,72,76,80,84,100,132,244,128,96,255]
palette_b = [255,16,32,48,64,80,100,116,132,148,168,184,200,216,232,252,72,92,112,132,152,172,196,220,4,12,20,28,64,100,132,168,4,20,44,72,92,120,148,176,4,16,32,52,76,108,124,144,164,192,0,60,128,0,8,28,56,80,108,136,0,4,8,16,24,32,16,0,128,192,0,8,16,28,40,56,76,88,108,128,0,0,4,4,12,20,28,44,24,32,48,60,76,92,108,124,24,44,72,88,108,136,168,200,0,0,4,12,24,44,64,88,16,24,40,56,64,80,96,112,128,148,4,20,40,64,96,136,68,84,100,116,136,164,192,224,112,144,172,196,224,252,252,252,108,132,160,184,212,220,232,240,252,252,96,108,120,132,160,192,220,252,52,52,52,88,124,160,200,236,112,140,168,196,224,248,255,252,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,4,0,48,100,152,88,104,124,140,164,188,216,224,52,64,76,92,252,248,236,216,172,244,245,246,247,248,249,250,251,252,253,254,255,8,24,52,84,126,0,0,0,0,0,0,0,0,0,0,0,0,0,112,116,120,124,128,144,168,252,164,140,255]
# Setup palette image, used for applying palette quickly
def palette_image(r, g, b):
	palette = []
	for i in range(len(r)):
		palette.append(r[i])
		palette.append(g[i])
		palette.append(b[i])
	#if verbose == True:
		#print("Palette:")
		#print("%d entries" % len(palette))
		#print(palette)
	palimage = Image.new('P', (256, 1))
	for x in range(256):
		palimage.putpixel((x, 0), x)
	palimage.putpalette(palette)
	return palimage
palimage=palette_image(palette_r, palette_g, palette_b)

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
	terrain_image = Image.open(terrain_list[terrain_key]).convert("RGB")
	shore_image = Image.open("shorelines_overlaynormal.png")
	shore_image = openttd_palettise(shore_image)
	width, height = shore_image.size
	target_image = terrain_image.crop((0, 0, width, height))
	# Save shore_image as palmask image
	shore_image.save(os.path.join("pygen", terrain_key+"_shoretiles_palmask.png"))
	# Overlay shading, if it exists
	target_image = target_image.convert("RGBA")
	if os.path.isfile("shorelines_overlayshading.png"):
		print("shorelines_overlayshading.png")
		shoreline_shading = Image.open("shorelines_overlayshading.png").convert("RGBA")
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
	target_image.save(os.path.join("pygen", terrain_key+"_shoretiles_32bpp.png"))