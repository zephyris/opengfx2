#!/usr/bin/env python3

# Custom processing of 2x2_mallandstadia sprites
# Composites fully built mall sprite onto the ground sprites

from PIL import Image
import glob, os, sys

scale = int(sys.argv[1])

palette = Image.open("2x2_mallandstadia_shape.png")
building_pal = Image.open(os.path.join("pygen", "2x2_mallandstadia_palmask.png")).convert("RGB").quantize(palette=palette, dither=False)
ground_pal = Image.open(os.path.join("pygen", "2x2_mallandstadia_base_palmask.png")).convert("RGB").quantize(palette=palette, dither=False)
building_32bpp = Image.open(os.path.join("pygen", "2x2_mallandstadia_32bpp.png"))
ground_32bpp = Image.open(os.path.join("pygen", "2x2_mallandstadia_base_32bpp.png"))

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

def simple_overlay_texture(image1, image2, image2_pal, sx, sy, ex, ey):
	# Crop input for ovelay
	image2 = image2.crop((sx, sy, ex, ey))
	image2_pal = image2_pal.crop((sx, sy, ex, ey))
	# Make black image for merging channels
	image_black = Image.new("L", (image2_pal.size), 0)
	# Make sharp mask from indices (white = in indices)
	v = [255] * 255
	v[0] = 0
	mask_palimg = palette_image(v, v, v)
	image2_pal.putpalette(mask_palimg.getpalette())
	mask = image2_pal.convert("L")
	# Overlay image2 onto image1 using mask from image2_pal index 0
	image1.paste(image2, (sx, sy, ex, ey), mask)
	return image1

out_pal = simple_overlay_texture(ground_pal, building_pal, building_pal, 0*scale, 0*scale, 130*scale, 179*scale) 
out_32bpp = simple_overlay_texture(ground_32bpp, building_32bpp, building_pal, 0*scale, 0*scale, 130*scale, 179*scale) 

out_pal.save(os.path.join("pygen", "2x2_mallandstadia_combo_palmask.png"))
out_32bpp.save(os.path.join("pygen", "2x2_mallandstadia_combo_32bpp.png"))
