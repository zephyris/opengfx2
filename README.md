# OpenGFX2
# ![opengfx2_titletext](https://github.com/zephyris/opengfx2/assets/2762690/1adabdf4-baf8-48b2-ae35-279c3d808d0e)

"OpenGFX2" graphics base set for [OpenTTD](https://github.com/OpenTTD/OpenTTD). This is a spiritual successor to [OpenGFX](https://github.com/OpenTTD/OpenGFX). Think of it as "OpenGFX version 2", or maybe that should be "OpenGFX director's edition", "refactored OpenGFX", or perhaps "OpenGFX extra zoom" or "OpenGFX 32bpp". Or some combination of all of them.

Partly derived directly from OpenGFX, partly redrawn or revised from my original 32bpp sources. Almost all sprites have been updated or revised.

Features far better organisation of sprites. Extensive use of automated composite sprite generation using Python of dubious quality. Drawn and coded with extra zoom levels and 32bpp in mind.

## Quick start

### In-game content downloader / BaNaNaS
It is easiest to use the in-game content downloader (`Check Online Content` in the OpenTTD main menu).

To install, search for `OpenGFX2`, tick the checkbox next to OpenGFX2 Base graphics, and hit `Download`.

To set as the base graphics set, go to `Game Options > (Graphics) > Base Graphics` from the OpenTTD main menu. Select `OpenGFX2 Classic`, then close the `Game Options` window.

### Manual download
Download a release from [the prebuilt grf releases](https://github.com/zephyris/opengfx2/tags) and install using the instructions below.

These are early release previews not available in the in-game content downloader. This includes base set versions (the "High Def" 32bpp 4x zoom version) and NewGRFs not yet available through the in-game downloader.

### Installation
Install the baseset by copying `opengfx2_8.tar` and/or `opengfx2_32ez.tar` into the `baseset` directory for your OpenTTD installation.

Install the newgrfs by copying each `.grf` file into the `newgrf` directory for your OpenTTD installation.

To set as the base graphics set, go to `Game Options>(Graphics)>Base Graphics` Set and select `OpenGFX2 Classic` (8bpp 1x zoom version) or `OpenGFX2 High Def` (32bpp 4x zoom version).

To set OpenGFX2 settings, go to `NewGRF Settings`, find `OpenGFX2 Settings` and add to `Active NewGRF files`. Then, select `OpenGFX2 Settings` in the `Active NewGRF files list` and select `Set parameters` then adjust the settings. This is a bit of a hack, and will hopefully change in the future.

Install other NewGRFs as normal using `NewGRF settings`.

## Building
These notes are for if you want to build OpenGFX2 from the source files. If you just want to download OpenGFX2 then you don't need to worry about these.

Requires `git lfs` for large file handling. Once `git lfs` is installed then clone using `git` as normal.

Requires a system which can run `bash` shell scripts, `python3` with `PIL`, `blend-modes`, `numpy`, `skimage`, `nmlc`, `concurrent`, `multiprocessing`, `tqdm`. This has been developed using Windows Subsystem for Linux (WSL) and might have peculiarities (eg. incorrect file permissions) on a real Linux install.

### To build
Clone the repository, navigate to the repository root directory and run `make_all.sh`. It will take a long time...

The built baseset will be in `baseset/`, making different versions called `opengfx2_<version>.tar`.

The built newgrf(s) will be in `newgrf/`, making various `.grf` files.

### Build process notes
Image processing makes a bunch of intermediate files, particularly `*_8bpp.png` and things in `pygen` directories. Others are `_bt32bpp`, `_rm32bpp.png`. These files are assumed to be temporary intermediates, and any user-modified versions will be blindly overwritten. Make sure you look at `.gitignore` see which files this applies to.

Files processed by `python` and encoded by `nml` are `.png` files, but those may be derived from other sources. Raw sprites were variously drawn\generated in Paint.NET, Aseprite, Blender and more. Conversion from those raw sources to `.png` files is not part of the build process - it must be done manually.

## Development
These notes are to help development. If you are just downloading or building OpenGFX2 then you don't need to worry about these.

### Release preparation
Remember to bump the versions: 
* Base set version in `baseset/baseset_generate_obg.py`
* NewGRF versions in `newgrf/nml/<newgrf_name>/<newgrf_name>-header.pmnl`
* `extra.grf` version in `baseset/nml/extra-header.pnml`
* `extra.grf`/`opengfx2_settings.grf` co-compatibility check in `baseset/nml/extra-header.pnml`

For better or worse, base set currently uses fractional (0.1, 0.2, ...) versioning and NewGRFs use integer (1, 2, ...) versioning.
