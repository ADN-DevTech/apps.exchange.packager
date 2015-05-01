rem @echo off
call scripts\setup-win.bat

if exist ".\output\%AppName%-win64.msi" del ".\output\%AppName%-win64.msi"
if exist ".\output\%AppName%-win64.wixpdb" del ".\output\%AppName%-win64.wixpdb"
rem if "%AppHost%" == "" set AppHost=maya

%PYTHON_EXE% scripts/createPluginInstaller.py --debug --source "%PackageSrc%" --installer ".\output\%AppName%-win64.msi" --version %Version% --platform win64 --template profiles/%Template%

if "%Certificate_AppStore%" == "" (
  echo Warning: MSI not signed, Windows7 and beyond will complain during install.
) else (
  tools\signtool sign /v /f .\DigitalSignature\%Certificate_AppStore% /p %Certificate_Password% /t http://timestamp.verisign.com/scripts/timstamp.dll ".\output\%AppName%-win64.msi"
  tools\signtool verify /v /pa ".\output\%AppName%-win64.msi"
)

pause