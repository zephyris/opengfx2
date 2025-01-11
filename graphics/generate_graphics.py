import os
from custom_dither import custom_dither_directory

base_path = os.path.dirname(__file__)

# effects
for scale in [1, 4]:
    custom_dither_directory(os.path.join(base_path, "effects", str(scale * 64)))

# infrastructure
# roads and rail
from infrastructure.roadrail_terrainoverlay import infrastructure_roadrail_terrainoverlay
modes = ["rail", "road", "road_noline", "road_town", "airport_modern", "rail_toyland", "road_toyland", "road_town_toyland"]
for scale in [1, 2, 4]:
    for mode in modes:
        try:
            infrastructure_roadrail_terrainoverlay(scale, mode, os.path.join(base_path, "infrastructure", str(scale * 64)))
        except:
            print("Failed to generate "+mode+" at scale "+str(scale))
# level crossings
from infrastructure.levelcrossing_infrastructureoverlay import infrastructure_levelcrossing_infrastructureoverlay
for scale in [1, 2, 4]:
    try:
        infrastructure_levelcrossing_infrastructureoverlay(scale, os.path.join(base_path, "infrastructure", str(scale * 64)))
    except:
        print("Failed to generate level crossings at scale "+str(scale))
# rivers and canals
from infrastructure.canalriver_terrainoverlay import intrastructure_canalriver_terrainoverlay
modes = ["canal", "river"]
for scale in [1, 2, 4]:
    for mode in modes:
        try:
            intrastructure_canalriver_terrainoverlay(scale, mode, os.path.join(base_path, "infrastructure", str(scale * 64)))
        except:
            print("Failed to generate "+mode+" at scale "+str(scale))
# infrastructure custom dither
for scale in [1, 2, 4]:
    custom_dither_directory(os.path.join(base_path, "infrastructure", str(scale * 64)))
    custom_dither_directory(os.path.join(base_path, "infrastructure", str(scale * 64), "pygen"))

# rail signals
for scale in [1, 4]:
    custom_dither_directory(os.path.join(base_path, "signals", str(scale * 64)))

# bridges
from bridges.bridge_infrastructureoverlay import infrastructure_bridge_infrastructureoverlay
modes = ["bridges", "railramps", "roadramps", "bridges_toyland", "railramps_toyland", "roadramps_toyland"]
for scale in [1, 4]:
    for mode in modes:
        try:
            infrastructure_bridge_infrastructureoverlay(scale, mode, os.path.join(base_path, "bridges", str(scale * 64)))
        except:
            print("Failed to generate "+mode+" at scale "+str(scale))
    custom_dither_directory(os.path.join(base_path, "bridges", str(scale * 64)))
    custom_dither_directory(os.path.join(base_path, "bridges", str(scale * 64), "pygen"))

# selectors
for scale in [0.25, 0.5, 1, 2, 4]:
    custom_dither_directory(os.path.join(base_path, "selectors", str(scale * 64)))

# vehicles
for scale in [1, 4]:
    custom_dither_directory(os.path.join(base_path, "vehicles", str(scale * 64)))

# icons
for scale in [1, 2, 4, "climates"]:
    custom_dither_directory(os.path.join(base_path, "icons", str(scale)))
