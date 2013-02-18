#!/bin/sh
python setup.py py2app -A
defaults write com.apple.mail EnableBundles -bool YES
mkdir -p ~/Library/Mail/Bundles
cp -R dist/plugin.mailbundle ~/Library/Mail/Bundles/
rm -Rf dist
