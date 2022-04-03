#!/usr/bin/python3

import colorsys
import nmea2kml as main
import re
import numpy as np

NUM_LINE = 0
MAX="100"    #max speed for color conversion, default 100Km/h
OUTPUT = "output.kml"

def placemark(index,NAME=None):
    """
    This function return the start or the end of a kml file
    It just need the dictionnary index you want : 'start' or 'end'
    """
    placemark = {
        "start" : """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.1">
    <Document>
        <name>%s</name>
        <description> Mon parcours </description>
            """ % NAME,
        "end" : """
    </Document>    
</kml>"""
    }
    return placemark[index]

def getMaxSpeed(path):
    """
    this function parse the entire input file to get the greater speed
    so the coloration is better 
    """

    global MAX
    list = []

    with open(path,'r') as file:

        for line in file:
            if line[:6]=="$GPVTG":
                nl=line.split(',')
                list.append(float(nl[7]))

    MAX = np.max(list)

def chksum(inp): 
    """
    checksum verification for each frame (work with GGA and VTG)
    not from me, original version here : https://gist.github.com/tomazas/90c45719b15a1c9cc2bf (thanks tomazas)
    """

    inp = inp[:len(inp)-1] #remove the '\n' at the end of a frame

    if not inp.startswith("$"): 
        return False    
    if not inp[-3:].startswith("*"): 
        return False
    payload = inp[1:-3]
    checksum = 0
    for i in range(len(payload)):
        checksum =  checksum ^ ord(payload[i])
    return ("%02X" % checksum) == inp[-2:]

def createPlacemark(color,coordinates):
    """
    function to create a placemark
    basically it create a big string with all the syntax to open a placemark in a KML file
    We will later add the coordinates, before closing the placemark with the corretc syntax, and then write it in the output file
    It in arguments the color of the path (color from the speed frames conversion) and the last coordinates of the last placemark
    (to avoid holes in the final path)
    """

    if color[:1] == "#":   #remove the # in the hex color if there is one
        color=color[1:]

    placemark="""<Placemark>
                <Style>
                    <LineStyle>
                        """
    placemark+="<color>" + color + "</color>"
    placemark+="""
                        <width>5</width>
                    </LineStyle>
                </Style>
                <LineString>
                    <extrude>1</extrude>
                    <tessellate>1</tessellate>
                    <altitudeMode>absolute</altitudeMode>
                    <coordinates>
"""

    placemark+= coordinates #we add the last coordinates of the previous placemark to avoid holes (or "" if it's the first placemark)

    return placemark

def endPlacemark(placemark,file):
    """
    simple function to end a placemark and to write it in the output file
    """

    placemark+="""                  </coordinates>
                </LineString>
            </Placemark>
            """
    try:
        file.write(placemark)
    except:
        return -1

def getSpeed(line):
    """
    this function parse a VTG frame to get the speed in Km/h
    it check if the frame isn't corrupted with the chksum function (checksum verification) and then return the speed value
    """
    nl=line.split(',')
    if chksum(line):
        return float(nl[7])
    else:
        return -1

def Speed2Color(speed):
    """
    function to convert the speed value of a VTG frame to a Hue value
    for later use it as in HSV format (Hue, Saturation, Value)
    MAX is a global variable with the max speed found in the input file
    """    

    Hue = -(140/MAX)*float(speed)+140    #the speed to color equation : we want Hue value as [0 km/h;MAX km/h] -> [140;0] ([turquoise;red])
    if Hue > 140 : Hue = 140
    elif Hue < 0 : Hue = 0
    return Hue

def HSV2HEX(Hue,Sat=100,Value=100):  # (°, %, %)
    """
    function to convert HSV coloration (from VTG speed frame conversion) to ABGR format (KML syntax)
    in HSV format, only the Hue modify the RGB coloration, so the Saturation and the Value are both equal to 100
    """

    Hue /= 360
    Sat /=100
    Value /=100
    red,green,blue=colorsys.hsv_to_rgb(Hue,Sat,Value)
    red,green,blue=int(red*255),int(green*255),int(blue*255)
    hexRGB="ff{:02x}{:02x}{:02x}".format(blue,green,red)        #https://stackoverflow.com/questions/3380726/converting-a-rgb-color-tuple-to-a-six-digit-code
    return hexRGB

def new_color_placemark(data,speed,previousCoordinates):
    """
    this function is like a "main" function : it create a placemark, get the right color from the speed  
    """
    newHue=Speed2Color(speed)                                  #get the HSV color from the speed
    newColor=HSV2HEX(newHue)                                   #get the hexcadecimal ABGR color from the HSV color
    placemark=createPlacemark(newColor,previousCoordinates)    #create a placemark with the right color and the last coordinates of the last placemark
    coordinates=getCoordinates(data)                           #get the coordinates from the raw GGA frames
    if coordinates != -1 and coordinates != -2:     #log the first coordinates  (after the last coordinates of the last placemark)
        placemark+=coordinates
        return coordinates,placemark                #return the coordinates for the previousCoordinates var and placemark
    else:
        pass

