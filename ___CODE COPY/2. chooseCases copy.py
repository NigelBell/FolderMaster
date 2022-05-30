    def step_chooseCases(self):
        namecasesDict = {}
        for item in self.formattedInput:
            print("item", item)
            if type(item) == list:
                rootFolder = item[0]
                print("\trootFolder", rootFolder)
                item = "//".join(item)
                print("\titem", item)
                if item[0].lower() not in self.caseListDict:
                    self.caseListDict[rootFolder.lower()] = [item]
                    namecasesDict[rootFolder.lower()] = [rootFolder]
                else:
                    self.caseListDict[rootFolder.lower()].append(item)
                    namecasesDict[rootFolder.lower()].append(rootFolder)
            else:
                if item.lower() not in self.caseListDict:
                    self.caseListDict[item.lower()] = [item]
                    namecasesDict[item.lower()] = [item]
                else:
                    self.caseListDict[item.lower()].append(item)
                    namecasesDict[item.lower()].append(item)
        print("caseListDict", self.caseListDict)
        print("namecasesDict", namecasesDict)

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