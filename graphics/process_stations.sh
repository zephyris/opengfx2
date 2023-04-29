export PATH=$PATH:$(pwd)

cd stations

cd general/64
# process all buildings
building_shapeproc.py 1
building_shapeproc.py 1 True
building_baseshapeproc.py 1
building_base_flatten.py heliport 1
# mask regions of depots (ie. back wall from rest of building)
mask_regions.py pygen/raildepots raildepots_regionmask.png 1
mask_regions.py pygen/monoraildepots monoraildepots_regionmask.png 1
mask_regions.py pygen/maglevdepots maglevdepots_regionmask.png 1
mask_regions.py pygen/roaddepots roaddepots_regionmask.png 1
mask_regions.py pygen/tramdepots tramdepots_regionmask.png 1
mask_regions.py pygen/shipdepots shipdepots_regionmask.png 1
mask_regions.py pygen/modernairdepots modernairdepots_regionmask.png 1
# mask regions of tunnels (ie. back wall and roadway from rest of tunnel/sloped tile)
mask_regions.py pygen/railtunnels railtunnels_regionmask.png 1
mask_regions.py pygen/railtunnels_snow railtunnels_regionmask.png 1
mask_regions.py pygen/monorailtunnels monorailtunnels_regionmask.png 1
mask_regions.py pygen/monorailtunnels_snow monorailtunnels_regionmask.png 1
mask_regions.py pygen/maglevtunnels maglevtunnels_regionmask.png 1
mask_regions.py pygen/maglevtunnels_snow maglevtunnels_regionmask.png 1
mask_regions.py pygen/roadtunnels roadtunnels_regionmask.png 1
mask_regions.py pygen/roadtunnels_snow roadtunnels_regionmask.png 1
# overlay tunnels onto terrain sprites
infrastructure_tunnels_infrastructureoverlay.py 1 road
infrastructure_tunnels_infrastructureoverlay.py 1 rail
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd ..
