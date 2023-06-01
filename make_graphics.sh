# Make all graphics filed
# Processes image files from sources

cd graphics
bash process_gui.sh
bash process_terrain.sh
bash process_buildings.sh
bash process_industries.sh
bash process_infrastructure.sh
bash process_bridges.sh
bash process_stations.sh
bash process_selectors.sh
bash process_trees.sh
bash process_effects.sh
bash process_vehicles.sh
cd ..
