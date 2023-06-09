from PIL import Image
import numpy
import blend_modes
import os

"""
Standard OpenTTD DOS palette
"""
openttd_palette = {
  "r": [0,16,32,48,64,80,100,116,132,148,168,184,200,216,232,252,52,68,88,108,132,156,176,204,48,64,80,96,120,148,176,204,72,88,104,124,152,184,212,244,64,88,112,136,160,188,204,220,236,252,252,252,252,76,96,116,136,156,176,196,68,96,128,156,184,212,232,252,252,252,32,64,84,108,128,148,168,184,196,212,8,16,32,48,64,84,104,128,28,44,60,80,104,128,152,180,16,32,56,76,96,120,152,184,32,56,72,88,104,124,140,160,76,96,116,136,164,184,204,212,224,236,80,100,120,140,160,184,36,48,64,80,100,132,172,212,40,64,88,104,120,140,160,188,0,0,0,0,0,24,56,88,128,188,16,24,40,52,80,116,156,204,172,212,252,252,252,252,252,252,72,92,112,140,168,200,208,232,60,92,128,160,196,224,252,252,252,252,252,252,252,252,204,228,252,252,252,252,8,12,20,28,40,56,72,100,92,108,124,144,224,200,180,132,88,244,245,246,247,248,249,250,251,252,253,254,255,76,108,144,176,210,252,252,252,252,252,252,252,64,255,48,64,80,255,32,36,40,44,48,72,100,216,96,68,255],
  "g": [0,16,32,48,64,80,100,116,132,148,168,184,200,216,232,252,60,76,96,116,140,160,184,208,44,60,76,92,120,148,176,204,44,60,80,104,132,160,188,220,0,4,16,32,56,84,104,132,156,188,208,232,252,40,60,88,116,136,156,180,24,44,68,96,120,156,184,212,248,252,4,20,28,44,56,72,92,108,128,148,52,64,80,96,112,132,148,168,52,68,88,104,124,148,176,204,52,72,96,116,136,164,192,220,24,28,40,52,64,84,108,128,40,52,68,84,96,112,128,148,168,188,28,40,56,76,100,136,40,52,64,80,100,132,172,212,20,44,64,76,88,104,136,168,24,36,52,72,96,120,144,168,196,224,64,80,96,112,140,172,204,240,52,52,52,100,144,184,216,244,20,44,68,100,136,176,184,208,0,0,0,0,0,0,0,80,108,136,164,192,220,252,136,144,156,176,196,216,24,36,52,68,92,120,152,172,156,176,200,224,244,236,220,188,152,0,0,0,0,0,0,0,0,0,0,0,0,24,44,72,108,146,60,84,104,124,148,172,196,0,0,48,64,80,255,68,72,76,80,84,100,132,244,128,96,255],
  "b": [255,16,32,48,64,80,100,116,132,148,168,184,200,216,232,252,72,92,112,132,152,172,196,220,4,12,20,28,64,100,132,168,4,20,44,72,92,120,148,176,4,16,32,52,76,108,124,144,164,192,0,60,128,0,8,28,56,80,108,136,0,4,8,16,24,32,16,0,128,192,0,8,16,28,40,56,76,88,108,128,0,0,4,4,12,20,28,44,24,32,48,60,76,92,108,124,24,44,72,88,108,136,168,200,0,0,4,12,24,44,64,88,16,24,40,56,64,80,96,112,128,148,4,20,40,64,96,136,68,84,100,116,136,164,192,224,112,144,172,196,224,252,252,252,108,132,160,184,212,220,232,240,252,252,96,108,120,132,160,192,220,252,52,52,52,88,124,160,200,236,112,140,168,196,224,248,255,252,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,4,0,48,100,152,88,104,124,140,164,188,216,224,52,64,76,92,252,248,236,216,172,244,245,246,247,248,249,250,251,252,253,254,255,8,24,52,84,126,0,0,0,0,0,0,0,0,0,0,0,0,0,112,116,120,124,128,144,168,252,164,140,255]
}

