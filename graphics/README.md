# Graphics generation pipeline
This is an 8-bit (8bpp) and RGBA (32bpp) base graphics set.

## Image sources
Many images are automatically generated. All 8-bit images are generated from RGB or RGBA png images.
The 32bpp png images may themselves have a source, and may be manually derived from Paint.NET (pdn), GIMP (xcf), Blender (blend) or Inkscape (svg) files.

All `*_8bpp.png`, `*_bt32bpp.png` and `*_rm32bpp.png` images are automatically generated from the file called `*_32bpp.png`.
Do not directly modify any file named `*_8bpp.png`, `*_bt32bpp.png` or `*_rm32bpp.png`, your changes will be overwritten!

Files within a directory named `pygen` are automatically generated from images in the parent directory.
This includes files named `*_32bpp.png`, do not modify them as your changes will be overwritten!

If in doubt, check the `.gitignore`.

NB. The `*_32bpp.png` images may not actually be RGB or RGBA, but their name indicates they should be handled as 32bpp source images.

## Generation methods
Typically, sprites are generated by:

Either, for buildings:
* Taking an object shape from a file named `*_shape.png` and recolouring and texturing it based on specialised pixels on row 1 of the image.
Or, for terrain and infrastructure tiles:
* Taking a base texture from a reference `*_32bpp.png` file, eg. standard ground grass

Overlaying various additional layers to add detail:
* `*_overlayalpha.png`: A 32bpp image overlaid in alpha blending mode.
* `*_overlayshading.png`: A 32bpp image overlaid in overlay blending mode.
* `*_overlaynormal.png`: A pseudo-8bpp image overlaid in alpha blending mode.

Converting to 8bpp:
Conversion uses a custom, standardised, dither script, making `*_8bpp.png`.
* If `*_palmask.png` exists, restricting dither to within the colour series/groups within this set.
* `*_palmask.png` might be manually provided, or generated from unshaded recoloured `*_shape.png` images, overlaid with `*_overlaynormal.png`.
* Animated palette indices are not used in normal dithering, unless in the `*_palmask.png` image, in which case they are protected and preserved.

Converting for 32bpp:
Conversion uses two passes.
1. If the 32bpp image lacks an alpha channel or is entirely opaque, replace tranparent blue in the 32bpp image with transparent, making the 'blue transparent' image `_bt32bpp.png`. If it has an alpha channel, then transparent blue is assigned by dithering the alpha channel. The resulting `_bt32bpp.png` image is suitable for use for most 32bpp sprites.
2. Next, measure the brightness difference in the 32bpp image to the 8bpp sprite making the 'remainder' image `_rm32bpp.png`. This image in combination with the `_8bpp.png` image is the preferred choice for recoloured 32bpp sprites.

Further sprite specific processing may be done, including:
* Overlaying/merging sprites (eg. building sprites onto their ground tile)
* Cutting up a sprite into individual sprites (eg. multi-tile buildings)
* Ensuring a region of multiple sprites is identical between them (eg. avoiding dither dancing for animations)
