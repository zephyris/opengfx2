# Make all graphics filed
# Processes image files from sources

if [ ! -d graphics/fonts/openttd-ttf ]; then
    cd graphics/fonts && git clone https://github.com/zephyris/openttd-ttf
fi
cd graphics/fonts && git pull
python3 graphics/generate_graphics.py
