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

param_dict = {'STID': 0,'STNM':1,'TIME':2,'RELH':3,'TAIR':4,'WSPD':5,'WVEC':6,'WDIR':7,'WDSD':8,'WSSD':9,'WMAX':10,'RAIN':11,'PRES':12,'SRAD':13,'TA9M':14,'WS2M':15,'TS10':16,'TB10':17,'TS05':18,'TS25':19,'TS60':20,'TR05':21,'TR25':22,'TR60':23}


# Main window class and methods		
## Based on: http://zetcode.com/gui/pygtk/firststeps/
class PyApp(gtk.Window):
    
	def __init__(self):
		# initialize the parent class
		super(PyApp, self).__init__()
		# connect signals for the GUI
		self.connect("destroy", gtk.main_quit)
		# set the initial requested size (may not end up this size if constrained)
		self.set_size_request(400, 250)
		# put the window in the center of the (primary? current?) screen
		self.set_position(gtk.WIN_POS_CENTER)
		# set the window title
		self.set_title("Matts Mesonet Master")		
		# set the window icon
		slash = os.sep
	##	self.set_icon_from_file(script_dir + slash + ".." + slash + "resources" + slash + "main_icon.ico")
		# get the text to add to the form for kicks
		found_locations = self.get_mesonet_data(param_dict['STID'])
		
		# build the menu bar
		mb = gtk.MenuBar()
		filemenu = gtk.Menu()
		filem = gtk.MenuItem("File")
		filem.set_submenu(filemenu)
		exit = gtk.MenuItem("Exit")
		exit.connect("activate", gtk.main_quit)
		filemenu.append(exit)
		mb.append(filem)

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
		for param in sorted(param_dict):
			check = gtk.CheckButton(param)
			check.connect("toggled", self.parameter_check_callback, param)
			self.which_params_box.pack_start(check, True, True, 0)
			check.show()
		self.which_params_scroller.add_with_viewport(self.which_params_box)
		self.notebook.append_page(self.which_params_scroller, gtk.Label("Which Parameters"))
		
		# get start and end dates and times
			# want to use comboboxes
		self.which_params_scroller = gtk.ScrolledWindow()
		self.which_params_box = gtk.VBox(True)
		combobox = gtk.combo_box_new_text()
		#for param in sorted(param_dict):
			#check = gtk.CheckButton(param)
			#check.connect("toggled", self.parameter_check_callback, param)
			#self.which_params_box.pack_start(check, True, True, 0)
			#check.show()
		self.which_params_scroller.add_with_viewport(self.which_params_box)
		self.notebook.append_page(self.which_params_scroller, gtk.Label("Dates and Times"))
				
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
		
	def get_mesonet_data(self,index):

		##array and variable initialization here
		vals = []
		f = ""

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
				line = f.readline()
				headerlines -= 1

			##read the rest of the lines in the file
			else:
				
				line = f.readline().decode()
				
				if line[0] == "<":
					break

				#strip the line endings and split the line into tokens
				tokens = line.strip().split()

				vals.append(tokens[index])
								        
		# return the list of abbreviations
		return vals
      
# once done doing any preliminary processing, actually run the application
main_window = PyApp()
gtk.main()
