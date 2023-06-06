export PATH=$PATH:$(pwd)

cd terrain

cd 64
terrain_gridoverlay.py 1
terrain_shoreoverlay.py 1 normal
terrain_shoreoverlay.py 1 toyland
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd 128
terrain_gridoverlay.py 2
terrain_shoreoverlay.py 2 normal
terrain_shoreoverlay.py 2 toyland
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd 256
terrain_gridoverlay.py 4
terrain_shoreoverlay.py 4 normal
terrain_shoreoverlay.py 4 toyland
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd ..

cd foundations

cd 64
custom_dither.py
cd ..

#cd 128
#custom_dither.py
#cd ..

cd 256
custom_dither.py
cd ..

cd ..
