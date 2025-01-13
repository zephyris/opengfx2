import os, shutil
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
snowy = [False, True]
for scale in [1, 4]:
    for snow in snowy:
        try:
            tree_shapeproc(os.path.join(base_path, "trees", str(scale * 64)), scale, snow)
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

# towns
# street furniture
for scale in [1, 4]:
    custom_dither_directory(os.path.join(base_path, "towns", "streetfurniture", str(scale * 64)))
# buildings
from towns.shapeproc import buildings_shapeproc
from towns.baseshapeproc import buildings_baseshapeproc
climates = ["temperate", "tropical", "arctic", "toyland"]
for climate in climates:
    snowy = [False]
    if climate == "arctic":
        snowy = [False, True]
    for scale in [1, 4]:
        for snow in snowy:
            try:
                buildings_shapeproc(scale, climate, snow, os.path.join(base_path, "towns", climate, str(scale * 64)))
            except:
                print("Failed to generate buildings at scale "+str(scale)+" with snow "+str(snow))
            try:
                buildings_baseshapeproc(scale, climate, snow, os.path.join(base_path, "towns", climate, str(scale * 64)))
            except:
                print("Failed to generate base buildings at scale "+str(scale)+" with snow "+str(snow))
# special handling
# currently handles scales independently - can be replaced with a scale in [1, 4] loop once all source sprites exist
from towns.base_flatten import buildings_base_flatten
from mask_tiles import mask_tiles
## temperate
### scale 1
scale = 1
current_path = os.path.join(base_path, "towns", "temperate", str(scale * 64))
#### flatten
flatten_list = ["bungalow", "2x2_mallandstadia", "hqs"]
for name in flatten_list:
    buildings_base_flatten(os.path.join(current_path, "pygen", name), scale)
#### tile mask
mask_list = {
    "2x1_hotel": "2x1_hotel_tilemask.png",
    "2x2_mallandstadia": "2x2_mallandstadia_tilemask.png",
    "2x2_mallandstadia_base": "2x2_mallandstadia_tilemask.png",
    "2x2_mallandstadia_combo": "2x2_mallandstadia_base_tilemask.png",
    "hqs_combo": "hqs_tilemask.png"
}
for name, mask in mask_list.items():
    mask_tiles(os.path.join(current_path, "pygen", name), os.path.join(current_path, mask), scale)
### scale 4
scale = 4
current_path = os.path.join(base_path, "towns", "temperate", str(scale * 64))
mask_tiles(os.path.join(current_path, "pygen", "2x1_hotel"), os.path.join(current_path, "2x1_hotel_tilemask.png"), scale)
## tropical
### scale 1
scale = 1
current_path = os.path.join(base_path, "towns", "tropical", str(scale * 64))
#### manual copy
shutil.copy(os.path.join(base_path, "towns", "temperate", str(scale * 64), "pygen", "hqs_32bpp.png"), os.path.join(current_path, "pygen"))
shutil.copy(os.path.join(base_path, "towns", "temperate", str(scale * 64), "pygen", "hqs_palmask.png"), os.path.join(current_path, "pygen"))
#### flatten
flatten_list = ["churches", "houses", "flats", "1x2_tallofficeblock", "shantyhouses", "tallofficeblock", "hqs"]
for name in flatten_list:
    buildings_base_flatten(os.path.join(current_path, "pygen", name), scale)
#### tile mask
mask_list = {
    "1x2_tallofficeblock": "1x2_tallofficeblock_tilemask.png",
    "hqs": os.path.join(base_path, "towns", "temperate", str(scale * 64), "hqs_tilemask.png")
}
for name, mask in mask_list.items():
    mask_tiles(os.path.join(current_path, "pygen", name), os.path.join(current_path, mask), scale)
## arctic
### scale 1
scale = 1
current_path = os.path.join(base_path, "towns", "arctic", str(scale * 64))
#### manual copy
shutil.copy(os.path.join(base_path, "towns", "temperate", str(scale * 64), "pygen", "hqs_32bpp.png"), os.path.join(current_path, "pygen"))
shutil.copy(os.path.join(base_path, "towns", "temperate", str(scale * 64), "pygen", "hqs_palmask.png"), os.path.join(current_path, "pygen"))
#### flatten
flatten_list = ["shopsandoffices", "tallofficeblock", "church", "2x1_hotel", "2x1_hotel_snow", "hqs"]
for name in flatten_list:
    buildings_base_flatten(os.path.join(current_path, "pygen", name), scale)
#### tile mask
mask_list = {
    "1x2_tallofficeblock": "1x2_tallofficeblock_tilemask.png",
    "1x2_tallofficeblock_snow": "1x2_tallofficeblock_tilemask.png",
    "1x2_tallofficeblock_base": "1x2_tallofficeblock_tilemask.png",
    "2x1_hotel_combo": "2x1_hotel_tilemask.png",
    "2x1_hotel_snow_combo": "2x1_hotel_tilemask.png",
    "hqs_combo": os.path.join(base_path, "towns", "temperate", str(scale * 64), "hqs_tilemask.png")
}
for name, mask in mask_list.items():
    mask_tiles(os.path.join(current_path, "pygen", name), os.path.join(current_path, mask), scale)
## toyland
### scale 1
scale = 1
current_path = os.path.join(base_path, "towns", "toyland", str(scale * 64))
#### manual copy
shutil.copy(os.path.join(base_path, current_path, "2x1_boot_32bpp.png"), os.path.join(current_path, "pygen"))
#### tile mask
mask_list = {
    "2x1_boot": "2x1_boot_tilemask.png",
    "hqs_toyland": "hqs_tilemask.png"
}
for name, mask in mask_list.items():
    mask_tiles(os.path.join(current_path, "pygen", name), os.path.join(current_path, mask), scale)
# dither everyting
for climate in climates:
    for scale in [1, 4]:
        custom_dither_directory(os.path.join(base_path, "towns", climate, str(scale * 64)))
        custom_dither_directory(os.path.join(base_path, "towns", climate, str(scale * 64), "pygen"))
