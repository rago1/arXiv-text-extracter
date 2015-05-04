from xml.dom import minidom
import os
import sys
import cPickle as pickle

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def extractIds(identifiers, subIds, xmlDoc):
    recordList = xmlDoc.getElementsByTagName('record')
    for item in recordList:
        ident = str(getText(item.getElementsByTagName('id')[0].childNodes))
        spec = str(getText(item.getElementsByTagName('setSpec')[0].childNodes))
        sub = str(getText(item.getElementsByTagName('categories')[0].childNodes))
        identifiers[ident] = spec.replace(":","~")
        subIds[ident] = sub.split(" ")[0].replace(".","-")
    return identifiers, subIds

def main():
    if "--help" in sys.argv[1:]:
        printhelp()
    else:
        pathToXML = sys.argv[-1]
        if os.path.isdir(pathToXML):
            identifiers = {}
            subIds = {}
            for dirpath, dirnames, files in os.walk(pathToXML):
                for file_ in files:
                    read = open(os.path.join(dirpath, file_), 'r')
                    xmlDoc = minidom.parse(read)
                    read.close()
                    identifiers, subIds = extractIds(identifiers, subIds, xmlDoc)
            with open(os.path.join('..','res','identifiers.p'), 'wb') as fp:
                pickle.dump(identifiers, fp)
            with open(os.path.join('..','res','subIds.p'), 'wb') as fp2:
                pickle.dump(subIds, fp2)
        else:
            print "Incorrect path specified, make sure this exists"


def printhelp():
    print """
---------------------------------------------------
Script to extract the categories and sub-categories
from the metadata for the arXiv bulk data sets. It
gets the first category listed in the metadata. It
places this information in two dictionaries
---------------------------------------------------
Usage:
createDictIDs.py [input folder]
---------------------------------------------------
"""

if __name__ == "__main__":
    if sys.argv[1:]:
        main()
    else:
        print "Please Provide arguments, for help use '--help'"
#    To open
#    import cPickle as pickle
#    with open('identifiers.p', 'rb') as fp:
#        identifiers = pickle.load(fp)
#
#    Access via
#    print identifiers['0801.1347']
#    or
#    identifiers['0807.0034']


