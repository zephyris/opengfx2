export PATH=$PATH:$(pwd)

cd terrain

cd 64
terrain_gridoverlay.py 1
terrain_shoreoverlay.py 1 normal
terrain_shoreoverlay.py 1 toyland
terrain_watergridoverlay.py 1 water
terrain_watergridoverlay.py 1 shore
terrain_watergridoverlay.py 1 watertoyland
terrain_watergridoverlay.py 1 shoretoyland
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd 128
terrain_gridoverlay.py 2
terrain_shoreoverlay.py 2 normal
terrain_shoreoverlay.py 2 toyland
terrain_watergridoverlay.py 2 water
terrain_watergridoverlay.py 2 shore
terrain_watergridoverlay.py 2 watertoyland
terrain_watergridoverlay.py 2 shoretoyland
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd 256
terrain_gridoverlay.py 4
terrain_shoreoverlay.py 4 normal
terrain_shoreoverlay.py 4 toyland
terrain_watergridoverlay.py 4 water
terrain_watergridoverlay.py 4 shore
terrain_watergridoverlay.py 4 watertoyland
terrain_watergridoverlay.py 4 shoretoyland
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd ..

cd foundations

cd 64
custom_dither.py
identical_regions.py foundations_temperate foundations_idmap.png
identical_regions.py foundations_arctic foundations_idmap.png
identical_regions.py foundations_tropical foundations_idmap.png
identical_regions.py foundations_toyland foundations_idmap.png
cd ..

#cd 128
#custom_dither.py
#cd ..

cd 256
custom_dither.py
identical_regions.py foundations_temperate foundations_idmap.png
identical_regions.py foundations_arctic foundations_idmap.png
identical_regions.py foundations_tropical foundations_idmap.png
identical_regions.py foundations_toyland foundations_idmap.png
cd ..

cd ..
