export PATH=$PATH:$(pwd)

cd infrastructure

cd 64
infrastructure_roadrail_terrainoverlay.py 1 rail
infrastructure_roadrail_terrainoverlay.py 1 road
infrastructure_roadrail_terrainoverlay.py 1 road_noline
infrastructure_roadrail_terrainoverlay.py 1 road_town
infrastructure_roadrail_terrainoverlay.py 1 airport_modern
infrastructure_roadrail_terrainoverlay.py 1 rail_toyland
infrastructure_roadrail_terrainoverlay.py 1 road_toyland
infrastructure_roadrail_terrainoverlay.py 1 road_town_toyland
infrastructure_levelcrossing_infrastructureoverlay.py 1
infrastructure_canalriver_terrainoverlay.py 1 canal
infrastructure_canalriver_terrainoverlay.py 1 river
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd 128
infrastructure_roadrail_terrainoverlay.py 2 rail
infrastructure_roadrail_terrainoverlay.py 2 road
infrastructure_roadrail_terrainoverlay.py 2 road_noline
infrastructure_roadrail_terrainoverlay.py 2 road_town
infrastructure_roadrail_terrainoverlay.py 2 rail_toyland
infrastructure_roadrail_terrainoverlay.py 2 road_toyland
infrastructure_roadrail_terrainoverlay.py 2 road_town_toyland
infrastructure_roadrail_terrainoverlay.py 2 airport_modern
infrastructure_levelcrossing_infrastructureoverlay.py 2
infrastructure_canalriver_terrainoverlay.py 2 canal
infrastructure_canalriver_terrainoverlay.py 2 river
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd 256
infrastructure_roadrail_terrainoverlay.py 4 rail
infrastructure_roadrail_terrainoverlay.py 4 road
infrastructure_roadrail_terrainoverlay.py 4 road_noline
infrastructure_roadrail_terrainoverlay.py 4 road_town
infrastructure_roadrail_terrainoverlay.py 4 rail_toyland
infrastructure_roadrail_terrainoverlay.py 4 road_toyland
infrastructure_roadrail_terrainoverlay.py 4 road_town_toyland
infrastructure_roadrail_terrainoverlay.py 4 airport_modern
infrastructure_levelcrossing_infrastructureoverlay.py 4
infrastructure_canalriver_terrainoverlay.py 4 canal
infrastructure_canalriver_terrainoverlay.py 4 river
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd ..

cd signals

cd 64
custom_dither.py
cd ..

cd 256
custom_dither.py
cd ..

cd ..
