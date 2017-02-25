@echo off
title Build a Windows installer with Qt Installer Framework

rem NOT WORKING. The application works fine, once installed it gives a fatal error.

rem https://download.qt.io/official_releases/qt-installer-framework/2.0.3/QtInstallerFramework-win-x86.exe

SET current_mpt_version="MetadataPublishingTool-1.0.rc.4.exe"

rem C:\Qt\QtIFW2.0.3\bin\archivegen.exe packages\nl.knaw.dans.ehri.mpt\data\mpt_win.7z ..\dist\%current_mpt_version%

C:\Qt\QtIFW2.0.3\bin\binarycreator.exe --offline-only -c config\config.xml -p packages MPT_win_installer

echo "Finished building MPT_win_installer"
