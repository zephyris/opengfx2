cd graphics
bash process_terrain.sh
bash process_buildings.sh
bash process_industries.sh
bash process_infrastructure.sh
bash process_bridges.sh
bash process_selectors.sh
bash process_trees.sh
bash process_effects.sh
cd ..

cd towns
nmlc OpenGFX_EZ_Towns.nml
mv OpenGFX_EZ_Towns.grf ../grf
cd ..

cd landscape
nmlc OpenGFX_EZ_Landscape.nml
mv OpenGFX_EZ_Landscape.grf ../grf
cd ..
