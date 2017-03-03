#!/usr/bin/env bash

# working with Qt Installer Framework from
# https://download.qt.io/official_releases/qt-installer-framework/2.0.3/QtInstallerFramework-mac-x64.dmg

current_mpt_version="MetadataPublishingTool.app"
current_qt_version="QtIFW2.0.3"

qt_bin=~/Qt/$current_qt_version/bin/binarycreator
qt_archivegen=~/Qt/$current_qt_version/bin/archivegen

if [ -e "$qt_bin" ]; then
    echo "Found $qt_bin"
else
    echo "No Qt Installer Framework found at $qt_bin"
    exit 1
fi

cp dist/$current_mpt_version .

echo "Archiving $current_mpt_version"
$qt_archivegen installer/packages/nl.knaw.dans.ehri.mpt/data/mpt_mac.7z $current_mpt_version
echo "Archived $current_mpt_version as installer/packages/nl.knaw.dans.ehri.mpt/data/mpt_mac.7z"

rm -Rf $current_mpt_version

echo "Creating installer..."
$qt_bin -c installer/config/config.xml -p installer/packages --offline-only MPT_mac_installer
echo "Created MPT_mac_installer.app"

echo "Code signing MPT_mac_installer.app..."
codesign -s "Code Signing Cerificate" MPT_mac_installer.app --deep


# Q: How to create a disk image?
# http://www.wikihow.com/Make-a-DMG-File-on-a-Mac

echo "Creating disk image..."
hdiutil create MPT_mac_installer.dmg -volname "MPT_mac_installer" \
    -srcfolder MPT_mac_installer.app


# Q: How to make a disk image window open automatically?
# A: https://discussions.apple.com/thread/3851123?tstart=0
# bless --openfolder /Volumes/MPT_mac_installer


mkdir dist_installer
rm -Rf dist_installer/*
echo "Moving files"
mv MPT_mac_installer.app dist_installer/
mv MPT_mac_installer.dmg dist_installer/
echo "Finished"

