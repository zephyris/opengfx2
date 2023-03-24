export PATH=$PATH:$(pwd)

cd terrain

cd 64
terrain_shoreoverlay.py 1
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd 128
terrain_shoreoverlay.py 2
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd 256
terrain_shoreoverlay.py 4
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd ..
