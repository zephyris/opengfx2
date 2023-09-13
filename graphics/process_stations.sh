export PATH=$PATH:$(pwd)

cd stations

cd general

cd 64
# process all buildings
building_shapeproc.py 1 temperate
building_shapeproc.py 1 temperate True
building_shapeproc.py 1 toyland
building_baseshapeproc.py 1 temperate
building_base_flatten.py heliport 1
# mask regions of depots (ie. back wall from rest of building)
mask_regions.py pygen/raildepots raildepots_regionmask.png 1
mask_regions.py pygen/raildepots_toyland raildepots_regionmask.png 1
mask_regions.py pygen/monoraildepots monoraildepots_regionmask.png 1
mask_regions.py pygen/monoraildepots_toyland monoraildepots_regionmask.png 1
mask_regions.py pygen/maglevdepots maglevdepots_regionmask.png 1
mask_regions.py pygen/maglevdepots_toyland maglevdepots_regionmask.png 1
mask_regions.py pygen/roaddepots roaddepots_regionmask.png 1
mask_regions.py pygen/roaddepots_toyland roaddepots_regionmask.png 1
mask_regions.py pygen/tramdepots tramdepots_regionmask.png 1
mask_regions.py pygen/tramdepots_toyland tramdepots_regionmask.png 1
mask_regions.py pygen/shipdepots shipdepots_regionmask.png 1
mask_regions.py pygen/shipdepots_toyland shipdepots_regionmask.png 1
mask_regions.py pygen/modernairdepots modernairdepots_regionmask.png 1
mask_regions.py pygen/modernairdepots_toyland modernairdepots_regionmask.png 1
mask_regions.py pygen/oldairdepots oldairdepots_regionmask.png 1
mask_regions.py pygen/oldairdepots_toyland oldairdepots_regionmask.png 1
# mask regions of tunnels (ie. back wall and roadway from rest of tunnel/sloped tile)
mask_regions.py pygen/railtunnels railtunnels_regionmask.png 1
mask_regions.py pygen/railtunnels_snow railtunnels_regionmask.png 1
mask_regions.py pygen/monorailtunnels monorailtunnels_regionmask.png 1
mask_regions.py pygen/monorailtunnels_snow monorailtunnels_regionmask.png 1
mask_regions.py pygen/maglevtunnels maglevtunnels_regionmask.png 1
mask_regions.py pygen/maglevtunnels_snow maglevtunnels_regionmask.png 1
mask_regions.py pygen/roadtunnels roadtunnels_regionmask.png 1
mask_regions.py pygen/roadtunnels_snow roadtunnels_regionmask.png 1
mask_regions.py pygen/nonetunnels nonetunnels_regionmask.png 1
mask_regions.py pygen/nonetunnels_snow nonetunnels_regionmask.png 1
# overlay tunnels onto terrain sprites
infrastructure_tunnels_infrastructureoverlay.py 1 road
infrastructure_tunnels_infrastructureoverlay.py 1 road_toyland
infrastructure_tunnels_infrastructureoverlay.py 1 rail
infrastructure_tunnels_infrastructureoverlay.py 1 rail_toyland
infrastructure_tunnels_infrastructureoverlay.py 1 terrain
# handle old airport
building_base_flatten.py oldairport_multitile 1
mask_tiles.py pygen/oldairport_multitile oldairport_multitile_tilemask.png 1
mask_tiles.py pygen/oldairport_multitile_combo oldairport_multitile_tilemask.png 1
building_base_flatten.py oldairport_multitile_toyland 1
mask_tiles.py pygen/oldairport_multitile_toyland oldairport_multitile_tilemask.png 1
mask_tiles.py pygen/oldairport_multitile_toyland_combo oldairport_multitile_tilemask.png 1
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd 256
# process all buildings
building_shapeproc.py 4 temperate
building_shapeproc.py 4 temperate True
building_shapeproc.py 4 toyland
building_baseshapeproc.py 4 temperate
# mask regions of depots (ie. back wall from rest of building)
mask_regions.py pygen/roaddepots roaddepots_regionmask.png 4
mask_regions.py pygen/roaddepots_toyland roaddepots_regionmask.png 4
mask_regions.py pygen/raildepots raildepots_regionmask.png 4
mask_regions.py pygen/raildepots_toyland raildepots_regionmask.png 4
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd ..

cd ..
