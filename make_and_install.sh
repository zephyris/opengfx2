echo "Making and installing to $1"
make all
cp baseset/*.tar $1/baseset/
cp newgrf/*.grf $1/newgrf/
