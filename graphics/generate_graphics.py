import os
from custom_dither import custom_dither_directory
from strict_convert import strict_convert_directory

base_path = os.path.dirname(__file__)

# fonts
from fonts.charactergrab import fonts_charactergrab
fonts_charactergrab(os.path.join(base_path, "fonts"))
for scale in [1, 2, 4]:
    strict_convert_directory(os.path.join(base_path, "fonts", str(scale)))
    strict_convert_directory(os.path.join(base_path, "fonts", str(scale), "pygen"))

# icons
for scale in [1, 2, 4, "climates"]:
    custom_dither_directory(os.path.join(base_path, "icons", str(scale)))

# cursors
from cursors.cursoroverlay import cursors_cursoroverlay
for scale in [1, 2]:
    cursors_cursoroverlay(os.path.join(base_path, "cursors", str(scale)), scale)
    custom_dither_directory(os.path.join(base_path, "gui", str(scale)))
    custom_dither_directory(os.path.join(base_path, "gui", str(scale), "pygen"))

# effects
for scale in [1, 4]:
    custom_dither_directory(os.path.join(base_path, "effects", str(scale * 64)))

# terrain
# ground tiles
from terrain.gridoverlay import terrain_gridoverlay
from terrain.shoreoverlay import terrain_shoreoverlay
shore_modes = ["normal", "toyland"]
from terrain.watergridoverlay import terrain_watergridoverlay
watergrid_modes = ["water", "shore", "watertoyland", "shoretoyland"]
for scale in [1, 2, 4]:
    try:
        terrain_gridoverlay(scale, os.path.join(base_path, "terrain", str(scale * 64)))
    except:
        print("Failed to generate ground gridlines at scale "+str(scale))
    for mode in shore_modes:
        try:
            terrain_shoreoverlay(scale, mode, os.path.join(base_path, "terrain", str(scale * 64)))
        except:
            print("Failed to generate "+mode+" shore at scale "+str(scale))
    for mode in watergrid_modes:
        try:
            terrain_watergridoverlay(scale, mode, os.path.join(base_path, "terrain", str(scale * 64)))
        except:
            print("Failed to generate "+mode+" water gridlines at scale "+str(scale))
    custom_dither_directory(os.path.join(base_path, "terrain", str(scale * 64)))
    custom_dither_directory(os.path.join(base_path, "terrain", str(scale * 64), "pygen"))

# foundations
from identical_regions import identical_regions
modes = ["temperate", "arctic", "tropical", "toyland"]
for scale in [1, 4]:
    custom_dither_directory(os.path.join(base_path, "foundations_"+str(scale * 64)))
    for mode in modes:
        try:
            identical_regions(os.path.join(base_path, "foundations", str(scale * 64), "foundations_"+mode), os.path.join(base_path, "foundations", str(scale *64), "foundations_idmap.png"))
        except:
            print("Failed to identical region mask "+mode+" foundations at scale "+str(scale))

# trees
from trees.shapeproc import tree_shapeproc
snowy = ["false", "true"]
for scale in [1, 4]:
    for snow in snowy:
        try:
            tree_shapeproc(scale, snow, os.path.join(base_path, "trees", str(scale * 64)))
        except:
            print("Failed to generate trees at scale "+str(scale)+" with snow "+snow)
    custom_dither_directory(os.path.join(base_path, "trees", str(scale * 64)))
    custom_dither_directory(os.path.join(base_path, "trees", str(scale * 64), "pygen"))

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
