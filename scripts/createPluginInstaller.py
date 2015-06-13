#
# Download wix from http://wix.sourceforge.net/
# Install it to a path that DOES NOT have spaces or use a subst drive
# Set windows environment variable DEVBIN 
#
# Parameter - Platform:
# 'macos' - for Mac OS
# 'win32' - for Windows 32bits
# 'win64' - for Windows 64bits
# 'linux' - for Linux OS 64bits
#
# Example:
# python.exe createPluginInstaller.py [--debug] --source "C:\test_source" --installer ./test.msi --version 2014 --platform win64 --template Profiles/winPerMachine
#
import os, sys, shutil, hashlib, socket, time, tempfile
import random, re
from xml.dom import minidom
from os.path import join, split
#import npath
import getopt

moduletags =''
shelvestags =''
filetags =''
componentrefs =''
versions =''
msms =[]

# command line settings
cmdLineArgs ={
	'source': 'none',
	'installer': 'none',
	'version': 'none',
	'platform': 'none',
	'template': 'none',
}

cmdLineArgsHelp ={
	'help': ( 'Display this usage message and exit', '' ),
	'debug': ( 'Do not delete the temporary files for debugging builds.\n        Store temp files in a temp folder under the current folder', '' ),
	'source': ( 'The path to the plug-in structure to be packaged', 'path' ),
	'installer': ( 'The path to the installer <output>', 'file' ),
	'version': ( 'The version of the product being targeted', 'version' ),
	'platform': ( 'The target platform. Can be one of: linux, macos, win32, win64', 'platform' ),
	'template': ( 'The path/filename to the installer templates', 'path' ),
}

# PackageContents.xml settings
noneSt ='none'
noguid ='????????-????-????-????-????????????'
configXml ={
	'Publisher': noneSt,
	'PublisherPhone': '',
	'PublisherEmail': '',
	'PublisherURL': '',
	
	'AppDescription': noneSt,
	'AppName': noneSt, # Use for INSTALLTO
	'AppVersion': noneSt,
	'AppNameSpace': noneSt, # Something like "appstore.exchange.autodesk.com"
	'ProductCode': '*',
	'UpgradeCode': noguid,
	'Documentation': noneSt
}
filestoskip =[ # ", someotherfile.ext" etc.
	'.DS_Store',
	'thumbs.db',
	'Thumbs.db'
]

#------------------------------------------------------------------------------
def buildwixtree (xdir):
	global cmdLineArgs, configXml, filestoskip
	global moduletags, shelvestags, filetags, componentrefs 
	dirs =[]
	modulelist =[]
	shelvelist =[]
	filelist =[]
	filesource =[]
	dirlist =os.listdir (xdir)
	for e in dirlist:
		if os.path.isdir (os.path.join (xdir, e)):
			dirs.append (e)
		else:
			if e not in filestoskip:
				unused_fileName, fileExtension =os.path.splitext (e)
				filelist.append (e)
				filesource.append (join (xdir, e))
	# Component
	compName =ValidateMsiLd ('%s.%s' % (os.path.basename (os.path.abspath (xdir)), hashlib.md5 (xdir + 'Comp').hexdigest ()))
	componentrefs +=("<ComponentRef Id='%s' />\n" % compName)
	filetags +=(("<Component Id='%s' Guid='%s'>\n"
	"	<RegistryValue Root='HKCU' Key='Software\\%s\\%s' Type='string' Value='' KeyPath='yes' />\n"
	"	<RemoveFile Id='%s.f' Name='*.*' On='uninstall' />\n"
	"	<RemoveFolder Id='%s.u' On='uninstall' />\n")
	% (compName, GenerateGUID (), configXml ['Publisher'], configXml ['AppName'], compName [-70:], compName [-70:]))
	# Files
	if len (filelist) > 0:
		for xfile, source in zip (filelist, filesource):
			fileName =ValidateMsiLd ('%s.%s' % (xfile, hashlib.md5 (source).hexdigest ()))
			filetags +=(("<File Id='%s' Name='%s' Source='%s' Vital='yes' DiskId='1' />\n") % (fileName, xfile, source))
	# Closing Component
	filetags +="</Component>\n"
	# Directories
	for d in dirs:
		dirName =ValidateMsiLd ('%s.%s' % (d, hashlib.md5 (join (xdir, d)).hexdigest ()))
		filetags +=("<Directory Id='%s' Name='%s'>\n" % (dirName, d))
		buildwixtree (join (xdir, d))
		filetags +="</Directory>\n"

