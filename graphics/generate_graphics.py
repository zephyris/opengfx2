import os
from custom_dither import custom_dither_directory

base_path = os.path.dirname(__file__)

# effects
custom_dither_directory(os.path.join(base_path, "effects", "64"))
custom_dither_directory(os.path.join(base_path, "effects", "256"))

# infrastructure
# bridges
from bridges.bridge_infrastructureoverlay import infrastructure_bridge_infrastructureoverlay
modes = ["bridges", "railramps", "roadramps", "bridges_toyland", "railramps_toyland", "roadramps_toyland"]
scales = [1, 4]
for scale in scales:
    for mode in modes:
        infrastructure_bridge_infrastructureoverlay(scale, mode, os.path.join(base_path, "bridges", str(scale * 64)))
    custom_dither_directory(os.path.join(base_path, "bridges", str(scale * 64)))
    custom_dither_directory(os.path.join(base_path, "bridges", str(scale * 64), "pygen"))
