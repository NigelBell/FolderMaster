############################################################################################
#      NSIS Installation Script created by NSIS Quick Setup Script Generator v1.09.18
#               Entirely Edited with NullSoft Scriptable Installation System                
#              by Vlasis K. Barkas aka Red Wine red_wine@freemail.gr Sep 2006               
############################################################################################

#Defines
    !define APP_NAME "FolderMaster"
    !define COMP_NAME "Nigel Bell"
    !define WEB_SITE "https://github.com/NigelBell/FolderMaster"
    !define VERSION "1.0.0.0"
    !define COPYRIGHT "Nigel Bell � 2022"
    !define DESCRIPTION "FolderMaster is a productivity software program that allows users to create several folders in one whole batch."
    !define LICENSE_TXT "LICENCE.txt"
    !define INSTALLER_NAME "FolderMaster Installer.exe"
    !define MAIN_APP_EXE "FolderMaster.exe"
    !define INSTALL_TYPE "SetShellVarContext current"
    !define REG_ROOT "HKEY_CURRENT_USER"
    !define REG_APP_PATH "Software\Microsoft\Windows\CurrentVersion\App Paths\${MAIN_APP_EXE}"
    !define UNINSTALL_PATH "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
    !define REG_START_MENU "Start Menu Folder"
    var SM_Folder

#Version Info (VI)
    VIProductVersion  "${VERSION}"
    VIAddVersionKey "ProductName"  "${APP_NAME}"
    VIAddVersionKey "CompanyName"  "${COMP_NAME}"
    VIAddVersionKey "LegalCopyright"  "${COPYRIGHT}"
    VIAddVersionKey "FileDescription"  "${DESCRIPTION}"
    VIAddVersionKey "FileVersion"  "${VERSION}"

#Core Installer Attributes
    SetCompressor ZLIB
    Name "${APP_NAME}"
    Caption "${APP_NAME}"
    OutFile "${INSTALLER_NAME}"
    BrandingText "${APP_NAME}"
    XPStyle on
    InstallDirRegKey "${REG_ROOT}" "${REG_APP_PATH}" ""
    InstallDir "$PROGRAMFILES\FolderMaster"

#Modern User Interface (MUI)
    !include "MUI.nsh"
    !define MUI_ABORTWARNING
    !define MUI_UNABORTWARNING
    !insertmacro MUI_PAGE_WELCOME
    !ifdef LICENSE_TXT
        !insertmacro MUI_PAGE_LICENSE "${LICENSE_TXT}"
    !endif
    !ifdef REG_START_MENU
        !define MUI_STARTMENUPAGE_NODISABLE
        !define MUI_STARTMENUPAGE_DEFAULTFOLDER "FolderMaster"
        !define MUI_STARTMENUPAGE_REGISTRY_ROOT "${REG_ROOT}"
        !define MUI_STARTMENUPAGE_REGISTRY_KEY "${UNINSTALL_PATH}"
        !define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "${REG_START_MENU}"
        !insertmacro MUI_PAGE_STARTMENU Application $SM_Folder
    !endif
    !insertmacro MUI_PAGE_INSTFILES
    !define MUI_FINISHPAGE_RUN "$INSTDIR\${MAIN_APP_EXE}"
    !insertmacro MUI_PAGE_FINISH
    !insertmacro MUI_UNPAGE_CONFIRM
    !insertmacro MUI_UNPAGE_INSTFILES
    !insertmacro MUI_UNPAGE_FINISH
    !insertmacro MUI_LANGUAGE "English"

