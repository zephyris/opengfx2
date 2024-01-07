# Make grf outputs
# Builds the output grfs (does not process image files from sources)
# If given an argument, copies the grfs to that path once complete
# eg. /my/install/of/openttd/newgrf/

cd newgrf

# Settings
python3 ../templates/nml_preprocessor.py ogfx2_settings 8
mv ogfx2_settings_8.nml ogfx2_settings.nml
nmlc ogfx2_settings.nml --quiet -c -l lang/settings

# Landscape
python3 ../templates/nml_preprocessor.py ogfx2_landscape 32ez
mv ogfx2_landscape_32ez.nml ogfx2_landscape.nml
nmlc ogfx2_landscape.nml --quiet -c -l lang/landscape

# Stations
python3 ../templates/nml_preprocessor.py ogfx2_stations 32ez
mv ogfx2_stations_32ez.nml ogfx2_stations.nml
nmlc ogfx2_stations.nml --quiet -c -l lang/stations

# Trees
python3 ../templates/nml_preprocessor.py ogfx2_trees 32ez
mv ogfx2_trees_32ez.nml ogfx2_trees.nml
nmlc ogfx2_trees.nml --quiet -c -l lang/trees

# Objects
python3 ../templates/nml_preprocessor.py ogfx2_objects 32ez
mv ogfx2_objects_32ez.nml ogfx2_objects.nml
nmlc ogfx2_objects.nml --quiet -c -l lang/objects

if [ ! -z "$1" ]; then
  cp *.grf "$1"
fi

cd ..
