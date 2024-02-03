@echo off
setlocal

REM Check if the correct number of arguments is provided
if "%~1"=="" (
    echo Usage: %~nx0 ^<mode^>
    echo Modes: dev, test, coverage
    exit /b 1
)

REM Set the mode variable to the first command-line argument
set MODE=%1

REM Activate the virtual environment
call venv\Scripts\activate

REM Check if the mode is valid
if /i "%MODE%"=="dev" (
    echo Running in dev mode
    call python FolderMaster.py
) else if /i "%MODE%"=="test" (
    echo Running in test mode
    call python FolderMasterUnitTesting.py
) else if /i "%MODE%"=="coverage" (
    echo Running in coverage mode
    call coverage run FolderMasterUnitTesting.py
    call coverage report -m
) else (
    echo Invalid mode.
    echo Modes: dev, test, coverage
    exit /b 1
)

endlocal