#!/usr/bin/env bash

# working with Qt Installer Framework from
# https://download.qt.io/official_releases/qt-installer-framework/2.0.3/QtInstallerFramework-mac-x64.dmg

current_mpt_version="MetadataPublishingTool-1.0.rc.4.app"
current_qt_version="QtIFW2.0.3"

qt_bin=~/Qt/$current_qt_version/bin/binarycreator
qt_archivegen=~/Qt/$current_qt_version/bin/archivegen

if [ -e "$qt_bin" ]; then
    echo "Found $qt_bin"
else
    echo "No Qt Installer Framework found at $qt_bin"
    exit 1
fi

$qt_archivegen packages/nl.knaw.dans.ehri.mpt/data/mpt_win.7z ../dist/$current_mpt_version

$qt_bin -c config/config.xml -p packages MPT-Installer