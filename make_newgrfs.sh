# Make grf outputs
# Builds the output grfs (does not process image files from sources)
# If given an argument, copies the grfs to that path once complete
# eg. /my/install/of/openttd/newgrf/

# "8, 8ez, 32 or 32ez"
alternates="8"
if [ ! -z "$1" ]; then
  alternates=$1
fi

cd newgrf
python3 ../templates/nml_preprocessor.py ogfx2_settings $alternates
nmlc ogfx2_settings.nml --quiet -c -l lang/settings

if [ ! -z "$2" ]; then
  cp *.grf "$2"
fi

cd ..
