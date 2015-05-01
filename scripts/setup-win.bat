rem @echo off
%~d0
rem cd /d %~dp0..

if exist m:\nul subst m: /d
subst m: "C:\Program Files (x86)\WiX Toolset v3.9"

call .\DigitalSignature\AppStore.bat
set DEVBIN=m:
set PYTHON_EXE=c:\Python27\python.exe

if not exist temp mkdir temp
del temp\*.* /q /s > nul
