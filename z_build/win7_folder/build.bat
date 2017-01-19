@echo off
title Build a Windows executable with pyinstaller

rem We assume that rspub-core (https://github.com/EHRI/rspub-core) is installed
rem alongside rspub-gui.

if exist build RMDIR /S /Q build
if exist dist RMDIR /S /Q dist
rem The postman always rings ...
if exist build RMDIR /S /Q build
if exist dist RMDIR /S /Q dist

pyinstaller rsapp.spec

echo "Finished"