"""
Standard OpenTTD Windows palette
"""
openttd_palette_win = {
  "r": [0,238,239,240,241,242,243,244,245,246,168,184,200,216,232,252,52,68,88,108,132,156,176,204,48,64,80,96,120,148,176,204,100,116,104,124,152,184,212,244,132,88,112,136,160,188,204,220,236,252,252,252,252,76,96,116,136,156,176,196,68,96,128,156,184,212,232,252,252,252,32,64,84,108,128,148,168,184,196,212,8,16,32,48,64,84,104,128,64,44,60,80,104,128,152,180,16,32,56,76,96,120,152,184,32,56,80,88,104,124,140,160,76,96,116,136,164,184,204,212,224,236,80,100,120,140,160,184,36,48,64,80,100,132,172,212,48,64,88,104,120,140,160,188,0,0,0,0,0,24,56,88,128,188,16,24,40,52,80,116,156,204,172,212,252,252,252,252,252,252,72,92,112,140,168,200,208,232,60,92,128,160,196,224,252,252,252,252,252,252,252,252,204,228,252,252,252,252,8,12,20,28,40,56,72,100,92,108,124,144,224,200,180,132,88,16,32,32,36,40,44,48,72,100,216,96,68,76,108,144,176,210,252,252,252,252,252,252,252,64,255,48,64,80,255,148,247,248,249,250,251,252,253,254,255,255],
  "g": [0,0,0,0,0,0,0,0,0,0,168,184,200,216,232,252,60,76,96,116,140,160,184,208,44,60,76,92,120,148,176,204,100,116,80,104,132,160,188,220,132,4,16,32,56,84,104,132,156,188,208,232,252,40,60,88,116,136,156,180,24,44,68,96,120,156,184,212,248,252,4,20,28,44,56,72,92,108,128,148,52,64,80,96,112,132,148,168,64,68,88,104,124,148,176,204,52,72,96,116,136,164,192,220,24,28,80,52,64,84,108,128,40,52,68,84,96,112,128,148,168,188,28,40,56,76,100,136,40,52,64,80,100,132,172,212,48,44,64,76,88,104,136,168,24,36,52,72,96,120,144,168,196,224,64,80,96,112,140,172,204,240,52,52,52,100,144,184,216,244,20,44,68,100,136,176,184,208,0,0,0,0,0,0,0,80,108,136,164,192,220,252,136,144,156,176,196,216,24,36,52,68,92,120,152,172,156,176,200,224,244,236,220,188,152,16,32,68,72,76,80,84,100,132,244,128,96,24,44,72,108,146,60,84,104,124,148,172,196,0,0,48,64,80,255,148,0,0,0,0,0,0,0,0,0,255],
  "b": [255,238,239,240,241,242,243,244,245,246,168,184,200,216,232,252,72,92,112,132,152,172,196,220,4,12,20,28,64,100,132,168,100,116,44,72,92,120,148,176,132,16,32,52,76,108,124,144,164,192,0,60,128,0,8,28,56,80,108,136,0,4,8,16,24,32,16,0,128,192,0,8,16,28,40,56,76,88,108,128,0,0,4,4,12,20,28,44,64,32,48,60,76,92,108,124,24,44,72,88,108,136,168,200,0,0,80,12,24,44,64,88,16,24,40,56,64,80,96,112,128,148,4,20,40,64,96,136,68,84,100,116,136,164,192,224,48,144,172,196,224,252,252,252,108,132,160,184,212,220,232,240,252,252,96,108,120,132,160,192,220,252,52,52,52,88,124,160,200,236,112,140,168,196,224,248,255,252,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,4,0,48,100,152,88,104,124,140,164,188,216,224,52,64,76,92,252,248,236,216,172,16,32,112,116,120,124,128,144,168,252,164,140,8,24,52,84,126,0,0,0,0,0,0,0,0,0,0,0,0,0,148,247,248,249,250,251,252,253,254,255,255]
}

"""
Palette indices of special colours
"""
openttd_palette_animated = [227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,245,246,247,248,249,250,251,252,253,254,254]
openttd_palette_generalmask = [0,255]

def palette_image(r, g, b):
  """
  Make a minimal image containing palette values
  :return: A 256 by 1 image in `P` mode with the specified r, g, b palette
  """
  palette = []
  for i in range(len(r)):
    palette.append(r[i])
    palette.append(g[i])
    palette.append(b[i])
  palimage = Image.new('P', (256, 1))
  for x in range(256):
    palimage.putpixel((x, 0), x)
  palimage.putpalette(palette)
  return palimage

def openttd_palette_image():
  """
  Make a minimal image containing all OpenTTD palette values
  :return: A 256 by 1 image in `P` mode with the OpenTTD DOS palette
  """
  palette_r = openttd_palette["r"]
  palette_g = openttd_palette["g"]
  palette_b = openttd_palette["b"]
  palette = palette_image(palette_r, palette_g, palette_b)
  return palette

