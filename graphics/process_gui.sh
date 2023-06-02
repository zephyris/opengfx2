export PATH=$PATH:$(pwd)

cd fonts
font_convert.py
cd ..

cd cursors

cd 1
custom_dither.py
gui_cursoroverlay.py 1
cd pygen
custom_dither.py
cd ../..

cd ..

cd icons

cd 1
custom_dither.py
cd ..

cd 2
custom_dither.py
cd ..

cd ..