#Section: Install Main Program 
    #Note: Files and directories that have been commented out are not required for the program to function. Therefore, they are not included in the installer.
    Section -MainProgram
    ${INSTALL_TYPE}
    SetOverwrite ifnewer
    SetOutPath "$INSTDIR"
    File "RefreshEnv.cmd"
    File "LICENCE.txt"
    File "dist\FolderMaster\base_library.zip"
    File "dist\FolderMaster\FolderMaster.exe"
    File "dist\FolderMaster\python3.dll"
    File "dist\FolderMaster\python39.dll"
    File "dist\FolderMaster\Qt5Core.dll"
    File "dist\FolderMaster\Qt5Gui.dll"
    File "dist\FolderMaster\Qt5Widgets.dll"
    File "dist\FolderMaster\select.pyd"
    File "dist\FolderMaster\_socket.pyd"
    SetOutPath "$INSTDIR\PyQt5"
    File "dist\FolderMaster\PyQt5\QtCore.pyd"
    File "dist\FolderMaster\PyQt5\QtGui.pyd"
    File "dist\FolderMaster\PyQt5\QtWidgets.pyd"
    File "dist\FolderMaster\PyQt5\sip.cp39-win_amd64.pyd"
    #SetOutPath "$INSTDIR\PyQt5\Qt5\translations"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_ar.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_bg.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_ca.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_cs.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_da.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_de.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_en.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_es.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_fi.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_fr.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_gd.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_he.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_hu.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_it.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_ja.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_ko.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_lv.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_pl.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_ru.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_sk.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_tr.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_uk.qm"
    #File "dist\FolderMaster\PyQt5\Qt5\translations\qtbase_zh_TW.qm"
    SetOutPath "$INSTDIR\PyQt5\Qt5\plugins\styles"
    File "dist\FolderMaster\PyQt5\Qt5\plugins\styles\qwindowsvistastyle.dll"
    #SetOutPath "$INSTDIR\PyQt5\Qt5\plugins\platformthemes"
    #File "dist\FolderMaster\PyQt5\Qt5\plugins\platformthemes\qxdgdesktopportal.dll"
    SetOutPath "$INSTDIR\PyQt5\Qt5\plugins\platforms"
    #File "dist\FolderMaster\PyQt5\Qt5\plugins\platforms\qminimal.dll"
    #File "dist\FolderMaster\PyQt5\Qt5\plugins\platforms\qoffscreen.dll"
    #File "dist\FolderMaster\PyQt5\Qt5\plugins\platforms\qwebgl.dll"
    File "dist\FolderMaster\PyQt5\Qt5\plugins\platforms\qwindows.dll"
    #SetOutPath "$INSTDIR\PyQt5\Qt5\plugins\imageformats"
    #File "dist\FolderMaster\PyQt5\Qt5\plugins\imageformats\qgif.dll"
    #File "dist\FolderMaster\PyQt5\Qt5\plugins\imageformats\qicns.dll"
    #File "dist\FolderMaster\PyQt5\Qt5\plugins\imageformats\qico.dll"
    #File "dist\FolderMaster\PyQt5\Qt5\plugins\imageformats\qjpeg.dll"
    #File "dist\FolderMaster\PyQt5\Qt5\plugins\imageformats\qsvg.dll"
    #File "dist\FolderMaster\PyQt5\Qt5\plugins\imageformats\qtga.dll"
    #File "dist\FolderMaster\PyQt5\Qt5\plugins\imageformats\qtiff.dll"
    #File "dist\FolderMaster\PyQt5\Qt5\plugins\imageformats\qwbmp.dll"
    #File "dist\FolderMaster\PyQt5\Qt5\plugins\imageformats\qwebp.dll"
    #SetOutPath "$INSTDIR\PyQt5\Qt5\plugins\iconengines"
    #File "dist\FolderMaster\PyQt5\Qt5\plugins\iconengines\qsvgicon.dll"
    SetOutPath "$INSTDIR\images"
    File "dist\FolderMaster\images\app_logo.ico"
    File "dist\FolderMaster\images\app_logo.png"
    File "dist\FolderMaster\images\folder.png"
    SectionEnd

