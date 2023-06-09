# Make grf outputs
# Builds the output grfs (does not process image files from sources)
# If given an argument, copies the grfs to that path once complete
# eg. /my/install/of/openttd/newgrf/

cd newgrf
python3 ../templates/nml_preprocessor.py ogfx2_settings 8
mv ogfx2_settings_8.nml ogfx2_settings.nml
nmlc ogfx2_settings.nml --quiet -c -l lang/settings

if [ ! -z "$1" ]; then
  cp *.grf "$1"
fi

cd ..
