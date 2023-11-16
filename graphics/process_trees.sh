export PATH=$PATH:$(pwd)

cd trees

cd 64
tree_shapeproc.py 1
tree_shapeproc.py 1 True
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd 256
tree_shapeproc.py 4
tree_shapeproc.py 4 True
cd pygen
custom_dither.py
cd ../..

cd ..