#Section: Install Icons Registry
    Section -Icons_Reg
    SetOutPath "$INSTDIR"
    WriteUninstaller "$INSTDIR\uninstall.exe"
    !ifdef REG_START_MENU
        !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
        CreateDirectory "$SMPROGRAMS\$SM_Folder"
        CreateShortCut "$SMPROGRAMS\$SM_Folder\${APP_NAME}.lnk" "$INSTDIR\${MAIN_APP_EXE}"
        CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${MAIN_APP_EXE}"
        CreateShortCut "$SMPROGRAMS\$SM_Folder\Uninstall ${APP_NAME}.lnk" "$INSTDIR\uninstall.exe"
        !ifdef WEB_SITE
            WriteIniStr "$INSTDIR\${APP_NAME} website.url" "InternetShortcut" "URL" "${WEB_SITE}"
            CreateShortCut "$SMPROGRAMS\$SM_Folder\${APP_NAME} Website.lnk" "$INSTDIR\${APP_NAME} website.url"
        !endif
        !insertmacro MUI_STARTMENU_WRITE_END
    !endif
    !ifndef REG_START_MENU
        CreateDirectory "$SMPROGRAMS\FolderMaster"
        CreateShortCut "$SMPROGRAMS\FolderMaster\${APP_NAME}.lnk" "$INSTDIR\${MAIN_APP_EXE}"
        CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${MAIN_APP_EXE}"
        CreateShortCut "$SMPROGRAMS\FolderMaster\Uninstall ${APP_NAME}.lnk" "$INSTDIR\uninstall.exe"
        !ifdef WEB_SITE
            WriteIniStr "$INSTDIR\${APP_NAME} website.url" "InternetShortcut" "URL" "${WEB_SITE}"
            CreateShortCut "$SMPROGRAMS\FolderMaster\${APP_NAME} Website.lnk" "$INSTDIR\${APP_NAME} website.url"
        !endif
    !endif
    WriteRegStr ${REG_ROOT} "${REG_APP_PATH}" "" "$INSTDIR\${MAIN_APP_EXE}"
    WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayName" "${APP_NAME}"
    WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayIcon" "$INSTDIR\${MAIN_APP_EXE}"
    WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayVersion" "${VERSION}"
    WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "Publisher" "${COMP_NAME}"
    WriteRegStr HKEY_CLASSES_ROOT "Directory\Background\shell\FolderMaster\command" "" "$INSTDIR\${MAIN_APP_EXE}"
    WriteRegStr HKEY_CLASSES_ROOT "Directory\Background\shell\FolderMaster" "Icon" "$INSTDIR\${MAIN_APP_EXE}"
    WriteRegStr HKEY_CLASSES_ROOT "Directory\shell\FolderMaster\command" '' 'cmd /c for %%f in ("%V") do setx FolderMasterFolderContextMenuEnvVar "%~nxf" & "$INSTDIR\refreshenv" & start FolderMaster & exit'
    WriteRegStr HKEY_CLASSES_ROOT "Directory\shell\FolderMaster" "Icon" '$INSTDIR\${MAIN_APP_EXE}'
    !ifdef WEB_SITE
        WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "URLInfoAbout" "${WEB_SITE}"
    !endif
    !include "winmessages.nsh"
    !define env_hkcu 'HKCU "Environment"'
    WriteRegExpandStr ${env_hkcu} FolderMasterInstallDir "$INSTDIR"
    SectionEnd

