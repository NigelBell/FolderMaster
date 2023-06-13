# FolderMaster
## Program description and features
* FolderMaster is a productivity software program that allows users to create several folders in one whole batch. This is done by obtaining the folder names (either by typing them into a plain-text edit box and/or loading them in from a text file) and then clicking the 'Create Folders' button.
* Folder names inside said plain-text edit box can be saved to a text file.
* The program will create the folders inside a specified directory, if the directory exists. The program will start with the directory that it is opened in. The directory can also be changed to a different one.
* The program will reject names that contain reserved characters, along with names that are reserved filenames.
* The program can handle duplicates of folder names by suffixing it with `(Copy X)`.
* The program can handle duplicates of folder names with different case usage by allowing the user to select one of the cases, and then suffixing any duplicates with `(Copy X)`.
* The installer adds registry keys and user environment variables to the computer. These allow the program to appear as an option in the file explorer context menu when:
    * right clicking within a folder's background. In this case, folders will be created inside the current working directory.
    * right clicking on a folder. In this case, folders will be created inside said folder.
## Program Shortcuts
* `Ctrl+O`: Open name list as text file
* `Ctrl+S`: Save name list as text file
* `Ctrl+D`: Change directory
## Languages and technologies used (prerequisites for working with the source code)
* Python for the programming language, along with several standard library modules. 
* PyQt5 (a Python binding of Qt) for the GUI toolkit.
* Qt Designer was used in order to design the initial GUI layout of the program. Copies of the `.ui` files for the main window (`FolderMaster.ui`) and case style window (`CaseStyleWindow.ui`) are provided inside the folder `ui_files` as reference points. These `ui` files were compiled into Python code and further modified over the course of the program's development. These modifications include implementing the program's folder making logic, a merge of the FolderMaster and CaseStyleWindow classes into the same file, and a few changes to the initial UI. Note that certain aspects (such as variable names) will differ when comparing the results from compiling the `.ui` files against the finalized Python code.
* I created unit tests (utilizing Python's unittest module, and PyQt5's QtTest module) in order to test the folder creation functionality. There are several 'basic' tests to test that the core functionality works on a small scale (eg a few cases) to begin with. There are also with several specialized 'testcase' tests which load text files inside the 'tests' folder, which contains multiple cases and edge cases.
* PyInstaller is used in order to take the program code and its dependencies and then compile it into a package with an executable that can be run without a Python interpreter.
* The Nullsoft Scriptable Install System (NSIS) is used to create a script for the NSIS compiler to compile into an installer. 
* The installer script was initially created using the NSIS Quick Setup Script Generator. It was then modified to increase readability (by adding formatting and replacing most of the dividers with labels) and functionality (by turning absolute paths into relative paths, adding code to handle creating (upon installation) and deleting (upon uninstallation) both registry keys and user environment variables).
* The aforementioned user environment variables have been used in order to perform the option that appears when right clicking on a folder. 
    * `FolderMasterFolderContextMenuEnvVar` is used to temporarily store the name of the folder that was right clicked on.
    * `FolderMasterInstallDir` is used in order to provide access to the RefreshEnv.cmd batch file.'
    * Note that due to the use of `setx` in order to create the user environment variables, folder names longer than 1024 characters will be truncated.
