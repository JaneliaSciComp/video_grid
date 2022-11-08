#!/usr/bin/env python

import glob
import os
import sys

os.chdir(sys.argv[1])

outfile = "final2.mp4"
cols = 12
rows = 7
max_items = rows * cols

max_width = 2560
max_height = 1440

video_width = int(float(max_width) / rows)
video_height = int(float(max_height) / cols)

cmd = "ffmpeg \\\n"

allfiles = glob.glob("*.avi")

print(f"found {len(allfiles)} files")

max_items = min(len(allfiles), max_items)

for filename in allfiles[:max_items]:
    cmd += f"-i {filename} \\\n"

cmd += "-filter_complex \" \\\n"

i = 0
rowrefs = []
for row in range(rows):

    vidrefs = []
    for col in range(cols):
        if i>=max_items: break
        cmd += f"  [{i}] scale=200x200 [s{i}]; \\\n"
        vidrefs.append(f"[s{i}]")
        i += 1

    if vidrefs:
        cmd += "".join(vidrefs) 
        cmd += f" hstack= inputs={len(vidrefs)} [r{row}]; \\\n"
        rowrefs.append(f"[r{row}]")

cmd += "".join(rowrefs)
cmd += f" vstack= inputs={len(rowrefs)} [v]\" \\\n"
cmd += f"-map \"[v]\" -c:v h264_videotoolbox "+outfile

print()
print(cmd)
print()
print(os.popen(cmd).read())

