export PATH=$PATH:$(pwd)

cd towns

cd streetfurniture/64/
custom_dither.py
cd ../../

cd streetfurniture/256/
custom_dither.py
cd ../../

cd temperate/64/
building_shapeproc.py 1 temperate
building_baseshapeproc.py 1 temperate
building_base_flatten.py bungalow 1
building_base_flatten.py 2x2_mallandstadia 1
mask_tiles.py pygen/2x1_hotel 2x1_hotel_tilemask.png 1
mask_tiles.py pygen/2x2_mallandstadia 2x2_mallandstadia_tilemask.png 1
mask_tiles.py pygen/2x2_mallandstadia_base 2x2_mallandstadia_tilemask.png 1
mask_tiles.py pygen/2x2_mallandstadia_combo 2x2_mallandstadia_base_tilemask.png 1
building_base_flatten.py hqs 1
mask_tiles.py pygen/hqs_combo hqs_tilemask.png 1
cd pygen
custom_dither.py
cd ../../../

cd tropical/64/
building_shapeproc.py 1 tropical
building_baseshapeproc.py 1 tropical
building_base_flatten.py churches 1
building_base_flatten.py houses 1
building_base_flatten.py flats 1
building_base_flatten.py 1x2_tallofficeblock 1
mask_tiles.py pygen/1x2_tallofficeblock_combo 1x2_tallofficeblock_tilemask.png 1
building_base_flatten.py shantyhouses 1
building_base_flatten.py tallofficeblock 1
cp -p ../../temperate/64/pygen/hqs_32bpp.png pygen/
cp -p ../../temperate/64/pygen/hqs_palmask.png pygen/
building_base_flatten.py hqs 1
mask_tiles.py pygen/hqs_combo ../../temperate/64/hqs_tilemask.png 1
cd pygen
custom_dither.py
cd ../../../

cd arctic/64/
building_shapeproc.py 1 arctic
building_shapeproc.py 1 arctic True
building_baseshapeproc.py 1 arctic
building_baseshapeproc.py 1 arctic True
building_base_flatten.py shopsandoffices 1
building_base_flatten.py tallofficeblock 1
building_base_flatten.py church 1
building_base_flatten.py 2x1_hotel 1
building_base_flatten.py 2x1_hotel_snow 1
mask_tiles.py pygen/1x2_tallofficeblock 1x2_tallofficeblock_tilemask.png 1
mask_tiles.py pygen/1x2_tallofficeblock_snow 1x2_tallofficeblock_tilemask.png 1
mask_tiles.py pygen/1x2_tallofficeblock_base 1x2_tallofficeblock_tilemask.png 1
mask_tiles.py pygen/2x1_hotel_combo 2x1_hotel_tilemask.png 1
mask_tiles.py pygen/2x1_hotel_snow_combo 2x1_hotel_tilemask.png 1
cp -p ../../temperate/64/pygen/hqs_32bpp.png pygen/
cp -p ../../temperate/64/pygen/hqs_palmask.png pygen/
building_base_flatten.py hqs 1
mask_tiles.py pygen/hqs_combo ../../temperate/64/hqs_tilemask.png 1
cd pygen
custom_dither.py
cd ../../../

cd toyland/64/
if [ ! -d pygen ]; then
  mkdir pygen
fi
cp -p 2x1_boot_32bpp.png pygen/
mask_tiles.py pygen/2x1_boot 2x1_boot_tilemask.png 1
building_shapeproc.py 1 toyland
mask_tiles.py pygen/hqs_toyland hqs_tilemask.png 1
custom_dither.py
cd pygen
custom_dither.py
cd ../../../

cd temperate/256/
building_shapeproc.py 4 temperate
building_baseshapeproc.py 4 temperate
mask_tiles.py pygen/2x1_hotel 2x1_hotel_tilemask.png 4
cd pygen
custom_dither.py
cd ../../../

cd ..
