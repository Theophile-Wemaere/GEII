#!/usr/bin/python3

#http://www.cedricaoun.net/eie/trames%20NMEA183.pdf <- frames informations (FR)

#https://ivanrublev.me/kml/                         <- KML viewer (very easy and fast to use)

#https://open.spotify.com/track/3ACa8DImXMFWsa44oEUKr1?si=22068d28e6fe4de8   <- (very good)


#                                             NMEA to KML frames converter
#
#                                        ----- Made by Théophile Wemaere -----
#
# This the main code for the nmea2kml converter, it use both the functions in functions.py and GUI.py to create the output file,
# parse each frame of the input file, and create a .kml file to display a GPS path with a kml viwer. You can choose to display the path with
# the speed coloration or not (thanks to the VTG frames)
#
# For now only work with GGA frames for coordinates and VTG frames for speed
#
# *NEW* Now with a brand new (beautiful) GUI
#
# **coming soon** (before april 10th): _different frames conversion to use with the GPS logger app 
#                                      _containment max radius calculation (even if it's a little bit late)

import functions as func
import GUI
import tkinter as tk
from os.path import exists
import sys

USE_GUI = True        #if you want to use the GUI, set to 'True', if you don't want, set to 'False' 
DEBUG_MESSAGE = True  #if you want to see debugs meesage, set to 'True', if you don't want, set to 'False'
OVERWRITE = False     #set to 'True' if you want to overwrite the output file. 'False' will trigger a warning when creating the output file and allow to choose antoher name

INPUT_FILE = "/tmp/data.txt"     #set the input file to convert (no necessary if using the GUI), set the FULL path (ex : /home/user/data.txt or C:\\Users\\data.txt)
OUTPUT = "output.kml"            #default output file name, can be found in the output/ directory 
MODE = "colored"                 #choose if the path is colored (speed indication) with "colored" or if the path is only one color "one color"
COLOR = "ff0000ff"               #ABGR hex code for 'one color' mode ex : red = ff0000ff
NAME = "My path"                 #the name of the path in the kml file


def init():

    global INPUT_FILE, OUTPUT, MODE, COLOR

    ###################################starting the GUI if requested

    if USE_GUI :

        func.debug("start_gui")
        root = tk.Tk()
        app = GUI.nmea_gui(root)
        choosing = False

        while not choosing:
            
            if len(app.color_entry.get())==6:
                try:
                    app.button_color["bg"] = "#" + app.color_entry.get()
                except:
                    pass

            #print(app.var_end.get())
            app.page.update()

            if app.var_end.get() == 1:
                
                choosing = True
                INPUT_FILE = app.file.get()

                if INPUT_FILE=="":                      #if no input 
                    func.debug("none_input")
                    choosing = False
                    app.var_end.set(0)

                if app.var_name.get() == 1:    
                    if app.output_entry.get()  == '':
                        func.debug("none_filename",OUTPUT)
                    else:
                        OUTPUT = app.output_entry.get()
                        if OUTPUT.find('.kml') ==  -1:    #add the .kml extension if there isn't one
                            OUTPUT += ".kml"

                if app.var_mode.get() == 1:
                    MODE = "one color"
                    if app.color_entry.get() == '' or len(app.color_entry.get()) != 6: #take default color if no color specified or bad syntax
                        func.debug("none_color",COLOR)
                    else:
                        COLOR = app.color_entry.get() 
                        if COLOR[:1] == "#":                #remove the # if there is one
                            COLOR=COLOR[1:]
                        COLOR="ff"+COLOR
                else:
                    MODE = "colored"

    ###################################checking if input file exist

    func.debug("checking_file")

    OUTPUT = func.verifString(OUTPUT) #verify if the file path doesn't have bad characted like '\' (usually found in a Windows path like C:\Users\...)

    if not exists(INPUT_FILE):
        func.debug("file_not_found",INPUT_FILE)
        sys.exit(1)

    ###################################creating output file

    func.debug("creating_file",OUTPUT)

    if exists("output/" + OUTPUT) and not OVERWRITE:  #checking if the output name choosed while overwrite another file
        func.debug("file_exist",OUTPUT)
        OUTPUT = func.OUTPUT

    out_path = "output/" + OUTPUT

    #writing the start of a kml file inside the output file

    try:
        outfile=open(out_path,'w')
        outfile.write(func.placemark("start",NAME))
        outfile.close()
    except:
        func.debug("error_creating_file",OUTPUT)
        sys.exit(1)

    #recap message before starting the conversion

    func.debug("input_recap",INPUT_FILE)
    func.debug("output_recap",OUTPUT)
    func.debug("mode_recap",MODE)


