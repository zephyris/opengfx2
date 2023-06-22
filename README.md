# OpenGFX2
Work-in-progress / development repo for an "OpenGFX v2". Or maybe that should be "OpenGFX director's edition", "refactored OpenGFX", or perhaps "OpenGFX extra zoom" or "OpenGFX 32bpp". Or some combination of all of them.

Partly derived directly from OpenGFX, partly redrawn or revised from my original 32bpp sources. Almost all sprites have been updated or revised.

Features far better organisation of sprites. Extensive use of automated composite sprite generation. Drawn and coded with extra zoom levels and 32bpp in mind.

## Building
Requires `git lfs` for large file handling.

Requires a system which can run `bash` shell scripts, `python3` with `PIL`, `blend-modes`, `numpy` and `nmlc`.

Clone the repository and run `make_all.sh`, it will take a long time...

The built baseset will be in `baseset/`, called `opengfx2.tar`.

The build newgrf(s) will be in `newgrf/`.

## Installation
Install the baseset by copying `opengfx2.tar` into the `baseset` directory for your OpenTTD installation.

Install the newgrfs by copying each `.grf` file into the `newgrf` directory for your OpenTTD installation. 

## Further notes
Image processing makes a bunch of intermediate files, particularly `*_8bpp.png` and things in `pygen` directories.

Files used by `python` are `.png` files, but those may be derived from other sources. Raw raw sprites wre variously drawn\generated in Paint.NET, Aseprite, Blender and more.
