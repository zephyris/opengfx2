export PATH=$PATH:$(pwd)

cd stations

cd general/64
building_shapeproc.py 1
mask_regions.py pygen/raildepots raildepots_regionmask.png 1
mask_regions.py pygen/maglevdepots maglevdepots_regionmask.png 1
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd ..