import cPickle as pickle
import os
import shutil
import sys

with open(os.path.join('..','res','identifiers.p'), 'rb') as fp:
    identifiers = pickle.load(fp)

with open(os.path.join('..','res','subIds.p'), 'rb') as fp2:
    subIds = pickle.load(fp2)

def checkDirectoryExists(outFile):
    directory = os.path.dirname(outFile)
    if not os.path.exists(directory):
        os.makedirs(directory)

def printhelp():
    print """
-------------------------------------------------------
Script to move text files from the current folder to
the category or sub-category folder . Designed to be
used on Arxiv files with the newest naming conventions
(April 2007 onwards.)
-------------------------------------------------------
Usage:
moveToCateg.py [options] [output folder] [input folder]

with input folder being the folder containing
the txt files
Options:
--move
  delete the original files
--sub-categories
  move to sub-categories rather than categories
-------------------------------------------------------
"""

def getNewDir(relPaths, sub):
    ident = identifiers[relPaths[0]+"."+relPaths[1]]
    if sub:
        subDir = subIds[relPaths[0]+"."+relPaths[1]]
        newDir = ident + os.sep + subDir
    else:
        newDir = ident
    return newDir

def main(old, new, move, sub):
    for src_dir, dirs, files in os.walk(old):
        for filename in files:
            if filename.endswith(".txt"):
                i = 1
                relPaths = os.path.relpath(src_dir, old).split(os.sep)
                try:
                    newDir = getNewDir(relPaths, sub)
                    ide = relPaths[0]+"-"+relPaths[1]+'--'
                    src_file = os.path.join(src_dir, filename)
                    dst_file = os.path.join(new, newDir, ide+str(i)+'.txt')
                    checkDirectoryExists(dst_file)
                    while os.path.isfile(dst_file):
                        i = i+1
                        dst_file = os.path.join(new, newDir, ide+str(i)+'.txt')
                    if move:
                        shutil.move(src_file,dst_file)
                    else:
                        shutil.copy(src_file,dst_file)
                except Exception, e:
                    print 'error'
                    print e

if __name__ == "__main__":
    if sys.argv[1:]:
        if "--help" in sys.argv[1:]:
            printhelp()
        else:
            oldRoot = sys.argv[-1]
            newRoot = sys.argv[-2]
            move=False
            sub=False
            if "--move" in sys.argv[1:]:
                move=True
            if "--sub-categories" in sys.argv[1:]:
                sub=True
            main(oldRoot, newRoot, move, sub)
    else:
        print "Please provide arguments, for help use '--help'"
