# Make grf outputs
# Builds the output grfs (does not process image files from sources)
# If given an argument, copies the grfs to that path once complete
# eg. /my/install/of/openttd/newgrf/

cd newgrf
python3 ../templates/nml_preprocessor.py ogfx2_controller
nmlc ogfx2_controller.nml --quiet -c -l lang/controller

python3 ../templates/nml_preprocessor.py ogfx2_landscape
nmlc ogfx2_landscape.nml --quiet -c -l lang/landscape

if [ ! -z "$1" ]; then
  cp *.grf "$1"
fi

cd ..
