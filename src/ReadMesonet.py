#!/usr/bin/env python

# always import sys first
import sys

# go ahead and determine the python version and platform early on in case other imports are dependent on this
python_version = float("%s.%s" % (sys.version_info.major, sys.version_info.minor))
if "linux" in sys.platform:
    platform = "linux"
elif "win" in sys.platform:
    platform = "windows"
elif "darwin" in sys.platform:
    platform = "mac"

## Hi! I'm a comment.
    ## Another comment

# the os library allows for file system and other machine stuff
# use it to get the current directory so we can access files relative to this
import os
script_dir = os.path.dirname(__file__)

# I'm not actually sure if installing the pygtk all-in-one will properly include the gtk libraries
# As such, I'll include the instructions for installing gtk first, for now, and test it out later
# Either way, after doing the following 2

# Of course, if you are running python right now, then you have a python interpreter, but...
# You'll want to make a clear note ahead of time which version you are running, including:
# 32 or 64 bit
# Python 2.7, Python 3, Python other?
# This is because the version of pygtk *must* match
# This information can be found by just running python.exe and reading the first line

# in order to install gtk on Windows, download a gtk all-in-one bundle from here:
# http://www.gtk.org/download/index.php
# then unzip the folder somewhere (c:\gtk)
# then add then bin folder to the system path (Right Click My Computer > Properties; Advanced System Settings; Environment Variables; System Variables; Path -- append the bin dir {;c:\gtk\bin})
import gtk

# in order to install pygtk, download a pygtk all-in-one installer from here:
# http://pygtk.org/downloads.html
# and run it; if it finds the matching python installation, you're done
import pygtk

# import appropriate libraries for reading the mesonet data
if python_version > 3:
    try:
        import urllib.request
    except:
        print("Could not import urllib, need to install it!!")
else:
    try:
        import urllib
    except:
        print("Could not import urllib, need to install it!!")

from datetime import datetime

# Main window class and methods     
## Based on: http://zetcode.com/gui/pygtk/firststeps/
class PyApp(gtk.Window):

    def __init__(self):
        # initialize the parent class
        super(PyApp, self).__init__()
        # connect signals for the GUI
        self.connect("destroy", gtk.main_quit)
        # set the initial requested size (may not end up this size if constrained)
        self.set_size_request(600, 350)
        # put the window in the center of the (primary? current?) screen
        self.set_position(gtk.WIN_POS_CENTER)
        # set the window title
        self.set_title("Matts Mesonet Master")      
        # set the window icon
        slash = os.sep
        self.set_icon_from_file(script_dir + slash + ".." + slash + "resources" + slash + "main_icon.ico")
        # get the text to add to the form for kicks
        found_locations = self.get_mesonet_data(0,1)
        data_labels = self.get_mesonet_data(0,0)
        
        # for convenience later
        now = datetime.now()
                
        # create the menu bar itself to hold the menus; this is what is added to the vbox, or in the case of Ubuntu the global menu
        mb = gtk.MenuBar()
        
        # create a dummy action item
        menu_item_file_doit = gtk.MenuItem("Do it")
        ##filemenu.connect("activate", self.do_it_button)
        menu_item_file_doit.show()
        
        # create an exit button
        menu_item_file_exit = gtk.MenuItem("Exit")
        menu_item_file_exit.connect("activate", gtk.main_quit)
        menu_item_file_exit.show()
        
        # create the base root menu item for FILE
        menu_item_file = gtk.MenuItem("File")
        
        # create a menu to hold FILE items and put them in there
        filemenu = gtk.Menu()
        filemenu.append(menu_item_file_doit)
        filemenu.append(menu_item_file_exit)
        menu_item_file.set_submenu(filemenu)

        # attach the FILE menu to the main menu bar
        mb.append(menu_item_file)
        
        # create a vbox to start laying out the geometry of the form
        vbox = gtk.VBox(False)
        
        # add the menu to the vbox
        vbox.pack_start(mb, False, False)
        
        # now create the bulk of the form layout by starting with a notebook
        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_TOP)
        
        # create the list of locations
        self.radio_button_scroller = gtk.ScrolledWindow()
        self.radio_button_box = gtk.VBox(True)
        self.dummy_radio = gtk.RadioButton(None, "")
        for loc in found_locations:
            button = gtk.RadioButton(self.dummy_radio, loc)
            button.connect("toggled", self.location_radio_callback, loc)
            self.radio_button_box.pack_start(button, True, True, 0)
            button.show()           
        self.radio_button_scroller.add_with_viewport(self.radio_button_box)
        self.notebook.append_page(self.radio_button_scroller, gtk.Label("Location"))
        
        # create the list of parameters to get
        self.which_params_scroller = gtk.ScrolledWindow()
        self.which_params_box = gtk.VBox(True)
        for label in data_labels:
            check = gtk.CheckButton(label)
            check.connect("toggled", self.parameter_check_callback, label)
            self.which_params_box.pack_start(check, True, True, 0)
            check.show()
        self.which_params_scroller.add_with_viewport(self.which_params_box)
        self.notebook.append_page(self.which_params_scroller, gtk.Label("Which Parameters"))
        
        # date/time tab
        
        # time zone selection, build widgets, then an hbox to hold it
        self.time_frame_utc_radio = gtk.RadioButton(None, "Use UTC (Mesonet)")
        self.time_frame_utc_radio.connect("toggled", self.timezone_radio_callback, "utc")
        self.time_frame_cst_radio = gtk.RadioButton(self.time_frame_utc_radio, "Use CST (Local)")
        self.time_frame_cst_radio.connect("toggled", self.timezone_radio_callback, "cst")
        time_frame_zone = gtk.HBox(True)
        time_frame_zone.pack_start(self.time_frame_utc_radio)
        time_frame_zone.pack_start(self.time_frame_cst_radio)

       
        ##### START SIDE #####
        
        # build a START label
        start_label = gtk.Label("<b>START TIME</b>")
        start_label.set_use_markup(True)
        
        # next build the calendar and initialize it
        self.datetimes_start_calendar = gtk.Calendar()
        self.datetimes_start_calendar.connect("day-selected", self.calendar_day_changed, "start")
        self.datetimes_start_calendar.connect("month-changed", self.calendar_month_changed, "start")
        self.datetimes_start_calendar.connect("next-year", self.calendar_year_changed, "start")
        self.datetimes_start_calendar.connect("prev-year", self.calendar_year_changed, "start")
        
        # initalize the date to today
        print "**Initializing start calendar day and month"
        self.datetimes_start_calendar.select_month(now.month-1, now.year)
        self.datetimes_start_calendar.select_day(now.day)
        
        # create spinners for the TIME
        self.datetimes_start_time_hours = gtk.SpinButton()
        self.datetimes_start_time_hours.set_range(0,23)
        self.datetimes_start_time_hours.set_increments(1,3)
        self.datetimes_start_time_hours.connect("value-changed", self.hours_changed, "start")
        self.datetimes_start_time_minutes = gtk.SpinButton()
        self.datetimes_start_time_minutes.set_range(0,55)
        self.datetimes_start_time_minutes.set_increments(5,3)
        self.datetimes_start_time_minutes.connect("value-changed", self.minutes_changed, "start")
        
        # initialize the time to "now"
        print "**Initializing end time values"
        self.datetimes_start_time_hours.set_value(now.hour)
        ## rounds the current minute back to the nearest 5 minute interval
        if now.minute < 5:
            minute = 0
        else:
            minute = now.minute - now.minute % 5 	
        self.datetimes_start_time_minutes.set_value(minute)
   
        # now pack the time spinners in an hbox
        datetimes_start_time_box = gtk.HBox(True)
        datetimes_start_time_box.pack_start(gtk.Label("Hour"))
        datetimes_start_time_box.pack_start(self.datetimes_start_time_hours, False, False)
        datetimes_start_time_box.pack_start(gtk.Label("Min."))
        datetimes_start_time_box.pack_start(self.datetimes_start_time_minutes, False, False)
        
        # drop the everything in to create the START side
        datetimes_start_box = gtk.VBox(False)
        datetimes_start_box.pack_start(start_label, False)
        datetimes_start_box.pack_start(self.datetimes_start_calendar)
        datetimes_start_box.pack_start(datetimes_start_time_box)
        
        ##### END START SIDE #####
        
        ##### "END" SIDE #####
        
        # build an END label
        end_label = gtk.Label("<b>FINISH TIME</b>")
        end_label.set_use_markup(True)
        
        # next build the calendar and initialize it
        self.datetimes_end_calendar = gtk.Calendar()
        self.datetimes_end_calendar.connect("day-selected", self.calendar_day_changed, "end")
        self.datetimes_end_calendar.connect("month-changed", self.calendar_month_changed, "end")
        self.datetimes_end_calendar.connect("next-year", self.calendar_year_changed, "end")
        self.datetimes_end_calendar.connect("prev-year", self.calendar_year_changed, "end")
        
        # initailize the date to today
        print "**Initializing end calendar day and month"
        self.datetimes_end_calendar.select_month(now.month-1, now.year)
        self.datetimes_end_calendar.select_day(now.day)
        
        # create spinners for the TIME
        self.datetimes_end_time_hours = gtk.SpinButton()
        self.datetimes_end_time_hours.set_range(0,23)
        self.datetimes_end_time_hours.set_increments(1,3)
        self.datetimes_end_time_hours.connect("value-changed", self.hours_changed, "end")
        self.datetimes_end_time_minutes = gtk.SpinButton()
        self.datetimes_end_time_minutes.set_range(0,55)
        self.datetimes_end_time_minutes.set_increments(5,3)
        self.datetimes_end_time_minutes.connect("value-changed", self.minutes_changed, "end")
       
        # initialize the time to "now"
        print "**Initializing end time values"
        self.datetimes_end_time_hours.set_value(now.hour)
        ## rounds the current minute back to the nearest 5 minute interval
        if now.minute < 5:
            minute = 0
        else:
            minute = now.minute - now.minute % 5 	
        self.datetimes_start_time_minutes.set_value(minute)
        self.datetimes_end_time_minutes.set_value(minute)
        
        # now pack the time spinners in an hbox
        datetimes_end_time_box = gtk.HBox(True)
        datetimes_end_time_box.pack_start(gtk.Label("Hour"))
        datetimes_end_time_box.pack_start(self.datetimes_end_time_hours)
        datetimes_end_time_box.pack_start(gtk.Label("Min."))
        datetimes_end_time_box.pack_start(self.datetimes_end_time_minutes)
        
        datetimes_end_box = gtk.VBox(False)
        datetimes_end_box.pack_start(end_label, False)
        datetimes_end_box.pack_start(self.datetimes_end_calendar)
        datetimes_end_box.pack_start(datetimes_end_time_box)
        
        ##### END "END" SIDE #####
        
        # create a box to hold the date/time details
        datetimes_details_box = gtk.HBox(True)
        datetimes_details_box.pack_start(datetimes_start_box)
        datetimes_details_box.pack_start(datetimes_end_box)
                
        # finally the highest level datetime box 
        main_datetimes_box = gtk.VBox(False)
        main_datetimes_box.pack_start(time_frame_zone)
        main_datetimes_box.pack_start(datetimes_details_box)
        
        self.notebook.append_page(main_datetimes_box, gtk.Label("Dates and Times"))

        # create the selection of output reports
        self.which_params_scroller = gtk.ScrolledWindow()
        self.which_params_box = gtk.VBox(True)

        self.which_params_scroller.add_with_viewport(self.which_params_box)
        self.notebook.append_page(self.which_params_scroller, gtk.Label("Output Reports"))
                
        # now put the notebook in the main vbox
        vbox.pack_start(self.notebook)
        
        # now add the entire vbox to the main form (note you can and should nest vbox's and hbox's within each other)
        self.add(vbox)

        # I'm not sure the difference between show and show_all, but maybe show_all initializes all the widgets?
        self.show_all()

    def location_radio_callback(self, widget, location):
        print "Location radio callback: %s was toggled %s" % (location, ("OFF", "ON")[widget.get_active()])
        
    def parameter_check_callback(self, widget, param_name):
        print "Parameter radio callback: %s was toggled %s" % (param_name, ("OFF", "ON")[widget.get_active()])

    def timezone_radio_callback(self, widget, time_zone_string):
        print "Timezone radio callback: %s was toggled %s" % (time_zone_string, ("OFF","ON")[widget.get_active()])

    def calendar_day_changed(self, widget, start_or_end):    
        y, m, d = widget.get_date()
        print "%s day changed, new value = %s" % (start_or_end, d)
        
    def calendar_month_changed(self, widget, start_or_end):
        y, m, d = widget.get_date()
        print "%s month changed, new value = %s (zero-based index, 0-11)" % (start_or_end, m)
    
    def calendar_year_changed(self, widget, start_or_end):
        y, m, d = widget.get_date()
        print "%s year changed, new value = %s" % (start_or_end, y)
    
    def hours_changed(self, widget, start_or_end):
        print "%s hours changed, new value = %s" % (start_or_end, widget.get_value())
    
    def minutes_changed(self, widget, start_or_end):
        print "%s minutes changed, new value = %s" % (start_or_end, widget.get_value())
                
    def get_mesonet_data(self,index,dataFlag):

        ##array and variable initialization here
        vals = []
        f = ""
        labels = []

        ##src URL link
        link = "http://www.mesonet.org/index.php/dataMdfMts/dataController/getFile/201401150000/mdf/TEXT/"

        # try reading the url, it is inside a try block so that it can handle a bad connection, etc.
        try:
            if python_version > 3:
                f = urllib.request.urlopen(link)
            else:
                f = urllib.urlopen(link)
        except:
            return "Could not read mesonet URL..."
            
        ##number of header line in the MESONET text data files
        headerlines = 3

        ##read the first line
        line = f.readline()

        #while there are lines...
        while line:

            ##skip the header lines
            if headerlines > 0:
                if headerlines  == 1:
                    labels = line.strip().split()
                    
                line = f.readline().decode()
                headerlines -= 1

            ##read the rest of the lines in the file
            else:
                
                line = f.readline().decode()
                
                if line[0] == "<":
                    break

                #strip the line endings and split the line into tokens
                tokens = line.strip().split()

                vals.append(tokens[index])
        if dataFlag == 1:                           
            # return the list of abbreviations
            return vals
        elif dataFlag == 0:
            return labels
      
# once done doing any preliminary processing, actually run the application
main_window = PyApp()
gtk.main()
