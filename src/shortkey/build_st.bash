#!/bin/bash
rm -rf dist
pyinstaller --console --add-data "../resources/keys.json:resources" start.py
rm -rf ../resources/start
cp -a ./dist/start ../resources/
