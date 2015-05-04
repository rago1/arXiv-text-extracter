import urllib
import re
import time
import sys
import os

def download(URL, filename):
    webFile = urllib.urlopen(URL)
    localFile = open(filename, "w+")
    w=webFile.read()
    localFile.write(w)
    webFile.close()
    localFile.close()
    try:
        t = re.search(r'<resumption[^>]+>([^<]+)<', w).group(1)
        print "Resumption token =",t
        return t
    except:
        if len(w)<200:
            print w
        return None

def runDownloader(startURL, i, maxIts, folder):
    z = True
    while z:
        try:
            time.sleep(30)
            x = download(startURL, folder+os.sep+"file"+str(i)+".xml")
            resumeURL = "http://export.arxiv.org/oai2?verb=ListRecords&resumptionToken="
            if x == None:
                z=False
            else:
                startURL = resumeURL+str(x)
            i=i+1
            if i>maxIts:
                z = False
        except Exception, e:
            print e
            print Exception
            z=False

def checkDirectoryExists(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)

def main():
    if "--help" in sys.argv[1:]:
        printHelp()
    else:
        maxIts = 3000
        if "--resume" in sys.argv[1:]:
            resume = sys.argv.index("--resume")
            startURL = "http://export.arxiv.org/oai2?verb=ListRecords&resumptionToken=" \
                       + sys.argv[resume+1]
            i = int(sys.argv[resume+2])
        else:
            startURL = "http://export.arxiv.org/oai2?verb=ListRecords&metadataPrefix=arXiv"
            i = 1
        if "--maximum-files" in sys.argv[1:]:
            try:
                maxIts = int(sys.argv[sys.argv.index("--maximum-files")+1])
            except:
                print "Incorrect value entered for maximum files, please enter an integer"
        folder = sys.argv[-1]
        checkDirectoryExists(folder)
        runDownloader(startURL, i, maxIts, folder)

def printHelp():
    print """
---------------------------------------------------
Script to download the metadata for the arXiv bulk
data sets. It does this by accessing the OAI for
arXiv. Due to the nature of OAI, each file
downloaded contains one thousand records and there
must be a thirty second pause between each
downloaded file. Each file downloaded will be
saved as "fileX.xml" with X being the number of
the file. A resumption token will be printed to
the screen should the download need to be
interupted and resumed
---------------------------------------------------
Usage:
downloadMetadata.py [options] [output]

with output being the folder to store the files
Options:
--resume "resumption token" "file number"
  resumes the download operation from the file
  number and resumption token
---------------------------------------------------
"""

if __name__ == "__main__":
    if sys.argv[1:]:
        main()
    else:
        print "Please provide arguments, for help use '--help'"
