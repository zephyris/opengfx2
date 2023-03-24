export PATH=$PATH:$(pwd)

cd industries

cd temperate/64/
building_shapeproc.py 1
building_baseshapeproc.py 1
building_base_flatten.py steelmill 1
tile_mask.py pygen/steelmill_combo steelmill_tilemask.png 1
building_base_flatten.py factory 1
tile_mask.py pygen/factory_combo factory_tilemask.png 1
tile_mask.py pygen/coalmine_base coalmine_base_tilemask.png 1
tile_mask.py pygen/farm farm_tilemask.png 1
tile_mask.py pygen/farm_base farm_tilemask.png 1
tile_mask.py pygen/bank bank_tilemask.png 1
tile_mask.py pygen/bank_base bank_tilemask.png 1
building_base_flatten.py ironoremine 1
tile_mask.py pygen/ironoremine_combo ironoremine_tilemask.png 1
tile_mask.py pygen/oilrig oilrig_tilemask.png 1
custom_dither.py
cd pygen
custom_dither.py
cd ../../../

cd arctic/64/
building_shapeproc.py 1
building_baseshapeproc.py 1
building_base_flatten.py foodprocessingplant 1
tile_mask.py pygen/bank bank_tilemask.png 1
tile_mask.py pygen/bank_base bank_tilemask.png 1
building_base_flatten.py papermill 1
building_base_flatten.py printingworks 1
tile_mask.py pygen/printingworks_combo printingworks_tilemask.png 1
building_base_flatten.py goldmine 1
tile_mask.py pygen/goldmine_combo goldmine_tilemask.png 1
custom_dither.py
cd pygen
custom_dither.py
cd ../../../

cd tropical/64/
building_shapeproc.py 1
building_baseshapeproc.py 1
custom_dither.py
cd pygen
custom_dither.py
cd ../../../

cd ..
