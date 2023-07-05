# Build the base set grfs
# Does not trigger image processing
# If given an argument, copies the grfs to that path once complete
# eg. /my/install/of/openttd/baseset/

cd baseset

# Clone OpenGFX and copy sprites for unchanged source
# No longer needed - OpenGFX independent
#if [ ! -d sprites ]; then
#  git clone https://github.com/OpenTTD/OpenGFX
#  cp -r OpenGFX/sprites sprites
#  rm -rf OpenGFX
#fi

# "8, 8ez, 32 or 32ez"
alternates="8"
if [ ! -z "$1" ]; then
  alternates=$1
fi

echo "OGFX2 Base"
python3 ../templates/nml_preprocessor.py ogfx21_base $alternates
nmlc -p DOS --quiet -c ogfx21_base.nml --md5 ogfx21_base.md5

echo "OGFX2 Arctic"
python3 ../templates/nml_preprocessor.py ogfx2c_arctic $alternates
nmlc -p DOS --quiet -c ogfx2c_arctic.nml --md5 ogfx2c_arctic.md5

echo "OGFX2 Extra"
python3 ../templates/nml_preprocessor.py ogfx2e_extra $alternates
nmlc -p DOS --quiet -c ogfx2e_extra.nml --md5 ogfx2e_extra.md5

echo "OGFX2 Tropical"
python3 ../templates/nml_preprocessor.py ogfx2h_tropical $alternates
nmlc -p DOS --quiet -c ogfx2h_tropical.nml --md5 ogfx2h_tropical.md5

echo "OGFX2 Logos"
python3 ../templates/nml_preprocessor.py ogfx2i_logos $alternates
nmlc -p DOS --quiet -c ogfx2i_logos.nml --md5 ogfx2i_logos.md5

echo "OGFX2 Toyland"
python3 ../templates/nml_preprocessor.py ogfx2t_toyland $alternates
nmlc -p DOS --quiet -c ogfx2t_toyland.nml --md5 ogfx2t_toyland.md5

python3 baseset_generate_obg.py $alternates

tar -cf opengfx2_${alternates}.tar *.grf *.obg

if [ ! -z "$2" ]; then
  echo "Copying to install directory"
  cp opengfx2_${alternates}.tar "${2}/opengfx2.tar"
fi

cd ..
