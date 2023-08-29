# OpenGFX2
# ![opengfx2_titletext](https://github.com/zephyris/opengfx2/assets/2762690/1adabdf4-baf8-48b2-ae35-279c3d808d0e)

Work-in-progress / development repo for an "OpenGFX v2". Or maybe that should be "OpenGFX director's edition", "refactored OpenGFX", or perhaps "OpenGFX extra zoom" or "OpenGFX 32bpp". Or some combination of all of them.

Partly derived directly from OpenGFX, partly redrawn or revised from my original 32bpp sources. Almost all sprites have been updated or revised.

Features far better organisation of sprites. Extensive use of automated composite sprite generation using Python of bubious quality. Drawn and coded with extra zoom levels and 32bpp in mind.

## Quick start

Download a release from [the prebuilt grf releases](https://github.com/zephyris/opengfx2/tags) and install using the instructions below.

Thease are early release previews not available in the in-game content downloader.

## Building
Requires `git lfs` for large file handling.

Requires a system which can run `bash` shell scripts, `python3` with `PIL`, `blend-modes`, `numpy`, `skimage`, `nmlc`, `concurrent`, `multiprocessing`, `tqdm`.

Clone the repository and run `make_all.sh`, it will take a long time...

The built baseset will be in `baseset/`, called `opengfx2.tar`.

The build newgrf(s) will be in `newgrf/`.

## Installation
Install the baseset by copying `opengfx2.tar` into the `baseset` directory for your OpenTTD installation.

Install the newgrfs by copying each `.grf` file into the `newgrf` directory for your OpenTTD installation. 

To set as the base graphics set, go to `Game Options>(Graphics)>Base Graphics` Set and select `OpenGFX2`.

To set OpenGFX2 settings, go to `NewGRF Settings`, find `OpenGFX2 Settings` and add to `Active NewGRF files`. Then, select `OpenGFX2 Settings` in the `Active NewGRF files list` and select `Set parameters` then adjust the settings. This is a bit of a hack, and will hopefully change in the future.

Install other NewGRFs as normal using `NewGRF settings`.

## Further notes
Image processing makes a bunch of intermediate files, particularly `*_8bpp.png` and things in `pygen` directories.

Files used by `python` are `.png` files, but those may be derived from other sources. Raw raw sprites wre variously drawn\generated in Paint.NET, Aseprite, Blender and more.