def openttd_palettise(source):
  """
  Convert an image to an 8-bit palette image with the OpenTTD palette. Does not do dithering.
  :param source: Input image, will be treated as RGB.
  :return: Image converted to the OpenTTD palette
  """
  # Conventional conversion would be source.quantize(palette=[openttdpalette], dither=False)
  # DON'T EVER USE THAT! There is a bug which leads to clipping of r, g or b values to 252 prior to palette index assignment
  # Plus, I think mine looks nicer

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
        dist = 255 * 255 * 255
        index = 0
        for i in range(len(r)):
          d = (pr - r[i]) * (pr - r[i]) + (pg - g[i]) * (pg - g[i]) + (pb - b[i]) * (pb - b[i])
          if d < dist:
            dist = d
            index = i
        target.putpixel((x, y), index)
  return target

def check_update_needed(input_file_list, output_file):
  """
  Check whether an output file needs updating, based on date modified and a list of files used to generate the output file.

  :param input_file_list: List of input file paths.
  :param output_file: Output file path.
  :return: If the output file needs updating.
  """
  if not os.path.isfile(output_file):
    # output file does not exist, needs update
    return True
  for input_file in input_file_list:
    # check all input files
    if os.path.isfile(input_file):
      # implicitly treat missing files as up-to-date
      if os.path.getmtime(input_file) > os.path.getmtime(output_file):
        # at least one input is newer than output, needs update
        return True
  # otherwise all up-to-date
  print("  Skipped, output exists and is up-to-date")
  return False

def color_to_alpha(input, r, g, b):
  """
  Makes any pixels equal to r, g, b in the input image transparent, while preserving alpha of other pixel values

  :param input: Input image
  :param r: Red value
  :param g: Green value
  :param b: Blue value
  :return: Image with pixels equal to r, g, b now alpha zero
  """
  input = input.convert("RGBA")
  # update alpha channel
  ir, ig, ib, ia = input.split()
  # update ia so pixels equal to r, g, b are also full transparent
  width, height = input.size
  for x in range(width):
    for y in range(height):
      pr, pg, pb, pa = input.getpixel((x, y))
      if r == pr and g == pg and b == pb:
        ia.putpixel((x, y), 0)
  return Image.merge("RGBA", (ir, ig, ib, ia))

def blue_to_alpha(input):
  return color_to_alpha(input, 0, 0, 255)

def paste_to_unscaled(input, ix, iy, iw, ih, output, ox, oy):
  output = paste_to(input, ix, iy, iw, ih, output, ox, oy, 1)
  return output

def paste_to(input, ix, iy, iw, ih, output, ox, oy, scale):
  """
  Paste from a rectangle in the input image to a rectangle in the output image of the same size.

  :param input: Input image.
  :param ix: Rectangle x coordinate in input.
  :param iy: Rectangle y coordinate in input.
  :param iw: Rectangle width.
  :param ih: Rectangle width.
  :param input: Output image.
  :param ix: Rectangle x coordinate in output.
  :param iy: Rectangle y coordinate in output.
  :param scale: Scale factor for coordinates.
  :return: Modified output image.
  """
  crop = input.crop((ix * scale, iy * scale, (ix + iw) * scale, (iy + ih) * scale))
  output.paste(crop, (ox * scale, oy * scale))
  return output

def alpha_to(input1, ix1, iy1, w, h, input2, ix2, iy2, scale):
  """
  Paste using alpha blending from a rectangle in the input image to a rectangle in the output image of the same size.

  :param input: Input image.
  :param ix: Rectangle x coordinate in input.
  :param iy: Rectangle y coordinate in input.
  :param iw: Rectangle width.
  :param ih: Rectangle width.
  :param input: Output image.
  :param ix: Rectangle x coordinate in output.
  :param iy: Rectangle y coordinate in output.
  :param scale: Scale factor for coordinates.
  :return: Modified output image.
  """
  crop1 = input1.convert("RGBA").crop((ix1 * scale, iy1 * scale, (ix1 + w) * scale, (iy1 + h) * scale))  
  crop2 = input2.convert("RGBA").crop((ix2 * scale, iy2 * scale, (ix2 + w) * scale, (iy2 + h) * scale))
  crop = Image.alpha_composite(crop2, crop1)
  output = paste_to(crop, 0, 0, w, h, input2, ix2, iy2, scale)
  return output

def colour_to(input1, ix1, iy1, w, h, input2, ix2, iy2, scale, r, g, b):
  """
  Paste using a specific colour as transparent from a rectangle in the input image to a rectangle in the output image of the same size.

  :param input: Input image.
  :param ix: Rectangle x coordinate in input.
  :param iy: Rectangle y coordinate in input.
  :param iw: Rectangle width.
  :param ih: Rectangle width.
  :param input: Output image.
  :param ix: Rectangle x coordinate in output.
  :param iy: Rectangle y coordinate in output.
  :param scale: Scale factor for coordinates.
  :param r: red value for transparent.
  :param g: green value for transparent.
  :param b: blue value for transparent.
  :return: Modified output image.
  """
  crop1 = input1.convert("RGBA").crop((ix1 * scale, iy1 * scale, (ix1 + w) * scale, (iy1 + h) * scale))  
  crop2 = input2.convert("RGBA").crop((ix2 * scale, iy2 * scale, (ix2 + w) * scale, (iy2 + h) * scale))
  # update alpha channel of crop 1
  crop1 = color_to_alpha(crop1, r, g, b)
  # alpha over with updated 
  crop = Image.alpha_composite(crop2, crop1)
  output = paste_to(crop, 0, 0, w, h, input2, ix2, iy2, scale)
  return output 

