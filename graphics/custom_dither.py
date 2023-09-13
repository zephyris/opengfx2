#!/usr/bin/env python3

from PIL import Image
from PIL import ImageFilter
from random import randint
import numpy, blend_modes # For overlay blending
import glob, os, sys

from tools import openttd_palettise, check_update_needed, openttd_palette, openttd_palette_animated, openttd_palette_generalmask

verbose = True

# Define the working palette
palette_r = openttd_palette["r"]
palette_g = openttd_palette["g"]
palette_b = openttd_palette["b"]
# Setup palette image, used for applying palette quickly
def palette_image(r, g, b):
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
palimage=palette_image(palette_r, palette_g, palette_b)

# Setup palette dict for quick lookup

# Define special palette index sets
# 'Normal' palette entries
colors_normal = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 255]
# Action colours (animated palette indices)
colors_action = openttd_palette_animated
# Special colours, do not propagate errors through these indices
colors_special = openttd_palette_generalmask

# Palette colour sets
# Color set start indices
color_set_start = [1, 16, 24, 32, 40, 50, 53, 60, 70, 80, 88, 96, 104, 112, 122, 128, 136, 144, 154, 162, 170, 178, 192, 198, 206]
# Color set length
color_set_length = [15, 8, 8, 8, 10, 3, 7, 10, 10, 8, 8, 8, 8, 10, 6, 8, 8, 10, 8, 8, 8, 14, 6, 8, 4]

# Primary conversion function
# dither_factor is the additional multiplicative factor on error diffusion, use between 0 and 1
# src and pal are the image to dither and an image defining palette restrictions
def make_8bpp(src, pal, dither_factor):
  width, height = src.size
  # Start by making sure the images are the correct mode
  # Source must be RGB (no alpha)
  src = src.convert("RGB")
  # Palette must be 8-bit with OpenTTD palette
  pal = openttd_palettise(pal)
  
  # Convert src to 8-bit with OpenTTD palette using custom dithering
  # Dithers in HSV space, restricting colour sets when specified in pal
  dithered = make_dithered(src, pal, dither_factor)
  
  # Overlay pixels in pal exactly matching indices in colors_action over dithered image
  # Mask from indices
  v = [0] * 255
  for i in range(len(colors_action)):
    v[colors_action[i]] = 255
  mask_palimg = palette_image(v, v, v)
  mask = pal.copy()
  mask.putpalette(mask_palimg.getpalette())
  mask = mask.convert("L")
  # Paste using mask
  dithered.paste(pal, (0, 0), mask)
  
  # Return result
  return dithered

def most_similar_in_palette(pr, pg, pb):
  dist = 255 * 255 * 255
  index = 0
  for i in colors_normal:
    cd = (pr - palette_r[i]) * (pr - palette_r[i]) + (pg - palette_g[i]) * (pg - palette_g[i]) + (pb - palette_b[i]) * (pb - palette_b[i])
    if cd < dist:
      dist = cd
      index = i
  return index

def most_similar_in_color_set(pr, pg, pb, color_set):
  dist = 255 * 255 * 255
  index = 0
  start_index = color_set_start[color_set]
  end_index = start_index + color_set_length[color_set]
  for i in range(start_index, end_index):
    cd = (pr - palette_r[i]) * (pr - palette_r[i]) + (pg - palette_g[i]) * (pg - palette_g[i]) + (pb - palette_b[i]) * (pb - palette_b[i])
    if cd < dist:
      dist = cd
      index = i
  return index

