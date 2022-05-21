import os
import io
import sys
import shutil
import unittest
from PyQt5 import QtGui, QtWidgets, QtTest, QtCore
import FolderMaster

app = QtWidgets.QApplication(sys.argv)

class FolderMasterTest(unittest.TestCase):
    def setUp(self):
        self.form = FolderMaster.MainWindow()
        self.input = []
        self.baseDirectory = str(os.getcwd()[0].upper()) + str(os.getcwd()[1:])
        self.createButton = self.form.ui.createButton
        unitTestFolderName = "UnitTestFolder"
        self.unitTestDirectory = self.baseDirectory + "\\" + unitTestFolderName
        self.form.directory = self.unitTestDirectory
        if not os.path.exists(self.unitTestDirectory):
            os.mkdir(self.unitTestDirectory)
        if len(os.listdir(self.unitTestDirectory)) > 0:
            for name in os.listdir(self.unitTestDirectory):
                shutil.rmtree(self.unitTestDirectory + "//" +  name[0])
        self.form.ui.directoryTextbox.setText(self.unitTestDirectory)
        self.expectedOutput = []
        self.actualOutput = []
    def suppressNonTestOutput(self, method, input = None):
        suppress_text = io.StringIO()
        sys.stdout = suppress_text
        if method == self.step_createFolders:
            method(input)
        if method == self.step_chooseCases:
            method()
        sys.stdout = sys.__stdout__
    def step_openTestCasesFile(self, testCasesFile):
        with open(testCasesFile, "r") as fileContents:
            for name in fileContents:
                self.input.append(name.strip("\n"))
        fileContents.close()
    def step_chooseCases(self):
        for item in self.input:
            if item.lower() not in self.caseListDict:
                self.caseListDict[item.lower()] = [item]
            else:
                self.caseListDict[item.lower()].append(item)
        for key in self.caseListDict.keys():
            namecases = set(self.caseListDict[key])
            if (len(namecases) > 1):
                if (key in self.chosenCases):
                    choice = self.chosenCases[key]
                    w = FolderMaster.CaseStyleWindow(namecases)
                    for i in range(len(namecases)):
                        if(w.ui.listWidget.item(i).text() == choice):
                            chosenItem = w.ui.listWidget.item(i)
                            rect = w.ui.listWidget.visualItemRect(chosenItem)
                            QtTest.QTest.mouseClick(w.ui.listWidget.viewport(), QtCore.Qt.LeftButton, pos = rect.center())
                            self.revisedInput += [w.selectedCase] * len(self.caseListDict[key])
            else:
                self.revisedInput += list(namecases) * len(self.caseListDict[key])
    def step_createFolders(self, input):
        for name in input:
            self.form.ui.folderNames.appendPlainText(name)
        QtTest.QTest.mouseClick(self.createButton, QtCore.Qt.LeftButton)
    def step_getActualOutput(self):
       for item in os.listdir(self.unitTestDirectory):
            self.actualOutput.append([item])
            for root,dirs,files in os.walk(self.unitTestDirectory + "//" + item, topdown=True):
                if dirs != []:
                    self.actualOutput[-1].append(dirs[-1])
                else:
                    break
    def step_removeFolders(self):
        for name in self.expectedOutput:
            shutil.rmtree(self.unitTestDirectory + "//" +  name[0])
        self.actualOutput = os.listdir(self.unitTestDirectory)

    def test_basic1_createFolder(self):
        self.input = ["a"]
        self.expectedOutput = [["a"]]
        #create the folders
        self.suppressNonTestOutput(
            self.step_createFolders,
            self.input
        )
        #check expected result vs actual result
        self.step_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove the folders
        self.step_removeFolders()
        self.assertEqual(self.actualOutput, [])
    def test_basic2_createCumulativeDuplicates(self):
        self.input = ["a", "a"]
        self.expectedOutput = [["a"], ["a (Copy 1)"]]
        #tick the checkbox
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        #create the folders
        self.suppressNonTestOutput(
            self.step_createFolders,
            self.input
        )
        #check expected result vs actual result
        self.step_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove the folders
        self.step_removeFolders()
        self.assertEqual(self.actualOutput, [])
    def test_basic3_createMultiLevelFolder(self):
        self.input = ["a//a"]
        self.expectedOutput = [["a", "a"]]
        #create the folders
        self.suppressNonTestOutput(
            self.step_createFolders,
            self.input
        )
        #check expected result vs actual result
        self.step_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove the folders
        self.step_removeFolders()
        self.assertEqual(self.actualOutput, [])
    def test_basic4_conflictingCases(self):
        self.input = ["AA", "aa", "Aa"] 
        self.chosenCases = {"aa": "Aa"}
        self.expectedOutput = [["Aa"]]
        self.revisedInput = []
        #choose the cases
        self.caseListDict = {}
        self.suppressNonTestOutput(
            self.step_chooseCases
        )
        #create the folders
        self.suppressNonTestOutput(
            self.step_createFolders,
            self.revisedInput
        )
        #check expected result vs actual result
        self.step_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove folder
        self.step_removeFolders()
        self.assertEqual(self.actualOutput, [])
    
    #TEST SET 1: periods tests
    def test_testcase1a_periodsTestWithoutDuplicates(self):
        testCasesFile = "tests/z_testcases1.txt"
        self.step_openTestCasesFile(testCasesFile)
        self.expectedOutput = [[".a"], ["a"], ["a a"], ["a.a"]]
        self.revisedInput = []
        #choose the cases
        self.caseListDict = {}
        self.suppressNonTestOutput(
            self.step_chooseCases
        )
        #create the folders
        self.suppressNonTestOutput(
            self.step_createFolders,
            self.revisedInput
        )
        #check expected result vs actual result
        self.step_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove folder
        self.step_removeFolders()
        self.assertEqual(self.actualOutput, [])
    def test_testcase1b_periodsTestWithDuplicates(self):
        testCasesFile = "tests/z_testcases1.txt"
        self.step_openTestCasesFile(testCasesFile)
        self.expectedOutput = [[".a"], ["a"], ["a (Copy 1)"], ["a (Copy 2)"], ["a (Copy 3)"], ["a a"], ["a.a"]]
        self.revisedInput = []
        #tick the checkbox
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        #choose the cases
        self.caseListDict = {}
        self.suppressNonTestOutput(
            self.step_chooseCases
        )
        #create the folders
        self.suppressNonTestOutput(
            self.step_createFolders,
            self.revisedInput
        )
        #check expected result vs actual result
        self.step_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove folder
        self.step_removeFolders()
        self.assertEqual(self.actualOutput, [])

    
if __name__ == "__main__":
    #Supress non unittest output:
    #suppress_text = io.StringIO()
    #sys.stdout = suppress_text
    
    unittest.main(verbosity=2)
    
    #Release non unittest output:
    #sys.stdout = sys.__stdout__