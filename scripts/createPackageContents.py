#
# Download wix from http://wix.sourceforge.net/
# Install it to a path that DOES NOT have spaces or use a subst drive
# Set windows environment variable DEVBIN 
#
import os, sys, shutil, hashlib, socket, time, tempfile
import random, re
from xml.dom import minidom
from os.path import join
import getopt

packageFiles =""

# command line settings
cmdLineArgs ={
	'name' : 'none',
	'source': 'none',
	'template': 'none',
}

cmdLineArgsHelp ={
	'help': ( 'Display this usage message and exit', '' ),
	'debug': ( 'Do not delete the temporary files for debugging builds.\n        Store temp files in a temp folder under the current folder', '' ),
	'name': ( 'The plug-in application name', 'path' ),
	'source': ( 'The path to the plug-in directory', 'path' ),
	'template': ( 'The path/filename to the xml file', 'path' ),
}

filestoskip =[ # ", someotherfile.ext" etc.
	'.DS_Store',
	'thumbs.db',
	'PackageContents.xml'
]

#------------------------------------------------------------------------------
def buildwixtree (xdir):
	global cmdLineArgs, filestoskip, packageFiles
	dirs =[]
	xxdir =xdir.replace (cmdLineArgs ['source'], './')
	for e in os.listdir (xdir):
		if os.path.isdir (os.path.join (xdir, e)):
			dirs.append (e)
		else:
			if e not in filestoskip:
				# ComponentEntry
				packageFiles +=("\t\t<ComponentEntry ModuleName=\"%s\" />\n" % join (xxdir, e).replace ('\\', '/'))
	# Directories
	for d in dirs:
		buildwixtree (join (xdir, d))
	
#------------------------------------------------------------------------------
def RenderFile (filename, outfile):
	global cmdLineArgs, packageFiles
	wix =open (filename, 'r')
	lines ='' . join (wix.readlines ())
	wix.close ()
	lines =lines.replace ('{{AppName}}', cmdLineArgs ['name'])
	lines =lines.replace ('{{GUID}}', GenerateGUID ())
	lines =lines.replace ('{{FILES}}', packageFiles)
	out =open (outfile, 'w')
	out.write (lines)
	out.close ()
		
#------------------------------------------------------------------------------
def createPackageContentsFile ():
	global cmdLineArgs
	buildwixtree (cmdLineArgs ['source'])
	if os.path.isfile (cmdLineArgs ['template']):
		RenderFile (cmdLineArgs ['template'], os.path.join (cmdLineArgs ['source'], 'PackageContents.xml'))

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
	# Add a trailing slash to the source directory
	cmdLineArgs ['source'] +='/'
	
#------------------------------------------------------------------------------
def main ():
	global cmdLineArgs, packageFiles
	if len (sys.argv) < 2:
		return (-1)
	try:
		parseargs ()
	except getopt.GetoptError, err:
		# Print help information and exit:
		print str (err) # Will print something like "option -a not recognized"
		return (2)
	if os.path.isfile (os.path.join (cmdLineArgs ['source'], 'PackageContents.xml')):
		for num in range(0, 1000):
			if not os.path.isfile (os.path.join (cmdLineArgs ['source'], 'PackageContents.bak%d' % num)):
				shutil.copy2 (os.path.join (cmdLineArgs ['source'], 'PackageContents.xml'), os.path.join (cmdLineArgs ['source'], 'PackageContents.bak%d' % num))
				break
				
	createPackageContentsFile ()
	return (0)

#------------------------------------------------------------------------------
if __name__ == "__main__":
	sys.exit(main())
