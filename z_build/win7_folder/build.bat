@echo off
title Build a Windows executable with pyinstaller

rem We assume that rspub-core (https://github.com/EHRI/rspub-core) is installed
rem alongside rspub-gui.

rem WARN will not work on Windows10:
rem https://www.reddit.com/r/learnpython/comments/3um6l0/pyinstaller_not_working_on_windows_10/
rem https://answers.microsoft.com/en-us/windows/forum/windows_10-other_settings/problem-with-universal-runtime-on-windows-10-pro/9fda2f7d-5cf8-4906-a542-77147e557d5d

if exist build RMDIR /S /Q build
if exist dist RMDIR /S /Q dist
rem The postman always rings ...
if exist build RMDIR /S /Q build
if exist dist RMDIR /S /Q dist

pyinstaller rsapp.spec

echo "Finished"