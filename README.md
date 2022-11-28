# video_grid
Display many small videos in a grid

## Initial Setup  
1. Install Anaconda (https://www.anaconda.com/).
2. Install mpv (https://mpv.io/) to the Applications directory.
2. Install ffmpeg (https://ffmpeg.org/download.html) to the Applications directory.
3. Download this script (git clone or https://github.com/JaneliaSciComp/video_grid/releases).
4. Run ```conda update conda```

## Usage  
```
usage: vidgrid.py [-h] [-m MPV] [-f FFMPEG] [--encoder ENCODER] [-i INPUT] [-r ROW] [-c COL] [-s SCALE] [--width WIDTH] [--height HEIGHT] [-t] [--verbose]

optional arguments:
  -h, --help                  show this help message and exit
  -m MPV, --mpv MPV           path to mpv (you do not need this option on Mac if you install mpv to the Applications directory)
  -f FFMPEG, --ffmpeg FFMPEG  path to ffmpeg (you do not need this option on Mac if you install ffmpeg to the Applications directory)
  --encoder ENCODER           encoder for video output (default libx264 (Win), h264_videotoolbox (Mac))
  -i INPUT, --input INPUT     input files or directory
  -r ROW, --row ROW           number of rows
  -c COL, --col COL           number of colmuns
  -s SCALE, --scale SCALE     scale factor
  --width WIDTH               max width
  --height HEIGHT             max height
  -t, --transpose             transpose a grid
  --verbose                   enable verbose logging
```

### Examples
```python vidgrid.py -i "/input/*.avi" -s 0.3 -t``` (Mac)  
```python vidgrid.py -m "C:\path\to\mpv" -i "C:\input\*.avi" -s 0.3 -t``` (Windows)  
If every input filename contains the pattern "\_\<number\>\<letter\>\_" then the videos will be tiled according to the convention (column=number/row=letter), with missing slots blank.  
Otherwise, the videos will be shown in alphabetical order.   

You can output a grid video by using -o option.  
```python vidgrid.py -i "/input/*.avi" -o "/output/grid.avi" -s 0.3 -t```  
On Windows, it might be better to use h264_nvenc (for nvidia cards) or h264_amf (for amd cards) for encoding.  
```python vidgrid.py -m "C:\path\to\mpv" -i "C:\input\*.avi" -f C:\path\to\ffmpeg --encoder h264_nvenc -s 0.3 -t``` (Windows)  
  
You can set number of rows and columns by using -r and -c. The output video dimensions will be (input_video_width * scale_factor * columns) x (input_video_height * scale_factor * rows)  
```python vidgrid.py -i "/input/*.mp4" -r 12 -c 7 -s 0.3```  

If you do not set number of rows and columns, they are calculated from the max width and height.  
(The default max size is 1280x720)  
```python vidgrid.py -i "/input/*.avi" --width 2500 --height 1200 -s 0.3```  
  
Multiple files can be set as input.  
```python vidgrid.py -i "video1.avi,video2.avi,video3.avi,video4.avi" -r 2 -c 2 -s 0.3```  

This script can be run on the Janelia LSF cluser.  
```bsub -J "vgrid_gpu" -P scicompsoft -n 4 -gpu "num=1" -q gpu_rtx -o output2.log 'python3 vidgrid.py -i "/input/*.avi" -f bin/ffmpeg -s 0.3 -t -o grid.avi --encoder h264_nvenc'```