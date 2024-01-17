export PATH=$PATH:$(pwd)

cd industries

cd temperate/

cd 64/
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
rm bank_palmask.png # remove bank palmask to allow patina roof effects
custom_dither.py
identical_regions.py coalmine ../coalmine_idmap.png
cd ../../

cd 256/
building_shapeproc.py 4 temperate
building_baseshapeproc.py 4 temperate
mask_tiles.py pygen/bank bank_tilemask.png 4
mask_tiles.py pygen/bank_base bank_tilemask.png 4
custom_dither.py
cd pygen
rm bank_palmask.png # remove bank palmask to allow patina roof effects
custom_dither.py
cd ../../

cd ..

cd temperate/256/
building_shapeproc.py 4 temperate
building_baseshapeproc.py 4 temperate
mask_tiles.py pygen/bank bank_tilemask.png 4
mask_tiles.py pygen/bank_base bank_tilemask.png 4
custom_dither.py
cd pygen
rm bank_palmask.png # remove bank palmask to allow patina roof effects
custom_dither.py
cd ../../../

cd temperate/256/
building_shapeproc.py 4 temperate
building_baseshapeproc.py 4 temperate
mask_tiles.py pygen/bank bank_tilemask.png 4
mask_tiles.py pygen/bank_base bank_tilemask.png 4
custom_dither.py
cd pygen
rm bank_palmask.png # remove bank palmask to allow patina roof effects
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
identical_regions.py copperoremine ../copperoremine_idmap.png
cd ../../../

cd toyland/64/
if [ ! -d pygen ]; then
  mkdir pygen
fi
building_baseshapeproc.py 1 toyland
cp -p fizzy_drink_factory_32bpp.png pygen/
cp -p fizzy_drink_factory_palmask.png pygen/
mask_tiles.py pygen/fizzy_drink_factory fizzy_drink_factory_tilemask.png 1
cp -p toy_shop_32bpp.png pygen/
building_base_flatten.py toy_shop 1
mask_tiles.py pygen/toy_shop toy_shop_tilemask.png 1
cp -p toy_factory_32bpp.png pygen/
cp -p toy_factory_constr_32bpp.png pygen/
mask_tiles.py pygen/toy_factory toy_factory_tilemask.png 1
mask_tiles.py pygen/toy_factory_constr toy_factory_constr_tilemask.png 1
cp -p sweet_factory_32bpp.png pygen/
mask_tiles.py pygen/sweet_factory toy_shop_tilemask.png 1
cp -p toffee_quarry_32bpp.png pygen/
mask_tiles.py pygen/toffee_quarry toffee_quarry_tilemask.png 1
cp -p bubble_generator_32bpp.png pygen/
cp -p bubble_generator_palmask.png pygen/
mask_tiles.py pygen/bubble_generator bubble_generator_tilemask.png 1
cp -p sugar_mine_stand_32bpp.png pygen/
cp -p sugar_mine_stockpile_32bpp.png pygen/
mask_tiles.py pygen/sugar_mine_stand sugar_mine_stand_tilemask.png 1
mask_tiles.py pygen/sugar_mine_stockpile sugar_mine_stockpile_tilemask.png 1
custom_dither.py
cd pygen
custom_dither.py
cd ../../../

cd tropical/256/
custom_dither.py
cd ../..

cd arctic/256/
custom_dither.py
cd ../..

cd ..
