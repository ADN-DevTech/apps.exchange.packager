@echo off

set rootAppDir=.\Apps\
set Template=winPerMachineIcon
set Version=2016

rem If you ever wanted to add MSM do your MSI automatically, uncomment the line below and add them here
rem Use the ; (semi-column) as separator
rem set MergeMSM=%CommonProgramFiles(x86)%\Microsoft_VC110_CRT_x64.msm;C:\MyMSMFolder\Microsoft_VC110_ATL_x64.msm

:loop
if not "%1" == "" (
    if "%1" == "-h" (
        goto help
        goto:eof
    )
    if "%1" == "-p" (
        set rootAppDir=%2
        shift & shift
        goto loop
    )
    if "%1" == "-t" (
        set Template=%2
        shift & shift
        goto loop
    )
    if "%1" == "-v" (
        set Version=%2
        shift & shift
        goto loop
    )
    set AppName=%1
)

set PackageSrc=%rootAppDir%%AppName%

call scripts\build-win.bat
goto:eof

:help
echo win [^-h] [^-p ^<path^>] [^-t ^<template^>] [^-v ^<version^>] ^<project^>
echo.
echo 	^-p^|^-^-path	Path to the directory containing the project root folder
echo 			(default is %rootAppDir%)
echo 	^-t^|^-^-template	Template to use for packaging the project
echo 			(default is %Template%)
echo 	^-v^|^-^-version	Product version string
echo 			(default is %Version%)
echo 	^<project^>	Folder name of the project to package
echo.
echo 	^-h^|^-^-help	This message
echo.
