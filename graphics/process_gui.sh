export PATH=$PATH:$(pwd)

cd fonts

# clone and update ttfs
if [ ! -d openttd-ttf ]; then
    git clone https://github.com/zephyris/openttd-ttf
fi
cd openttd-ttf
git pull
cd ..

cd ..