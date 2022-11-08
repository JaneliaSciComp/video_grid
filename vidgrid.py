#!/usr/bin/env python

import glob
import os
import sys

os.chdir(sys.argv[1])

cols = 12
rows = 7
max_items = rows * cols

max_width = 2560
max_height = 1440

video_width = int(float(max_width) / rows)
video_height = int(float(max_height) / cols)

allfiles = glob.glob("*.avi")
max_items = min(len(allfiles), max_items)

filelist = ":".join(allfiles[1:])

print(f"#!/bin/bash\ncd {sys.argv[1]}\nmpv --lavfi-complex=\"\\")

i = 1
rowrefs = ""
for row in range(rows):

    vidrefs = ""
    for col in range(cols):
        print(f"[vid{i}] scale=200x200 [s{i}];\\")
        vidrefs += f"[s{i}]"
        i += 1

    print(f"{vidrefs} hstack= inputs={cols} [r{row}];\\")
    rowrefs += f"[r{row}]"

print(f"{rowrefs} vstack= inputs={rows} [vo]\\")
print(f"\" {allfiles[0]} \\")
print(f"--external-files=\"{filelist}\"")

