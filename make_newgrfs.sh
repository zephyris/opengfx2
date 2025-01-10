# Make grf outputs
# Builds the output grfs (does not process image files from sources)
# If given an argument, copies the grfs to that path once complete
# eg. /my/install/of/openttd/newgrf/

cd newgrf

# Settings
python3 ../templates/nml_preprocessor.py ogfx2_settings.pnml 8 exclude_name_suffix
nmlc ogfx2_settings.nml --quiet -c -l lang/settings

# Landscape
python3 ../templates/nml_preprocessor.py ogfx2_landscape.pnml 32ez exclude_name_suffix
nmlc ogfx2_landscape.nml --quiet -c -l lang/landscape

# Stations
python3 ../templates/nml_preprocessor.py ogfx2_stations.pnml 32ez exclude_name_suffix
nmlc ogfx2_stations.nml --quiet -c -l lang/stations

# Trees
python3 ../templates/nml_preprocessor.py ogfx2_trees.pnml 32ez exclude_name_suffix
nmlc ogfx2_trees.nml --quiet -c -l lang/trees

# Objects
python3 ../templates/nml_preprocessor.py ogfx2_objects.pnml 32ez exclude_name_suffix
nmlc ogfx2_objects.nml --quiet -c -l lang/objects

if [ ! -z "$1" ]; then
  cp *.grf "$1"
fi

cd ..
