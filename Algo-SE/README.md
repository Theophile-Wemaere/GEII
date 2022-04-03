# NMEA to KML python converter

#### (by me)

### What does it do :

Take for input a file with NMEA frames (GGA for positions and VTG for speed)

Generate a	.kml file, to display the route, with or without speed coloration on a kml viewer like https://ivanrublev.me/kml/

##### Without speed coloration:
![NoSpeed](./data/img1.png)

##### With speed coloration:
![Speed](./data/img3.png)

Also have altitudes informations, so you can display it in google earth:

##### google earth 3D view:
![GoogleEarth](./data/img2.png)

I was bored so there is also a *beautiful* interface with tkinter to select your file and other options :

![gui](./data/img4.png)

### How to use it :

simply launch the main script with `python3 src/nmea2kml.py`

You'll need the following pip packages to fully use it :
```
tkinter
os
sys
colorsys
numpy
re
```

You can manage each options with the globals variables in `src/nmea2kml.py`:
```py
USE_GUI = True
DEBUG_MESSAGE = True
OVERWRITE = True

INPUT_FILE="/tmp/data.txt"
OUTPUT="output.kml"
MODE="colored"
COLOR="ff0000ff
NAME="My path"
```