#------------------------------------------------------------------------------
def RenderFile (filename, outfile):
	global cmdLineArgs, configXml
	global moduletags, shelvestags, filetags, versions, componentrefs
	wix =open (filename, 'r')
	lines ='' . join (wix.readlines ())
	wix.close ()
	for i in configXml.keys ():
		lines =lines.replace ('{{' + i + '}}', configXml [i])
	if cmdLineArgs ['platform'] == 'win64':
		lines =lines.replace ('{{PLATFORM}}', 'x64')
		lines =lines.replace ('{{-PLATFORM}}', '-x64')
		lines =lines.replace ('{{WIN64}}', " Win64='yes'")
		lines =lines.replace ('{{64}}', '64')
		lines =lines.replace ('{{-64}}', '-64')
	else:
		lines =lines.replace ('{{PLATFORM}}', 'x86')
		lines =lines.replace ('{{-PLATFORM}}', '')
		lines =lines.replace ('{{WIN64}}', '')
		lines =lines.replace ('{{64}}', '')
		lines =lines.replace ('{{-64}}', '')
	lines =lines.replace ('{{BUNDLE}}', cmdLineArgs ['bundle'])
	lines =lines.replace ('{{VERSION}}', cmdLineArgs ['version'])
	lines =lines.replace ('{{SOURCE}}', cmdLineArgs ['source'])
	lines =lines.replace ('{{INSTALLER-OUTPUT}}', cmdLineArgs ['installer'])
	installerPkgTemp =os.path.basename (cmdLineArgs ['installer'])
	lines =lines.replace ('{{INSTALLER-PKG}}', installerPkgTemp)
	lines =lines.replace ('{{modules}}', moduletags)
	lines =lines.replace ('{{shelves}}', shelvestags)
	lines =lines.replace ('{{data}}', filetags)
	lines =lines.replace ('{{_Version_}}', versions)
	lines =lines.replace ('{{componentrefs}}', componentrefs)
	lines =lines.replace ('{{AUTODESKGUID}}', GenerateGUID ())
	lines =lines.replace ('{{APPLICATIONPLUGINSGUID}}', GenerateGUID ())
	lines =lines.replace ('{{MAYAUSERGUID}}', GenerateGUID ())
	lines =lines.replace ('{{MAYAVERSIONUSERGUID}}', GenerateGUID ())
	lines =lines.replace ('{{MAYAVERSIONMODULESGUID}}', GenerateGUID ())
	lines =lines.replace ('{{MAYAVERSIONPREFSGUID}}', GenerateGUID ())
	lines =lines.replace ('{{MAYAVERSIONPREFSSHELVESGUID}}', GenerateGUID ())
	lines =lines.replace ('{{INSTALLDIRGUID}}', GenerateGUID ())
	out =open (outfile, 'w')
	out.write (lines)
	out.close ()
	
def RenderRtfFile (filename, outfile):
	global cmdLineArgs, configXml
	global moduletags, shelvestags, filetags, componentrefs
	wix =open (filename, 'r')
	lines ='' . join (wix.readlines ())
	wix.close ()
	for i in configXml.keys ():
		lines =lines.replace ('\\{\\{' + i + '\\}\\}', configXml [i])
	out =open (outfile, 'w')
	out.write (lines)
	out.close ()
		
