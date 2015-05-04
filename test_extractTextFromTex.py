from arXivExtracter.extractTextFromTex import extractText, compileRegex, sortArgs
from xml.dom import minidom
import unittest
import os

class TestSortArgs(unittest.TestCase):
    def testDefault(self):
        self.assertEqual(sortArgs([]),
                         (False,[],["word","hword"],False,False,False,False),
                         'sortArgs Default not working')

    def testUsedArgs(self):
        self.assertEqual(sortArgs(["--replace-inline-math","inline__math","--output",
                                   "/Volumes/Corpus/Test06","Volumes/Corpus/Test03"]),
                         ("inline__math",[],["word","hword"],False,False,
                          "/Volumes/Corpus/Test06",False))

    def testNoPunc(self):
        self.assertEqual(sortArgs(["--no-punctuation"]),
                         (False,[],["word","hword"],True,False,False,False))

    def testIgnoreDefault(self):
        self.assertEqual(sortArgs(["--ignore-default-extraction"]),
                         (False,[],[],False,False,False,False))

    def testReplaceInlineMath(self):
        self.assertEqual(sortArgs(["--replace-inline-math","inline__math"]),
                         ("inline__math",[],["word","hword"],False,False,False,False))

    def testReplaceInlineMathIncorrectUsage(self):
        self.assertEqual(sortArgs(['--replace-inline-math','--output', 'file.txt']),
                         ("--output",[],["word","hword"],False,False,'file.txt',False))

    def testReplaceClass(self):
        self.assertEqual(sortArgs(["--replace-class","math", "maths"]),
                         (False,[["math","maths"]],["word","hword"],False,False,False,False))

    def testReplaceClasses(self):
        self.assertEqual(sortArgs(["--replace-class", "math", "maths",
                                   "--replace-class", "mathgroup", "more_maths"]),
                         (False, [["math","maths"],["mathgroup","more_maths"]],
                          ["word","hword"],False,False,False,False))

    def testExtractClass(self):
        self.assertEqual(sortArgs(["--extract-class", "math"]),
                         (False,[],["word","hword","math"],False,False,False,False))

    def testPuncFile(self):
        self.assertEqual(sortArgs(["--punctuation-file", "/Users/paolo/Desktop/puncFile.txt"]),
                         (False,[],["word","hword"],False,"/Users/paolo/Desktop/puncFile.txt",
                          False,False))

    def testOutputFile(self):
        self.assertEqual(sortArgs(["--output", "/Users/paolo/Desktop/output.txt"]),
                         (False,[],["word","hword"],False,False,
                          "/Users/paolo/Desktop/output.txt", False))

    def testOutputFileIncorrectUsage(self):
        self.assertEqual(sortArgs(["--output", "/Users/paolo/Desktop/output.tex"]),
                         (False,[],["word","hword"],False,False,
                          "/Users/paolo/Desktop/output.tex", "/Users/paolo/Desktop/output.tex"))

    def testInputFile(self):
        self.assertEqual(sortArgs(["/Users/paolo/Desktop/file.tex"]),
                         (False,[],["word","hword"],False,False,False,
                          "/Users/paolo/Desktop/file.tex"))

    def testErrorInlineMath(self):
        with self.assertRaises(IndexError):
            sortArgs(["--replace-inline-math"])

    def testErrorReplaceClass(self):
        with self.assertRaises(IndexError):
            sortArgs(["--replace-class"])

    def testErrorReplaceClass2(self):
        with self.assertRaises(IndexError):
            sortArgs(["--replace-class",'word'])

    def testErrorReplaceClass3(self):
        with self.assertRaises(IndexError):
            sortArgs(["--replace-class",'/Users/paolo/Desktop/input.tex'])

    def testErrorReplaceClasses(self):
        with self.assertRaises(IndexError):
            sortArgs(["--replace-class",'word',"hello","--replace-class","T"])

    def testErrorExtractClass(self):
        with self.assertRaises(IndexError):
            sortArgs(["--extract-class"])

    def testErrorExtractClass2(self):
        with self.assertRaises(IndexError):
            sortArgs(["word","--extract-class"])

    def testErrorPuncFile(self):
        with self.assertRaises(IndexError):
            sortArgs(["--punctuation-file"])

    def testErrorOutputFile(self):
        with self.assertRaises(IndexError):
            sortArgs(["--output"])



