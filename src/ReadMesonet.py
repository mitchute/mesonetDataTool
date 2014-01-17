#!/usr/bin/env python

# as a precursor, find out the python version and system platform in case they need to be checked
import sys
import pygtk

## start working on the GUI
    ## I copied this example from here: http://zetcode.com/gui/pygtk/firststeps/
    ## It doesn't work :(
##class PyApp(pygtk.window):
##    def __init__(self):
##        #super(PyApp, self).__init__()
##        
##        self.set_title("Icon")
##        self.set_size_request(250, 150)
##        self.set_position(pygtk.WIN_POS_CENTER)
##
##        try:
##            self.set_icon_from_file("WeatherIcon.png")
##        except Exception, e:
##            print e.message
##            sys.exit(1)
##
##        self.connect("destroy", pygtk.main_quit)
##
##        self.show()
##
##PyApp()
##pygtk.main()

python_version = float("%s.%s" % (sys.version_info.major, sys.version_info.minor))
if "linux" in sys.platform:
    platform = "linux"
elif "win" in sys.platform:
    platform = "windows"

##array and variable initialization here
vals = []
f = ""

##src URL link
link = "http://www.mesonet.org/index.php/dataMdfMts/dataController/getFile/201401150000/mdf/TEXT/"

if python_version > 3:
    # we can wrap the imports in try blocks to cleanly report on missing things
    try:
        import urllib.request
        #open the URL
        f = urllib.request.urlopen(link)
    except:
        print("Could not import urllib, need to install it!!")
else:
    try:
        import urllib
        #open the URL
        f = urllib.urlopen(link)
    except:
        print("Could not import urllib, need to install it!!")

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

        print(tokens[0])
        
        