# Dither function
# Do dithering in RGB space
# Do not dither (propagate pixel value errors) to indices in colors_action or colors_special
# If pal pixel index is in one of the color sets, restrict dithering to only indices in that set
def make_dithered(src, pal, dither_factor):
  # Find colour groups in pal image and make an image recording the color set per pixel
  # If sets pixel is not 255 then dithering is restricted to indices in color_set[pixel value]
  v = [255] * 256
  for i in range(len(color_set_start)):
    for j in range(color_set_length[i]):
      v[color_set_start[i] + j] = i
  sets_palimg = palette_image(v, v, v)
  sets = pal.copy()
  sets.putpalette(sets_palimg.getpalette())
  sets = sets.convert("L")
  
  # Find pixels in src exactly matching colors_special and make an image with this mask
  # Do not propagate pixel value errors through donotdither pixels with value 255
  width, height = src.size
  donotdither = Image.new("L", (width, height), 0)
  for x in range(width):
    for y in range(height):
      pr, pg, pb = src.getpixel((x, y))
      for i in range(len(colors_special)):
        if palette_r[colors_special[i]] == pr and palette_g[colors_special[i]] == pg and palette_b[colors_special[i]] == pb:
          donotdither.putpixel((x, y), 255)
          break
  
  # Dither settings
  # Sierra http://www.tannerhelland.com/4660/dithering-eleven-algorithms-source-code/
  #dox = 2
  #doy = 0
  #df = 32
  #da = [
  #  [-1, -1, -1,  5,  3],
  #  [ 2,  4,  5,  4,  2],
  #  [ 0,  2,  3,  2,  0]
  #]
  
  # Sierra lite http://www.tannerhelland.com/4660/dithering-eleven-algorithms-source-code/
  dox = 1
  doy = 0
  df = 4
  da = [
    [-1, -1,  2],
    [ 1,  1,  0]
  ]
  
  # Do dithering
  # TODO?: Change to dithering in HSV space, with error propogation factors of h, s, v = 0, 0.8, 1.0
  res = Image.new("P", (src.size))
  res.putpalette(palimage.getpalette())
  for y in range(height):
    for x in range(width):
      pr, pg, pb = src.getpixel((x, y))
      if donotdither.getpixel((x, y)) == 255:
        # Do not dither this pixel, just set nearest value
        res.putpixel((x, y), most_similar_in_palette(pr, pg, pb))
      else:
        # Dither this pixel
        if sets.getpixel((x, y)) != 255:
          # Dither this pixel within a color set
          res.putpixel((x, y), most_similar_in_color_set(pr, pg, pb, sets.getpixel((x, y))))
        else:
          # Dither this pixel to any color
          res.putpixel((x, y), most_similar_in_palette(pr, pg, pb))
        # Diffuse errors according to the dithering matrix
        error = [0, 0, 0]
        error[0] = pr - palette_r[res.getpixel((x, y))]
        error[1] = pg - palette_g[res.getpixel((x, y))]
        error[2] = pb - palette_b[res.getpixel((x, y))]
        # Do error propagation
        for b in range(len(da)):
          for a in range(len(da[0])):
            # For each x and y offset a and b in dither array
            if da[b][a] != -1 and x + a < width - 1 and y + b < height - 1:
              # If a valid dither value and within image bounds
              if donotdither.getpixel((x, y)) != 255:
                # Do not propagate errors through pixels identified as donotdither
                # Alter pixel value to propagate errors
                pcr, pcg, pcb = src.getpixel((x + a - dox, y + b - doy))
                pcr = int(pcr + error[0] * dither_factor * da[b][a] / df)
                pcg = int(pcg + error[1] * dither_factor * da[b][a] / df)
                pcb = int(pcb + error[2] * dither_factor * da[b][a] / df)
                src.putpixel((x + a - dox, y + b - doy), (pcr, pcg, pcb))
                # Clamp propagated error to a maximum of 16 per channel
                maxerror = 16
                error = [min(error[0], maxerror), min(error[1], maxerror), min(error[2], maxerror)]

  # Return result
  return res

def make_output_parallel_handler(input=input):
  # input is: image, palmask, dither factor, x, y
  image_8bpp = make_8bpp(input[0], input[1], input[2])
  image_bt32bpp = bluewhite_to_transp(input[0])
  image_rm32bpp = remainder_32bpp(image_8bpp, image_bt32bpp)
  return [image_8bpp, image_bt32bpp, image_rm32bpp, input[3], input[4]]

def make_output_parallel(image, palmask, factor):
  import concurrent, multiprocessing
  from tqdm.auto import tqdm
  sprites = find_sprites(image)
  #setup worklist by cropping sprites from input image
  worklist = []
  for i in range(len(sprites)):
    # each entry is: image, palmask, dither factor, x, y
    worklist.append([image.crop((sprites[i][0], sprites[i][1], sprites[i][2], sprites[i][3])), palmask.crop((sprites[i][0], sprites[i][1], sprites[i][2], sprites[i][3])), factor, sprites[i][0], sprites[i][1]])
  #setup workers based on multiprocess mode
  multiprocess_mode = "process" # process seems to give easily the highest performance
  workers = multiprocessing.cpu_count()
  if multiprocess_mode is None:
    # run in a single thread, still use the ThreadPoolExecutor since that's equivalent
    Executor = concurrent.futures.ThreadPoolExecutor
    workers = 1
  elif multiprocess_mode == "process":
    # setup executor as a process pool
    Executor = concurrent.futures.ProcessPoolExecutor
  elif multiprocess_mode == "thread":
    # setup executor as a thread pool
    Executor = concurrent.futures.ThreadPoolExecutor
  #process
  with Executor(workers) as executor:
    futures = [executor.submit(make_output_parallel_handler, input=input) for input in worklist]
    results = [future.result() for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), smoothing=0)]
  #recombine cropped sprites into spritesheets
  image_8bpp = Image.new("P", (image.size), 255)
  image_8bpp.putpalette(palimage.getpalette())
  image_bt32bpp = Image.new("RGBA", (image.size), (255, 255, 255, 255))
  image_rm32bpp = Image.new("RGBA", (image.size), (255, 255, 255))
  for i in range(len(results)):
    image_8bpp.paste(results[i][0], (results[i][3], results[i][4]))
    image_bt32bpp.paste(results[i][1], (results[i][3], results[i][4]))
    image_rm32bpp.paste(results[i][2], (results[i][3], results[i][4]))
  return image_8bpp, image_bt32bpp, image_rm32bpp

