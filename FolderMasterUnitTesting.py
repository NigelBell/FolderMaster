import os
import io
import sys
import shutil
import unittest
from PyQt5 import QtWidgets, QtTest, QtCore
import FolderMaster

app = QtWidgets.QApplication(sys.argv)

class FolderMasterTest(unittest.TestCase):
    def setUp(self):
        self.form = FolderMaster.MainWindow()
        self.input = []
        self.chosenCases = {}
        self.expectedOutput = []
        self.actualOutput = []
        self.revisedInput = []

        self.createButton = self.form.ui.createButton
        self.baseDirectory = str(os.getcwd()[0].upper()) + str(os.getcwd()[1:])
        self.unitTestDirectory = self.baseDirectory + "\\" + "UnitTestFolder"
        if not os.path.exists(self.unitTestDirectory):
            os.mkdir(self.unitTestDirectory)
        if len(os.listdir(self.unitTestDirectory)) > 0:
            for name in os.listdir(self.unitTestDirectory):
                shutil.rmtree(self.unitTestDirectory + "//" + name)
        self.form.ui.directoryTextbox.setText(self.unitTestDirectory)

    def suppressNonTestOutput(self, method, input = None, willSupress = True):
        if willSupress == True:
            suppress_text = io.StringIO()
            sys.stdout = suppress_text
            if method in [
                self.ut_createFolders
            ]:
                method(input)
            if method in [
                self.ut_preselectCases, 
                self.form.createFolders_step1_nameFormatting, 
                self.form.createFolders_step2_namesAndNamecases
            ]:
                method()
            sys.stdout = sys.__stdout__
        else:
            if method in [
                self.ut_createFolders
            ]:
                method(input)
            if method in [
                self.ut_preselectCases, 
                self.form.createFolders_step1_nameFormatting, 
                self.form.createFolders_step2_namesAndNamecases
            ]:
                method()
    
    def ut_appendFolders(self, input):
        for name in input:
            self.form.ui.folderNames.appendPlainText(name)
    def ut_createFolders(self, input):
        print("input", input)
        self.ut_appendFolders(input)
        QtTest.QTest.mouseClick(self.createButton, QtCore.Qt.LeftButton)
    def ut_getActualOutput(self):
       for item in os.listdir(self.unitTestDirectory):
            self.actualOutput.append([item])
            for root, dirs, files in os.walk(self.unitTestDirectory + "//" + item, topdown=True):
                if dirs != []:
                    self.actualOutput[-1].append(dirs[-1])
                else:
                    break
    def ut_removeFolders(self):
        for name in self.expectedOutput:
            shutil.rmtree(self.unitTestDirectory + "//" +  name[0])
        self.actualOutput = os.listdir(self.unitTestDirectory)

    def ut_preselectCases(self):
        print("PRESELECT START")
        print("pc folderNamecasesDict", self.form.folderNamecasesDict)
        print("pc folderNameDict", self.form.folderNameDict)
        print("pc chosenCases", self.chosenCases)
        chosenNamecasesDict = {}
        for key in self.form.folderNamecasesDict.keys():
            #if (self.form.ui.duplicateFoldersCheckbox.isChecked()):
                #print("\ta key", key)
            #else:
            print("\tb key", key)
            namecases = set(self.form.folderNamecasesDict[key])
            print("\tnamecases", namecases)
            if (len(namecases) > 1):
                print("\t\t#a")
                if (key in self.chosenCases):
                    print("\t\t\t#a1")
                    choice = self.chosenCases[key]
                    caseStyleWindow = FolderMaster.CaseStyleWindow(namecases)
                    for i in range(len(namecases)):
                        if (caseStyleWindow.ui.listWidget.item(i).text() == choice):
                            chosenItem = caseStyleWindow.ui.listWidget.item(i)
                            rect = caseStyleWindow.ui.listWidget.visualItemRect(chosenItem)
                            QtTest.QTest.mouseClick(
                                caseStyleWindow.ui.listWidget.viewport(), 
                                QtCore.Qt.LeftButton, 
                                pos = rect.center()
                            )
                            chosenNamecase = caseStyleWindow.selectedCase
                            chosenNamecasesDict[chosenNamecase.lower()] = chosenNamecase
                else:
                    chosenNamecase = list(namecases)[0]
                    chosenNamecasesDict[chosenNamecase.lower()] = chosenNamecase
                    print("\t\t\tchosenNamecase", chosenNamecase)
            else:
                print("\t\t#b")
                chosenNamecase = list(namecases)[0]
                chosenNamecasesDict[chosenNamecase.lower()] = chosenNamecase
            print("\tchosenNamecasesDict", chosenNamecasesDict)
            print("\tchosenNamecase", chosenNamecase)
            for i in range(len(self.form.folderNameDict[key])):
                case = self.form.folderNameDict[key][i]
                print("\t\tcase", case)
                if type(case) == list:
                    case[0] = chosenNamecasesDict[chosenNamecase.lower()]
                    caseAsString = "//".join(case)
                    self.revisedInput.append(caseAsString)
                else:
                    case = chosenNamecasesDict[chosenNamecase.lower()]
                    self.revisedInput.append(case)
        #clear the lists and dictionaries used in the main window
        self.form.ui.folderNames.clear()
        self.form.formattedInputList = []
        self.form.folderNameDict = {}
        self.form.folderNamecasesDict = {}
        print("PRESELECT END")
    def ut_openTestCasesFile(self, testCasesFile):
        with open(testCasesFile, "r") as fileContents:
            for name in fileContents:
                self.input.append(name.strip("\n"))
        fileContents.close()
    
    def utSet_withoutConflictingNamecases(self, testCasesFile, willSupressMainWindow = True, willSupressCaseStyleWindow = True, willSupressFormatting = True):
        self.ut_openTestCasesFile(testCasesFile)
        #print("input", self.input)

        self.ut_appendFolders(self.input)

        #perform the first 2 steps from createFolders
        self.suppressNonTestOutput(
            self.form.createFolders_step1_nameFormatting,
            willSupress = willSupressFormatting
        )
        #print("formattedInputList", self.form.formattedInputList)
        self.suppressNonTestOutput(
            self.form.createFolders_step2_namesAndNamecases,
            willSupress = willSupressFormatting
        )

        #choose the cases
        self.suppressNonTestOutput(
            self.ut_preselectCases,
            willSupress = willSupressCaseStyleWindow
        )
        #create the folders
        self.suppressNonTestOutput(
            self.ut_createFolders,
            self.revisedInput,
            willSupress = willSupressMainWindow
        )
        #check expected result vs actual result
        self.ut_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove folder
        self.ut_removeFolders()
        self.assertEqual(self.actualOutput, [])

    #FOLDER TEST SET 0: basic tests
    def test_basic1_createFolder(self):
        self.input = ["a"]
        self.expectedOutput = [["a"]]

        #create the folders
        self.suppressNonTestOutput(
            self.ut_createFolders,
            self.input
        )
        #check expected result vs actual result
        self.ut_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove the folders
        self.ut_removeFolders()
        self.assertEqual(self.actualOutput, [])
    def test_basic2_createCumulativeDuplicates(self):
        self.input = ["a", "a"]
        self.expectedOutput = [["a"], ["a (Copy 1)"]]

        #tick the checkbox
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        #create the folders
        self.suppressNonTestOutput(
            self.ut_createFolders,
            self.input
        )
        #check expected result vs actual result
        self.ut_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove the folders
        self.ut_removeFolders()
        self.assertEqual(self.actualOutput, [])
    def test_basic3_createMultiLevelFolder(self):
        self.input = ["a//a"]
        self.expectedOutput = [["a", "a"]]

        #create the folders
        self.suppressNonTestOutput(
            self.ut_createFolders,
            self.input
        )
        #check expected result vs actual result
        self.ut_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove the folders
        self.ut_removeFolders()
        self.assertEqual(self.actualOutput, [])
    def test_basic4_conflictingCases(self):
        self.input = ["AA", "aa", "Aa"] 
        self.chosenCases = {"aa": "Aa"}
        self.expectedOutput = [["Aa"]]

        self.ut_appendFolders(self.input)
        
        #perform the first 2 steps from createFolders
        self.suppressNonTestOutput(
            self.form.createFolders_step1_nameFormatting
        )
        #print("formattedInputList", self.form.formattedInputList)
        self.suppressNonTestOutput(
            self.form.createFolders_step2_namesAndNamecases
        )
        #print("folderNameDict", self.form.folderNameDict)
        #print("folderNamecasesDict", self.form.folderNamecasesDict)

        #choose the cases
        self.suppressNonTestOutput(
            self.ut_preselectCases,
            #willSupress = False
        )
        #create the folders
        self.suppressNonTestOutput(
            self.ut_createFolders,
            self.revisedInput,
        )

        #check expected result vs actual result
        self.ut_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove folder
        self.ut_removeFolders()
        self.assertEqual(self.actualOutput, [])
    def test_basic5a_createCumulativeDuplicatesAlongWithPreexistingFolders(self):
        os.mkdir(self.unitTestDirectory + "\\" + "Aa")
        self.input = ["AA", "aa", "Aa"] 
        self.chosenCases = {"aa": "Aa"}
        self.expectedOutput = [["Aa"], ["Aa (Copy 1)"], ["Aa (Copy 2)"], ["Aa (Copy 3)"]]

        #tick the checkbox
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)

        self.ut_appendFolders(self.input)

        #perform the first 2 steps from createFolders
        self.suppressNonTestOutput(
            self.form.createFolders_step1_nameFormatting
        )
        self.suppressNonTestOutput(
            self.form.createFolders_step2_namesAndNamecases
        )

        #choose the cases
        self.suppressNonTestOutput(
            self.ut_preselectCases
        )
        #create the folders
        self.suppressNonTestOutput(
            self.ut_createFolders,
            self.revisedInput
        )

        #check expected result vs actual result
        self.ut_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove folder
        self.ut_removeFolders()
        self.assertEqual(self.actualOutput, [])
    def test_basic5b_createCumulativeDuplicatesClickDouble(self):
        self.input = ["AA", "aa", "Aa"] 
        self.chosenCases = {"aa": "Aa"}
        self.expectedOutput = [["Aa"], ["Aa (Copy 1)"], ["Aa (Copy 2)"], ["Aa (Copy 3)"], ["Aa (Copy 4)"], ["Aa (Copy 5)"]]
    
        #tick the checkbox
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)

        self.ut_appendFolders(self.input)

        #perform the first 2 steps from createFolders
        self.suppressNonTestOutput(
            self.form.createFolders_step1_nameFormatting
        )
        self.suppressNonTestOutput(
            self.form.createFolders_step2_namesAndNamecases
        )

        #choose the cases
        self.suppressNonTestOutput(
            self.ut_preselectCases
        )
        #create the folders
        self.suppressNonTestOutput(
            self.ut_createFolders,
            self.revisedInput
        )
        #click the button again
        QtTest.QTest.mouseClick(self.createButton, QtCore.Qt.LeftButton)

        #check expected result vs actual result
        self.ut_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove folder
        self.ut_removeFolders()
        self.assertEqual(self.actualOutput, [])
    
    def test_basic5c_switchPreexistingFolderCase(self):
        os.mkdir(self.unitTestDirectory + "\\" + "Aa")
        self.input = ["AA", "aa", "Aa"] 
        self.chosenCases = {"aa": "AA"}
        self.expectedOutput = [["AA"], ["AA (Copy 1)"], ["AA (Copy 2)"], ["AA (Copy 3)"]]

        #tick the checkbox
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)

        self.ut_appendFolders(self.input)

        #perform the first 2 steps from createFolders
        self.suppressNonTestOutput(
            self.form.createFolders_step1_nameFormatting
        )
        self.suppressNonTestOutput(
            self.form.createFolders_step2_namesAndNamecases
        )
        
        #choose the cases
        self.suppressNonTestOutput(
            self.ut_preselectCases
        )
        #create the folders
        self.suppressNonTestOutput(
            self.ut_createFolders,
            self.revisedInput
        )

        #check expected result vs actual result
        self.ut_getActualOutput()
        self.assertEqual(self.expectedOutput, self.actualOutput)
        #remove folder
        self.ut_removeFolders()
        self.assertEqual(self.actualOutput, [])
    #FOLDER TEST SET 1a: periods tests, single letter (a)
    def test_testcase1a_noDupe(self):
        testCasesFile = "tests/z_testcases1a.txt"
        self.expectedOutput = [[".a"], ["a", "a", "a"], ["a a"], ["a.a"]]
        self.utSet_withoutConflictingNamecases(testCasesFile, 
            #willSupressMainWindow = False, 
            #willSupressCaseStyleWindow = False, 
            #willSupressFormatting = False
        )
    def test_testcase1a_yesDupe(self):
        testCasesFile = "tests/z_testcases1a.txt"
        self.expectedOutput = [[".a"], ["a", "a", "a"], ["a (Copy 1)"], ["a (Copy 2)", "a"], ["a (Copy 3)"], ["a (Copy 4)"], ["a a"], ["a.a"]]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.utSet_withoutConflictingNamecases(testCasesFile)
    
    #FOLDER TEST SET 1b: periods tests, a word (apple)
    def test_testcase1b_noDupe(self):
        testCasesFile = "tests/z_testcases1b.txt"
        self.expectedOutput = [[".apple"], ["apple", "apple", "apple"], ["apple apple"], ["apple.apple"]]
        self.utSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase1b_yesDupe(self):
        testCasesFile = "tests/z_testcases1b.txt"
        self.expectedOutput = [[".apple"], ["apple", "apple", "apple"], ["apple (Copy 1)"], ["apple (Copy 2)", "apple"], ["apple (Copy 3)"], ["apple (Copy 4)"], ["apple apple"], ["apple.apple"]]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.utSet_withoutConflictingNamecases(testCasesFile)

    #FOLDER TEST SET 2: slashes tests
    #2a: prefixed and suffixed slashes are ignored
    def test_testcase2a_noDupe(self):
        testCasesFile = "tests/z_testcases2a.txt"
        self.expectedOutput = [["a"]]
        self.utSet_withoutConflictingNamecases(
            testCasesFile,
            #willSupressCaseStyleWindow = False,
            #willSupressMainWindow = False 
        )
    def test_testcase2a_yesDupe(self):
        testCasesFile = "tests/z_testcases2a.txt"
        self.expectedOutput = [["a"], ["a (Copy 1)"], ["a (Copy 2)"], ["a (Copy 3)"], ["a (Copy 4)"], ["a (Copy 5)"], ["a (Copy 6)"]]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.utSet_withoutConflictingNamecases(testCasesFile)
    #2b: multiple infixed slashes are treated as just one slash
    def test_testcase2b_noDupe(self):
        testCasesFile = "tests/z_testcases2b.txt"
        self.expectedOutput = [["a", "a"]]
        self.utSet_withoutConflictingNamecases(
            testCasesFile,
            #willSupressCaseStyleWindow = False
        )
    def test_testcase2b_yesDupe(self):
        testCasesFile = "tests/z_testcases2b.txt"
        self.expectedOutput = [
            ["a", "a"], ["a (Copy 1)", "a"], ["a (Copy 2)", "a"], ["a (Copy 3)", "a"], ["a (Copy 4)", "a"], ["a (Copy 5)", "a"]
        ]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.utSet_withoutConflictingNamecases(testCasesFile)
    #2c: forward and backward shashes are treated the same.
    def test_testcase2c_noDupe(self):
        testCasesFile = "tests/z_testcases2c.txt"
        self.expectedOutput = [["a", "a", "a"]]
        self.utSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase2c_yesDupe(self):
        testCasesFile = "tests/z_testcases2c.txt"
        self.expectedOutput = [["a", "a", "a"], ["a (Copy 1)", "a", "a"], ["a (Copy 2)", "a", "a"], ["a (Copy 3)", "a", "a"]]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.utSet_withoutConflictingNamecases(testCasesFile)
    #2d: prefixed and/or suffixed slashes are ignored
    def test_testcase2d_noDupe(self):
        testCasesFile = "tests/z_testcases2d.txt"
        self.expectedOutput = [["a", "a"]]
        self.utSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase2d_yesDupe(self):
        testCasesFile = "tests/z_testcases2d.txt"
        self.expectedOutput = [["a", "a"], ["a (Copy 1)", "a"], ["a (Copy 10)", "a"], ["a (Copy 11)", "a"], ["a (Copy 12)", "a"], ["a (Copy 13)", "a"], ["a (Copy 2)", "a"], ["a (Copy 3)", "a"], ["a (Copy 4)", "a"], ["a (Copy 5)", "a"], ["a (Copy 6)", "a"], ["a (Copy 7)", "a"], ["a (Copy 8)", "a"], ["a (Copy 9)", "a"]]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.utSet_withoutConflictingNamecases(testCasesFile)
    
    #FOLDER TEST SET 3: reserved filenames tests
    def test_testcase3_noDupe(self):
        testCasesFile = "tests/z_testcases3.txt"
        self.expectedOutput = []
        self.utSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase3_yesDupe(self):
        testCasesFile = "tests/z_testcases3.txt"
        self.expectedOutput = []
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.utSet_withoutConflictingNamecases(testCasesFile)
    
    #FOLDER TEST SET 4: reserved characters tests
    def test_testcase4_noDupe(self):
        testCasesFile = "tests/z_testcases4.txt"
        self.expectedOutput = []
        self.utSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase4_yesDupe(self):
        testCasesFile = "tests/z_testcases4.txt"
        self.expectedOutput = []
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.utSet_withoutConflictingNamecases(testCasesFile)
    
    #FOLDER TEST SET 5: duplicate name cases (with different letters that are upper and lower case)
    #5a: 3 names with some duplicate cases, along with one name with no duplicates
    def test_testcase5a_noDupe(self):
        testCasesFile = "tests/z_testcases5a.txt"
        self.chosenCases = {"aa": "Aa", "ab": "ab", "abc": "aBc"}
        self.expectedOutput = [["Aa"], ["ab"], ["aBc"], ["AC"]]
        self.utSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase5a_yesDupe(self):
        testCasesFile = "tests/z_testcases5a.txt"
        self.chosenCases = {"aa": "Aa", "ab": "ab", "abc": "aBc"}
        self.expectedOutput = [["Aa"], ["Aa (Copy 1)"], ["Aa (Copy 2)"], ["ab"], ["ab (Copy 1)"], ["aBc"], ["aBc (Copy 1)"], ["aBc (Copy 2)"], ["aBc (Copy 3)"], ["aBc (Copy 4)"], ["aBc (Copy 5)"], ["aBc (Copy 6)"], ["AC"], ["AC (Copy 1)"], ["AC (Copy 2)"]]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.utSet_withoutConflictingNamecases(testCasesFile)
    #5b: duplicate name cases with nested folders
    def test_testcase5b_noDupe(self):
        testCasesFile = "tests/z_testcases5b.txt"
        self.chosenCases = {"aa": "Aa", "ab": "ab"}
        self.expectedOutput = [["Aa", "a"], ["ab", "a"], ["AC", "a"]]
        self.utSet_withoutConflictingNamecases(
            testCasesFile,
            #willSupressCaseStyleWindow = False,
            #willSupressFormatting = False
        )
    def test_testcase5b_yesDupe(self):
        testCasesFile = "tests/z_testcases5b.txt"
        self.chosenCases = {"aa": "Aa", "ab": "ab"}
        self.expectedOutput = [["Aa", "a"], ["Aa (Copy 1)", "a"], ["Aa (Copy 2)", "a"], ["Aa (Copy 3)", "a", "a"], ["ab", "a"], ["ab (Copy 1)", "a"], ["ab (Copy 2)", "a"], ["ab (Copy 3)", "a", "a"], ["AC", "a"],["AC (Copy 1)", "a"],["AC (Copy 2)", "a"], ["AC (Copy 3)", "a", "a"]]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.utSet_withoutConflictingNamecases(testCasesFile)
    #5c: handling both nested and non nested folders
    def test_testcase5c_noDupe(self):
        testCasesFile = "tests/z_testcases5c.txt"
        self.chosenCases = {"aa": "Aa", "ab": "ab", "ac": "Ac", "ad": "Ad", "af": "Af"}
        self.expectedOutput = [["Aa"], ["ab"], ["Ac"], ["Ad"], ["AE"], ["Af", "a"]]
        self.utSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase5c_yesDupe(self):
        testCasesFile = "tests/z_testcases5c.txt"
        self.chosenCases = {"aa": "Aa", "ab": "ab", "ac": "Ac", "ad": "Ad", "af": "Af"}
        self.expectedOutput = [["Aa"], ["Aa (Copy 1)"], ["Aa (Copy 2)"], ["Aa (Copy 3)", "a"], ["Aa (Copy 4)", "a"], ["Aa (Copy 5)", "a"], ["ab"], ["ab (Copy 1)"], ["ab (Copy 2)"], ["ab (Copy 3)", "a"], ["ab (Copy 4)", "a"], ["ab (Copy 5)", "a"], ["Ac"], ["Ac (Copy 1)"], ["Ac (Copy 2)"], ["Ac (Copy 3)", "a"], ["Ac (Copy 4)", "a"], ["Ac (Copy 5)", "a"], ["Ad"], ["Ad (Copy 1)"], ["AE"], ["AE (Copy 1)"], ["Af", "a"], ["Af (Copy 1)", "a"], ["Af (Copy 2)", "a"]]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.utSet_withoutConflictingNamecases(testCasesFile)
    
    #FOLDER TEST SET 6: handling the order that non-nested and nested versions of files are made (created in the order that it is listed)
    #6a: with duplicate names
    def test_testcase6a_noDupe(self):
        testCasesFile = "tests/z_testcases6a.txt"
        self.chosenCases = {"ab": "AB", "ac": "AC"}
        self.expectedOutput = [["Aa"], ["AB", "a"], ["AC"], ["Ad", "a"]]
        self.utSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase6a_yesDupe(self):
        testCasesFile = "tests/z_testcases6a.txt"
        self.chosenCases = {"ab": "AB", "ac": "AC"}
        self.expectedOutput = [["Aa"], ["AB", "a"], ["AB (Copy 1)"], ["AC"], ["AC (Copy 1)", "a"], ["Ad", "a"]]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.utSet_withoutConflictingNamecases(testCasesFile)
    #6b: without duplicate names
    def test_testcase6b_noDupe(self):
        testCasesFile = "tests/z_testcases6b.txt"
        self.expectedOutput = [["Aa"], ["AB", "a"], ["AC"], ["Ad", "a"]]
        self.utSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase6b_yesDupe(self):
        testCasesFile = "tests/z_testcases6b.txt"
        self.expectedOutput = [["Aa"], ["AB", "a"], ["AB (Copy 1)"], ["AC"], ["AC (Copy 1)", "a"], ["Ad", "a"]]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.utSet_withoutConflictingNamecases(testCasesFile)
    #6c: further alternating, along with multiple nesting
    def test_testcase6c_noDupe(self):
        testCasesFile = "tests/z_testcases6c.txt"
        self.expectedOutput = [["Aa"], ["AB", "a"], ["AC"], ["Ad", "a", "a"]]
        self.utSet_withoutConflictingNamecases(testCasesFile)
    def test_testcase6c_yesDupe(self):
        testCasesFile = "tests/z_testcases6c.txt"
        self.expectedOutput = [
            ["Aa"], ["Aa (Copy 1)", "a"], ["Aa (Copy 2)", "a", "a"], ["Aa (Copy 3)"], 
            ["AB", "a"], ["AB (Copy 1)"], ["AB (Copy 2)", "a"], ["AB (Copy 3)"], 
            ["AC"], ["AC (Copy 1)", "a"], ["AC (Copy 2)"], ["AC (Copy 3)", "a"], 
            ["Ad", "a", "a"], ["Ad (Copy 1)"], ["Ad (Copy 2)"], ["Ad (Copy 3)", "a"]
        ]
        QtTest.QTest.mouseClick(self.form.ui.duplicateFoldersCheckbox, QtCore.Qt.LeftButton)
        self.utSet_withoutConflictingNamecases(testCasesFile)
    
if __name__ == "__main__":
    unittest.main(verbosity=2)