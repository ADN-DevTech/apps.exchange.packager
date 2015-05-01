@echo off

set argC=0
for %%x in (%*) do set /A argC+=1
if "%1" == "-h" goto :help
if %argC% lss 1 goto :help
if %argC% gtr 3 goto :help

set AppName=default
if not "%1" == "" set AppName=%1
set rootAppDir=..\Apps\
if not "%2" == "" set rootAppDir=%2
set PackageSrc=%rootAppDir%%AppName%
set Template=Profiles\PackageContents.xml
if not "%3" == "" set Template=%3

call scripts\setup.bat
%PYTHON_EXE% scripts\createPackageContents.py --name %AppName% --source "%PackageSrc%" --template %Template%
goto :eof

:help
echo Usage: _xml [-h] AppName [rootAppDir] [Template]
echo.
echo          -h           - This message
echo          AppName      - Application name (should match the folder name in rootAppDir
echo          rootAppDir   - Optional folder where to find the App to create the XML for (default is: ..\Apps\)
echo          Template     - Optional argument to specify the PackageContents.xml to render (default is: Profiles\PackageContents.xml)
echo.
echo  Ex:
echo          _xml -h
echo          _xml MathNode
echo          _xml MathNode ..\Apps\
echo          _xml MathNode ..\Apps\ Profiles\PackageContents.xml