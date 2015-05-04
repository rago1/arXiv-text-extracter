import os, sys
import tarfile
import time
import gzip
import sys

def py_files2(members):
    for tarinfo in members:
        if os.path.splitext(tarinfo.name)[1] == ".gz":
            yield tarinfo

def py_files3(members):
    for tarinfo in members:
        if os.path.splitext(tarinfo.name)[1] == ".tex":
            yield tarinfo

def checkDirectoryExists(outFile):
    directory = os.path.dirname(outFile)
    if not os.path.exists(directory):
        os.makedirs(directory)

def printhelp():
    print """
---------------------------------------------------
Script to extract tex files from all the tar
files in a folder. Designed to be used on
Arxiv files with the newest naming conventions
(April 2007 onwards.)
---------------------------------------------------
Usage:
extractTexFromTar.py [output folder] [input folder]

with input folder being the folder containing
the tar files
---------------------------------------------------
"""

def main(inFolder, outFolder):
    TarErrors = []
    for (dirpath, dirnames, filenames) in os.walk(inFolder):
        for file_ in filenames:
            if file_.split(".")[-1] == "tar":
                try:
                    filePath = os.path.join(dirpath, file_)
                    tar = tarfile.open(filePath)
                    tar.extractall(path=outFolder,members=py_files2(tar))
                    tar.close()
                except:
                    TarErrors.append(str(filePath))

    errorfile1 = open("ExtractTarErrors.txt", "w+")

    for error in TarErrors:
        errorfile1.write(str(error)+"\n")

    errorfile1.close()

    Errors = []

    for (dirpath, dirnames, filenames) in os.walk(outFolder):
        for anyFile in filenames:
            pathToFile = os.path.join(dirpath, anyFile)
            try:
                pathToNewFile=outFolder+os.sep+str(anyFile).split(".")[0]+ \
                       os.sep+str(anyFile).split(".")[1]
            except:
                Errors.append(str(anyFile)+"  can't assign new name")
            try:
                if anyFile.split(".")[-1] == "gz":
                    tar = tarfile.open(pathToFile)
                    tar.extractall(path=pathToNewFile+os.sep,members=py_files3(tar))
                    tar.close()
                    os.remove(pathToFile)
            except Exception,e:
                try:
                    if anyFile.split(".")[-1] == "gz":
                        try:
                            os.makedirs(str(pathToNewFile))
                        except Exception, e3:
                            print e3
                        f_out=open(pathToNewFile+os.sep+"tex.tex","w")
                        f_in=gzip.open(pathToFile,'rb')
                        file_content=f_in.read()
                        for line in file_content:
                            f_out.write(line)
                        f_in.close()
                        f_out.close()
                        os.remove(pathToFile)
                except Exception, e2:
                    Errors.append(str(anyFile)+"  -  "+str(e)+" - "+str(e2))

    errorfile = open("ExtractTexErrors.txt", "w+")

    for error in Errors:
        errorfile.write(str(error)+"\n")

    errorfile.close()
    return 0

if __name__ == "__main__":
    if sys.argv[1:]:
        if "--help" in sys.argv[1:]:
            printhelp()
        else:
            oldRoot = sys.argv[-1]
            newRoot = sys.argv[-2]
            main(oldRoot, newRoot)
    else:
        print "Please provide arguments, for help use '--help'"
