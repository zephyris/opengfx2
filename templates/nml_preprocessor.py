"""
Loads a pnml file and:
Populates with information from #import lines.
Removes comments to configure extra zoom and 32bpp alternative sprites.

Import lines in the pnml must be formatted:
#import "path/to/nml/file.nml"
Path must be quoted, no additional whitespace is tolerated.

Extra zoom and 32bpp alternative sprites are controlled by removing comment strings exactly matching:
"#ez" for extra zoom sprites
"#32" for 32bpp sprites

Argument:
pnml name (without extension)

Output:
nml file with the same name as the pnml file
"""

comment_import = "#include"

comment_alternate = ["#ez ", "#32 "]
settings_alternate = [True, True]

import sys

def handle_alternates(line, options = []):
  for c in range(len(comment_alternate)):
    comment = comment_alternate[c]
    if comment in line:
      if settings_alternate[c]:
        line = line.replace(comment, "")
      else:
        line = line.replace(comment, comment.replace("#", "//"))
  return line

with open(sys.argv[1]+".nml", "w") as nml:
  with open(sys.argv[1]+".pnml", "r") as pnml:
    lines = pnml.read().splitlines()
    for line in lines:
      if line.startswith(comment_import):
        path = line[len(comment_import)+2:-1]
        with open(path, "r") as include:
          include_lines = include.read().splitlines()
          for include_line in include_lines:
            include_line = handle_alternates(include_line)
            nml.write(include_line + "\n")
      else:
        include_line = handle_alternates(include_line)
        nml.write(line + "\n")