def blue_to(input1, ix1, iy1, w, h, input2, ix2, iy2, scale):
  return colour_to(input1, ix1, iy1, w, h, input2, ix2, iy2, scale, 0, 0, 255)

def mask_image(source, mask):
  """
  Masks the source image, based on mask. Pure blue or white in mask are taken from the mask, otherwise from source.
  
  :param source: Input image.
  :Param mask: Input mask, blue or white pixel is taken from mask, otherwise from source.
  :return: Modified source image, RGB.
  """
  source = source.convert("RGB")
  mask = mask.convert("RGB")
  image_width, image_height = source.size
  # Make mask from blue pixels in overlay
  output = source.copy()
  mask_values = [(0, 0, 255), (255, 255, 255)]
  for x in range(image_width):
    for y in range(image_height):
      r, g, b = mask.getpixel((x, y))
      if (r, g, b) in mask_values:
        output.putpixel((x, y), (r, g, b))
  return output

def blue_over(image1, image2):
  """
  Overlay image2 onto image1, assuming image2 is indexed, using blue as transparent

  :input source: Input image.
  :input overlay: Overlay image.
  :return: Output image.
  """
  v = [255] * 256
  v[0] = 0
  palette = []
  for i in range(len(v)):
    palette.append(v[i])
    palette.append(v[i])
    palette.append(v[i])
  mask = image2.copy()
  mask.putpalette(palette)
  mask = mask.convert("L")
  image1.paste(image2, (0, 0), mask)
  return image1

def overlay_bluetransp(source, overlay):
  """
  Simple overlay, treating blue pixels in source as transparent.

  :input source: Input image.
  :input overlay: Overlay image.
  :return: Output image.
  """
  source = source.convert("RGB")
  overlay = overlay.convert("RGB")
  image_width, image_height = source.size
  # Make mask from blue pixels in overlay
  image_mask = Image.new("L", (image_width, image_height), 0)
  for x in range(image_width):
    for y in range(image_height):
      r, g, b = overlay.getpixel((x, y))
      if r != 0 or g != 0 or b != 255:
        image_mask.putpixel((x, y), 255)
  # Paste using mask
  source.paste(overlay, (0, 0), image_mask)
  return source

def bluewhite_to_transp(source):
  """
  Transforms all pixels in input image with b == 255 (includes pure blue, white) to tranparent.

  :param source: Input image.
  :return: Modified input image, now RGBA.
  """
  source = source.convert("RGBA")
  image_width, image_height = source.size
  for x in range(image_width):
    for y in range(image_height):
      r, g, b, a = source.getpixel((x, y))
      if b == 255:
        source.putpixel((x, y), (r, g, b, 0))
  return source

def blendmode_overlay(image_32bit, image_texture, opacity, blendmode):
  """
  Applies an image texture, overlayed with a custom opacity, on an RGB image.
  :param image_32bit: Base image, treated as RGB
  :param image_texture: Image to overlay, 
  :param opacity: Overlay opacity
  :param blendmode: Name of the blend_mode to use
  :return: 
  """
  # Used to be named `overlay_simple`
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
  if blendmode == "overlay":
    image_blended_arr_float = blend_modes.overlay(image_bg_arr, image_fg_arr, opacity)
  elif blendmode == "normal":
    image_blended_arr_float = blend_modes.normal(image_bg_arr, image_fg_arr, opacity)
  elif blendmode == "darken_only":
    image_blended_arr_float = blend_modes.darken_only(image_bg_arr, image_fg_arr, opacity)
  image_blended_arr = numpy.uint8(image_blended_arr_float)
  image_out = Image.fromarray(image_blended_arr)
  return image_out

def blend_overlay(image_32bit, image_texture, opacity):
  """
  Applies an image texture, overlayed with a custom opacity, on an RGB image. Uses blend_modes.overlay
  :param image_32bit: Base image, treated as RGB
  :param image_texture: Image to overlay, 
  :param opacity: Overlay opacity
  :return: 
  """
  # Used to be named `overlay_simple`
  return blendmode_overlay(image_32bit, image_texture, opacity, "overlay")