#Section: Uninstall
    #Note: Files and directories that have been commented out are not required for the program to function. Therefore, they are not included in the installer.
    Section Uninstall
    ${INSTALL_TYPE}
    Delete "$INSTDIR\RefreshEnv.cmd"
    Delete "$INSTDIR\LICENCE.txt"
    Delete "$INSTDIR\base_library.zip"
    Delete "$INSTDIR\FolderMaster.exe"
    Delete "$INSTDIR\python3.dll"
    Delete "$INSTDIR\python39.dll"
    Delete "$INSTDIR\Qt5Core.dll"
    Delete "$INSTDIR\Qt5Gui.dll"
    Delete "$INSTDIR\Qt5Widgets.dll"
    Delete "$INSTDIR\select.pyd"
    Delete "$INSTDIR\_socket.pyd"
    Delete "$INSTDIR\PyQt5\QtCore.pyd"
    Delete "$INSTDIR\PyQt5\QtGui.pyd"
    Delete "$INSTDIR\PyQt5\QtWidgets.pyd"
    Delete "$INSTDIR\PyQt5\sip.cp39-win_amd64.pyd"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_ar.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_bg.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_ca.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_cs.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_da.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_de.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_en.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_es.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_fi.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_fr.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_gd.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_he.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_hu.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_it.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_ja.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_ko.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_lv.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_pl.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_ru.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_sk.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_tr.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_uk.qm"
    #Delete "$INSTDIR\PyQt5\Qt5\translations\qtbase_zh_TW.qm"
    Delete "$INSTDIR\PyQt5\Qt5\plugins\styles\qwindowsvistastyle.dll"
    #Delete "$INSTDIR\PyQt5\Qt5\plugins\platformthemes\qxdgdesktopportal.dll"
    #Delete "$INSTDIR\PyQt5\Qt5\plugins\platforms\qminimal.dll"
    #Delete "$INSTDIR\PyQt5\Qt5\plugins\platforms\qoffscreen.dll"
    #Delete "$INSTDIR\PyQt5\Qt5\plugins\platforms\qwebgl.dll"
    Delete "$INSTDIR\PyQt5\Qt5\plugins\platforms\qwindows.dll"
    #Delete "$INSTDIR\PyQt5\Qt5\plugins\imageformats\qgif.dll"
    #Delete "$INSTDIR\PyQt5\Qt5\plugins\imageformats\qicns.dll"
    #Delete "$INSTDIR\PyQt5\Qt5\plugins\imageformats\qico.dll"
    #Delete "$INSTDIR\PyQt5\Qt5\plugins\imageformats\qjpeg.dll"
    #Delete "$INSTDIR\PyQt5\Qt5\plugins\imageformats\qsvg.dll"
    #Delete "$INSTDIR\PyQt5\Qt5\plugins\imageformats\qtga.dll"
    #Delete "$INSTDIR\PyQt5\Qt5\plugins\imageformats\qtiff.dll"
    #Delete "$INSTDIR\PyQt5\Qt5\plugins\imageformats\qwbmp.dll"
    #Delete "$INSTDIR\PyQt5\Qt5\plugins\imageformats\qwebp.dll"
    #Delete "$INSTDIR\PyQt5\Qt5\plugins\iconengines\qsvgicon.dll"
    Delete "$INSTDIR\images\app_logo.ico"
    Delete "$INSTDIR\images\app_logo.png"
    Delete "$INSTDIR\images\folder.png"
    RmDir "$INSTDIR\images"
    #RmDir "$INSTDIR\PyQt5\Qt5\plugins\iconengines"
    #RmDir "$INSTDIR\PyQt5\Qt5\plugins\imageformats"
    RmDir "$INSTDIR\PyQt5\Qt5\plugins\platforms"
    #RmDir "$INSTDIR\PyQt5\Qt5\plugins\platformthemes"
    RmDir "$INSTDIR\PyQt5\Qt5\plugins\styles"
    #RmDir "$INSTDIR\PyQt5\Qt5\translations"
    RmDir "$INSTDIR\PyQt5"
    Delete "$INSTDIR\uninstall.exe"
    !ifdef WEB_SITE
        Delete "$INSTDIR\${APP_NAME} website.url"
    !endif
    RmDir "$INSTDIR"
    !ifdef REG_START_MENU
        !insertmacro MUI_STARTMENU_GETFOLDER "Application" $SM_Folder
        Delete "$SMPROGRAMS\$SM_Folder\${APP_NAME}.lnk"
        Delete "$SMPROGRAMS\$SM_Folder\Uninstall ${APP_NAME}.lnk"
        !ifdef WEB_SITE
            Delete "$SMPROGRAMS\$SM_Folder\${APP_NAME} Website.lnk"
        !endif
        Delete "$DESKTOP\${APP_NAME}.lnk"
        RmDir "$SMPROGRAMS\$SM_Folder"
    !endif
    !ifndef REG_START_MENU
        Delete "$SMPROGRAMS\FolderMaster\${APP_NAME}.lnk"
        Delete "$SMPROGRAMS\FolderMaster\Uninstall ${APP_NAME}.lnk"
        !ifdef WEB_SITE
            Delete "$SMPROGRAMS\FolderMaster\${APP_NAME} Website.lnk"
        !endif
        Delete "$DESKTOP\${APP_NAME}.lnk"
        RmDir "$SMPROGRAMS\FolderMaster"
    !endif
    DeleteRegKey ${REG_ROOT} "${REG_APP_PATH}"
    DeleteRegKey ${REG_ROOT} "${UNINSTALL_PATH}"
    DeleteRegKey HKEY_CLASSES_ROOT "Directory\Background\shell\FolderMaster"
    DeleteRegKey HKEY_CLASSES_ROOT "Directory\shell\FolderMaster"
    DeleteRegValue ${env_hkcu} FolderMasterInstallDir
    DeleteRegValue ${env_hkcu} FolderMasterFolderContextMenuEnvVar
    SectionEnd