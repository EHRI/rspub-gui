#!/bin/bash --

# We assume that rspub-core (https://github.com/EHRI/rspub-core) is installed
# alongside rspub-gui.

# APPNAME should equal > app = BUNDLE(exe, name=xxx < in rsapp.spec
APPNAME="MetadataPublishingTool-1.0.rc.1.app"

rm -Rf build dist

pyinstaller --onefile -w rsapp.spec

# pyinstaller is lazy: Mac oss app still missing files
cp -R dist/MetadataPublishingTool/* "dist/$APPNAME/Contents/MacOs"

# codesign has problems with these two:
rm -Rf "dist/$APPNAME/Contents/MacOs/include"
rm -Rf "dist/$APPNAME/Contents/MacOs/lib"
# they can be missed.

echo "This step will probably not work on your machine!"
cd dist/
codesign -s "Code Signing Cerificate" "$APPNAME" --deep
cd ../
echo "Finished"