#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <mode>"
    echo "Modes: dev, test, coverage"
    exit 1
fi

# Set the mode variable to the first command-line argument
MODE=$1

# Activate the virtual environment
source venv/Scripts/activate

# Check if the mode is valid
if [ "$MODE" = "dev" ]; then
    echo "Running in dev mode"
    python FolderMaster.py
elif [ "$MODE" = "test" ]; then
    echo "Running in test mode"
    python FolderMasterUnitTesting.py
elif [ "$MODE" = "coverage" ]; then
    echo "Running in coverage mode"
    coverage run FolderMasterUnitTesting.py
    coverage report -m
else
    echo "Invalid mode"
    echo "Modes: dev, test, coverage"
    exit 1
fi