def main():



    ###################################opening the output file

    try:
        outfile = open("output/" + OUTPUT,'a')
    except:
        func.debug("error_open_out_file")
        sys.exit(1)

    ###################################declaration of variables

    count,previousSpeed = 0,0

    #max range in Km/h before switching color
    N = 0.5                 

    begin = True

    previousCoordinates=""
    placemark="",

    ###################################opening input file

    func.debug("open_in_file",INPUT_FILE)

    try:
        file = open(INPUT_FILE,'r')
    except:
        func.debug("error_open_in_file")
        return -1
    
    ###################################beginning conversion

    func.debug("start")

    ###################################conversion with colored path and speed indication
    if MODE == "colored" :

        func.getMaxSpeed(INPUT_FILE)

        for line in file:   
            line_type = line[:6] 
            if line_type=="$GPGGA":                 #check if the current line is a GGA frame
                data=line                           #if it's a GGA frame, store it in data

            elif line_type=="$GPVTG":
                speed=line                          #if it's not, it's a speed frame
                speed=func.getSpeed(speed)          #we get the speed value

                if speed != -1:                     #if the checksum if good, we can process the speed value and convert it to a colored path

                    if begin:                                                                                       #if it's the first frame, we create the first placermak
                        begin = False       
                        previousSpeed=speed                                                                         
                        previousCoordinates, placemark = func.new_color_placemark(data,speed,previousCoordinates)   #the function create the placemark with the right color from the speed value

                    elif (speed < previousSpeed + N) and (speed > previousSpeed - N):    #else if the speed is not is the range +/- N km, we add the coordinates to the current placemark
                        previousSpeed=speed
                        coordinates=func.getCoordinates(data)
                        if coordinates != -1 and coordinates != -2:                      #if the coordinates checksum and alt are good, we add them to the placemark
                            placemark+=coordinates
                            previousCoordinates=coordinates                              #we new to add the lasts coordinates when starting a new palcemark to avoid hole in the final path
                        else:
                            pass

                    else:
                        endPlacemark=func.endPlacemark(placemark,outfile)                            #if the speed difference is to high (bigger or smaller than N km), we end the placemark
                        if endPlacemark == -1 :
                            func.debug("error_writing",OUTPUT)
                            sys.exit(1)
                        previousSpeed=speed
                        previousCoordinates, placemark = func.new_color_placemark(data,speed,previousCoordinates) #we create a new placemark
                else:
                    func.debug("bad_chksum_speed")

            else:   #if it's not a GGA or VTG frame, this is an unknow data line
                func.debug("unknow_line")

            func.NUM_LINE+=1     #update the line counter (for the debug function)

    ###################################conversion with only one color
    elif MODE == "one color":
        
        func.debug("placemark_color",COLOR)
        placemark = func.createPlacemark(COLOR,"")          #we create the placemark (only one) wit the requested color

        for line in file:                                   
            if line[:6] == "$GPGGA":                        #we only use GGA frames for this path
                coordinates = func.getCoordinates(line)
                if coordinates != -1 and coordinates != -2:
                    placemark += coordinates
            
        endPlacemark = func.endPlacemark(placemark,outfile)
        if endPlacemark == -1:
            func.debug("error_writing",OUTPUT)
            sys.exit(1)

    else:
        func.debug("bad_mode",MODE)
        sys.exit(1)

    ###################################we close all the files
    file.close()
    outfile.write(func.placemark("end"))  #we add to the output file the closing syntax for a kml file
    outfile.close()
    func.debug("end")
            
if __name__ == "__main__":
    try:    
        init()
        main()
    except KeyboardInterrupt:
        func.debug("KeyboardInterrupt")
