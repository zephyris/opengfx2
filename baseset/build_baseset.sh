# Build the base set grfs
# Does not trigger image processing
# If given an argument, copies the grfs to that path once complete
# eg. /my/install/of/openttd/baseset/

# Clone OpenGFX and copy sprites for unchanged source
if [ ! -d sprites ]; then
  git clone https://github.com/OpenTTD/OpenGFX
  cp -r OpenGFX/sprites sprites
  rm -rf OpenGFX
fi

echo "OGFX2 Base"
python3 baseset_nml_preprocessor.py ogfx21_base
nmlc -p DOS -c ogfx21_base.nml --md5 ogfx21_base.md5

echo "OGFX2 Arctic"
python3 baseset_nml_preprocessor.py ogfx2c_arctic
nmlc -p DOS -c ogfx2c_arctic.nml --md5 ogfx2c_arctic.md5

echo "OGFX2 Extra"
python3 baseset_nml_preprocessor.py ogfx2e_extra
nmlc -p DOS -c ogfx2e_extra.nml --md5 ogfx2e_extra.md5

echo "OGFX2 Tropical"
python3 baseset_nml_preprocessor.py ogfx2h_tropical
nmlc -p DOS -c ogfx2h_tropical.nml --md5 ogfx2h_tropical.md5

echo "OGFX2 Logos"
python3 baseset_nml_preprocessor.py ogfx2i_logos
nmlc -p DOS -c ogfx2i_logos.nml --md5 ogfx2i_logos.md5

echo "OGFX2 Toyland"
python3 baseset_nml_preprocessor.py ogfx2t_toyland
nmlc -p DOS -c ogfx2t_toyland.nml --md5 ogfx2t_toyland.md5

python3 baseset_generate_obg.py

tar -cf opengfx2.tar *.grf *.obg

if [ ! -z "$1" ]; then
  echo "Copying to install directory"
  cp *.grf "$1"
  cp *.obg "$1"
fi
