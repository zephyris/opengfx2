export PATH=$PATH:$(pwd)

cd bridges

cd 64
infrastructure_bridge_infrastructureoverlay.py 1 bridges
infrastructure_bridge_infrastructureoverlay.py 1 railramps
infrastructure_bridge_infrastructureoverlay.py 1 roadramps
infrastructure_bridge_infrastructureoverlay.py 1 bridges_toyland
infrastructure_bridge_infrastructureoverlay.py 1 railramps_toyland
infrastructure_bridge_infrastructureoverlay.py 1 roadramps_toyland
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd 256
infrastructure_bridge_infrastructureoverlay.py 4 bridges
infrastructure_bridge_infrastructureoverlay.py 4 railramps
infrastructure_bridge_infrastructureoverlay.py 4 roadramps
infrastructure_bridge_infrastructureoverlay.py 4 bridges_toyland
infrastructure_bridge_infrastructureoverlay.py 4 railramps_toyland
infrastructure_bridge_infrastructureoverlay.py 4 roadramps_toyland
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd ..