class TestExtractText(unittest.TestCase):
    def setUp(self):
        os.chdir('arXivExtracter')

    def tearDown(self):
        os.chdir('..')

    def testMinimalExample(self):
        file_ = os.path.abspath(os.path.join('..','testFiles','minimalExample.tex'))
        sArgs = sortArgs([])
        repRE, extRE, puncRE, delRE = compileRegex(sArgs[0], sArgs[1], sArgs[3],
                                           sArgs[4], sArgs[2])
        text = extractText(file_, repRE, extRE, puncRE, delRE)
        self.assertEqual(text, "")

    def testSampleOneDefault(self):
        file_ = os.path.abspath(os.path.join('..','testFiles','example1.tex'))
        sArgs = sortArgs([])
        repRE, extRE, puncRE, delRE = compileRegex(sArgs[0], sArgs[1], sArgs[3],
                                           sArgs[4], sArgs[2])
        text = extractText(file_, repRE, extRE, puncRE, delRE)
        self.assertEqual(text, "Sample Article One This is a sample document to test expected extraction."+\
                         " Section One Title This is section one. Section Two This is section two.")

    def testSampleOneNoPunc(self):
        file_ = os.path.abspath(os.path.join('..','testFiles','example1.tex'))
        sArgs = sortArgs(["--no-punctuation"])
        repRE, extRE, puncRE, delRE = compileRegex(sArgs[0], sArgs[1], sArgs[3],
                                           sArgs[4], sArgs[2])
        text = extractText(file_, repRE, extRE, puncRE, delRE)
        self.assertEqual(text, "Sample Article One This is a sample document to test expected extraction"+\
                         " Section One Title This is section one Section Two This is section two")

    def testSampleOneIgnoreDefault(self):
        file_ = os.path.abspath(os.path.join('..','testFiles','example1.tex'))
        sArgs = sortArgs(["--ignore-default-extraction","--extract-class","word"])
        repRE, extRE, puncRE, delRE = compileRegex(sArgs[0], sArgs[1], sArgs[3],
                                           sArgs[4], sArgs[2])
        text = extractText(file_, repRE, extRE, puncRE, delRE)
        self.assertEqual(text, "This is a sample document to test expected extraction."+\
                         " This is section one. This is section two.")

    def testSampleOneReplaceClass(self):
        file_ = os.path.abspath(os.path.join('..','testFiles','example1.tex'))
        sArgs = sortArgs(["--replace-class","hword","Header"])
        repRE, extRE, puncRE, delRE = compileRegex(sArgs[0], sArgs[1], sArgs[3],
                                           sArgs[4], sArgs[2])
        text = extractText(file_, repRE, extRE, puncRE, delRE)
        self.assertEqual(text, "Header Header Header This is a sample document to test expected extraction."+\
                         " Header Header Header This is section one. Header Header This is section two.")
        

    def testSample2default(self):
        file_ = os.path.abspath(os.path.join('..','testFiles','example2.tex'))
        sArgs = sortArgs([])
        repRE, extRE, puncRE, delRE = compileRegex(sArgs[0], sArgs[1], sArgs[3],
                                           sArgs[4], sArgs[2])
        text = extractText(file_, repRE, extRE, puncRE, delRE)
        self.assertEqual(text, "Sample Article Two This is a sample document to test expected extraction."+\
                         " Section One Title This is section one. This is an inline equation with text surrounding it."+\
                         " This is a normal equation This is a figure")

    def testSample2ExtractClass(self):
        file_ = os.path.abspath(os.path.join('..','testFiles','example2.tex'))
        sArgs = sortArgs(["--extract-class","oword"])
        repRE, extRE, puncRE, delRE = compileRegex(sArgs[0], sArgs[1], sArgs[3],
                                           sArgs[4], sArgs[2])
        text = extractText(file_, repRE, extRE, puncRE, delRE)
        self.assertEqual(text, "Sample Article Two This is a sample document to test expected extraction."+\
                         " Section One Title This is section one. This is an inline equation with text surrounding it."+\
                         " This is a normal equation This is a figure This is a figure caption")

    def testSample2ReplaceInlineMath(self):
        file_ = os.path.abspath(os.path.join('..','testFiles','example2.tex'))
        sArgs = sortArgs(["--replace-inline-math","inline_math"])
        repRE, extRE, puncRE, delRE = compileRegex(sArgs[0], sArgs[1], sArgs[3],
                                           sArgs[4], sArgs[2])
        text = extractText(file_, repRE, extRE, puncRE, delRE)
        self.assertEqual(text, "Sample Article Two This is a sample document to test expected extraction."+\
                         " Section One Title This is section one. This is an inline equation inline_math with text surrounding it."+\
                         " This is a normal equation This is a figure")

    def testSample2PuncFile(self):
        file_ = os.path.abspath(os.path.join('..','testFiles','example2.tex'))
        pFile = os.path.abspath(os.path.join('..','testFiles','samplePuncFile.txt'))
        sArgs = sortArgs(["--punctuation-file",pFile])
        repRE, extRE, puncRE, delRE = compileRegex(sArgs[0], sArgs[1], sArgs[3],
                                           sArgs[4], sArgs[2])
        text = extractText(file_, repRE, extRE, puncRE, delRE)
        self.assertEqual(text, "Sample Article Two This is a sample document to test expected extraction."+\
                         " Section One Title This is section one. This is an inline equation with text surrounding it."+\
                         " This is a normal equation This is a figure:")

    def testSample2PuncFileInlineMath(self):
        file_ = os.path.abspath(os.path.join('..','testFiles','example2.tex'))
        pFile = os.path.abspath(os.path.join('..','testFiles','samplePuncFile.txt'))
        sArgs = sortArgs(["--replace-inline-math","inline_math","--punctuation-file",pFile])
        repRE, extRE, puncRE, delRE = compileRegex(sArgs[0], sArgs[1], sArgs[3],
                                           sArgs[4], sArgs[2])
        text = extractText(file_, repRE, extRE, puncRE, delRE)
        self.assertEqual(text, "Sample Article Two This is a sample document to test expected extraction."+\
                         " Section One Title This is section one. This is an inline equation inline_math with text surrounding it."+\
                         " This is a normal equation This is a figure:")



if __name__ == "__main__":
    unittest.main()
