#!/bin/bash
# echo build_start
# pushd src/shortkey
# ./build_st.bash
# popd
# echo build_main
rm -rf dist
pyinstaller --onefile --windowed --name ShortKey --icon=src/shortkey/resources/icon.icns --add-data "src/shortkey/resources/icon.png:resources" --add-data "src/shortkey/resources/keys.json:resources" src/main.py
