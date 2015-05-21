import os
import re
import sys
import progressbar

# Requires progressbar

def sortArgs(listOfArgs):
    replaceInlineMath = False
    replaceClasses = []
    if "--ignore-default-extraction" in listOfArgs:
        extractClasses = []
    else:
        extractClasses = ["word", "hword"]
    noPunc = False
    puncFile = False
    outputFile = False
    inputFile = False
    for i, arg in enumerate(listOfArgs):           
        if arg == "--replace-class":
            dummylist = []
            dummylist.append(listOfArgs[i+1])
            dummylist.append(listOfArgs[i+2])
            replaceClasses.append(dummylist)
        elif arg == "--extract-class":
            extractClasses.append(listOfArgs[i+1])
        elif arg == "--replace-inline-math":
            replaceInlineMath = listOfArgs[i+1]
        elif arg == "--no-punctuation":
            noPunc = True
        elif arg == "--punctuation-file":
            puncFile = listOfArgs[i+1]
        elif arg == "--output":
            outputFile = listOfArgs[i+1]
        elif arg.endswith(".tex"):
            inputFile = arg
    return (replaceInlineMath, replaceClasses, extractClasses, noPunc,
            puncFile, outputFile, inputFile)
    

def compileRegex(replaceInlineMath, replaceClasses, noPunc, puncFile, extractClasses):

    replace = []
    if replaceInlineMath:
        replaceItem = []
        replaceItem.append(re.compile(
            r'<span class=\'mathgroup\'>\$</span>(.*?)<span class=\'mathgroup\'>\$</span>'))
        replaceItem.append(replaceInlineMath)
        replace.append(replaceItem)

    for item in replaceClasses:
        replaceItem = []
        replaceItem.append(re.compile(r'<span class=\''+item[0]+\
                                   '\'>([^<]+?)</span>'))
        replaceItem.append(item[1])
        replace.append(replaceItem)

    extract = []
    for item in extractClasses:
        extract.append(re.compile(r'<span class=\''+item+'\'>([^<]+?)</span>'))
    if not noPunc:
        punc = []
        if not puncFile:
            puncFile = os.path.join('..','res',"defaultPunc.txt")
        puncOpen = open(puncFile, "r")
        for line in puncOpen.readlines():
            punc.append(re.escape(line[:-1]))
        puncOpen.close()
        puncRegex = '({})'.format("|".join(punc))
        puncRe = (re.compile(r'([a-z])<span class=\'ignore\'>'+puncRegex+'</span>'))
    else:
        puncRe = False

    deleteRemaining = re.compile(r'<span class=[^>]+>([^<])+</span>')
    return replace, extract, puncRe, deleteRemaining

def extractText(inFile, repRE, extRE, puncRE, delRE):
    try:
        os.chdir('..')
        p = os.system('perl TeXcount/texcount.pl -v -html "'+inFile+'"> res'+os.sep+'dummy.html')
        os.chdir('arXivExtracter')
        htmlFile = open(os.path.join('..','res','dummy.html'), 'r')
        html = htmlFile.read()
        htmlFile.close()
        text = html.split("<div class='parse'><p>")[-1].split("</p></div>")[0]
        for replaceRE in repRE:
            text = replaceRE[0].sub(replaceRE[1], text)
        for extractRE in extRE:
            text = extractRE.sub(r'\1', text)
        if puncRE:
            text = puncRE.sub(r'\1\2',text)
        text = delRE.sub("", text)
        text = text.replace("<br>","").replace("&nbsp;", "")
        text = " ".join(text.split())
        return text
    except Exception, e:
        print "error"
        print e
        return -1
    
def checkDirectoryExists(outFile):
    directory = os.path.dirname(outFile)
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    arguments = []
    for arg in sys.argv[1:]:
        arguments.append(arg)
    if "--help" in arguments:
        printhelp()
    else:
        sArgs = sortArgs(arguments)
        if sArgs[6]:
            if sArgs[5]:
                outFile = sArgs[5]
                if os.sep in outFile:
                    checkDirectoryExists(outFile)
            else:
                outFile = sArgs[6].split(".tex")[0] + ".txt"
            repRE, extRE, puncRE, delRE = compileRegex(sArgs[0], sArgs[1], sArgs[3],
                                               sArgs[4], sArgs[2])
            toSave = extractText(sArgs[6], repRE, extRE, puncRE, delRE) 
            fileToSave = open(outFile, "w+")
            try:
                fileToSave.write(toSave)
            except:
                try:
                    fileToSave.write(toSave.encode('utf8'))
                except:
                    print "error writing to file"
            fileToSave.close()
        elif os.path.isdir(arguments[-1]):
            rootPath = arguments[-1]
            if sArgs[5]:
                newRoot = sArgs[5]
            else:
                newRoot = rootPath
            repRE, extRE, puncRE, delRE = compileRegex(sArgs[0], sArgs[1], sArgs[3],
                                               sArgs[4], sArgs[2])
            fileCount = sum((len(f) for _, _, f in os.walk(rootPath)))
            i=0
            widgets=[progressbar.FormatLabel('File %(value)d/%(max)d'),'  ',
                     progressbar.Bar(),'  ',progressbar.ETA() ]
            pBar = progressbar.ProgressBar(maxval = fileCount, widgets=widgets)
            pBar.start()
            for dirpath, dirnames, files in os.walk(rootPath):
                for filename in files:
                    pBar.update(i+1)
                    i=i+1
                    if filename.endswith(".tex"):
                        inFile = os.path.join(dirpath, filename)
                        outFile = inFile.replace(rootPath, newRoot).replace(
                            '.tex','.txt')
                        checkDirectoryExists(outFile)
                        toSave = extractText(inFile, repRE, extRE, puncRE, delRE)
                        if toSave != -1:
                            fileToSave = open(outFile, "w+")
                            try:
                                fileToSave.write(toSave)
                            except:
                                try:
                                    fileToSave.write(toSave.encode('utf8'))
                                except:
                                    print "error writing to file"
                            fileToSave.close()
            pBar.finish()
    
def printhelp():
    print """
---------------------------------------------------
Script to extract text from all the tex files in a
folder. Requires perl and progressbar. This
script uses TexCount to process the files, check
TexCount documentation for information on classes
---------------------------------------------------
Usage:
extractTextFromTex.py [options] [input]

with input being the tex file or a folder
containing the tex files
Options:
--replace-class "class" "string"
  replaces all instances of class with the string
--extract-class "class"
  extracts all the class contents, default options
  are word and hword
--ignore-default-extraction
  no defaults for extracting are set
--replace-inline-math "string"
  replaces all inline math with the string
--punctuation-file "file.txt"
  specify the punctuation to extract in a file,
  each item of punctuation must be the first item
  on the line, default is for "," and "."
--no-punctuation
  ignore the defaults for punctuation
--output [output file/folder]
  specify the output file or folder
---------------------------------------------------
"""

if __name__ == "__main__":
    if sys.argv[1:]:
        main()
    else:
        print "Please provide arguments, for help use '--help'"