* The `RefreshEnv.cmd` batch file is used in order to refresh the environment variables, which allows the name of the folder that was right clicked on to be passed into the program. It is a lightly modified version of the `RefreshEnv.cmd` batch file found in the repository for Chocolatey (https://github.com/chocolatey/choco). The only modification done to it is the removal of output messages to the command prompt.
## Environment installation:
1. 
    ```
    python -m venv venv
    ```
2. If not using bash:
    ```
    venv/Scripts/activate
    ```
    If using bash:
    ```
    source venv/Scripts/activate
    ```
3. If installing the known-to-work packages frozen in `requirements.txt`:
    ```
    pip install -r requirements.txt
    ```
    If installing the latest packages:
    ```
    pip install PyQt5 pyinstaller
    ```
## Running the scripts:
* Main program:
    ```
    python FolderMaster.py
    ```
* Unit tests:
    ```
    python FolderMasterUnitTesting.py
    ```
## Compilation instructions
### For Windows
1. Run the following command:
    ```
    pyinstaller FolderMaster.spec
    ```
2. Access the compiled program within the `dist\FolderMaster` folder.
3. Open up the NSIS Menu, and click on "Compile NSI scripts"
4. Drag the .nsi file into the window to start compiling the installer.
5. After compiling, the installer is ready for use. It can be tested right away by clicking on "Test Installer".

## (Optional) Compiling the `.ui` files into `.py` files
1. Change the directory to `ui_files`
    ```
    cd ui_files
    ```
2. Run the following commands:
    ```
    pyuic5 FolderMaster.ui > FolderMaster.py
    pyuic5 CaseStyleWindow.ui > CaseStyleWindow.py
    ```

## Proposed changes for future updates
* Support for multiple folders being created in multiple layers, represented via tabs (which are currently treated as whitespace). For example, the following input should create folders `b` and `c` inside `a`, and folders `f` and `g` inside the `e` folder of `d/e`:
    ```
    a
        b
        c
    d/e
        f
        g
    ```
* The addition of several options, which will appear in "Settings/Preferences" ("Settings" is a menu name, "Preferences" is a menu item):
    * An option to customize the `(Copy X)` suffix (by default, use the `(Copy X)` suffix).
    * An option to add line numbers to the plain-text edit box (by default, have this enabled).
    * An option to add a red background to lines either containing reserved characters or being/formatting to one of the reserved filenames (by default, have this enabled). This is to clearly indicate that these names are invalid.
        * If the user tries to create a batch of names with some invalid names, a popup should appear warning them that lines coloured red are invalid names. The popup should also ask if they want to proceed with creating folders with the valid names available.
    * An option to choose how to handle loading names from a text file into the plain-text edit box. Either: 
        * append the names to whatever exists in the box already (by default, use this option).
        * replace the text altogether with the names in the text file.
    * An option or popup dialog box when creating non cumulative duplicates if creating a folder with a preexisting name within the directory. 
        * Either:
            * rename the folder (by default, use this option).
            * create a new empty folder.
* Porting the code to a different language and/or GUI framework, in order to reduce the size and performance of the program further.
* Ports for macOS and Linux.

## History
### (dev) Pre-release versions 
* v1 (28/03/22) - basic functionality
* v2 (11/04/22) - file list input functionality added
* v3 (16/04/22) - pyinstaller experimentation
* v4 (21/04/22) - name case handling
* v5 (23/04/22) - pre connector for CaseStyleWindow
* v6 (30/04/22) - connector for CaseStyleWindow attached
* v7.1.1 to v7.1.2 (30/04/22) - variable renaming
* v7.2 to v7.2.5 (02/05/22 to 13/05/22) - improvements to handling cases for folder names
* v8.1 (15/05/22) - converting for unit testing
* v8.2 (16/05/22) - first unit test
* v8.2.1 to v8.2.3 (17/05/22 to 21/05/22) - improvements to test submethods
* v8.3 (30/05/22) - all txt testcases working
* v8.3.1 (30/05/22) - edited tab space
* v8.4 (31/05/22) - added directory shortcut, also allowed folders to be created from different folders
* v8.5 (07/06/22) - refined code, unit tests need to be fixed
* v9 (19/06/22) - close to completion
* v10 (27/06/22) - first release version. Fixed a crash that occurs with certain choices when not creating cumulative duplicates, and a crash that occurs when creating a folder in the same directory as an extensionless file with the same name. Provided some more basic tests along with some extra names in a few of the testcases. Finished creating the NSIS installer script. Provided a copy of the RefreshEnv batch file from Chocolatey's source code.
### (rel) Release versions 
* 1.0 - (27/06/22) see (dev) v10
* 1.1 - (13/07/23) provided python virtual environment, `requirements.txt` and `.gitignore`