export PATH=$PATH:$(pwd)

cd stations

cd general/64
building_shapeproc.py 1
tile_mask.py pygen/raildepots raildepots_tilemask.png 1
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd ..