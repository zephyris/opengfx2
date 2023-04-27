# Make grf outputs
# Builds the output grfs (does not process image files from sources)
# If given an argument, copies the grfs to that path once complete

if [ ! -d grf ]; then
  mkdir grf
fi

cd towns
nmlc OpenGFX_EZ_Towns.nml
mv OpenGFX_EZ_Towns.grf ../grf
cd ..

cd landscape
nmlc OpenGFX_EZ_Landscape.nml
mv OpenGFX_EZ_Landscape.grf ../grf
cd ..

if [ ! -z "$1" ]; then
  cd grf
  cp *.grf "$1"
  cd ..
fi