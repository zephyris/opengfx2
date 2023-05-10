export PATH=$PATH:$(pwd)

cd industries

cd temperate/64/
building_shapeproc.py 1 temperate
building_baseshapeproc.py 1 temperate
building_base_flatten.py steelmill 1
mask_tiles.py pygen/steelmill_combo steelmill_tilemask.png 1
building_base_flatten.py factory 1
mask_tiles.py pygen/factory_combo factory_tilemask.png 1
mask_tiles.py pygen/coalmine_base coalmine_base_tilemask.png 1
mask_tiles.py pygen/farm farm_tilemask.png 1
mask_tiles.py pygen/farm_base farm_tilemask.png 1
mask_tiles.py pygen/bank bank_tilemask.png 1
mask_tiles.py pygen/bank_base bank_tilemask.png 1
building_base_flatten.py ironoremine 1
mask_tiles.py pygen/ironoremine_combo ironoremine_tilemask.png 1
mask_tiles.py pygen/oilrig oilrig_tilemask.png 1
custom_dither.py
cd pygen
custom_dither.py
cd ../../../

cd arctic/64/
building_shapeproc.py 1 arctic
building_baseshapeproc.py 1 arctic
building_base_flatten.py foodprocessingplant 1
mask_tiles.py pygen/bank bank_tilemask.png 1
mask_tiles.py pygen/bank_base bank_tilemask.png 1
mask_tiles.py pygen/farm farm_tilemask.png 1
mask_tiles.py pygen/farm_base farm_tilemask.png 1
building_base_flatten.py papermill 1
building_base_flatten.py printingworks 1
mask_tiles.py pygen/printingworks_combo printingworks_tilemask.png 1
building_base_flatten.py goldmine 1
mask_tiles.py pygen/goldmine_combo goldmine_tilemask.png 1
custom_dither.py
cd pygen
custom_dither.py
cd ../../../

cd tropical/64/
building_shapeproc.py 1 tropical
building_baseshapeproc.py 1 tropicaldesert
building_base_flatten.py diamondmine 1
mask_tiles.py pygen/diamondmine_combo diamondmine_tilemask.png 1
building_base_flatten.py lumbermill 1
mask_tiles.py pygen/lumbermill_combo lumbermill_tilemask.png 1
custom_dither.py
cd pygen
custom_dither.py
cd ../../../

cd toyland/64/
if [ ! -d pygen ]; then
  mkdir pygen
fi
cp fizzy_drink_factory_32bpp.png pygen/
cp fizzy_drink_factory_palmask.png pygen/
mask_tiles.py pygen/fizzy_drink_factory fizzy_drink_factory_tilemask.png 1
custom_dither.py
cd pygen
custom_dither.py
cd ../../../

cd ..
