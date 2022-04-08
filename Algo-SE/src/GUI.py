#!/usr/bin/python3

#A simple GUI made with tkinter to use the nmea to kml converter


import tkinter as tk
import tkinter.font as tkFont
from tkinter.filedialog import askopenfilename
from os.path import exists

SHOW_ENTRY = False

class nmea_gui:

    def __init__(self, root):

        self.page = root
        ft = tkFont.Font(family='Times',size=10)

        #setting title

        root.title("nmea2kml GUI")

        #setting window size
        width=480
        height=680
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        ######################define the 'start conversion' button

        self.var_end = tk.IntVar()  #dynamic variable to end the GUI
        self.var_end.set(0) 

        button_start=tk.Button(root)
        button_start["bg"] = "#2f8213"
        button_start["font"] = ft
        button_start["fg"] = "#ffffff"
        button_start["justify"] = "center"
        button_start["text"] = "Start conversion"
        button_start.place(x=181,y=620,width=118,height=30)
        button_start["command"] = self.button_start

        ############################################File selection

        #label for file selection

        label_choose=tk.Label(root)
        label_choose["font"] = tkFont.Font(family='Times',size=12,weight = 'bold')
        label_choose["fg"] = "#333333"
        label_choose["justify"] = "center"
        label_choose["text"] = "Choose file :"
        label_choose.place(x=40,y=40,width=90,height=25)

        ######################button for file selection

        button_choose=tk.Button(root)
        button_choose["bg"] = "#e9e9ed"
        button_choose["font"] = ft
        button_choose["fg"] = "#000000"
        button_choose["justify"] = "center"
        button_choose["text"] = "choose file"
        button_choose.place(x=200,y=110,width=108,height=30)
        button_choose["command"] = self.button_choose_file  #the function open the files explorer

        #label for file selection n°2

        label_select=tk.Label(root)
        label_select["font"] = ft
        label_select["fg"] = "#333333"
        label_select["justify"] = "center"
        label_select["text"] = "Select your NMEA file :"
        label_select.place(x=40,y=110,width=148,height=30)

        #label to display the choosed file

        self.file = tk.StringVar() #dynamic string for label content
        self.file.set("")

        self.label_filename=tk.Label(root)
        self.label_filename["font"] = ft
        self.label_filename["fg"] = "#333333"
        self.label_filename["justify"] = "center"
        self.label_filename["textvariable"] = self.file

        ############################################Format selection

        #label for format selection

        label_format=tk.Label(root)
        label_format["font"] = tkFont.Font(family='Times',size=12,weight = 'bold')
        label_format["fg"] = "#333333"
        label_format["justify"] = "center"
        label_format["text"] = "Choose frames format :"
        label_format.place(x=40,y=210,width=160,height=25)

        self.var_gga = tk.IntVar()     #dynamic variables for checkbox values
        self.var_app = tk.IntVar()

        #checkbox for GGA format

        checkBox_gga=tk.Checkbutton(root)
        checkBox_gga["font"] = ft
        checkBox_gga["fg"] = "#333333"
        checkBox_gga["justify"] = "left"
        checkBox_gga["text"] = " GGA + VTG format"
        checkBox_gga.place(x=-100,y=270,width=400,height=30)
        checkBox_gga["variable"] = self.var_gga

        #checkbox for GPS logger application format

        checkBox_app=tk.Checkbutton(root)
        checkBox_app["font"] = ft
        checkBox_app["fg"] = "#333333"
        checkBox_app["justify"] = "left"
        checkBox_app["text"] = " GPS logger application format"
        checkBox_app.place(x=-71,y=310,width=400,height=30)
        checkBox_app["variable"] = self.var_app

        #label for double selection warning

        self.label_warning=tk.Label(root)
        self.label_warning["font"] = tkFont.Font(family='Times',size=10,weight = 'bold')
        self.label_warning["fg"] = "#ff0000"
        self.label_warning["justify"] = "center"
        self.label_warning["text"] = "/!\ Please select only one format"        

        ############################################labels

        #label for settings

        label_settings=tk.Label(root)
        label_settings["font"] = tkFont.Font(family='Times',size=12,weight = 'bold')
        label_settings["fg"] = "#333333"
        label_settings["justify"] = "center"
        label_settings["text"] = "Others settings :"
        label_settings.place(x=40,y=400,width=116,height=30)

        #label just to make the GUI look better

        label_bar1=tk.Label(root)
        label_bar1["bg"] = "black"
        label_bar1.place(x=20,y=70,width=430,height=2)

        label_bar2=tk.Label(root)
        label_bar2["bg"] = "black"
        label_bar2.place(x=20,y=430,width=430,height=2)

        label_bar3=tk.Label(root)
        label_bar3["bg"] = "black"
        label_bar3.place(x=20,y=240,width=430,height=2)

        ############################################define the checkbox for settings

        self.var_mode = tk.IntVar()     #dynamic variables for checkbox values
        self.var_name = tk.IntVar()

        ######################checkbox for coloration mode

        checkBox_color=tk.Checkbutton(root)
        checkBox_color["font"] = ft
        checkBox_color["fg"] = "#333333"
        checkBox_color["justify"] = "left"
        checkBox_color["text"] = " Mono-colored path"
        checkBox_color.place(x=-100,y=460,width=400,height=30)
        checkBox_color["variable"] = self.var_mode
        checkBox_color["command"] = self.color_cb

        #label for color entry

        self.label_color=tk.Label(root)
        self.label_color["font"] = ft
        self.label_color["fg"] = "#333333"
        self.label_color["justify"] = "left"
        self.label_color["text"] = "BGR color (hex) : "

        #color entry

        self.color_entry=tk.Entry(root)
        self.color_entry["font"] = ft
        self.color_entry["fg"] = "#333333"
        self.color_entry["justify"] = "center"
        self.color_entry["border"] = 1
        self.color_entry["relief"] = "flat"

        ######################colored button to display current color

        self.button_color=tk.Button(root)
        self.button_color["state"] = "disabled"

        ######################checkbox for different output name

        checkBox_name=tk.Checkbutton(root)
        checkBox_name["font"] = ft
        checkBox_name["fg"] = "#333333"
        checkBox_name["justify"] = "left"
        checkBox_name["text"] = " Change output name (default output.kml, will overwrite)"
        checkBox_name.place(x=2,y=520,width=400,height=30)
        checkBox_name["variable"] = self.var_name
        checkBox_name["command"] = self.name_cb

        #label for output entry

        self.label_output=tk.Label(root)
        self.label_output["font"] = ft
        self.label_output["fg"] = "#333333"
        self.label_output["justify"] = "left"
        self.label_output["text"] = "Output file name : "

        #output file name entry

        self.output_entry=tk.Entry(root)
        self.output_entry["font"] = ft
        self.output_entry["fg"] = "#333333"
        self.output_entry["justify"] = "center"
        self.output_entry["border"] = 1
        self.output_entry["relief"] = "flat"



    #function to start the conversion

    def button_start(self):
        self.var_end.set(1)

    #function to choose the file

    def button_choose_file(self):
            filename = askopenfilename()
            self.file.set(filename)
            self.label_filename.place(x=0,y=160,width=480,height=32)

    def name_cb(self):

        if self.var_name.get() == 1:
            self.output_entry.place(x=150,y=560,width=200,height=30)
            self.label_output.place(x=50,y=560,width=100,height=32)
        else:
            self.output_entry.place_forget()
            self.label_output.place_forget()

    def color_cb(self):

        if self.var_mode.get() == 1:
            self.color_entry.place(x=160,y=490,width=150,height=30)
            self.label_color.place(x=40,y=490,width=120,height=32)
            self.button_color.place(x=350,y=490,width=108,height=30)
        else:
            self.color_entry.place_forget()
            self.label_color.place_forget()
            self.button_color.place_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = nmea_gui(root)
    root.mainloop()
