import os
import sys
import collections
import re
import platform
import shutil
from PyQt5 import QtCore, QtGui, QtWidgets

basedir = os.path.dirname(__file__)
"""
try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass
"""

reservedCharacters = []
subfolderDividers = []
reservedFileNames = []
if platform.system() == "Windows":
    reservedCharacters = ["<", ">", ":", "|", "?", "*"] #Note: "\" and "/" are also reserved, but are used to create subfolders.
    subfolderDividers = ["\\", "/"]
    reservedFileNames = [
        "CON", 
        "PRN", 
        "AUX", "NUL", 
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", 
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    ]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.originalDirectory = str(os.getcwd()[0].upper()) + str(os.getcwd()[1:])
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 520)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(400, 520))
        MainWindow.setMaximumSize(QtCore.QSize(400, 520))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(basedir, 'images', "app_logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.sourceButton = QtWidgets.QPushButton(self.centralwidget)
        self.sourceButton.setGeometry(QtCore.QRect(355, 15, 30, 30))
        self.sourceButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(os.path.join(basedir, 'images', "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sourceButton.setIcon(icon1)
        self.sourceButton.setObjectName("sourceButton")
        self.sourceButton.clicked.connect(MainWindow.chooseDirectory)
        self.directoryTextbox = QtWidgets.QLineEdit(self.centralwidget)
        self.directoryTextbox.setGeometry(QtCore.QRect(72, 15, 280, 30))
        self.directoryTextbox.setObjectName("directoryTextbox")
        self.directoryTextbox.setText(self.originalDirectory)
        self.folderNames = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.folderNames.setTabStopDistance(
            QtGui.QFontMetricsF(self.folderNames.font()).horizontalAdvance(' ') * 4
        )
        self.folderNames.setGeometry(QtCore.QRect(20, 109, 364, 331))
        self.folderNames.setObjectName("folderNames")
        self.createButton = QtWidgets.QPushButton(self.centralwidget)
        self.createButton.setGeometry(QtCore.QRect(274, 455, 111, 31))
        self.createButton.setObjectName("createButton")
        self.createButton.clicked.connect(MainWindow.createFolders)
        self.directoryLabel = QtWidgets.QLabel(self.centralwidget)
        self.directoryLabel.setGeometry(QtCore.QRect(20, 23, 47, 13))
        self.directoryLabel.setObjectName("directoryLabel")
        self.folderNamesLabel = QtWidgets.QLabel(self.centralwidget)
        self.folderNamesLabel.setGeometry(QtCore.QRect(20, 60, 71, 16))
        self.folderNamesLabel.setObjectName("folderNamesLabel")
        self.duplicateFoldersCheckbox = QtWidgets.QCheckBox(self.centralwidget)
        self.duplicateFoldersCheckbox.setGeometry(QtCore.QRect(20, 83, 200, 17))
        self.duplicateFoldersCheckbox.setObjectName("duplicateFoldersCheckbox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpenNameListFile = QtWidgets.QAction(MainWindow)
        self.actionOpenNameListFile.setObjectName("actionOpenNameListFile")
        self.actionOpenNameListFile.triggered.connect(MainWindow.openNameListFile)
        self.actionSaveNameListFile = QtWidgets.QAction(MainWindow)
        self.actionSaveNameListFile.setObjectName("actionSaveNameListFile")
        self.actionSaveNameListFile.triggered.connect(MainWindow.saveNameListFile)
        self.actionChooseDirectory = QtWidgets.QAction(MainWindow)
        self.actionChooseDirectory.setObjectName("actionChooseDirectory")
        self.actionChooseDirectory.triggered.connect(MainWindow.chooseDirectory)
        self.menuFile.addAction(self.actionOpenNameListFile)
        self.menuFile.addAction(self.actionSaveNameListFile)
        self.menuFile.addAction(self.actionChooseDirectory)
        self.menubar.addAction(self.menuFile.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FolderMaster"))
        self.createButton.setText(_translate("MainWindow", "Create Folders"))
        self.directoryLabel.setText(_translate("MainWindow", "Directory:"))
        self.folderNamesLabel.setText(_translate("MainWindow", "Folder Names:"))
        self.duplicateFoldersCheckbox.setText(_translate("MainWindow", "Create cumulative duplicate folders"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpenNameListFile.setText(_translate("MainWindow", "Open name list file"))
        self.actionOpenNameListFile.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSaveNameListFile.setText(_translate("MainWindow", "Save name list file"))
        self.actionSaveNameListFile.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionChooseDirectory.setText(_translate("MainWindow", "Choose directory"))
        self.actionChooseDirectory.setShortcut(_translate("MainWindow", "Ctrl+D"))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #variables for createFolders
        self.currentDirectory = ""
        self.formattedInputList = []
        self.folderNameDict = {}
        self.folderNamecasesDict = {}
        self.chosenNamecasesDict = {}
        self.folderNameCounterDict = {}
        self.preexistingDuplicatesCounterDict = {}
        self.finalNamesList = []

    def openWindow(self, namecases):
        caseStyleWindow = CaseStyleWindow(namecases)
        caseStyleWindow.exec_()
        return caseStyleWindow.selectedCase
    def chooseDirectory(self):
        previousDirectoryTextCopy = self.ui.directoryTextbox.text()
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, 
            "Choose Directory to Insert Files"
        )
        if folder == "":
            folder = previousDirectoryTextCopy
        folder = folder.replace("/", "\\")
        self.ui.directoryTextbox.setText(folder)
    def openNameListFile(self):
        fileToOpen = QtWidgets.QFileDialog.getOpenFileName(
            self, 
            "Open Name List Text File",
            self.ui.directoryTextbox.text(),
            "Text Files (*.txt)"
        )
        if (fileToOpen[0] != ""):
            with open(fileToOpen[0], "r") as fileContents:
                for name in fileContents:
                    self.ui.folderNames.appendPlainText(name.strip("\n"))
            fileContents.close()
    def saveNameListFile(self):
        fileToSave = QtWidgets.QFileDialog.getSaveFileName(
            self, 
            "Save Name List Text File",
            self.ui.directoryTextbox.text(),
            "Text Files (*.txt)"
        )
        if (fileToSave[0] != ""):
            with open(fileToSave[0], "w") as fileContents:
                folderNames = self.ui.folderNames.toPlainText()
                fileContents.write(folderNames)
            fileContents.close()

    def createFolders(self):
        #Getting the current directory.
        self.currentDirectory = self.ui.directoryTextbox.text()
        if self.currentDirectory == "":
            QtWidgets.QMessageBox.question(
                self, 
                'No source folder',
                "Please provide a source folder",
                QtWidgets.QMessageBox.Ok
            )
            return
        if not os.path.exists(self.currentDirectory):
            QtWidgets.QMessageBox.question(
                self, 
                'Folder does not exist',
                "Please provide an existing source folder",
                QtWidgets.QMessageBox.Ok
            )
            return
        
        #Collecting the strings from the input box, then format the strings.
        self.createFolders_step1_nameFormatting()

        #Create two dictionaries (organised by the folder name in lowercase):
            #folderNameDict, to store the folder names.
            #folderNamecasesDict, to store the namecases (names which differ only by the letter casing used within them, for example "Apple" and "apple").    
        self.createFolders_step2_namesAndNamecases()

        #Create two dictionaries (organised by the folder name in lowercase):
            #chosenNamecasesDict, to store the chosen namecases.
            #folderNameCounterDict, to store the number of times a folder name appears from folderNameDict.
        self.createFolders_step3_chosenAndNameCounts()

        #Create a Counter dictionary to get the number of preexisting duplicates of a folder within the target directory. This is used for creating cumulative duplicate folders.
        self.createFolders_step4_preexistingDuplicateCounts()

        #Create a list containing the final names for the folders (appending "(Copy X)" for duplicate names)
        self.createFolders_step5_finalNames()
        
        #Create the folders. If no duplicate folder are to be created but there is a folder copy with the same name or with only different casing and without the (Copy X) suffix, that first copy with have any content such as subfolders removed.
        self.createFolders_step6_makeDirectories()

        #Clear all global list and dictionary variables
        self.createFolders_step7_resetGlobalVariables()

    def createFolders_step1_nameFormatting(self):
        def folderFormattingAndReserveHandling(currentLine):
            if currentLine == "/" or currentLine == "\\":
                return False
            if currentLine[0] in ["/"] or currentLine[-1] in ["/"]:
                currentLine = currentLine.strip("/")
            if currentLine[0] in ["\\"] or currentLine[-1] in ["\\"]:
                currentLine = currentLine.strip("\\")
            if any(char in currentLine for char in subfolderDividers):
                currentLine = re.split("[/\\\\]+", currentLine)
            if type(currentLine) == list:
                for i in range(len(currentLine)):
                    if currentLine[i][-1] == ".":
                        currentLine[i] = currentLine[i].rstrip(".")
                    if currentLine[i].upper() in reservedFileNames:
                        return False
                    if any(char in currentLine[i] for char in reservedCharacters):
                        return False
                return currentLine
            else:
                if currentLine == ".":
                    return False
                if currentLine[-1] == ".":
                    currentLine = currentLine.rstrip(".")
                if currentLine.upper() in reservedFileNames:
                    return False
                if any(char in currentLine for char in reservedCharacters):
                    return False
                return currentLine
        #print("STEP 1")
        despacedNamesList = [
            x.strip()
            for x in self.ui.folderNames.toPlainText().split("\n") 
            if x.strip()
        ]
        #print("despacedNamesList", despacedNamesList)
        for i in range(len(despacedNamesList)):
            currentLine = folderFormattingAndReserveHandling(despacedNamesList[i])
            if currentLine == False:
                continue
            else:
                self.formattedInputList.append(currentLine)
    def createFolders_step2_namesAndNamecases(self):
        #print("STEP 2")
        for item in self.formattedInputList:
            if type(item) == list:
                rootFolder = item[0]
                if item[0].lower() not in self.folderNameDict:
                    self.folderNameDict[rootFolder.lower()] = []
                    self.folderNamecasesDict[rootFolder.lower()] = set()
                self.folderNameDict[rootFolder.lower()].append(item)
                self.folderNamecasesDict[rootFolder.lower()].add(rootFolder)
            else:
                if item.lower() not in self.folderNameDict:
                    self.folderNameDict[item.lower()] = []
                    self.folderNamecasesDict[item.lower()] = set()
                self.folderNameDict[item.lower()].append(item)
                self.folderNamecasesDict[item.lower()].add(item)
    def createFolders_step3_chosenAndNameCounts(self):
        #print("STEP 3")
        for key in self.folderNamecasesDict.keys():
            namecases = list(set(self.folderNamecasesDict[key]))
            if (len(namecases) > 1):
                chosenNamecase = self.openWindow(namecases)
                if chosenNamecase == "":
                    continue
                for namecase in namecases:
                    if(namecase == chosenNamecase):
                        self.chosenNamecasesDict[chosenNamecase.lower()] = chosenNamecase
            else:
                chosenNamecase = list(namecases)[0]
                self.chosenNamecasesDict[chosenNamecase.lower()] = chosenNamecase
            for i in range(len(self.folderNameDict[key])):
                case = self.folderNameDict[key][i]
                if type(case) == list:
                    case[0] = self.chosenNamecasesDict[chosenNamecase.lower()]
                else:
                    case = self.chosenNamecasesDict[chosenNamecase.lower()]
            self.folderNameCounterDict[key] = len(self.folderNameDict[key])
        #print("chosenNamecasesDict", self.chosenNamecasesDict)
        #print("uniqueNamesCounterDict", self.folderNameCounterDict)
    def createFolders_step4_preexistingDuplicateCounts(self):
        #print("STEP 4")
        preexistingDuplicatesList = []
        for item in os.listdir(self.currentDirectory):
            if item.lower() in self.chosenNamecasesDict.keys():
                preexistingDuplicatesList.append(item.lower())
                os.rename(
                    os.path.join(self.currentDirectory, item), 
                    os.path.join(self.currentDirectory, self.chosenNamecasesDict[item.lower()])
                )
                continue
            parser = re.findall('[(]Copy [0-9]+[)]', item)
            if (parser != []):
                strippedItem = item.replace(parser[-1], "").strip()
                if strippedItem.lower() in self.chosenNamecasesDict.keys():
                    preexistingDuplicatesList.append(self.chosenNamecasesDict[strippedItem.lower()].lower())
                    os.rename(
                        os.path.join(self.currentDirectory, item), 
                        os.path.join(self.currentDirectory, self.chosenNamecasesDict[strippedItem.lower()] + " " + parser[-1])
                    )
        #print("files", os.listdir(self.currentDirectory))
        self.preexistingDuplicatesCounterDict = collections.Counter(preexistingDuplicatesList)
        #print("preexistingDuplicatesList", preexistingDuplicatesList)
        #print("preexistingDuplicatesCounterDict", self.preexistingDuplicatesCounterDict)
    def createFolders_step5_finalNames(self):
        #print("STEP 5")
        for item in self.folderNameCounterDict.keys():
            if(
                self.ui.duplicateFoldersCheckbox.isChecked() 
                and self.folderNameCounterDict[item] > 0
            ):
                #print("many", item)
                if(self.chosenNamecasesDict[item] not in os.listdir(self.currentDirectory)):
                    if type(self.folderNameDict[item][0]) == list:
                        self.finalNamesList.append(self.folderNameDict[item][0])
                        #print("\ta item", self.folderNameDict[item][0])
                    else:
                        self.finalNamesList.append(self.chosenNamecasesDict[item])
                        #print("\tb item", self.chosenNamecasesDict[item])
                    for i in range(1, self.folderNameCounterDict[item]):
                        #print("choice1", self.chosenNamecasesDict[item])
                        if type(self.folderNameDict[item][i]) == list:
                            newItem = self.chosenNamecasesDict[item] + " " + "(Copy " + str(i) + ")"
                            self.folderNameDict[item][i][0] = newItem
                        else:
                            newItem = self.chosenNamecasesDict[item] + " " + "(Copy " + str(i) + ")"
                            self.folderNameDict[item][i] = newItem
                        self.finalNamesList.append(self.folderNameDict[item][i])
                        #print("\titem", self.folderNameDict[item][i])
                else:
                    for i in range(0, self.folderNameCounterDict[item]):
                        #print("choice2", self.chosenNamecasesDict[item])
                        if type(self.folderNameDict[item][i]) == list:
                            #print("\titem", self.folderNameDict[item][i])
                            #print("\t\tnumber", (i + 1) + self.preexistingDuplicatesCounterDict[item])
                            newItem = self.chosenNamecasesDict[item] + " " + "(Copy " + str(i + self.preexistingDuplicatesCounterDict[item]) + ")"
                            #print("\t\tnewItem", newItem)
                            self.folderNameDict[item][i][0] = newItem
                            #print("\t\tresult", self.folderNameDict[item][i])
                        else:
                            #print("\titem", self.folderNameDict[item][i])
                            #print("\t\tnumber", (i + 1) + self.preexistingDuplicatesCounterDict[item])
                            newItem = self.chosenNamecasesDict[item] + " " + "(Copy " + str(i + self.preexistingDuplicatesCounterDict[item]) + ")"
                            #print("\t\tnewItem", newItem)
                            self.folderNameDict[item][i] = newItem
                            #print("\t\tresult", self.folderNameDict[item][i])
                        self.finalNamesList.append(self.folderNameDict[item][i])
            else:
                #print("zero", self.folderNameDict[item][0])
                self.finalNamesList.append(self.folderNameDict[item][0])
        #print("finalNamesList", self.finalNamesList)
    def createFolders_step6_makeDirectories(self):
        #print("STEP 6")
        if not self.ui.duplicateFoldersCheckbox.isChecked():
            for name in self.finalNamesList:
                if type(name) == list:
                    if name[0] in os.listdir(self.currentDirectory):
                        folderDirectory = os.path.join(self.currentDirectory, "\\".join(name[0]))
                        shutil.rmtree(folderDirectory)
                    os.makedirs(self.currentDirectory + "\\" + "\\".join(name))
                else:
                    if name in os.listdir(self.currentDirectory):
                        folderDirectory = os.path.join(self.currentDirectory, name)
                        if len(os.listdir(folderDirectory)) > 0:
                            shutil.rmtree(folderDirectory)
                        else:
                            continue
                    os.mkdir(self.currentDirectory + "\\" + name)
        else:
            for name in self.finalNamesList:
                if type(name) == list:
                    os.makedirs(self.currentDirectory + "\\" + "\\".join(name))
                else: 
                    os.mkdir(self.currentDirectory + "\\" + name)
    def createFolders_step7_resetGlobalVariables(self):
        self.currentDirectory = ""
        self.formattedInputList = []
        self.folderNameDict = {}
        self.folderNamecasesDict = {}
        self.chosenNamecasesDict = {}
        self.folderNameCounterDict = {}
        self.preexistingDuplicatesCounterDict = {}
        self.finalNamesList = []

class Ui_CaseStyleWindow(object):
    def setupUi(self, CaseStyleWindow):
        CaseStyleWindow.setObjectName("CaseStyleWindow")
        CaseStyleWindow.resize(300, 420)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CaseStyleWindow.sizePolicy().hasHeightForWidth())
        CaseStyleWindow.setSizePolicy(sizePolicy)
        CaseStyleWindow.setMinimumSize(QtCore.QSize(300, 420))
        CaseStyleWindow.setMaximumSize(QtCore.QSize(300, 420))
        self.centralwidget = QtWidgets.QWidget(CaseStyleWindow)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 300, 418))
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 40, 260, 300))
        self.listWidget.setObjectName("listWidget")
        self.chooseCasesLabel = QtWidgets.QLabel(self.centralwidget)
        self.chooseCasesLabel.setGeometry(QtCore.QRect(20, 15, 241, 16))
        self.chooseCasesLabel.setObjectName("chooseCasesLabel")
        self.cancelLabel = QtWidgets.QLabel(self.centralwidget)
        self.cancelLabel.setGeometry(QtCore.QRect(20, 350, 241, 21))
        self.cancelLabel.setObjectName("cancelLabel")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setGeometry(QtCore.QRect(130, 380, 150, 25))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.retranslateUi(CaseStyleWindow)
        QtCore.QMetaObject.connectSlotsByName(CaseStyleWindow)
    def retranslateUi(self, CaseStyleWindow):
        _translate = QtCore.QCoreApplication.translate
        CaseStyleWindow.setWindowTitle(_translate("CaseStyleWindow", "Choose a case style"))
        self.chooseCasesLabel.setText(_translate("CaseStyleWindow", "Choose the case style to use:"))
        self.cancelLabel.setText(_translate("CaseStyleWindow", "Click \'Cancel\' in order to use none of them."))

class CaseStyleWindow(QtWidgets.QDialog):
    def __init__(self, namecases):
        super(CaseStyleWindow, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint) #This disables the '?' hint button
        self.ui = Ui_CaseStyleWindow()
        self.ui.setupUi(self)
        self.namecases = namecases
        self.selectedCase = ""
        self.isAccepted = False
        self.ui.listWidget.addItems(sorted(self.namecases, key=str.swapcase))
        self.ui.listWidget.itemSelectionChanged.connect(self.selectionChanged)
        self.ui.buttonBox.accepted.connect(self.closeWithCaseStyle)
        self.ui.buttonBox.rejected.connect(self.closeWithoutCaseStyle)
    def selectionChanged(self):
        self.selectedCase = self.ui.listWidget.currentItem().text()
    def closeWithCaseStyle(self):
        if self.selectedCase != "":
            self.selectedCase = self.ui.listWidget.currentItem().text()
            self.isAccepted = True
            QtWidgets.QDialog.close(self)
        else:
            QtWidgets.QMessageBox.question(
                self, 
                'No Case Style Selected',
                "Please select a case style. If you don't want any case, click 'Cancel'",
                QtWidgets.QMessageBox.Ok
            )
    def closeWithoutCaseStyle(self):
        self.selectedCase = ""
        QtWidgets.QDialog.close(self)
    def closeEvent(self, event): #overridden method
        if self.isAccepted == True:
            event.accept()
        else:
            self.selectedCase = ""
            event.accept()
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.selectedCase = ""
            event.accept()
            QtWidgets.QDialog.close(self)
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'images', 'app_logo.ico')))
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())