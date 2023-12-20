export PATH=$PATH:$(pwd)

cd fonts

# clone and update ttfs
if [ ! -d openttd-ttf ]; then
    git clone https://github.com/zephyris/openttd-ttf
fi
cd openttd-ttf
git pull
cd ..

if [ ! -d 1 ]; then
    mkdir 1
fi
cd 1
if [ ! -d pygen ]; then
    mkdir pygen
fi
cd ..
if [ ! -d 2 ]; then
    mkdir 2
fi
cd 2
if [ ! -d pygen ]; then
    mkdir pygen
fi
cd ..
if [ ! -d 4 ]; then
    mkdir 4
fi
cd 4
if [ ! -d pygen ]; then
    mkdir pygen
fi
cd ..

fonts_charactergrab.py
