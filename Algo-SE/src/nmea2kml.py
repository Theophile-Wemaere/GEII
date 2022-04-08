#!/usr/bin/python3

#http://www.cedricaoun.net/eie/trames%20NMEA183.pdf <- frames informations (FR)

#frame description for GPS logger application:
#type,date time,latitude,longitude,accuracy(m),altitude(m),geoid_height(m),speed(m/s),bearing(deg),sat_used,sat_inview,name,desc


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
# *NEW* New format conversion for the GPS logger app on Google Store
#
# **coming soon** (before april 10th): containment max radius calculation (even if it's a little bit late)

import functions as func
import GUI
import tkinter as tk
from os.path import exists
import sys
import converter

USE_GUI = True        #if you want to use the GUI, set to 'True', if you don't want, set to 'False' 
DEBUG_MESSAGE = True  #if you want to see debugs meesage, set to 'True', if you don't want, set to 'False'
OVERWRITE = True      #set to 'True' if you want to overwrite the output file. 'False' will trigger a warning when creating the output file and allow to choose antoher name

INPUT_FILE = "/tmp/data.txt"     #set the input file to convert (no necessary if using the GUI), set the FULL path (ex : /home/user/data.txt or C:\\Users\\data.txt)
OUTPUT = "output.kml"            #default output file name, can be found in the output/ directory 
MODE = "colored"                 #choose if the path is colored (speed indication) with "colored" or if the path is only one color "one color"
COLOR = "ff00ffff"               #ABGR hex code for 'one color' mode ex : red = ff0000ff
NAME = "My path"                 #the name of the path in the kml file
FORMAT = "GGA"                   #the frames format to convert. Choose 'GGA' for GGA+VTG frames and 'APP' for the GPS logger app format


def init():

    global INPUT_FILE, OUTPUT, MODE, COLOR, FORMAT

    ###################################starting the GUI if requested

    if USE_GUI :

        func.debug("start_gui")
        root = tk.Tk()
        app = GUI.nmea_gui(root)
        choosing = True

        while choosing:
            
            if len(app.color_entry.get())==6:
                try:
                    app.button_color["bg"] = "#" + app.color_entry.get()[::-1]
                except:
                    pass

            if app.var_gga.get() == 1 and app.var_app.get() == 1: #warning label for both format selected
                app.label_warning.place(x=80,y=350,width=300,height=30)
            else:
                app.label_warning.place_forget()

            #print(app.var_end.get())
            app.page.update()

            if app.var_end.get() == 1:
                
                choosing = False
                INPUT_FILE = app.file.get()

                if INPUT_FILE=="":                      #if no input 
                    func.debug("none_input")
                    choosing = True
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

                if app.var_gga.get() == 1:
                    FORMAT = "GGA"
                elif app.var_app.get() == 1:
                    FORMAT = "APP"
                elif app.var_gga.get() == 1 and app.var_app.get() == 1:
                    app.label_warning.place(x=80,y=350,width=300,height=30)
                    app.var_end.set(0)
                    choosing = True
                else :
                    func.debug("no_format")
                    app.var_end.set(0)
                    choosing = True


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

    ###################################checking if the format is correct

    if FORMAT != "GGA" and FORMAT !="APP":
        func.debug("bad_format")
        if FORMAT == None:
            func.debug("no_format")
            func.debug("choose_format")
            FORMAT = func.FORMAT
            

    #recap message before starting the conversion

    func.debug("input_recap",INPUT_FILE)
    func.debug("output_recap",OUTPUT)
    func.debug("mode_recap",MODE)
    func.debug("format_recap",FORMAT)


def main():

    #max range in Km/h before switching color
    N = 0.5   

    ###################################opening the output file

    try:
        outfile = open("output/" + OUTPUT,'a')
    except:
        func.debug("error_open_out_file")
        sys.exit(1)

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

        if FORMAT == "GGA":
            converter.GGA_colored(file,outfile,INPUT_FILE,OUTPUT,N,FORMAT)
        elif FORMAT == "APP":
            converter.APP_colored(file,outfile,INPUT_FILE,OUTPUT,N,FORMAT)
        else:
            func.debug("bad_format",FORMAT)

    ###################################conversion with only one color
    elif MODE == "one color":
        
        if FORMAT == "GGA":
            converter.GGA_oneColor(file,outfile,OUTPUT,COLOR,FORMAT)
        elif FORMAT == "APP":
            converter.APP_oneColor(file,outfile,OUTPUT,COLOR,FORMAT)
        else:
            func.debug("bad_format")
            
    ###################################error : unknow format        
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
