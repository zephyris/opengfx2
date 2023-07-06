# Make all outputs
# Processes image files from sources then builds the output grfs
# If given an argument, copies the base and new grfs to the appropriate subdirectories of that install once complete
# eg. /my/install/of/openttd/

bash make_graphics.sh

if [ ! -z "$1" ]; then
  bash make_newgrfs.sh "$1/newgrf/"
else
  bash make_newgrfs.sh
fi

if [ ! -z "$1" ]; then
  bash make_baseset.sh 8 "$1/baseset/"
  bash make_baseset.sh 32ez "$1/baseset/"
else
  bash make_baseset.sh 8
  bash make_baseset.sh 32ez
fi
