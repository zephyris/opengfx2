export PATH=$PATH:$(pwd)

cd stations

cd general/64
building_shapeproc.py 1
building_shapeproc.py 1 True
mask_regions.py pygen/raildepots raildepots_regionmask.png 1
mask_regions.py pygen/raildepots_snow raildepots_regionmask.png 1
mask_regions.py pygen/monoraildepots monoraildepots_regionmask.png 1
mask_regions.py pygen/monoraildepots_snow monoraildepots_regionmask.png 1
mask_regions.py pygen/maglevdepots maglevdepots_regionmask.png 1
mask_regions.py pygen/maglevdepots_snow maglevdepots_regionmask.png 1
mask_regions.py pygen/roaddepots roaddepots_regionmask.png 1
mask_regions.py pygen/roaddepots_snow roaddepots_regionmask.png 1
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd ..
