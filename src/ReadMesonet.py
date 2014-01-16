## import libraries here
import urllib.request

##array and variable initialization here
vals = []

##src URL link
link = "http://www.mesonet.org/index.php/dataMdfMts/dataController/getFile/201401150000/mdf/TEXT/"

##open the URL
f = urllib.request.urlopen(link)

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
        ##read the line and decode the bytes into unicode
            ##see stackoverflow example: http://stackoverflow.com/questions/13857856/split-byte-string-into-lines
        line = f.readline().decode()

        #strip the line endings and split the line into tokens
        tokens = line.strip().split()

        print(tokens[0])

        ##ends the read after the last data line.
            ##probably needs to be a better way to do this.
        if tokens[0] == "WYNO":
            break
        
        