#------------------------------------------------------------------------------
def createWindowsInstaller ():
	global cmdLineArgs, configXml
	global moduletags, shelvestags, filetags, componentrefs, msms
	tempdir =createTempFolder ()

	moduleDir =('%s/%s' % (cmdLineArgs ['source'], 'Contents'))
	if os.path.isfile (cmdLineArgs ['template'] + '/manifest.manifest') and not os.path.isfile (moduleDir + '/' + cmdLineArgs ['bundleNoExt'] + '.manifest'):
		print "Note: Creating manifest file in your source folder\n"
		RenderFile (cmdLineArgs ['template'] + '/manifest.manifest', moduleDir + '/' + cmdLineArgs ['bundleNoExt'] + '.manifest')
    
	msms =os.getenv ('MergeMSM', '').split (';')
	# Build Wix Data Structures
	dirName =ValidateMsiLd (configXml ['AppName'])
	configXml ['AppNameLd'] =dirName
	filetags +=("<Directory Id='%s' Name='%s'>\n" % (dirName, cmdLineArgs ['bundle']))
	for e in msms:
		e =e.replace ('\\', '/')
		if e == '': # or not os.path.isfile (e):
			continue
		compName =GenerateGUID ()
		componentrefs +=("<MergeRef Id='%s' />\n" % compName)
		filetags +=("<Merge Id='%s' SourceFile='%s' DiskId='1' Language='1033' />\n" % (compName, e))
	buildwixtree (cmdLineArgs ['source'])
	filetags +="</Directory>\n"
	# Render Wix and default Help file
	configXml ['PLATFORM'] ='x86'
	configXml ['-PLATFORM'] =''
	configXml ['WIN64'] =''
	configXml ['64'] =''
	configXml ['-64'] =''
	if cmdLineArgs ['platform'] == 'win64':
		configXml ['PLATFORM'] ='x64'
		configXml ['-PLATFORM'] ='-x64'
		configXml ['WIN64'] =" Win64='yes'"
		configXml ['64'] ='64'
		configXml ['-64'] ='-64'
	configXml ['VERSION'] =cmdLineArgs ['version']
	configXml ['AUTODESKGUID'] =GenerateGUID ()
	configXml ['APPLICATIONPLUGINSGUID'] =GenerateGUID ()
	configXml ['MAYAUSERGUID'] =GenerateGUID ()
	configXml ['MAYAVERSIONUSERGUID'] =GenerateGUID ()
	configXml ['MAYAVERSIONMODULESGUID'] =GenerateGUID ()
	configXml ['MAYAVERSIONPREFSGUID'] =GenerateGUID ()
	configXml ['MAYAVERSIONPREFSSHELVESGUID'] =GenerateGUID ()
	configXml ['INSTALLDIRGUID'] =GenerateGUID ()
	dirlist =os.listdir (cmdLineArgs ['template'])
	for e in dirlist:
		if os.path.isfile (os.path.join (cmdLineArgs ['template'], e)):
			RenderFile (cmdLineArgs ['template'] + e, tempdir + '/' + e)
	return (1)

#------------------------------------------------------------------------------
'''
	Old PackageMaker build <legacy / deprecated by Apple>
	
	PackageMaker -build
	 -p cmdLineArgs ['installer']
	 -f tempdir + '/root'
	 -ds
	 -r resDir
	 -i tempdir + '/Info.plist'
	 -d tempdir + '/Description.plist'
'''

