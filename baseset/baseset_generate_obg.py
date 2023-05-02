def pad(string, length, character=" ", pad_left=True):
  out = string
  if pad_left:
    return character * (length - len(string)) + out
  else:
    return out + character * (length - len(string))

files = [
  {"type": "base", "name": "ogfx21_base"},
  {"type": "arctic", "name": "ogfx2c_arctic"},
  {"type": "tropical", "name": "ogfx2h_tropical"},
  {"type": "toyland", "name": "ogfx2t_toyland"},
  {"type": "logos", "name": "ogfxi_logos", "md5": "53030590b9ff87b4cff119556d301d2c"}, 
  {"type": "extra", "name": "ogfxe_extra", "md5": "535f24c86cf7d77204f5a883e135c085"}
]

with open("opengfx2.obg", "w") as obg:
  obg.write("[metadata]" + "\n")
  pad_length = 12
  obg.write(pad("name", pad_length, pad_left=False) + "= OpenGFX2" + "\n")
  obg.write(pad("shortname", pad_length, pad_left=False) + "= ogfx2" + "\n")
  obg.write(pad("version", pad_length, pad_left=False) + "= 0" + "\n")
  obg.write(pad("palette", pad_length, pad_left=False) + "= DOS" + "\n")
  obg.write(pad("blitter", pad_length, pad_left=False) + "= 8bpp" + "\n")
  obg.write(pad("description", pad_length, pad_left=False) + "= OpenGFX2 base graphics set for OpenTTD. Freely available under the terms of the GNU General Public License version 2." + "\n")
  obg.write("\n");
  obg.write("[files]" + "\n")
  for file in files:
    obg.write(pad(file["type"], 9, pad_left=False) + "= " + file["name"] + ".grf" + "\n")
  obg.write("\n");
  obg.write("[md5s]" + "\n")
  for file in files:
    if "md5" in file:
      md5 = file["md5"] + "\n"
    else:
      with open(file["name"] + ".md5", "r") as md5_file:
        md5 = md5_file.read()
    obg.write(pad(file["name"] + ".grf", 20, pad_left=False) + "= " + md5)
  obg.write("\n")
  obg.write("[origin]" + "\n")
  obg.write("default = Development version, blame Zephyris.")
