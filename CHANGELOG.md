# OpenGFX2 Changelog

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
