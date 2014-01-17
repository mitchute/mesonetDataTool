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

# Main window class and methods		
## Based on: http://zetcode.com/gui/pygtk/firststeps/
class PyApp(gtk.Window):
    
	def __init__(self):
		# initialize the parent class
		super(PyApp, self).__init__()
		# connect signals for the GUI
		self.connect("destroy", gtk.main_quit)
		# set the initial requested size (may not end up this size if constrained)
		self.set_size_request(250, 150)
		# put the window in the center of the (primary? current?) screen
		self.set_position(gtk.WIN_POS_CENTER)
		# get the text to add to the form for kicks
		initial_text = self.get_mesonet_data()
		# make a label out of the text
		self.tmplabel = gtk.Label(initial_text)
		# make a scrollable container for holding the text so you can see it all
		self.main_scroller = gtk.ScrolledWindow()
		# add the label to the scrollable container 
		#   (labels are apparently funny with scrolls, so have to use add_with_viewport instead of just add)
		self.main_scroller.add_with_viewport(self.tmplabel)
		# then add the scrollable container to the main form
		self.add(self.main_scroller)
		# I'm not sure the difference between show and show_all, but maybe show_all initializes all the widgets?
		self.show_all()

	def get_mesonet_data(self):

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

				vals.append(tokens[0])
								        
		# now return a single string for now that is just each entry on a new line
		return '\n'.join(vals)
      
# once done doing any preliminary processing, actually run the application
main_window = PyApp()
gtk.main()