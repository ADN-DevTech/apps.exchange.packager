
# Cross platform Apps Exchange Store Packager Scripts
producing WIX/MSI for Windows, PKG for Mac OSX and shell/tar file for Linux,

<b>Note:</b> Signatures files aren't posted in this repo. But the scripts can work with/or 
without the signatures files. Signing installers for Windows and Mac OSX aren't strictly
required, but recommended. If no digital signature is provided, the user will be prompted 
during install.


## Setup

For all OS, clone this repo on your local machine.


### Windows

1. Go to http://wixtoolset.org/
   * Download and install
2. Got to http://python.org
   * Download and install the latest 2.x version
3. Go in apps.exchange.packager\scripts, and open the setup-win.bat file in a text editor
   * Change the subst @ line #6 to point where you installed the 'Wix Toolset' at step #1
   * Change the PYTHON_EXE variable @ line #10 to point to your Python executable


### OSX

1. Download the PackageMaker tool from the [Apple developer center](https://developer.apple.com/downloads/index.action) in the Auxiliary Tools for Xcode package.

2. Go in apps.exchange.packager\scripts, and open the setup-osx file in a text editor
   * Change the PACKAGER variable @ line #9 to point where you installed the 'PackageMaker.app' 

3. Make sure the temp and output folders have write permission.


### Linux

No setup required! You're all set.<br />
Just make sure the temp and output folders have write permission.


## Usage

There is 3 scripts available. One for each platform: win, osx, linux.
```
osx [-h] [-p <path>] [-t <template>] [-v <version>] <project>

	-p			Path to the directory containing the project root folder
				(default is ./Apps/)
	-t			Template to use for packaging the project
				(default is osxPerMachine)
	-v			Product version string
				(default is 2016)
	<project>	Folder name of the project to package

	-h			This message
```

By default, the scripts assume:<br />
1. they should find the app in ./Apps/
2. they should use the per-machine templates
3. the current Autodesk product platform is the 2016 version

You can change these options using the command flags.

<b>Note:</b> Do not forgoet the closing / on OSX and Linux or \ on Windows for the -p path option.



### Examples with the MathNode sample for Maya

Windows: `win MathNode`
OSX: `osx MathNode`
Linux: `linux MathNode`

#### with the arguments to change the default template

Windows: `win -t winPerUser MathNode`
OSX: `osx -t osxPerUser MathNode`

#### with an hypothetical AutoCAD/Revit/Inventor bundle

Windows: `win -p d:\Dev\ -t winPerMachineIcon MyApp.bundle`
OSX: `osx -p ~/Projects/ -t osxPerMachine MyApp.bundle`

<b>Note:</b> Note the difference between Maya and the other products. Maya cannot accept a .bundle extenstion for an apps.echange bundle. Whereas, all others do require that extension.


--------

## License

This utility is licensed under the terms of the [MIT License](http://opensource.org/licenses/MIT). Please see the [LICENSE](LICENSE) file for full details.


## Written by

Cyrille Fauvel (Autodesk Developer Network)<br />
http://www.autodesk.com/adn<br />
http://around-the-corner.typepad.com/<br />