def getCoordinates(line):
    """
    Parsing function, take for argument a GGA frame
    and return a tuple with(latitude,longitude,altitude)
    If the checksum is wrong or if the altitude is equal to '00,
    we assume the frame is corrupted
    """
    
    nl=line.split(',')              #parse the line to get a list of the differents data
    lat,long,alt=nl[2],nl[4],nl[9]  #get the value of latitude, longitude and altitude
    if alt=="00":                   #if the altitude is equal to '00', the frame is bad
        debug("error_alt")
        return -1  
    elif not chksum(line):          #if the checksum is bad, the frame is corrupted
        debug("bad_chksum_coordinates")
        return -2
    else:                                                               
        lat = float(lat[:2]) + (float(lat[2:])/60)                  #get the real latitude value (ex: nl[2] = 4306.9122 is 43° and 06.9122 minutes = 43.11520° equal to 43+(06.9122/60))
        long = float(long[:3]) + (float(long[3:])/60)               #get the real longitude value (almost the same calcul)

        if nl[3]=='S' :      #if the latitude is south oriented, lat is negative
            lat = -lat              
        if nl[5]=='W' :      #if the longitude is west oriented, long is negative
            long = -long

        alt = float(alt) + 10  #adding 10 to the altitude to avoid dead zone on google earth view

        coordinates="                       {},{},{} \n".format(str(long),str(lat),str(alt))  #create the line with the right format to lin a kml file
        return coordinates
        

def verifString(string):
    """
    verify if the input file path doesn't have bad char 
    """

    #for exemple "C:\Users\data.txt" will become "C:\\Users\\data.txt" which can be read without error
    verified_string = string.translate(str.maketrans({"\"": r"\"", "\\": r"\\","\'": r"\'"})) 
    return verified_string

################################### debugging function : 

#not sure if it's very usefull but I wanted to try something

def debug(index, arg=None):
    """
    Function to display debug message about the conversion progress
    Will display infos, error messages and also allow for some actions
    It's awfull but python doesn't have switch-case :(
    """

    global OUTPUT

    if main.DEBUG_MESSAGE:

        if index=="creating_file":
            print("[nmea2kml] Creating file with name :",arg )

        elif index=="file_not_found":
            print("[nmea2kml] Error : input file with name \'%s\' not found, exiting" % arg)

        elif index=="checking_file":
            print("[nmea2kml] Checking if input file exist")

        elif index=="open_in_file":
            print("[nmea2kml] Opening %s" % arg)

        elif index=="error_alt" :
            print("[nmea2kml] Error : bad altitude value on line ",arg)

        elif index=="start":
            print("[nmea2kml] Starting conversion")

        elif index=="start_gui":
            print("[nmea2kml] Starting graphical user interface")

        elif index=="input_recap":
            print("[nmea2kml] Input file selected :",arg)

        elif index=="output_recap":
            print("[nmea2kml] Output file selected :",arg)

        elif index=="mode_recap":
            print("[nmea2kml] Mode selected :",arg)

        elif index=="file_exist":
            print("[nmea2kml] Error : file with name %s already exist" % arg)
            print("[nmea2kml] What do you want to do : [1] overwrite | [2] choose another name")
            choice = input("           Choose 1 or 2 : ")
            if choice == "2":
                OUTPUT = input("           new name : ")

        elif index=="end":
            print("[nmea2kml] Conversion finished, closing all files")

        elif index=="error_open_in_file":
            print("[nmea2kml] Error : cannot open the input file at %s" % arg)

        elif index=="bad_chksum_speed":
            print("[nmea2kml] Error : bad cheksum on VTG frame line",NUM_LINE)

        elif index=="bad_chksum_coordinates":
            print("[nmea2kml] Error : bad cheksum on GGA frame line",NUM_LINE)

        elif index=="error_writing":
            print("[nmea2kml] Error : cannot write to the file",arg)

        elif index=="bad_mode":
            print("[nmea2kml] Error mode %s is unknow. Select \'one color\' or \'colored\'" % arg)

        elif index=="unknow_line":
            print("[nmea2kml] Error : unknow line type on line",NUM_LINE)

        elif index=="none_input":
            print("[nmea2kml] Please select an input file")

        elif index=="none_filename":
            print("[nmea2kml] No output file name specified, taking default name :",arg)

        elif index=="none_color":
            print("[nmea2kml] No color specified, taking default value :",arg)

        elif index=="placemark_color":
            print("[nmea2kml] Creating mono-colored path with color",arg)


