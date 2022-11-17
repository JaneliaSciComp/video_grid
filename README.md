# video_grid
Display many small videos in a grid

## Initial Setup  
1. Install python3 (https://www.python.org/downloads/).
2. Install mpv (https://mpv.io/) to the Applications directory.
3. Download this script (git clone or https://github.com/JaneliaSciComp/video_grid/releases).

## Usage  
```
usage: vidgrid.py [-h] [-m MPV] [-i INPUT] [-r ROW] [-c COL] [-s SCALE] [--width WIDTH] [--height HEIGHT] [-t]

optional arguments:
  -h, --help                show this help message and exit
  -m MPV, --mpv MPV         path to mpv (you do not need this option on Mac if you installed mpv to the Applications directory)
  -i INPUT, --input INPUT   input files or directory
  -r ROW, --row ROW         number of rows
  -c COL, --col COL         number of colmuns
  -s SCALE, --scale SCALE   scale factor
  --width WIDTH             max width
  --height HEIGHT           max height
  -t, --transpose           transpose a grid
  --verbose                 enable verbose logging
```

### Examples
```python vidgrid.py -i "/input/*.avi" -s 0.3 -t``` (Mac)  
```python vidgrid.py -m "C:\path\to\mpv" -i "C:\input\*.avi" -s 0.3 -t``` (Windows)  
If every input filename contains the pattern "\_\<number\>\<letter\>\_" then the videos will be tiled according to the convention (column=number/row=letter), with missing slots blank.  
  
Otherwise, the videos will be shown in alphabetical order.   
You can set number of rows and columns by using -r and -c. The output video dimension will be (input_video_width * scale_factor * columns) x (input_video_height * scale_factor * rows)  
```python vidgrid.py -i "/input/*.mp4" -r 12 -c 7 -s 0.3```  

If you do not set number of rows and columns, they are calculated from the max width and height.  
(The default max size is 1280x720)  
```python vidgrid.py -i "/input/*.avi" --width 2500 --height 1200 -s 0.3```  
  
Multiple files can be set as input.  
```python vidgrid.py -i "video1.avi,video2.avi,video3.avi,video4.avi" -r 2 -c 2 -s 0.3```  