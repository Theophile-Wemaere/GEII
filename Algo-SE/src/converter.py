#!/usr/bin/python3

#just another file to store all conversion operations, so the main  file is still clear

import tkinter as tk
import functions as func
import nmea2kml as main
import sys

############################################################################# GGA + VTG format

def GGA_colored(file, outfile, INPUT_FILE,OUTPUT,N,FORMAT):

    ###################################declaration of variables

    count,previousSpeed = 0,0    

    begin = True

    previousCoordinates=""
    placemark=""

    func.getMaxSpeed(INPUT_FILE,FORMAT)

    for line in file:   
        line_type = line[:6] 
        if line_type=="$GPGGA":                 #check if the current line is a GGA frame
            data=line                           #if it's a GGA frame, store it in data

        elif line_type=="$GPVTG":
            speed=line                          #if it's not, it's a speed frame
            speed=func.getSpeed(speed,FORMAT)          #we get the speed value

            if speed != -1:                     #if the checksum if good, we can process the speed value and convert it to a colored path

                if begin:                                                                                       #if it's the first frame, we create the first placermak
                    begin = False       
                    previousSpeed=speed                                                                         
                    previousCoordinates, placemark = func.new_color_placemark(data,speed,previousCoordinates,FORMAT)   #the function create the placemark with the right color from the speed value

                elif (speed < previousSpeed + N) and (speed > previousSpeed - N):    #else if the speed is not is the range +/- N km, we add the coordinates to the current placemark
                    previousSpeed=speed
                    coordinates=func.getCoordinates(data,FORMAT)
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
                    previousCoordinates, placemark = func.new_color_placemark(data,speed,previousCoordinates,FORMAT) #we create a new placemark
            else:
                func.debug("bad_chksum_speed")

        else:   #if it's not a GGA or VTG frame, this is an unknow data line
            func.debug("unknow_line")

        func.NUM_LINE+=1     #update the line counter (for the debug function)

####################one color mode

def GGA_oneColor(file,outfile,OUTPUT,COLOR,FORMAT):
    func.debug("placemark_color",COLOR)
    placemark = func.createPlacemark(COLOR,"")          #we create the placemark (only one) wit the requested color

    for line in file:                                   
        if line[:6] == "$GPGGA":                        #we only use GGA frames for this path
            coordinates = func.getCoordinates(line,FORMAT)
            if coordinates != -1 and coordinates != -2:
                placemark += coordinates
        func.NUM_LINE+=1 
        
    endPlacemark = func.endPlacemark(placemark,outfile)
    if endPlacemark == -1:
        func.debug("error_writing",OUTPUT)
        sys.exit(1)


############################################################################# GPS logger application format

def APP_colored(file,outfile,INPUT_FILE,OUTPUT,N,FORMAT):

    ###################################declaration of variables

    count,previousSpeed = 0,0    

    begin = True

    previousCoordinates=""
    placemark=""

    func.getMaxSpeed(INPUT_FILE,FORMAT)

    for line in file:   
        
        speed = func.getSpeed(line,FORMAT)
        if begin:                          
            begin = False       
            previousSpeed=speed                                                                         
            previousCoordinates, placemark = func.new_color_placemark(line,speed,previousCoordinates,FORMAT)   #the function create the placemark with the right color from the speed value

        elif (speed < previousSpeed + N) and (speed > previousSpeed - N):    #else if the speed is not is the range +/- N km, we add the coordinates to the current placemark
            previousSpeed=speed
            coordinates=func.getCoordinates(line,FORMAT)
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
            previousCoordinates, placemark = func.new_color_placemark(line,speed,previousCoordinates,FORMAT) #we create a new placemark

        func.NUM_LINE+=1     #update the line counter (for the debug function)

####################one color mode

def APP_oneColor(file,outfile,OUTPUT,COLOR,FORMAT):
    func.debug("placemark_color",COLOR)
    placemark = func.createPlacemark(COLOR,"") #we create the placemark (only one) wit the requested color
    for line in file:                                   
        coordinates = func.getCoordinates(line,FORMAT)
        if coordinates != -1 and coordinates != -2:
            placemark += coordinates
        func.NUM_LINE+=1 
        
    endPlacemark = func.endPlacemark(placemark,outfile)
    if endPlacemark == -1:
        func.debug("error_writing",OUTPUT)
        sys.exit(1)