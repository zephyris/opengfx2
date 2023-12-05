import sys

blitter = 8
typelong = "8-bit"
typeshort = "8"

if len(sys.argv) > 1:
  # settings
  if "32" in sys.argv[1]:
    blitter = 32
    typelong = "32-bit"
    typeshort = "32"
  if "ez" in sys.argv[1]:
    typeshort += "ez"
    typelong += " Extra Zoom"
  else:
    typelong += " Normal Zoom"

# catch specific variant cases, release cases (8, 32ez)
if typeshort == "8":
  description = "Classic version (" + typelong + ")"
  namesuffix = "Classic"
elif typeshort == "32ez":
  description = "High definition version (" + typelong + ")"
  namesuffix = "High Def"
else:
  description = typelong + " version"
  namesuffix = typelong

# define unique short (4 character) names
namelookup = {"8": "ogfx", "8ez": "ogfX", "32": "ogFx", "32ez": "ogFX"}


def pad(string, length, character=" ", pad_left=True):
  out = string
  if pad_left:
    return character * (length - len(string)) + out
  else:
    return out + character * (length - len(string))

files = [
  {"type": "base", "name": "ogfx21_base_" + typeshort},
  {"type": "arctic", "name": "ogfx2c_arctic_" + typeshort},
  {"type": "tropical", "name": "ogfx2h_tropical_" + typeshort},
  {"type": "toyland", "name": "ogfx2t_toyland_" + typeshort},
  {"type": "logos", "name": "ogfx2i_logos_" + typeshort}, 
  {"type": "extra", "name": "ogfx2e_extra_" + typeshort}
]

with open("opengfx2_" + typeshort + ".obg", "w") as obg:
  obg.write("[metadata]" + "\n")
  pad_length = 12
  obg.write(pad("name", pad_length, pad_left=False) + "= OpenGFX2 " + namesuffix + "\n")
  obg.write(pad("shortname", pad_length, pad_left=False) + "= " + namelookup[typeshort] + "\n")
  obg.write(pad("version", pad_length, pad_left=False) + "= 4" + "\n")
  obg.write(pad("palette", pad_length, pad_left=False) + "= DOS" + "\n")
  obg.write(pad("blitter", pad_length, pad_left=False) + "= "+str(blitter)+"bpp" + "\n")
  obg.write(pad("description", pad_length, pad_left=False) + "= OpenGFX2, a pixel art style base graphics set for OpenTTD. "+description+". Freely available under the terms of the GNU General Public License version 2." + "\n")
  obg.write("\n");
  obg.write("[files]" + "\n")
  for file in files:
    obg.write(pad(file["type"], 12, pad_left=False) + "= " + file["name"] + ".grf" + "\n")
  obg.write("\n");
  obg.write("[md5s]" + "\n")
  for file in files:
    if "md5" in file:
      md5 = file["md5"] + "\n"
    else:
      with open(file["name"] + ".md5", "r") as md5_file:
        md5 = md5_file.read()
    obg.write(pad(file["name"] + ".grf", 26, pad_left=False) + "= " + md5)
  obg.write("\n")
  obg.write("[origin]" + "\n")
  obg.write("default = From the in-game content download system (BaNaNaS) or https://github.com/zephyris/opengfx2/")
