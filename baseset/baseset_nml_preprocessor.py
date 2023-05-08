"""
Loads a pnml file and:
Populates with information from #import lines.

Import lines in the pnml must be formatted:
#import "path/to/nml/file.nml"
Path must be quoted, no additional whitespace is tolerated.

Argument:
pnml name (without extension)

Output:
nml file with the same name as the pnml file
"""

import_comment = "#include"

import sys

with open(sys.argv[1]+".nml", "w") as nml:
  with open(sys.argv[1]+".pnml", "r") as pnml:
    lines = pnml.read().splitlines()
    for line in lines:
      if line.startswith(import_comment):
        path = line[len(import_comment)+2:-1]
        with open(path, "r") as include:
          include_text = include.read()
          nml.write(include_text)
      else:
        nml.write(line + "\n")
