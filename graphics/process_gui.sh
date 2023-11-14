export PATH=$PATH:$(pwd)

cd fonts

cd 1
font_convert.py
cd ..

cd 2
font_convert.py
cd ..

cd ..

cd cursors

cd 1
custom_dither.py
gui_cursoroverlay.py 1
cd pygen
custom_dither.py
cd ../..

cd 2
custom_dither.py
gui_cursoroverlay.py 2
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
