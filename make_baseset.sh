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

function encode() {
  echo $1 $2
  python3 ../templates/nml_preprocessor.py $1 $2
  if [ -f $1_$2.grf ]; then
    rm $1_$2.grf
  fi
  nmlc -p DOS --quiet -c $1_$2.nml --md5 $1_$2.md5
}

encode ogfx21_base $alternates
encode ogfx2c_arctic $alternates
encode ogfx2e_extra $alternates
encode ogfx2h_tropical $alternates
encode ogfx2i_logos $alternates
encode ogfx2t_toyland $alternates

python3 baseset_generate_obg.py $alternates

mkdir opengfx2_${alternates}
cp ../README.md opengfx2_${alternates}/readme.txt
cp ../LICENSE opengfx2_${alternates}/license.txt
cp ../CHANGELOG.md opengfx2_${alternates}/changelog.txt
cp *_${alternates}.grf opengfx2_${alternates}/
cp *_${alternates}.obg opengfx2_${alternates}/
tar -cf opengfx2_${alternates}.tar opengfx2_${alternates}
rm -r opengfx2_${alternates}

if [ ! -z "$2" ]; then
  echo "Copying to install directory"
  cp opengfx2_${alternates}.tar "${2}"
fi

cd ..
