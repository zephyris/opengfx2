# OpenGFX2 Changelog

## v0.5
Base set:
* All GUI icons at 1x and 2x zoom, with some at 4x.
* Improved cursors, all at 1x and 2x zoom.
* Additional cursor styles.
* Build sprite font from TTFs, for full sprite font at 2x and 4x zoom.
* TTD-style custom monospaced sprite font, from TTF.
* Extended sprite font range to also cover Cyrillic and Greek alphabets.
* Prototype/first 4x rail vehicle sprites.
* Various additional bug fixes, including:
* Fix bridge colour, recolour and leg glitches.
* Fix/tweak town tree graphics.
* Fix Various rock and slope shading glitches.

NewGRFs:
* New standalone objects NewGRF, with fields, forests, rocks and building objects.
* Fix tree NewGRF to also replace cacti and palm trees.

## v0.4
Base set:
* 4x zoom trees for normal climates, including improved growth/death stages.
* 4x zoom tree/plantation industries.
* 4x zoom improved pixel art detailing of terrain.
* Improved maglev level crossings.
* Various bug fixes.

NewGRFs:
* New standalone trees NewGRF.

Known issues:
* If you're using a nightly, make sure you're using one from later than 29/10/2023, otherwise all climates will end up looking like temperate!

## v0.3
Base set:
* Baseset parameters, for baseset parameter support when OpenTTD 14.0 arrives.
* Removed pixel jitter in animated industries, and similar tweaks.
* Expanded 2x scale GUI scaling support.
* Prototype pixel art 4x zoom trees for Arctic.
* Various bug fixes.

Settings NewGRF:
* Preparation for depreciation when OpenTTD 14.0 arrives.

NewGRFs:
* New rail stations and waypoints NewGRF, just waypoints for now.
* Fixes for standalone behaviour of the landscape NewGRF.

Known issues:
* If you're using a nightly, make sure you're using one from later than 29/10/2023, otherwise all climates will end up looking like temperate!

## v0.21
Minor bugfix release.

Base set:
* Switch to integer version numbering for internal use, decimal not supported by OpenTTD for version comparisons.
* Minor bug fixes.

## v0.2
Base set:
* Bug fixes from v0.1, including a few game-breaking missing (white box) sprites.
* Initial support for 2x GUI scaling (including in 'Classic' variant).

Settings NewGRF:
* Parameter control of grass (terrain tile), foundation and tree style per climate. Almost fully mix-and-match.

NewGRFs:
* New standalone landscape NewGRF.

Backend:
* Multithreading for much faster 32bpp to 8bpp sprite conversion.

## v0.1
Base set:
* First OpenGFX-independent baseset.
* 8bpp 1x zoom 'Classic' variant.
* 32bpp 4x zoom 'High Def' variant.
'Classic' is a complete baseset. 'High Def' 32bpp and 4x zoom sprites are not universally complete, and uses 8bpp 1x zoom fallbacks.

Settings NewGRF:
* Sets parameters which the extra grf in the baseset reads.
* Configure presence/absence of gridlines, logo style, cursor styles.
