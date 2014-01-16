#!/usr/bin/env python

# as a precursor, find out the python version and system platform in case they need to be checked
import sys
python_version = float("%s.%s" % (sys.version_info.major, sys.version_info.minor))
if "linux" in sys.platform:
    platform = "linux"
elif "win" in sys.platform:
    platform = "windows"

# we can wrap the imports in try blocks to cleanly report on missing things
try:
    import urllib
except:
    print "Could not import urllib, need to install it!!"

##array and variable initialization here
vals = []

##src URL link
link = "http://www.mesonet.org/index.php/dataMdfMts/dataController/getFile/201401150000/mdf/TEXT/"

#open the URL
f = urllib.urlopen(link)

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
        
        line = f.readline()
        
        if line[0] == "<":
            break

        #strip the line endings and split the line into tokens
        tokens = line.strip().split()

        print(tokens[0])
        
        
