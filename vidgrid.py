#!/usr/bin/env python

import glob
import os
import sys
import re
import argparse
import platform

import subprocess

import logging

def get_index(str):
    m = re.search(r'(^[0-9]{1,2}[A-Z]_|_[0-9]{1,2}[A-Z]_|_[0-9]{1,2}[A-Z]\.)', str)
    return re.search(r'[0-9]{1,2}', m.group()).group().zfill(2) + re.search(r'[A-Z]', m.group()).group()

def fix_path_for_ffmpeg_win(p):
    p = p.replace("\\", "\\\\")
    p = p.replace(":", "\\:")
    return p

argv = sys.argv
argv = argv[1:]

usage_text = ("Usage:" + "  slice2octree.py" + " [options]")
parser = argparse.ArgumentParser(description=usage_text)
parser.add_argument("-m", "--mpv", dest="mpv", type=str, default=None, help="path to mpv")
parser.add_argument("-i", "--input", dest="input", type=str, default=None, help="input files or directory")
parser.add_argument("-r", "--row", dest="row", type=int, default=0, help="number of rows")
parser.add_argument("-c", "--col", dest="col", type=int, default=0, help="number of colmuns")
parser.add_argument("-s", "--scale", dest="scale", type=float, default=1.0, help="scale factor")
parser.add_argument("--width", dest="width", type=int, default=0, help="max width")
parser.add_argument("--height", dest="height", type=int, default=0, help="max height")
parser.add_argument("-t", "--transpose", dest="transpose", default=False, action="store_true", help="transpose a grid")
parser.add_argument("--verbose", dest="verbose", default=False, action="store_true", help="enable verbose logging")

if not argv:
    parser.print_help()
    exit()

args = parser.parse_args(argv)

if args.verbose:
    logging.basicConfig(level=logging.INFO)

input = args.input.split(",")
rows = args.row
cols = args.col
scale = args.scale
mpv = args.mpv
transpose = args.transpose

if not mpv:
    if platform.system() == "Darwin":
        mpv = "/Applications/mpv.app/Contents/MacOS/mpv"
    elif platform.system() == "Windows":
        mpv = "mpv.exe"
    else:
        mpv = "mpv"

allfiles = []
if input:
    for f in input:
        if os.path.isdir(f):
            if not f.endswith(os.path.sep):
                f += os.path.sep
            types = ('*.avi', '*.mp4')
            files_grabbed = []
            for file in types:
                files_grabbed.extend(glob.glob(f+file))
            allfiles = allfiles + files_grabbed
        elif os.path.exists(f):
            allfiles.append(f)
        else:
            tmp_flist = glob.glob(f)
            if tmp_flist and len(tmp_flist) > 0:
                allfiles = allfiles + tmp_flist

allfiles.sort()

indexed = True
max_id_num = 0
min_id_num = 9999
max_id_letter = ord('A')
min_id_letter = ord('Z')
for f in allfiles:
    m = re.search(r'(^[0-9]{,2}[A-Z]_|_[0-9]{,2}[A-Z]_|_[0-9]{,2}[A-Z]\.)', f)
    if not m:
        logging.info("Files are not indexed. They will be sorted in alphabetical order")
        indexed = False
        break
    else:
        n = int(re.search(r'[0-9]{1,2}', m.group()).group())
        if n < min_id_num:
            min_id_num = n
        if n > max_id_num:
            max_id_num = n
        c = ord(re.search(r'[A-Z]', m.group()).group())
        if c < min_id_letter:
            min_id_letter = c
        if c > max_id_letter:
            max_id_letter = c

if indexed:
    print("id: " + str(min_id_num) + " -> " + str(max_id_num))
    print("ch: " + chr(min_id_letter) + " -> " + chr(max_id_letter))

id_titles = []
blankfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "blank.avi")
if indexed:
    if rows <= 0:
        rows = max_id_num - min_id_num + 1
    if cols <= 0:
        cols = max_id_letter - min_id_letter + 1
    allfiles = sorted(allfiles, key=get_index)
    temp_list = []
    i = 0
    for row in range(rows):
        for col in range(cols):
            id_titles.append(str(row + min_id_num) + chr(col + min_id_letter))
            found = False
            if i < len(allfiles):
                m = re.search(r'(^[0-9]{,2}[A-Z]_|_[0-9]{,2}[A-Z]_|_[0-9]{,2}[A-Z]\.)', allfiles[i])
                if m:
                    num = int(re.search(r'[0-9]{1,2}', m.group()).group())
                    ch = ord(re.search(r'[A-Z]', m.group()).group())
                    if num == row + min_id_num and ch == col + min_id_letter:
                        temp_list.append(allfiles[i])
                        found = True
            if not found:
                temp_list.append(blankfile)
            else:
                i += 1
    allfiles = temp_list