def make_output(image, palmask, factor):
  image_8bpp = make_8bpp(image, palmask, 1);
  image_bt32bpp = bluewhite_to_transp(image)
  image_rm32bpp = remainder_32bpp(image_8bpp, image_bt32bpp)
  return image_8bpp, image_bt32bpp, image_rm32bpp

def find_sprites(src):
  """
  Find sprites within a 32bpp spritesheet. Assumes sprite background is (255, 255, 255). Identifies sprites as bounding rectangles of non-(255, 255, 255) areas.
  Returns a list of (x, y, x+w, y+h) bounds per sprite.
  """
  import numpy, skimage
  w, h = src.size
  r, g, b = src.convert("RGB").split()
  # make numpy image with (255, 255, 255)->0 else 1
  tmp = numpy.asarray(r).astype("int32") + numpy.asarray(g) + numpy.asarray(b)
  tmp[tmp != 255 * 3] = 0
  tmp[tmp == 255 * 3] = 255
  tmp = 255 - tmp
  # use skimage to find the objects (sprites)
  lab = skimage.measure.label(tmp)
  table = skimage.measure.regionprops_table(lab, tmp, properties=("bbox", "area_bbox"))
  # parse and return (swapped x and y in skimage)
  sprites = []
  for i in range(len(table["bbox-0"])):
    sprites.append([table["bbox-1"][i], table["bbox-0"][i], table["bbox-3"][i], table["bbox-2"][i]])
  return sprites

def bluewhite_to_transp(src):
  # Make sure src is RGB
  src = src.convert("RGB")
  # Find pixels in src exactly matching pure blue and make an alpha channel from this mask
  width, height = src.size
  a = Image.new("L", (width, height), 255)
  for x in range(width):
    for y in range(height):
      pr, pg, pb = src.getpixel((x, y))
      if 0 == pr and 0 == pg and 255 == pb:
        a.putpixel((x, y), 0)
  # Make RGBA composite
  r, g, b = src.split()
  return Image.merge("RGBA", (r, g, b, a))

def remainder_32bpp(src8bit, src32bit):
  """
  Uses a input 32bit image and its 8bit pallete conversion to make 32bpp (but grayscale) map of brightness remainder.
  Makes an output 32bit image which, when used with the input 8bit image as a mask, inherits hue/sat from 8bit but brightness from input 32bpp.
  Preserves alpha channel from 32bit image.
  """
  def v(r, g, b):
    return max(r, g, b)

  src8bit = src8bit.convert("RGBA")
  src32bit = src32bit.convert("RGBA")
  out32bit = src32bit.copy()
  width, height = src32bit.size
  for x in range(width):
    for y in range(height):
      pr8, pg8, pb8, pa8 = src8bit.getpixel((x, y))
      pr32, pg32, pb32, pa32 = src32bit.getpixel((x, y))
      deltav = v(pr32, pg32, pb32) - v(pr8, pg8, pb8) + 128
      alpha = 255
      if pr8 == 0 and pg8 == 0 and pb8 == 255:
        alpha = 0
      out32bit.putpixel((x, y), (deltav, deltav, deltav, alpha))
  return out32bit

suffix = "_32bpp.png";
print("Converting to 8-bit")
for input_file in glob.glob("*"+suffix):
  # Only process images lacking a *_8bpp output _or_ modified more recently than the *_8bpp output
  do_processing = True
  name = input_file[:-len(suffix)]
  if verbose == True:
    print(" "+name)
  find_sprites(Image.open(input_file))
  if check_update_needed([input_file, input_file+"_palmask.png"], name+"_8bpp.png") or check_update_needed([input_file, input_file+"_palmask.png"], name+"_bt32bpp.png") or check_update_needed([input_file, input_file+"_palmask.png"], name+"_rm32bpp.png"):
    with Image.open(input_file) as image:
      width, height = image.size
      if os.path.isfile(name+"_palmask.png"):
        palmask = Image.open(name+"_palmask.png")
      else:
        palmask = Image.new("P", (width, height), 0)
        palmask.putpalette(palimage.getpalette())
      image_8bpp, image_bt32bpp, image_rm32bpp = make_output_parallel(image, palmask, 1);
      #image_8bpp, image_bt32bpp, image_rm32bpp = make_output(image, palmask, 1)
      image_8bpp.save(name+"_8bpp.png", "PNG")
      image_bt32bpp.save(name+"_bt32bpp.png", "PNG")
      image_rm32bpp.save(name+"_rm32bpp.png", "PNG")
