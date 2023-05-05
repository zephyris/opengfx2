# Make grf outputs
# Builds the output grfs (does not process image files from sources)
# If given an argument, copies the grfs to that path once complete
# eg. /my/install/of/openttd/newgrf/

if [ ! -d newgrf ]; then
  mkdir newgrf
fi

cd towns
nmlc OpenGFX_EZ_Towns.nml --quiet -c
mv OpenGFX_EZ_Towns.grf ../newgrf
cd ..

cd landscape
nmlc OpenGFX_EZ_Landscape.nml --quiet -c
mv OpenGFX_EZ_Landscape.grf ../newgrf
cd ..

if [ ! -z "$1" ]; then
  cd newgrf
  cp *.grf "$1"
  cd ..
fi