if transpose:
    rows, cols = cols, rows

tile_width = 0
tile_height = 0
for f in allfiles:
    out = subprocess.check_output([mpv, "--script=getdims.lua", f])
    for line in out.splitlines():
        logging.info(line)
        if line.startswith(b"[getdims]"):
            strs = line.split()
            tile_width = int(strs[1])
            tile_height = int(strs[2])
        if tile_width > 0 and tile_height > 0:
            break
    if tile_width > 0 and tile_height > 0:
        break

tile_width = int(tile_width * scale)
tile_height = int(tile_height * scale)

max_width = args.width
if max_width == 0:
    if cols > 0:
        max_width = tile_width * cols
    else:
        max_width = 1280

max_height = args.height
if max_height == 0:
    if rows > 0:
        max_height = tile_height * rows
    else:
        max_height = 720

if rows <= 0:
    rows = int(float(max_height) / tile_height)
if cols <= 0:
    cols = int(float(max_width) / tile_width)

max_items = rows * cols

tile_max_width = int(float(max_width) / cols)
tile_max_height = int(float(max_height) / rows)
scale_fac_w = 1.0
scale_fac_h = 1.0
if tile_width > tile_max_width:
    scale_fac_w = float(tile_max_width) / tile_width 
if tile_height > tile_max_height:
    scale_fac_h = float(tile_max_height) / tile_height  

scale_fac = 1.0
if scale_fac_w < scale_fac_h:
    scale_fac = scale_fac_w
else:
    scale_fac = scale_fac_h

tile_width = int(tile_width * scale_fac)
tile_height = int(tile_height * scale_fac)

if transpose:
    temp_list = []
    temp_titles = []
    for row in range(rows):
        for col in range(cols):
            id = col*rows + row
            if id < len(allfiles):
                temp_list.append(allfiles[id])
            else:
                temp_list.append(blankfile)
            if indexed:
                if id < len(id_titles):
                    temp_titles.append(id_titles[id])
                else:
                    temp_titles.append("?")
    allfiles = temp_list
    id_titles = temp_titles

max_items = min(len(allfiles), max_items)

filelist = ":".join(allfiles[1:max_items])

titles = []
if indexed:
    titles = id_titles
else:
    for f in allfiles[:max_items]:
        titles.append(os.path.basename(f))

fontpass = os.path.join(os.path.dirname(os.path.realpath(__file__)), "arial.ttf")
if platform.system() == "Windows":
    fontpass = fix_path_for_ffmpeg_win(fontpass)

print("tile_width :" + str(tile_width))
print("tile_height :" + str(tile_height))
print("items :" + str(max_items))
print("rows: " + str(rows))
print("cols: " + str(cols))

commands = []
commands.append(f"{mpv}")
commands.append("--keep-open=yes")

vf = "--lavfi-complex="
i = 1
rowrefs = ""
for row in range(rows):
    vidrefs = ""
    for col in range(cols):
        vf += f"[vid{i}] scale={tile_width}x{tile_height} [t{i}]; [t{i}] drawtext=fontfile=\'{fontpass}\':text=\'{titles[i-1]}\':x=2:y=2:fontsize=10:fontcolor=black:box=1:boxcolor=white@0.5:boxborderw=5 "
        if max_items > 1:
            vf += f"[s{i}]; "
        else:
            vf += "[vo]"
        vidrefs += f"[s{i}]"
        i += 1
        if i-1 > max_items:
            break
    if cols > 1:
        vf += f"{vidrefs} hstack=inputs={cols} "
        if rows > 1:
            vf += f"[r{row}]; "
            rowrefs += f"[r{row}]"
        else:
            vf += " [vo]"
    else:
        rowrefs += vidrefs
    if i-1 > max_items:
        break

if rows > 1:
    vf += f"{rowrefs} vstack=inputs={rows} [vo]"
commands.append(vf)

if max_items > 1:
    for f in allfiles[1:max_items]:
        commands.append(f"--external-file={f}")

commands.append(allfiles[0])

logging.info(commands)
print("running mpv player...")
cp = subprocess.run(commands, capture_output=True)
logging.info(cp.stdout)
logging.info(cp.stderr)