def createMacInstaller ():
	global cmdLineArgs, configXml, filestoskip
	tempdir =installerFileCopy ()
	
	moduleDir =('%s/root/%s/%s' % (tempdir, cmdLineArgs ['bundle'], 'Contents'))
	if os.path.isfile (cmdLineArgs ['template'] + '/Info.plist') and not os.path.isfile (moduleDir + '/Info.plist'):
		RenderFile (cmdLineArgs ['template'] + 'Info.plist', moduleDir + '/Info.plist')
	if os.path.isfile (cmdLineArgs ['template'] + '/Description.plist') and not os.path.isfile (moduleDir + '/Description.plist'):
		RenderFile (cmdLineArgs ['template'] + 'Description.plist', moduleDir + '/Description.plist')
	if os.path.isfile (cmdLineArgs ['template'] + '/manifest.manifest') and not os.path.isfile (moduleDir + '/' + cmdLineArgs ['bundleNoExt'] + '.manifest'):
		RenderFile (cmdLineArgs ['template'] + '/manifest.manifest', moduleDir + '/' + cmdLineArgs ['bundleNoExt'] + '.manifest')

	resDir =('%s/Resources' % tempdir)
	mkdir (resDir)
	scriptsDir =('%s/Scripts' % tempdir)
	mkdir (scriptsDir)
	RenderRtfFile (cmdLineArgs ['template'] + '/Resources/Welcome.rtf', resDir + '/Welcome.rtf')
	RenderRtfFile (cmdLineArgs ['template'] + '/Resources/License.rtf', resDir + '/License.rtf')
	if os.path.isfile (cmdLineArgs ['template'] + '/Scripts/postinstall'):
		RenderFile (cmdLineArgs ['template'] + '/Scripts/postinstall', scriptsDir + '/postinstall')
	if os.path.isfile (cmdLineArgs ['template'] + '/distribution.xml') and not os.path.isfile (moduleDir + '/distribution.xml'):
		RenderFile (cmdLineArgs ['template'] + '/distribution.xml', tempdir + '/distribution.xml')
	if os.path.isfile (cmdLineArgs ['template'] + '/InstallerSections.plist') and not os.path.isfile (moduleDir + '/InstallerSections.plist'):
		RenderFile (cmdLineArgs ['template'] + '/InstallerSections.plist', tempdir + '/InstallerSections.plist')
	return (0)

#------------------------------------------------------------------------------
def createLinuxInstaller ():
	global cmdLineArgs, configXml, filestoskip
	tempdir =installerFileCopy ()

	RenderFile (cmdLineArgs ['template'] + 'install.sh', tempdir + '/' + cmdLineArgs ['installer'])

	return (0)

#------------------------------------------------------------------------------
def ReadFromXml (doc, tag, valDefault):
	try:
		stref =doc.getElementsByTagName (tag) [0].firstChild
	except:
		stref =None
	if stref is None:
		return (valDefault)
	st =stref.data
	return (st)

#------------------------------------------------------------------------------
# Generate a GUID for the windows installation
# Source: http://www.krugle.org/kse/files/svn/svn.sourceforge.net/nebuladevice/nebula2/buildsys3/guid.py
def GenerateGUID(): 
	t =long(time.time () * 1000) 
	r =long(random.random () * 100000000000000000L) 
	ip ='' 
	try: 
		ip =socket.gethostbyname (socket.gethostname ()) 
	except: 
		# if we can't get a network address, just imagine one 
		ip = str (random.random () * 100000000000000000L) 
	data =str (t) + ' ' + str (r) + ' ' + ip 
	guidStr =hashlib.md5 (data).hexdigest () 
	return '{%s-%s-%s-%s-%s}' % (guidStr [:8], guidStr [8:12], guidStr [12:16], guidStr [16:20], guidStr [20:]) 

#------------------------------------------------------------------------------
def ValidateMsiLd (ld):
	ld =re.sub (r'([^_.a-zA-Z0-9])', '_', ld)
	ld =ld [-71:]
	if not re.match (r'^[a-zA-Z]{1}.*', ld):
		ld ='_' + ld
	return (ld [-72:])
	
#------------------------------------------------------------------------------
# mkdir that allows creating multi levels and ignoring already existing silently  http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/82465
def mkdir (xdir):
	if os.path.isdir (xdir):
		pass
	elif os.path.isfile (xdir):
		print ("a file with the same name as the desired dir, '%s', already exists." % xdir)
		#raise OSError("a file with the same name as the desired dir, '%s', already exists." % xdir)
	else:
		head, tail =os.path.split (xdir)
		if head and not os.path.isdir (head):
			mkdir (head)
		if tail:
			os.mkdir (xdir)

#------------------------------------------------------------------------------
def createTempFolder():
	global cmdLineArgs, configXml
	if cmdLineArgs ['debug'] == True:
		mkdir ('temp')
		return ('temp')
	random.seed (hashlib.md5 (configXml ['AppDescription']).hexdigest ())
	tempdir =tempfile.gettempdir ()
	tempdir =tempdir.replace ('\\', '/')
	tempd =str (int (random.random () * 100000))
	while 1:
		if (not os.path.isdir (tempdir + '/' + tempd)) and (not os.path.isfile (tempdir + '/' + tempd)): break
		tempd =str (int (random.random () * 100000))
	tempdir +='/' + tempd
	mkdir (tempdir)
	return (tempdir)

