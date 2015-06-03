rem @echo off

%DEVBIN%\bin\candle.exe .\temp\root.wxs -out .\temp\plugin.wixobj
if ERRORLEVEL 1 (
	echo "Wix/Candle error - Build aborted!"
	goto end
) else (
	%DEVBIN%\bin\light.exe -sw1076 .\temp\plugin.wixobj -out ".\output\%AppName%-win64.msi"
	if ERRORLEVEL 1 (
		echo "Wix/Light error - Build aborted!"
		goto end
	)
)

:end
