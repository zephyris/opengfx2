export PATH=$PATH:$(pwd)

cd trees

cd 64
custom_dither.py
cd ..

cd 64_alt
tree_shapeproc.py 1
tree_shapeproc.py 1 True
cd pygen
custom_dither.py
cd ../..

cd 256
custom_dither.py
cd ..

cd 256_alt
tree_shapeproc.py 4
tree_shapeproc.py 4 True
cd pygen
custom_dither.py
cd ../..

cd ..
