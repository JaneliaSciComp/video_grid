# video_grid
Display many small videos in a grid

## Initial Setup  
1. Install python3 (https://www.python.org/downloads/).
2. Install mpv (https://mpv.io/) to the Applications directory.

## Usage  
```
usage: vidgrid.py [-h] [-m MPV] [-i INPUT] [-r ROW] [-c COL] [-s SCALE] [--width WIDTH] [--height HEIGHT] [-t]

optional arguments:
  -h, --help                show this help message and exit
  -m MPV, --mpv MPV         path to mpv (you do not need this option on Mac if you installed mpv in the Applications directory)
  -i INPUT, --input INPUT   input files or directory
  -r ROW, --row ROW         number of rows
  -c COL, --col COL         number of colmuns
  -s SCALE, --scale SCALE   scale factor
  --width WIDTH             max width
  --height HEIGHT           max height
  -t, --transpose           transpose a grid
```

### Examples
(Mac)  ```python3 vidgrid.py -i "/path/to/input/dir/*.avi" -s 0.3 -t```  
(Windows)  ```python3 vidgrid.py -m "C:\\path\to\mpv" -i "C:\\path\to\input\dir\*.avi" -s 0.3 -t```  
If every input filename contains the pattern "\_\<number\>\<letter\>\_" then the videos will be tiled according to your convention (column=number/row=letter), with missing slots blank.  
Otherwise, the videos will be shown in alphabetical order.  
  
You can set number of rows and columns. The output video dimension will be (input_video_width * scale_factor * columns) x (input_video_height * scale_factor * rows)  
```python3 vidgrid.py -i "/path/to/input/dir/*.mp4" -m "/Applications/mpv.app/Contents/MacOS/mpv" -r 12 -c 7 -s 0.3```  

If you do not set number of rows and columns, they are calculated from the max width and height. (The default max size is 1280x720)  
```python3 vidgrid.py -i "/path/to/input/dir/*.avi" -m "/Applications/mpv.app/Contents/MacOS/mpv" --width 2500 --height 1200 -s 0.3```  
  
You can set multiple files as input.  
```python3 vidgrid.py -i "/path/to/input/video1.avi,/path/to/input/video2.avi,/path/to/input/video3.avi" -m "/Applications/mpv.app/Contents/MacOS/mpv" -s 0.3```  