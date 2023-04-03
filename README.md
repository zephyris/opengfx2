#opengfx2

Work-in-progress / development repo for an "OpenGFX v2". Or maybe that should be OpenGFX director's edition, refactored OpenGFX, or perhaps OpenGFX extra zoom or OpenGFX 32bpp. Or some combination of all of them.

Partly derived directly from OpenGFX, partly redrawn or revised from my original 32bpp sources.

Far better organised sprites. Extensive use of automated composite sprite generation. Drawn and coded with extra zoom levels in mind.

Requires `git lfs` for large file handling.

Run `make_all.sh` to build the output `.grf` files. This makes a bunch of intermediate files `*_8bpp.png` and things in `pygen` directories.

Requires a system which can run `bash` shell scripts, `python3` with `PIL`, `blend-modes`, `numpy` and `nmlc`.

Files used by `python` are `.png` files, but those may be derived from other sources. Raw raw sprites variously drawn\generated in Paint.NET, Aseprite, Blender and more.

Currently, output are "newgrf" `.grf` files which can be loaded to replace sprites. Ultimately (hopefully) will generate base graphics set `.grf` files.