#------------------------------------------------------------------------------
def installerFileCopy ():
	global cmdLineArgs, configXml, filestoskip
	tempdir =createTempFolder ()
	files =os.walk (cmdLineArgs ['source'])
	for root, unused_dirs, files in files:
		dirtomake =root.replace (cmdLineArgs ['source'], '')
		if '.dSYM' in dirtomake:
			continue
		
		moduleDir =('%s/root/%s/%s' % (tempdir, cmdLineArgs ['bundle'], dirtomake))
		mkdir (moduleDir)
		for xfile in files:
			if xfile not in filestoskip:
				shutil.copy (join (root, xfile), moduleDir)
	return (tempdir)

#------------------------------------------------------------------------------
def parseargs():
	global cmdLineArgs, cmdLineArgsHelp
	for i, arg in enumerate (sys.argv):
		sys.argv [i] =arg.replace ('\\', '/')
	
	args =[]
	argsSt =''
	for i in cmdLineArgsHelp.keys ():
		if cmdLineArgsHelp [i] [1] == '':
			args.append (i)
			argsSt +=i [:1]
		else:
			args.append (i + '=')
			argsSt +=i [:1] + ':'
	opts, unused_args =getopt.getopt (sys.argv [1:], argsSt, args)
	# Debugging in Eclipse on the Mac add a second argument in sys.argv
	if len (opts) == 0:
		opts, unused_args =getopt.getopt (sys.argv [2:], argsSt, args)		
			
	# End of Debugging in Eclipse trick
	cmdLineArgs ['debug'] =False
	for o, a in opts:
		if o in ('-h', '--help'):
			usage ()
			sys.exit ()
		if o in ('-d', '--debug'):
			cmdLineArgs ['debug'] =True
		else:
			cmdLineArgs [o[2:]] =a
	# Bundle name vs AppName
	cmdLineArgs ['bundle'] =os.path.basename (cmdLineArgs ['source'])
	cmdLineArgs ['bundleNoExt'] =os.path.basename (os.path.splitext (cmdLineArgs ['source']) [0])
	# Add a trailing slash to the source directory
	cmdLineArgs ['source'] +='/'
	# Add a trailing slash to the template directory
	cmdLineArgs ['template'] +='/'

