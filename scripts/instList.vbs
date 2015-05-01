strComputer = "idefix"
Set objWMIService = GetObject("winmgmts:{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2")
Set colSoftware = objWMIService.ExecQuery ("Select * from Win32_Product where Caption like '%Topo%'")'
'Set colSoftware = objWMIService.ExecQuery ("Select * from Win32_Product")'
Set colSettings = objWMIService.ExecQuery ("Select * from Win32_OperatingSystem")

WScript.Echo "Installed Software List and OS Information"
WScript.Echo "=========================================="
WScript.Echo ""

' Computer Information'
WScript.Echo "COMPUTER INFORMATION"
WScript.Echo "===================="
WScript.Echo "Computer Name: " & strComputer
For Each objOperatingSystem in colSettings
	' Crop Operating system name for clean name'
	Result = InStr(objOperatingSystem.Name, "|")
	Result = Result -1
	MyString = Left(objOperatingSystem.Name,Result)
	' Echo stuff
	WScript.Echo "Operating System: " & MyString
	WScript.Echo "Service Pack: " & objOperatingSystem.ServicePackMajorVersion & "." & objOperatingSystem.ServicePackMinorVersion
	WScript.Echo "Installed In: " & objOperatingSystem.WindowsDirectory
	WScript.Echo ""
	Next

' Software Information'
WScript.Echo "SOFTWARE LIST"
WScript.Echo "============="
For Each objSoftware in colSoftware
	WScript.echo objSoftware.Caption
	WScript.echo "    Install Location: " & objSoftware.InstallLocation
	WScript.echo "    Install Source: " & objSoftware.InstallSource
	WScript.echo "    PackageCache: " & objSoftware.PackageCache
	WScript.echo "    PackageCode: " & objSoftware.PackageCode
	WScript.echo "    ProductID: " & objSoftware.ProductID
	WScript.echo "    Version: " & objSoftware.Version
	Next
