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
  nmlc -p DOS --quiet -c $1_$2.nml --md5 $1_$2.md5
}

encode ogfx21_base $alternates
encode ogfx2c_arctic $alternates
encode ogfx2e_extra $alternates
encode ogfx2h_tropical $alternates
encode ogfx2i_logos $alternates
encode ogfx2t_toyland $alternates

python3 baseset_generate_obg.py $alternates

cp ../README.md readme.txt
cp ../LICENSE license.txt
cp ../CHANGELOG.md changelog.txt
tar -cf opengfx2_${alternates}.tar *_${alternates}.grf *_${alternates}.obg readme.txt license.txt changelog.txt
rm readme.txt license.txt changelog.txt

if [ ! -z "$2" ]; then
  echo "Copying to install directory"
  cp opengfx2_${alternates}.tar "${2}"
fi

cd ..
