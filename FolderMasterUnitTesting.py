import os
import io
import re
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
        self.formattedInput = []
        self.chosenCases = {}
        self.baseDirectory = str(os.getcwd()[0].upper()) + str(os.getcwd()[1:])
        self.createButton = self.form.ui.createButton
        unitTestFolderName = "UnitTestFolder"
        self.unitTestDirectory = self.baseDirectory + "\\" + unitTestFolderName
        self.form.directory = self.unitTestDirectory
        if not os.path.exists(self.unitTestDirectory):
            os.mkdir(self.unitTestDirectory)
        if len(os.listdir(self.unitTestDirectory)) > 0:
            for name in os.listdir(self.unitTestDirectory):
                shutil.rmtree(self.unitTestDirectory + "//" +  name)
        self.form.ui.directoryTextbox.setText(self.unitTestDirectory)
        self.expectedOutput = []
        self.actualOutput = []
    def suppressNonTestOutput(self, method, input = None, willSupress = True):
        if willSupress == True:
            suppress_text = io.StringIO()
            sys.stdout = suppress_text
            if method == self.step_createFolders:
                method(input)
            if method == self.step_chooseCases:
                method()
            if method == self.form.folderFormattingAndReserveHandling:
                return method(input)
            sys.stdout = sys.__stdout__
        else:
            if method == self.step_createFolders: #or method == self.step_openTestCasesFile:
                method(input)
            if method == self.step_chooseCases:
                method()
            if method == self.form.folderFormattingAndReserveHandling:
                return method(input)
    def step_openTestCasesFile(self, testCasesFile):
        with open(testCasesFile, "r") as fileContents:
            for name in fileContents:
                self.input.append(name.strip("\n"))
        fileContents.close()
    def step_chooseCases(self):
        namecasesDict = {}
        for item in self.formattedInput:
            print("item", item)
            if type(item) == list:
                rootFolder = item[0]
                print("\t rootFolder", rootFolder)
                if item[0].lower() not in self.caseListDict:
                    self.caseListDict[rootFolder.lower()] = [item]
                    print("\t\t rootFolder", rootFolder)
                    namecasesDict[rootFolder.lower()] = set()
                    namecasesDict[rootFolder.lower()].add(rootFolder)
                else:
                    self.caseListDict[rootFolder.lower()].append(item)
                    print("\t\t rootFolder", rootFolder)
                    namecasesDict[rootFolder.lower()].add(rootFolder)
            else:
                if item.lower() not in self.caseListDict:
                    self.caseListDict[item.lower()] = [item]
                    print("\t\t item", item)
                    namecasesDict[item.lower()] = set()
                    namecasesDict[item.lower()].add(item)
                else:
                    self.caseListDict[item.lower()].append(item)
                    print("\t\t item", item)
                    namecasesDict[item.lower()].add(item)
        print("caseListDict", self.caseListDict)
        print("namecasesDict", namecasesDict)

        chosenNamecasesDict = {}        
        for key in namecasesDict.keys():
            namecases = set(namecasesDict[key])
            if (len(namecases) > 1):
                if (key in self.chosenCases):
                    choice = self.chosenCases[key]
                    w = FolderMaster.CaseStyleWindow(namecases)
                    for i in range(len(namecases)):
                        if(w.ui.listWidget.item(i).text() == choice):
                            chosenItem = w.ui.listWidget.item(i)
                            rect = w.ui.listWidget.visualItemRect(chosenItem)
                            QtTest.QTest.mouseClick(w.ui.listWidget.viewport(), QtCore.Qt.LeftButton, pos = rect.center())
                            chosenNamecase = w.selectedCase
                            chosenNamecasesDict[chosenNamecase.lower()] = chosenNamecase
            else:
                chosenNamecase = list(namecases)[0]
                chosenNamecasesDict[chosenNamecase.lower()] = chosenNamecase

            for i in range(len(self.caseListDict[key])):
                case = self.caseListDict[key][i]
                if type(case) == list:
                    case[0] = chosenNamecasesDict[chosenNamecase.lower()]
                    caseAsString = "//".join(case)
                    print("caseAsString", caseAsString)
                    #if self.ui.duplicateFoldersCheckbox.isChecked() == True and i == 0:
                    #    self.revisedInput.append(caseAsString)
                    #    break
                    #else:
                    self.revisedInput.append(caseAsString)
                else:
                    #if self.ui.duplicateFoldersCheckbox.isChecked() == True and i == 0:
                    #    self.revisedInput.append(case)
                    #    break
                    #else:
                    case = chosenNamecasesDict[chosenNamecase.lower()]
                    self.revisedInput.append(case)
                    print("case", case)
        print(chosenNamecasesDict)
        print("revisedInput", self.revisedInput)

        """
        for key in self.caseListDict.keys():
            namecases = set(namecasesDict[key])
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
                #print("before", self.revisedInput)
                self.revisedInput += self.caseListDict[key] #list(namecases) * len(self.caseListDict[key])
                #print("after", self.revisedInput)
        """
        
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
    
    def stepSet_withoutConflictingNamecases(self, testCasesFile, willSupressMainWindow = True, willSupressCaseStyleWindow = True, willSupressFormatting = True):
        ##print("2")
        self.step_openTestCasesFile(testCasesFile)
        print("input", self.input)
        ##print("3")
        for currentLine in list(self.input):
            #formattedName = self.form.folderFormattingAndReserveHandling(currentLine)
            formattedName = self.suppressNonTestOutput(
                self.form.folderFormattingAndReserveHandling,
                currentLine,
                willSupress = willSupressFormatting
            )
            if formattedName == False:
                #self.input.remove(currentLine)
                continue
            else:
                self.formattedInput.append(formattedName)
        print(self.formattedInput) 
        self.revisedInput = []
        #choose the cases
        self.caseListDict = {}
        self.suppressNonTestOutput(
            self.step_chooseCases,
            willSupress = willSupressCaseStyleWindow
        )
        print("revisedInput", self.revisedInput)
        #create the folders
        self.suppressNonTestOutput(
            self.step_createFolders,
            self.revisedInput,
            willSupress = willSupressMainWindow
        )
        #check expected result vs actual result
        self.step_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove folder
        self.step_removeFolders()
        self.assertEqual(self.actualOutput, [])

    #FOLDER TEST SET 0: basic tests
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

        for currentLine in list(self.input):
            #formattedName = self.form.folderFormattingAndReserveHandling(currentLine)
            formattedName = self.suppressNonTestOutput(
                self.form.folderFormattingAndReserveHandling,
                currentLine,
                willSupress = False
            )
            if formattedName == False:
                self.input.remove(currentLine)
            else:
                self.formattedInput.append(formattedName)

        #choose the cases
        self.caseListDict = {}
        self.suppressNonTestOutput(
            self.step_chooseCases,
            willSupress = False
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

    #FOLDER TEST SET 1: periods tests
    def test_testcase1_noDupe(self):
        testCasesFile = "tests/z_testcases1.txt"
        self.expectedOutput = [[".a"], ["a"], ["a a"], ["a.a"]]
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase1_yesDupe(self):
        testCasesFile = "tests/z_testcases1.txt"
        self.expectedOutput = [[".a"], ["a"], ["a (Copy 1)"], ["a (Copy 2)"], ["a (Copy 3)"], ["a a"], ["a.a"]]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    
    #FOLDER TEST SET 2: slashes tests
    #2a: prefixed and suffixed slashes are ignored
    def test_testcase2a_noDupe(self):
        testCasesFile = "tests/z_testcases2a.txt"
        self.expectedOutput = [["a"]]
        self.stepSet_withoutConflictingNamecases(
            testCasesFile,
            #willSupressCaseStyleWindow = False,
            #willSupressMainWindow = False 
        )
    def test_testcase2a_yesDupe(self):
        testCasesFile = "tests/z_testcases2a.txt"
        self.expectedOutput = [["a"], ["a (Copy 1)"], ["a (Copy 2)"], ["a (Copy 3)"], ["a (Copy 4)"], ["a (Copy 5)"], ["a (Copy 6)"]]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    #2b: multiple infixed slashes are treated as just one slash
    def test_testcase2b_noDupe(self):
        testCasesFile = "tests/z_testcases2b.txt"
        self.expectedOutput = [["a", "a"]]
        self.stepSet_withoutConflictingNamecases(
            testCasesFile,
            willSupressCaseStyleWindow = False
        )
    def test_testcase2b_yesDupe(self):
        testCasesFile = "tests/z_testcases2b.txt"
        self.expectedOutput = [
            ["a", "a"], ["a (Copy 1)", "a"], ["a (Copy 2)", "a"], ["a (Copy 3)", "a"], ["a (Copy 4)", "a"], ["a (Copy 5)", "a"]
        ]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    #2c: forward and backward shashes are treated the same.
    def test_testcase2c_noDupe(self):
        testCasesFile = "tests/z_testcases2c.txt"
        self.expectedOutput = [["a", "a", "a"]]
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase2c_yesDupe(self):
        testCasesFile = "tests/z_testcases2c.txt"
        self.expectedOutput = [["a", "a", "a"], ["a (Copy 1)", "a", "a"], ["a (Copy 2)", "a", "a"], ["a (Copy 3)", "a", "a"]]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    #2d: prefixed and/or suffixed slashes are ignored
    def test_testcase2d_noDupe(self):
        testCasesFile = "tests/z_testcases2d.txt"
        self.expectedOutput = [["a", "a"]]
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase2d_yesDupe(self):
        testCasesFile = "tests/z_testcases2d.txt"
        self.expectedOutput = [["a", "a"], ["a (Copy 1)", "a"], ["a (Copy 10)", "a"], ["a (Copy 11)", "a"], ["a (Copy 12)", "a"], ["a (Copy 13)", "a"], ["a (Copy 2)", "a"], ["a (Copy 3)", "a"], ["a (Copy 4)", "a"], ["a (Copy 5)", "a"], ["a (Copy 6)", "a"], ["a (Copy 7)", "a"], ["a (Copy 8)", "a"], ["a (Copy 9)", "a"]]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.stepSet_withoutConflictingNamecases(testCasesFile)

    #FOLDER TEST SET 3: reserved filenames tests
    def test_testcase3_noDupe(self):
        testCasesFile = "tests/z_testcases3.txt"
        self.expectedOutput = []
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase3_yesDupe(self):
        testCasesFile = "tests/z_testcases3.txt"
        self.expectedOutput = []
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.stepSet_withoutConflictingNamecases(testCasesFile)
   
    #FOLDER TEST SET 4: reserved characters tests
    def test_testcase4_noDupe(self):
        testCasesFile = "tests/z_testcases4.txt"
        self.expectedOutput = []
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase4_yesDupe(self):
        testCasesFile = "tests/z_testcases4.txt"
        self.expectedOutput = []
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.stepSet_withoutConflictingNamecases(testCasesFile)

    #FOLDER TEST SET 5: duplicate name cases (with different letters that are upper and lower case)
    #5a: 3 names with some duplicate cases, along with one name with no duplicates
    def test_testcase5a_noDupe(self):
        testCasesFile = "tests/z_testcases5a.txt"
        self.chosenCases = {"aa": "Aa", "ab": "ab", "abc": "aBc"}
        self.expectedOutput = [["Aa"], ["ab"], ["aBc"], ["AC"]]
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase5a_yesDupe(self):
        testCasesFile = "tests/z_testcases5a.txt"
        self.chosenCases = {"aa": "Aa", "ab": "ab", "abc": "aBc"}
        self.expectedOutput = [["Aa"], ["Aa (Copy 1)"], ["Aa (Copy 2)"], ["ab"], ["ab (Copy 1)"], ["aBc"], ["aBc (Copy 1)"], ["aBc (Copy 2)"], ["aBc (Copy 3)"], ["aBc (Copy 4)"], ["aBc (Copy 5)"], ["aBc (Copy 6)"], ["AC"], ["AC (Copy 1)"], ["AC (Copy 2)"]]
        #print("expectedOutput", self.expectedOutput)
        #print("actualOutput", self.actualOutput)
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    #5b: duplicate name cases with nested folders
    def test_testcase5b_noDupe(self):
        testCasesFile = "tests/z_testcases5b.txt"
        self.chosenCases = {"aa": "Aa", "ab": "ab"}
        self.expectedOutput = [["Aa", "a"], ["ab", "a"], ["AC", "a"]]
        self.stepSet_withoutConflictingNamecases(
            testCasesFile,
            willSupressCaseStyleWindow = False,
            willSupressFormatting = False
        )
    def test_testcase5b_yesDupe(self):
        testCasesFile = "tests/z_testcases5b.txt"
        self.chosenCases = {"aa": "Aa", "ab": "ab"}
        self.expectedOutput = [["Aa", "a"], ["Aa (Copy 1)", "a"], ["Aa (Copy 2)", "a"], ["Aa (Copy 3)", "a", "a"], ["ab", "a"], ["ab (Copy 1)", "a"], ["ab (Copy 2)", "a"], ["ab (Copy 3)", "a", "a"], ["AC", "a"],["AC (Copy 1)", "a"],["AC (Copy 2)", "a"], ["AC (Copy 3)", "a", "a"]]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    #5c: handling both nested and non nested folders
    def test_testcase5c_noDupe(self):
        testCasesFile = "tests/z_testcases5c.txt"
        self.chosenCases = {"aa": "Aa", "ab": "ab", "ac": "Ac", "ad": "Ad", "af": "Af"}
        self.expectedOutput = [["Aa"], ["ab"], ["Ac"], ["Ad"], ["AE"], ["Af", "a"]]
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase5c_yesDupe(self):
        testCasesFile = "tests/z_testcases5c.txt"
        self.chosenCases = {"aa": "Aa", "ab": "ab", "ac": "Ac", "ad": "Ad", "af": "Af"}
        self.expectedOutput = [["Aa"], ["Aa (Copy 1)"], ["Aa (Copy 2)"], ["Aa (Copy 3)", "a"], ["Aa (Copy 4)", "a"], ["Aa (Copy 5)", "a"], ["ab"], ["ab (Copy 1)"], ["ab (Copy 2)"], ["ab (Copy 3)", "a"], ["ab (Copy 4)", "a"], ["ab (Copy 5)", "a"], ["Ac"], ["Ac (Copy 1)"], ["Ac (Copy 2)"], ["Ac (Copy 3)", "a"], ["Ac (Copy 4)", "a"], ["Ac (Copy 5)", "a"], ["Ad"], ["Ad (Copy 1)"], ["AE"], ["AE (Copy 1)"], ["Af", "a"], ["Af (Copy 1)", "a"], ["Af (Copy 2)", "a"]]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    #FOLDER TEST SET 6: handling the order that non-nested and nested versions of files are made (created in the order that it is listed)
    #6a: with duplicate names
    def test_testcase6a_noDupe(self):
        testCasesFile = "tests/z_testcases6a.txt"
        self.chosenCases = {"ab": "AB", "ac": "AC"}
        self.expectedOutput = [["Aa"], ["AB", "a"], ["AC"], ["Ad", "a"]]
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase6a_yesDupe(self):
        testCasesFile = "tests/z_testcases6a.txt"
        self.chosenCases = {"ab": "AB", "ac": "AC"}
        self.expectedOutput = [["Aa"], ["AB", "a"], ["AB (Copy 1)"], ["AC"], ["AC (Copy 1)", "a"], ["Ad", "a"]]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    #6b: without duplicate names
    def test_testcase6b_noDupe(self):
        testCasesFile = "tests/z_testcases6b.txt"
        self.expectedOutput = [["Aa"], ["AB", "a"], ["AC"], ["Ad", "a"]]
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase6b_yesDupe(self):
        testCasesFile = "tests/z_testcases6b.txt"
        self.expectedOutput = [["Aa"], ["AB", "a"], ["AB (Copy 1)"], ["AC"], ["AC (Copy 1)", "a"], ["Ad", "a"]]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    #6c: further alternating, along with multiple nesting
    def test_testcase6c_noDupe(self):
        testCasesFile = "tests/z_testcases6c.txt"
        self.expectedOutput = [["Aa"], ["AB", "a"], ["AC"], ["Ad", "a", "a"]]
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase6c_yesDupe(self):
        testCasesFile = "tests/z_testcases6c.txt"
        self.expectedOutput = [
            ["Aa"], ["Aa (Copy 1)", "a"], ["Aa (Copy 2)", "a", "a"], ["Aa (Copy 3)"], 
            ["AB", "a"], ["AB (Copy 1)"], ["AB (Copy 2)", "a"], ["AB (Copy 3)"], 
            ["AC"], ["AC (Copy 1)", "a"], ["AC (Copy 2)"], ["AC (Copy 3)", "a"], 
            ["Ad", "a", "a"], ["Ad (Copy 1)"], ["Ad (Copy 2)"], ["Ad (Copy 3)", "a"]
        ]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.stepSet_withoutConflictingNamecases(testCasesFile)
    
    #FUNCTIONALITY TESTS:
        #Load (load all the files)

        #Save (save as file all)
        

if __name__ == "__main__":
    #Supress non unittest output:
    #suppress_text = io.StringIO()
    #sys.stdout = suppress_text
    
    unittest.main(verbosity=2)
    
    #Release non unittest output:
    #sys.stdout = sys.__stdout__