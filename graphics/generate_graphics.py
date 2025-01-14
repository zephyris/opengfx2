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
    custom_dither_directory(os.path.join(base_path, "cursors", str(scale)))
    custom_dither_directory(os.path.join(base_path, "cursors", str(scale), "pygen"))

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
    buildings_base_flatten(os.path.join(current_path, name), scale)
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
    buildings_base_flatten(os.path.join(current_path, name), scale)
#### tile mask
mask_list = {
    "1x2_tallofficeblock_combo": "1x2_tallofficeblock_tilemask.png",
    "hqs_combo": os.path.join(base_path, "towns", "temperate", str(scale * 64), "hqs_tilemask.png")
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
    buildings_base_flatten(os.path.join(current_path, name), scale)
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

# industries
# buildings
from identical_regions import identical_regions
from towns.shapeproc import buildings_shapeproc
from towns.baseshapeproc import buildings_baseshapeproc
climates = ["temperate", "tropical", "arctic", "toyland"]
for climate in climates:
    for scale in [1, 4]:
        snow = False
        try:
            buildings_shapeproc(scale, climate, snow, os.path.join(base_path, "industries", climate, str(scale * 64)))
        except:
            print("Failed to generate buildings at scale "+str(scale)+" with snow "+str(snow))
        try:
            if climate == "tropical":
                # exception for topical, where all industries with groundtiles are on desert
                buildings_baseshapeproc(scale, "tropicaldesert", snow, os.path.join(base_path, "industries", climate, str(scale * 64)))
            else:
                buildings_baseshapeproc(scale, climate, snow, os.path.join(base_path, "industries", climate, str(scale * 64)))
        except:
            print("Failed to generate base buildings at scale "+str(scale)+" with snow "+str(snow))
# special handling
from towns.base_flatten import buildings_base_flatten
from mask_tiles import mask_tiles
# currently handles scales independently - can be replaced with a scale in [1, 4] loop once all source sprites exist
## temperate
### scale 1
scale = 1
current_path = os.path.join(base_path, "industries", "temperate", str(scale * 64))
#### flatten
flatten_list = ["steelmill", "factory", "ironoremine"]
for name in flatten_list:
    buildings_base_flatten(os.path.join(current_path, name), scale)
#### tile mask
mask_list = {
    "steelmill_combo": "steelmill_tilemask.png",
    "factory_combo": "factory_tilemask.png",
    "coalmine_base": "coalmine_base_tilemask.png",
    "farm": "farm_tilemask.png",
    "farm_base": "farm_tilemask.png",
    "bank": "bank_tilemask.png",
    "bank_base": "bank_tilemask.png",
    "ironoremine_combo": "ironoremine_tilemask.png",
    "oilrig": "oilrig_tilemask.png"
}
for name, mask in mask_list.items():
    mask_tiles(os.path.join(current_path, "pygen", name), os.path.join(current_path, mask), scale)
### scale 4
scale = 4
current_path = os.path.join(base_path, "industries", "temperate", str(scale * 64))
#### tile mask
mask_list = {
    "bank": "bank_tilemask.png",
    "bank_base": "bank_tilemask.png",
}
for name, mask in mask_list.items():
    mask_tiles(os.path.join(current_path, "pygen", name), os.path.join(current_path, mask), scale)
## arctic
### scale 1
scale = 1
current_path = os.path.join(base_path, "industries", "arctic", str(scale * 64))
#### flatten
flatten_list = ["foodprocessingplant", "papermill", "printingworks", "goldmine"]
for name in flatten_list:
    buildings_base_flatten(os.path.join(current_path, name), scale)
#### tile mask
mask_list = {
    "bank": "bank_tilemask.png",
    "bank_base": "bank_tilemask.png",
    "farm": "farm_tilemask.png",
    "farm_base": "farm_tilemask.png",
    "printingworks_combo": "printingworks_tilemask.png",
    "goldmine_combo": "goldmine_tilemask.png"
}
for name, mask in mask_list.items():
    mask_tiles(os.path.join(current_path, "pygen", name), os.path.join(current_path, mask), scale)
## tropical
### scale 1
scale = 1
current_path = os.path.join(base_path, "industries", "tropical", str(scale * 64))
#### flatten
flatten_list = ["diamondmine", "lumbermill"]
for name in flatten_list:
    buildings_base_flatten(os.path.join(current_path, name), scale)
#### tile mask
mask_list = {
    "diamondmine_combo": "diamondmine_tilemask.png",
    "lumbermill_combo": "lumbermill_tilemask.png"
}
for name, mask in mask_list.items():
    mask_tiles(os.path.join(current_path, "pygen", name), os.path.join(current_path, mask), scale)
## toyland
### scale 1
scale = 1
current_path = os.path.join(base_path, "industries", "toyland", str(scale * 64))
#### manual copy
copy_list = ["fizzy_drink_factory_32bpp.png", "fizzy_drink_factory_palmask.png", "toy_shop_32bpp.png", "toy_factory_32bpp.png", "toy_factory_constr_32bpp.png", "sweet_factory_32bpp.png", "toffee_quarry_32bpp.png", "bubble_generator_32bpp.png", "bubble_generator_palmask.png", "sugar_mine_stand_32bpp.png", "sugar_mine_stockpile_32bpp.png"]
for name in copy_list:
    shutil.copy(os.path.join(current_path, name), os.path.join(current_path, "pygen"))
#### tile mask
mask_list = {
    "fizzy_drink_factory": "fizzy_drink_factory_tilemask.png",
    "toy_shop": "toy_shop_tilemask.png",
    "toy_factory": "toy_factory_tilemask.png",
    "toy_factory_constr": "toy_factory_constr_tilemask.png",
    "sweet_factory": "toy_shop_tilemask.png",
    "toffee_quarry": "toffee_quarry_tilemask.png",
    "bubble_generator": "bubble_generator_tilemask.png",
    "sugar_mine_stand": "sugar_mine_stand_tilemask.png",
    "sugar_mine_stockpile": "sugar_mine_stockpile_tilemask.png"
}
for name, mask in mask_list.items():
    mask_tiles(os.path.join(current_path, "pygen", name), os.path.join(current_path, mask), scale)
# dither everyting
for climate in climates:
    for scale in [1, 4]:
        custom_dither_directory(os.path.join(base_path, "industries", climate, str(scale * 64)))
        if climate == "temperate":
            if os.path.exists(os.path.join(base_path, "industries", climate, str(scale * 64), "pygen", "bank_palmask.png")):
                os.remove(os.path.join(base_path, "industries", climate, str(scale * 64), "pygen", "bank_palmask.png")) # remove bank palmask to allow patina roof effects
        custom_dither_directory(os.path.join(base_path, "industries", climate, str(scale * 64), "pygen"))
# identical regions
for scale in [1, 4]:
    identical_regions(os.path.join(base_path, "industries", "temperate", str(scale * 64), "pygen", "coalmine"), os.path.join(base_path, "industries", "temperate", str(scale * 64), "coalmine_idmap.png"))
    identical_regions(os.path.join(base_path, "industries", "tropical", str(scale * 64), "pygen", "copperoremine"), os.path.join(base_path, "industries", "tropical", str(scale * 64), "copperoremine_idmap.png"))

# stations
from stations.tunnels_infrastructureoverlay import stations_tunnels_infrastructureoverlay
from towns.shapeproc import buildings_shapeproc
from towns.baseshapeproc import buildings_baseshapeproc
for scale in [1, 4]:
    try:
        buildings_shapeproc(scale, "temperate", False, os.path.join(base_path, "stations", "general", str(scale * 64),))
        buildings_shapeproc(scale, "temperate", True, os.path.join(base_path, "stations", "general", str(scale * 64),))
        buildings_shapeproc(scale, "toyland", False, os.path.join(base_path, "stations", "general", str(scale * 64),))
    except:
        print("Failed to generate buildings at scale "+str(scale))
    try:
        buildings_baseshapeproc(scale, "temperate", False, os.path.join(base_path, "stations", "general", str(scale * 64)))
        buildings_baseshapeproc(scale, "toyland", False, os.path.join(base_path, "stations", "general", str(scale * 64)))
    except:
        print("Failed to generate base buildings at scale "+str(scale))
# special handling
from towns.base_flatten import buildings_base_flatten
from mask_regions import mask_regions
from mask_tiles import mask_tiles
## general
# currently handles scales independently - can be replaced with a scale in [1, 4] loop once all source sprites exist
### scale 1
scale = 1
current_path = os.path.join(base_path, "stations", "general", str(scale * 64))
#### flatten
flatten_list = ["heliport", "oldairport_multitile", "oldairport_multitile_toyland"]
for name in flatten_list:
    buildings_base_flatten(os.path.join(current_path, name), scale)
#### region mask
region_list = {
    # mask regions of depots (ie. back wall from rest of building)
    "raildepots": "raildepots_regionmask.png",
    "raildepots_toyland": "raildepots_regionmask.png",
    "monoraildepots": "monoraildepots_regionmask.png",
    "monoraildepots_toyland": "monoraildepots_regionmask.png",
    "maglevdepots": "maglevdepots_regionmask.png",
    "maglevdepots_toyland": "maglevdepots_regionmask.png",
    "roaddepots": "roaddepots_regionmask.png",
    "roaddepots_toyland": "roaddepots_regionmask.png",
    "tramdepots": "tramdepots_regionmask.png",
    "tramdepots_toyland": "tramdepots_regionmask.png",
    "shipdepots": "shipdepots_regionmask.png",
    "shipdepots_toyland": "shipdepots_regionmask.png",
    "modernairdepots": "modernairdepots_regionmask.png",
    "modernairdepots_toyland": "modernairdepots_regionmask.png",
    "oldairdepots": "oldairdepots_regionmask.png",
    "oldairdepots_toyland": "oldairdepots_regionmask.png",
    # mask regions of tunnels (ie. back wall and roadway from rest of tunnel/sloped tile)
    "railtunnels": "railtunnels_regionmask.png",
    "railtunnels_snow": "railtunnels_regionmask.png",
    "monorailtunnels": "monorailtunnels_regionmask.png",
    "monorailtunnels_snow": "monorailtunnels_regionmask.png",
    "maglevtunnels": "maglevtunnels_regionmask.png",
    "maglevtunnels_snow": "maglevtunnels_regionmask.png",
    "roadtunnels": "roadtunnels_regionmask.png",
    "roadtunnels_snow": "roadtunnels_regionmask.png",
    "nonetunnels": "nonetunnels_regionmask.png",
    "nonetunnels_snow": "nonetunnels_regionmask.png"
}
for name, mask in region_list.items():
    mask_regions(os.path.join(current_path, "pygen", name), os.path.join(current_path, mask), scale)
#### overlay tunnels onto terrain sprites
infrastructure_list = ["road", "road_toyland", "rail", "rail_toyland", "terrain"]
for infrastructure in infrastructure_list:
    stations_tunnels_infrastructureoverlay(scale, infrastructure, os.path.join(base_path, "stations", "general", str(scale * 64)))
#### tile mask
tile_list = {
    "oldairport_multitile": "oldairport_multitile_tilemask.png",
    "oldairport_multitile_combo": "oldairport_multitile_tilemask.png",
    "oldairport_multitile_toyland": "oldairport_multitile_tilemask.png",
    "oldairport_multitile_toyland_combo": "oldairport_multitile_tilemask.png"
}
for name, mask in tile_list.items():
    mask_tiles(os.path.join(current_path, "pygen", name), os.path.join(current_path, mask), scale)
### scale 4
scale = 4
current_path = os.path.join(base_path, "stations", "general", str(scale * 64))
#### region mask
region_list = {
    # mask regions of depots (ie. back wall from rest of building)
    "raildepots": "raildepots_regionmask.png",
    "raildepots_toyland": "raildepots_regionmask.png",
    "roaddepots": "roaddepots_regionmask.png",
    "roaddepots_toyland": "roaddepots_regionmask.png",
    # mask regions of tunnels (ie. back wall and roadway from rest of tunnel/sloped tile)
    "railtunnels": "railtunnels_regionmask.png",
    "railtunnels_snow": "railtunnels_regionmask.png",
    "monorailtunnels": "monorailtunnels_regionmask.png",
    "monorailtunnels_snow": "monorailtunnels_regionmask.png",
    "maglevtunnels": "maglevtunnels_regionmask.png",
    "maglevtunnels_snow": "maglevtunnels_regionmask.png",
    "roadtunnels": "roadtunnels_regionmask.png",
    "roadtunnels_snow": "roadtunnels_regionmask.png",
    "nonetunnels": "nonetunnels_regionmask.png",
    "nonetunnels_snow": "nonetunnels_regionmask.png"
}
for name, mask in region_list.items():
    mask_regions(os.path.join(current_path, "pygen", name), os.path.join(current_path, mask), scale)
#### overlay tunnels onto terrain sprites
infrastructure_list = ["road", "road_toyland", "rail", "rail_toyland", "terrain"]
for infrastructure in infrastructure_list:
    stations_tunnels_infrastructureoverlay(scale, infrastructure, os.path.join(base_path, "stations", "general", str(scale * 64)))
# dither everything
for scale in [1, 4]:
    custom_dither_directory(os.path.join(base_path, "stations", "general", str(scale * 64)))
    custom_dither_directory(os.path.join(base_path, "stations", "general", str(scale * 64), "pygen"))
