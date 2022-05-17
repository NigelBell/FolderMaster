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
        self.baseDirectory = str(os.getcwd()[0].upper()) + str(os.getcwd()[1:])
        self.createButton = self.form.ui.createButton
        unitTestFolderName = "UnitTestFolder"
        self.unitTestDirectory = self.baseDirectory + "\\" + unitTestFolderName
        self.form.directory = self.unitTestDirectory
        if not os.path.exists(self.baseDirectory + "\\" + unitTestFolderName):
            os.mkdir(self.unitTestDirectory)
        #print("Before", self.form.ui.directoryTextbox.text())
        self.form.ui.directoryTextbox.setText(self.unitTestDirectory)
        #print("After", self.form.ui.directoryTextbox.text())
        self.expectedOutput = []
        self.actualOutput = []
    
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

    def test_basic_createFolder(self):
        self.input = ["a"]
        #create the folders
        self.step_createFolders(self.input)
        #check expected result vs actual result
        self.expectedOutput = [["a"]]
        self.step_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove the folders
        self.step_removeFolders()
        self.assertEqual(self.actualOutput, [])
    
    def test_basic_createCumulativeDuplicates(self):
        self.input = ["a", "a"]
        #tick the checkbox
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        print(self.form.ui.duplicateFoldersCheckbox.isChecked())
        #create the folders
        self.step_createFolders(self.input)
        #check expected result vs actual result
        self.expectedOutput = [["a"], ["a (Copy 1)"]]
        self.step_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove the folders
        self.step_removeFolders()
        self.assertEqual(self.actualOutput, [])

    def test_basic_createMultiLevelFolder(self):
        self.input = ["a//a"]
        #create the folders
        self.step_createFolders(self.input)
        #check expected result vs actual result
        self.expectedOutput = [["a", "a"]]
        self.step_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove the folders
        self.step_removeFolders()
        self.assertEqual(self.actualOutput, [])
    
    """
    def test_basic_conflictingCases(self):
        self.input = ["AA", "aa", "Aa"]
        #choose the cases
        chosenCases = ""

        #create the folders
        self.step_createFolders(self.input)
        #check expected result vs actual result
        self.expectedOutput = [["aa"]]
        self.step_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove folder
        self.step_removeFolders()
        self.assertEqual(self.actualOutput, [])
    """
if __name__ == "__main__":
    #Supress non unittest output:
    #suppress_text = io.StringIO()
    #sys.stdout = suppress_text
    
    unittest.main(verbosity=2)
    
    #Release non unittest output:
    #sys.stdout = sys.__stdout__