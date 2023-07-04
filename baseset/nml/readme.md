# Coding style
Sprites used in `replace` and `replace_new` blocks should aim to use the folowing structure:

```
replace XXX(sprXXX, <file>) { template(1) }
#ez alternative_sprites(sprXXX, ZOOM_LEVEL_IN_4X, BIT_DEPTH_8BPP, <*_8bpp.png file>) { template(4) }
#32 alternative_sprites(sprXXX, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, <*_bt32bpp.png file>) { template(1) }
#32 #ez alternative_sprites(sprXXX, ZOOM_LEVEL_IN_4X, BIT_DEPTH_8BPP, <*_bt32bpp.png file>) { template(4) }
```

Each `replace` should be named `sprXXX` (where XXX is the start number of the replacement). Similarly, each `replace_new` should be named `<feature>_sprXXX`. Every replacement must use a zoom level-sensitive template, to allow easy definition of extra zoom and 32bpp alternative sprites.

Where possible, define templates of general use in `../../templates/zoom-sensitive.pnml`. For single use very individual sprites layouts, define a specific template named `template_sprXXX` _immediately_ before the replace:

```
template template_sprXXX(z) {
    <template here>
}
<do the replacement here>
```

`alternative_sprites` for extra zoom and 32bpp should be prefixed with `#ez ` and `#32 ` respectively, or `#32 #ez ` for extra zoom and 32bpp.

# 32bpp sprites
Most 32bpp sprites should use `_bt32bpp.png" sprites. These have a simple conversion of rgb(0, 0, 255) to rgba(0, 0, 0, 0).

If a sprite is recoloured or has palette animation, 32bpp sprites should use `_rm32bpp.png` with a mask of the standard `_8bpp.png` sprite.