#------------------------------------------------------------------------------
def parsePackageContentsXml():
	global cmdLineArgs, configXml, noguid, noneSt
	# Determine if we have an XML config or are using the defaults
	xmlFilename =cmdLineArgs ['source'] + 'PackageContents.xml'
	if os.path.isfile (xmlFilename) == False:
		return (-1)
	doc =minidom.parse (xmlFilename)
	elt =doc.getElementsByTagName ('ApplicationPackage') [0]
	configXml ['AppDescription'] =str (elt.getAttribute ('Description'))
	configXml ['AppName'] =str (elt.getAttribute ('Name'))
	configXml ['AppNameSpace'] =str (elt.getAttribute ('AppNameSpace'))
	configXml ['AppVersion'] =str (elt.getAttribute ('AppVersion'))
	configXml ['ProductCode'] =str (elt.getAttribute ('ProductCode'))
	configXml ['UpgradeCode'] =str (elt.getAttribute ('UpgradeCode'))
	configXml ['Documentation'] =str (elt.getAttribute ('HelpFile'))
	configXml ['Author'] =str (elt.getAttribute ('Author'))
	configXml ['AutodeskProduct'] =str (elt.getAttribute ('AutodeskProduct'))
	
	elt =doc.getElementsByTagName ('CompanyDetails') [0]
	configXml ['Publisher'] =str (elt.getAttribute ('Name'))
	configXml ['PublisherPhone'] =str (elt.getAttribute ('Phone'))
	configXml ['PublisherEmail'] =str (elt.getAttribute ('Email'))
	configXml ['PublisherURL'] =str (elt.getAttribute ('Url'))

	elt =doc.getElementsByTagName ('RuntimeRequirements') [0]
	configXml ['OS'] =str (elt.getAttribute ('OS'))

	doc.unlink ()

	configXml ['UpgradeCodeLessBackets'] =configXml ['UpgradeCode'].strip ('{').strip ('}')
	configXml ['manifestOS'] =configXml ['OS'].replace ('macOS', 'mac')
	configXml ['manifestOS'] =configXml ['manifestOS'].replace ('win32|win64', 'windows')
	configXml ['manifestOS'] =configXml ['manifestOS'].replace ('Win32|Win64', 'windows')
	configXml ['manifestOS'] =configXml ['manifestOS'].replace ('win32', 'windows')
	configXml ['manifestOS'] =configXml ['manifestOS'].replace ('Win32', 'windows')
	configXml ['manifestOS'] =configXml ['manifestOS'].replace ('win64', 'windows')
	configXml ['manifestOS'] =configXml ['manifestOS'].replace ('Win64', 'windows')
	if configXml ['Author'] != configXml ['Publisher']:
		configXml ['AuthorPublisher'] =("%s - %s" % (configXml ['Author'], configXml ['Publisher']))
	else:
		configXml ['AuthorPublisher'] =configXml ['Author']
	# Determine if we have been provided with a GUID in the config file
	if len (configXml ['ProductCode']) <= 1:
		configXml ['ProductCode'] =GenerateGUID ()
	# Determine if we have been provided with a GUID in the config file
	if len (configXml ['UpgradeCode']) < 1 or configXml ['UpgradeCode'] == noguid:
		configXml ['UpgradeCode'] =GenerateGUID ()
	# Documentation url
	if configXml ['Documentation'] == noneSt or configXml ['Documentation'] == '':
		configXml ['Documentation'] ='./Contents/docs/index.html'
	elif configXml ['Documentation'] [:2] in ( './', ".\\" ):
		configXml ['Documentation'] =cmdLineArgs ['bundle'] + configXml ['Documentation'] [1:]
	if configXml ['PublisherPhone'] == noneSt or configXml ['PublisherPhone'] == '':
		configXml ['PublisherPhone'] =configXml ['PublisherEmail']
	return (0)
			
#------------------------------------------------------------------------------
def usage():
	global cmdLineArgs, cmdLineArgsHelp 
	print '\n  createPluginInstaller.py -- create an installer for Maya plug-ins'
	print ''
	print '  createPluginInstaller.py'
	for i in cmdLineArgsHelp.keys ():
		print ''
		print '    -' + i [:1] + ', --' + i + '    ' + cmdLineArgsHelp [i] [1]
		print '        ' + cmdLineArgsHelp [i] [0]
	print ''
	print '  The DEVBIN environment variable pointing to the Wix directory must be defined. Windows only.'
	print '  Exits with 0 on success.'

#------------------------------------------------------------------------------
def main ():
	global cmdLineArgs, configXml, noneSt, noguid
	if len (sys.argv) < 2:
		usage ()
		return (-1)
	try:
		parseargs ()
	except getopt.GetoptError, err:
		# Print help information and exit:
		print str (err) # Will print something like "option -a not recognized"
		usage ()
		return (2)

	if parsePackageContentsXml () != 0:
		print 'no PackageContents.xml file in: ' + cmdLineArgs ['source']
		return (3)
	
	retCode =-1
	if cmdLineArgs ['platform'] == 'win32' or cmdLineArgs ['platform'] == 'win64':
		retCode =createWindowsInstaller ()
	elif cmdLineArgs ['platform'] == 'macos':
		retCode =createMacInstaller () 
	elif cmdLineArgs ['platform'] == 'linux':
		retCode =createLinuxInstaller ()
	else:
		print 'no platform matched: ' + cmdLineArgs ['platform']
	return (retCode)

#------------------------------------------------------------------------------
if __name__ == "__main__":
	sys.exit(main())
