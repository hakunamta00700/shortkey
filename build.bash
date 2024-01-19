#!/bin/bash

pyinstaller --onefile --windowed --name ShortKey --icon=src/resources/icon.icns --add-data "src/resources/icon.png:resources" --add-data "src/resources/keys.json:resources" src/main.py
