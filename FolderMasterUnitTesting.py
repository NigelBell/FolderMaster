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

    def test_basicCreateFolder(self):
        self.expectedOutput = ["a"]
        for name in self.expectedOutput:
            self.form.ui.folderNames.appendPlainText(name)
        QtTest.QTest.mouseClick(self.createButton, QtCore.Qt.LeftButton)

        #check expected result vs actual result
        self.actualOutput = os.listdir(self.unitTestDirectory)
        self.assertEqual(self.expectedOutput, self.actualOutput)

        #remove folder
        for name in self.expectedOutput:
            shutil.rmtree(self.unitTestDirectory + "//" + name)
        self.actualOutput = os.listdir(self.unitTestDirectory)
        print(self.actualOutput)
        self.assertEqual(self.actualOutput, [])

if __name__ == "__main__":
    #Supress non unittest output:
    suppress_text = io.StringIO()
    sys.stdout = suppress_text
    
    unittest.main(verbosity=2)
    
    #Release non unittest output:
    sys.stdout = sys.__stdout__