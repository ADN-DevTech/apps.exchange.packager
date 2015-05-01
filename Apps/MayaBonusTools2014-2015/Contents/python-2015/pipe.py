# Copyright (C) 1997-2014 Autodesk, Inc., and/or its licensors.
# All rights reserved.
#
# The coded instructions, statements, computer programs, and/or related
# material (collectively the "Data") in these files contain unpublished
# information proprietary to Autodesk, Inc. ("Autodesk") and/or its licensors,
# which is protected by U.S. and Canadian federal copyright law and by
# international treaties.
#
# The Data is provided for use exclusively by You. You have the right to use,
# modify, and incorporate this Data into other products for purposes authorized 
# by the Autodesk software license agreement, without fee.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. AUTODESK
# DOES NOT MAKE AND HEREBY DISCLAIMS ANY EXPRESS OR IMPLIED WARRANTIES
# INCLUDING, BUT NOT LIMITED TO, THE WARRANTIES OF NON-INFRINGEMENT,
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, OR ARISING FROM A COURSE 
# OF DEALING, USAGE, OR TRADE PRACTICE. IN NO EVENT WILL AUTODESK AND/OR ITS
# LICENSORS BE LIABLE FOR ANY LOST REVENUES, DATA, OR PROFITS, OR SPECIAL,
# DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES, EVEN IF AUTODESK AND/OR ITS
# LICENSORS HAS BEEN ADVISED OF THE POSSIBILITY OR PROBABILITY OF SUCH DAMAGES.

########################
########################
## Pipe Documentation ##
########################
########################
################
# Pipe Startup #
################

## Import the module
#import pipe

## Initialize the Pipe
## pipeInitPipe(basePath,show,verbosity)
#pipe.pipeInitPipe("C:/pipe/","TortiseAndHair",0)

## Create a New Show/Project
## pipeCreateShow(pipeBasePath,pipeShow):
#pipe.pipeInitPipe("C:/pipe/","StarWarz",0)


########################
# Define Data Elements #
########################

## Add an Asset Type to the Current Show
## pipeAddAssetType(newAssetType)
#pipe.pipeAddAssetType("character")

## Add a Representation Type to the Show
##  pipeAddRepType(name,data,subdir,filename,numMetric)
#pipe.pipeAddRepType("modelLoRes","mayaAscii","maya","[ASSET].[VAR].[REP]","25")

## Add a Representation to the Asset Type List
##pipeAddAssetTypeRep(type,repType)
#pipe.pipeAddAssetTypeRep("character","preViz")

## Add a Data Type to a show
## pipeAddDataType(dataType,dataEditor,dataAuthor,dataExt)
#pipe.pipeAddDataType("OBJ","maya","maya",".obj")

## Re-Define the Asset Library (Completely Destructive)
# pipeCreateNewLib()



#########################
# Define Asset Elements #
#########################

## Add an Asset to the Show
## pipeAddAsset(newAssetName,newAssetType,newNotes):
#pipe.pipeAddAsset('lukeSkywalker','character','He is the hero'):

## Add a Variation to an Asset
##pipeEditAsset(AssetName,[variationName],"addVar")
#pipe.pipeEditAsset('lukeSkywalker',['pilot'],'addVar')

## Add a Representation to a Variation to an Asset
##pipeEditAsset(AssetName,[variationName,representation],"addRep")
#pipe.pipeEditAsset(lukeSkywalker,['pilot','geoLo'],'addRep')

#########################################
# Query Define Asset Elements Existance #
#########################################

## Check if an Asset Type exists
##pipeAssetTypeExists(type)
#pipe.pipeAssetTypeExists("character")

## Check if a Data Type exists
##pipeDataTypeExists(type)
#pipe.pipeDataTypeExists("OBJ")

## Check if an Asset exists
##pipeAssetExists(name)
#pipe.pipeAssetExists("lukeSkywalker")

## Check if an Asset Variation exists
##pipeAssetVariationExists(asset,variation)
#pipe.pipeAssetVariationExists('lukeSkywalker','preViz')

## Check if a Representation exists for an Asset Variation
##pipeAssetVarRepExists(assetName,varType, representation)
#pipe.pipeAssetVarRepExists('lukeSkywalker','preViz', 'bBoxLo')

## Check if a Representation exists for the Show
##pipeRepExists(representation)
#pipe.pipeRepExists('bBoxLo')


#########################
# List Pipe Information #
#########################

## List Asset Types for Show
#pipe.pipeListAssetTypes()

## List Assets in Library
#pipe.pipeListAssets()

## List the Data Types for the Show
#pipe.pipeListDataTypes()

## List the Representation Types for the Show
#pipe.pipeListRepTypes()

## List the Varations for an Asset
## pipeListAssetVars(assetName)
#pipe.pipeListAssetVars('lukeSkywalker')

## List the Representations for an Asset Variation
## pipeListAssetVarReps(assetName,varType)
#pipe.pipeListAssetVarReps('lukeSkywalker','preViz')

## List Asset Type Representations
## pipeListAssetTypeReps(asset)
#pipe.pipeListAssetTypeReps('char')


########################
# Get Pipe Information #
########################

## Get the Current Show Name
#pipeGetPipeShow()

## Get the Current Pipe Base Path
#pipeGetPipePath()

## Get Asset Information
## pipeGetAssetInfoName(tempName,info)
#pipe.pipeGetAssetInfoName("lukeSkywalker","Id")
#pipe.pipeGetAssetInfoName("lukeSkywalker","Type")
#pipe.pipeGetAssetInfoName("lukeSkywalker","Note")
#pipe.pipeGetAssetInfoName("lukeSkywalker","Creator")

## Get Data Type Information
## pipeGetDataTypeInfo(dataType,Tag)
#pipe.pipeGetDataTypeInfo('alembic','Editor')
#pipe.pipeGetDataTypeInfo('alembic','Author')
#pipe.pipeGetDataTypeInfo('alembic','Extension')

## Get Represenation Data Type Information
## pipeGetRepDataType(repType, Tag)
#pipe.pipeGetRepDataType("bBox","Data")
#pipe.pipeGetRepDataType("bBox","SubDir")
#pipe.pipeGetRepDataType("bBox","Filename")
#pipe.pipeGetRepDataType("bBox","NumMetric")



###############
###############
## Pipe Code ##
###############
###############

# Import Modules
import xml.etree.ElementTree as xmlT
import os
import os.path
import shutil
from xml.dom import minidom
# Setup Globals
global pipeBasePath
global pipeShow
global verbosity
global pipeXMLConfigPath
global pipeAssetLibPath
global pipeAssetDBPath
global pipeAssetProdPath
# Set Variables
verbosity = 0

########################
# INITIALIZE THE PIPE #
########################
def pipeInitPipe(basePath,show,verbos):

# Init Variables
    global pipeShow
    global pipeBasePath
    global verbosity
    global pipeXMLConfigPath
    global pipeAssetLibPath
    global pipeAssetDBPath
    global pipeAssetProdPath

# Set Variables
    verbosity = verbos
    pipeShow=show
    pipeBasePath=basePath

    if verbosity == 1:
        print "\n\n-------------------------------------"
        print "-    PIPE: INITIALIZE THE PIPE      -"
        print "-------------------------------------"
        print "  - Check for Pipe XML Config Files"

# Set Paths
    pipeXMLConfigPath = pipeBasePath + pipeShow + "/config/"
    pipeAssetLibPath = pipeBasePath + pipeShow + "/lib/"
    pipeAssetDBPath = pipeBasePath + pipeShow + "/db/"
    pipeAssetProdPath = pipeBasePath + pipeShow + "/prod/"

# Check if Show Exists
    if os.path.exists(pipeBasePath + pipeShow):
        if verbosity == 1:
            print '  - Project "' + pipeShow + '" Exists'
    else:
        if verbosity == 1:
            print '  - Project "' + pipeShow + '" Does Not Exists'
            print '  - Configure New Project "' + pipeShow + '" \n'
        pipeCreateShow(pipeBasePath,pipeShow)

     
########################
# Create A New Project #
########################

def pipeCreateShow(pipeBasePath,pipeShow):
    if verbosity == 1:
       print "---------------------------"
       print "PIPE: CONFIGURE NEW PROJECT"
       print "---------------------------"
       print "  - Setting up Variables"

    pipeXMLConfigPath = pipeBasePath + pipeShow + "/config/"
    pipeAssetLibPath = pipeBasePath + pipeShow + "/lib/"
    pipeAssetDBPath = pipeBasePath + pipeShow + "/db/"
    pipeAssetProdPath = pipeBasePath + pipeShow + "/prod/"

# Make Startup Directories
    if verbosity == 1:
         print "  - Create Initial Directory Structure"
    if os.path.exists(pipeXMLConfigPath)!=True:
        os.makedirs(pipeXMLConfigPath, 0777)
    if os.path.exists(pipeAssetLibPath)!=True:
        os.makedirs(pipeAssetLibPath, 0777)
        os.makedirs(pipeAssetLibPath+"assets/", 0777)
        os.makedirs(pipeAssetLibPath+"xml/", 0777)
    if os.path.exists(pipeAssetDBPath)!=True:
        os.makedirs(pipeAssetDBPath, 0777)
    if os.path.exists(pipeAssetProdPath)!=True:
        os.makedirs(pipeAssetProdPath, 0777)

# Create Initial Asset Library XML
    pipeCreateNewLib()

# Create the Rep Types XML Document
    initialRepTypes = ["rig","rigLow","rigMed","rigHigh","col","bBoxLo","bBox","geoLo","geo","gpuLo","gpu"]
    initialRepDataTypes = ["mayaAscii","mayaAscii","mayaAscii","mayaAscii","mayaAscii","bBoxA","bBoxA","mayaAscii","mayaAscii","bBoxC","gpuCache"]
    initialSubdirs = ["maya","maya","maya","maya","maya","maya","maya","maya","maya","cache","cache"]
    initialFilenames = ["[ASSET].[VAR].[REP]","[ASSET].[VAR].[REP]","[ASSET].[VAR].[REP]","[ASSET].[VAR].[REP]","[ASSET].[VAR].[REP]","[ASSET].[VAR].[REP]","[ASSET].[VAR].[REP]","[ASSET].[VAR].[REP]","[ASSET].[VAR].[REP]","[ASSET].[VAR].[REP]","[ASSET].[VAR].[REP]"]
    initialNumMetric = ["75","70","80","90","10","20","30","40","50","35","60"]
    i=0
    for tempRepType in initialRepTypes:
        pipeAddRepType(initialRepTypes[i], initialRepDataTypes[i], initialSubdirs[i], initialFilenames[i], initialNumMetric[i])
        i=i+1
        print tempRepType

# Create the Asset Types XML Document
#    initialAssetTypes = ["envir"]
#    for tempAssetType in initialAssetTypes:

    xmlAssTypes = "pipeAssetTypes.xml"
    xmlAssTypesPath = pipeXMLConfigPath+xmlAssTypes
    XMLAssTypeRoot = xmlT.Element("pipeAssetTypes")
    file = open(xmlAssTypesPath, 'w')
    xmlT.ElementTree(XMLAssTypeRoot).write(file)
    file.close()



#        pipeAddAssetType(tempAssetType)
#        for tempRepTyp in initialRepTypes:
#            pipeAddAssetTypeRep(tempAssetType,tempRepTyp)

# Create the Data Types XML Document
    initialDataTypes = ["mayaAscii", "mayaBinary", "alembic","gpuCache","bBoxA","bBoxB","bBoxC"]
    initialDataEditor = ["Maya","Maya","Maya","Maya","Maya","Maya", "Maya"]
    initialDataAuthor = ["Maya","Maya","Maya","Maya","Maya","Maya","Maya"]
    initialDataExt = [".ma",".mb",".abc",".abc",".ma",".mb",".abc" ]
    i=0
    for tempDataType in initialDataTypes:
        pipeAddDataType(initialDataTypes[i],initialDataEditor[i],initialDataAuthor[i],initialDataExt[i])
        i=i+1

    if verbosity == 1:
         print '  - New Project "' + pipeShow + '" Initialized\n'


##################################
# Define the Asset/Data Structure#
##################################

def pipeAddAssetType(newAssetType):
# Create the Asset Types XML Document
 if verbosity == 1:
     print "\n--------------------"
     print "PIPE: ADD ASSET TYPE"
     print "--------------------"
     print '  - Add Asset Type: "' + newAssetType+ '"'
 if pipeAssetTypeExists(newAssetType):
     print "  - Asset Type " +newAssetType + " already Exists:  ABORTING"
     return
 tempAssetTypes=[]
 tempRepTypes=[]
 xmlAssTypes = "pipeAssetTypes.xml"
 xmlAssTypesPath = pipeXMLConfigPath+xmlAssTypes
 if os.path.exists(xmlAssTypesPath)==True:
     tempAssetTypes = pipeListAssetTypes()
 tempAssetTypes.append(newAssetType)
 XMLroot = xmlT.Element("pipeAssetTypes")
# Loop through the Types
 for tempCurrentType in tempAssetTypes:
     if tempCurrentType != "*N/A*":
         currentType = xmlT.SubElement(XMLroot,tempCurrentType)
         tempRepTypes = pipeListAssetTypeReps(tempCurrentType)
         for currentRep in tempRepTypes:
             if currentRep != "*N/A*":
                 tempCurrentType = xmlT.SubElement(currentType,currentRep)

# Write out the XML file
 file = open(xmlAssTypesPath, 'w')
 xmlT.ElementTree(XMLroot).write(file)
 file.close()
 xmlDataTypes = "pipeDataTypes.xml"
 xmlAssDataPath = pipeXMLConfigPath+xmlDataTypes
#


def pipeAddAssetTypeRep(type,repType):
 if verbosity == 1:
     print "\n------------------------"
     print "PIPE: ADD ASSET TYPE REP"
     print "------------------------"
     print '  - Add '  + type + ' Representation Type: "' + repType+ '"'
 tempAssetTypes=[]
 tempReps=[]
 tempRep=""
 tempCurrentData=""
 if pipeAssetTypeExists(type)== False:
     print '  - Asset Type "'  + type + '" does not exist -- Aborting'
     return
####
 if pipeAssetTypeRepExists(type, repType)== True:
     print '  - Asset Type Rep "' + repType + '" for "'+ type + '" already exist -- Aborting'
     return
####
 xmlAssTypes = "pipeAssetTypes.xml"
 xmlAssTypesPath = pipeXMLConfigPath+xmlAssTypes
 if os.path.exists(xmlAssTypesPath)!=True:
     print '  - pipeAssetTypes.xml does not exist -- Aborting'
     return
 tempAssetTypes=pipeListAssetTypes()
 XMLroot = xmlT.Element("pipeAssetTypes")
# Loop through the Types
 for tempAssetType in tempAssetTypes:
     tempAssetTypeObj = xmlT.SubElement(XMLroot,tempAssetType)
     tempReps = pipeListAssetTypeReps(tempAssetType)
     if tempReps[0]=='*N/A*':
         tempReps=[]
     for tempRep in tempReps:
         tempRepObj = xmlT.SubElement(tempAssetTypeObj, tempRep)
     if tempAssetType==type:
     	tempRepObj2 = xmlT.SubElement(tempAssetTypeObj, repType)
# Write out the XML file
 file = open(xmlAssTypesPath, 'w')
 xmlT.ElementTree(XMLroot).write(file)
 file.close()

def pipeAddRepType(name,data,subdir,filename, numMetric):
 if verbosity == 1:
     print "\n------------------"
     print "PIPE: ADD REP TYPE"
     print "------------------"
     print '  - Add Representation Type: "' + name+ '"'
 tempRepTypes=[]
 tempCurrentData=""
 xmlRepTypes = "pipeRepTypes.xml"
 xmlRepTypesPath = pipeXMLConfigPath+xmlRepTypes
 if pipeRepExists(name):
     print '  - Representation Type "'+ name + '" Exists'
     return
 XMLroot = xmlT.Element("pipeRepTypes")
# Loop through the Types
 tempRepTypes=pipeListRepTypes()
 for tempExRepTyp in tempRepTypes:
     tempCurrentData = xmlT.SubElement(XMLroot,tempExRepTyp)
# getVars
     tData = pipeGetRepDataType(tempExRepTyp,"Data")
     tSubDir=pipeGetRepDataType(tempExRepTyp,"SubDir")
     tFilename = pipeGetRepDataType(tempExRepTyp,"Filename")
     tNumMetric = pipeGetRepDataType(tempExRepTyp,"NumMetric")
# Make XML
     tempDataObj = xmlT.SubElement(tempCurrentData, tempExRepTyp+"Data")
     tempDataObj.text = tData
     tempSubDirObj = xmlT.SubElement(tempCurrentData, tempExRepTyp+"SubDir")
     tempSubDirObj.text = tSubDir
     tempFilenameObj = xmlT.SubElement(tempCurrentData, tempExRepTyp+"Filename")
     tempFilenameObj.text = tFilename
     tempNumMetricObj = xmlT.SubElement(tempCurrentData, tempExRepTyp+"NumMetric")
     tempNumMetricObj.text = tNumMetric

 tempNewRepObj=xmlT.SubElement(XMLroot, name)
 tempNewDataObj = xmlT.SubElement(tempNewRepObj, name+"Data")
 tempNewDataObj.text = data
 tempNewSubDirObj = xmlT.SubElement(tempNewRepObj, name+"SubDir")
 tempNewSubDirObj.text = subdir
 tempNewFilenameObj = xmlT.SubElement(tempNewRepObj, name+"Filename")
 tempNewFilenameObj.text = filename
 tempNewNumMetricObj = xmlT.SubElement(tempNewRepObj, name+"NumMetric")
 tempNewNumMetricObj.text = numMetric
 print (name,data,subdir,filename, numMetric)
# Write out the XML file
 file = open(xmlRepTypesPath, 'w')
 xmlT.ElementTree(XMLroot).write(file)
 file.flush()
 file.close()


def pipeAddDataType(dataType,dataEditor,dataAuthor,dataExt):
 if verbosity == 0:
     print "\n--------------------------"
     print "PIPE: Register a Data Type"
     print "--------------------------"
     print '  - Register Data Type: "' + dataType+ '"'
 xmlDataTypes = "pipeDataTypes.xml"
 xmlAssDataTypesPath = pipeXMLConfigPath+xmlDataTypes
# Check if Data Type of new name already exists
 tempDataTypes=[]
 if pipeDataTypeExists(dataType):
     print '  - Data Type with name "'+ name + '" Already Registered'
     return
# Create a New XML Doc node with the exsting Data Types
 XMLroot = xmlT.Element("pipeDataTypes")
# Loop Through Existing Data Types
 tempDataTypes = pipeListDataTypes()
 for tempDataType in tempDataTypes:
# get data type info
     tempDataEditor=pipeGetDataTypeInfo(tempDataType,'Editor')
     tempDataAuthor=pipeGetDataTypeInfo(tempDataType,'Author')
     tempDataExtension=pipeGetDataTypeInfo(tempDataType,'Extension')
# add to XML node         
     tempDataTypeObj = xmlT.SubElement(XMLroot,tempDataType)
     tempDataEditorObj = xmlT.SubElement(tempDataTypeObj, tempDataType+"Editor")
     tempDataEditorObj.text = tempDataEditor
     tempDataAuthorObj = xmlT.SubElement(tempDataTypeObj, tempDataType+"Author")
     tempDataAuthorObj.text = tempDataAuthor
     tempDataExtensionObj = xmlT.SubElement(tempDataTypeObj, tempDataType+"Extension")
     tempDataExtensionObj.text = tempDataExtension
#
 newDataTypeObj = xmlT.SubElement(XMLroot,dataType)
 newDataEditorObj = xmlT.SubElement(newDataTypeObj, dataType+"Editor")
 newDataEditorObj.text = dataEditor
 newDataAuthorObj = xmlT.SubElement(newDataTypeObj, dataType+"Author")
 newDataAuthorObj.text = dataAuthor
 newDataExtensionObj = xmlT.SubElement(newDataTypeObj, dataType+"Extension")
 newDataExtensionObj.text = dataExt

# Write out the XML file
 file = open(xmlAssDataTypesPath, 'w')
 xmlT.ElementTree(XMLroot).write(file)
 file.close()


#########################
# Add Asset Placeholder #
#########################

def pipeAddAsset(newAssetName,newAssetType,newNotes):
# Declare Variables
    tempDecs = 5
    newAssetID = ""
    tempLen = -1
# Begin New Asset Placeholder Process
    if verbosity == 1:
        print "\n--------------------------------"
        print " PIPE: Create Asset Placeholder"
        print "--------------------------------"
        print '  - Get Asset List'
        print '  - Asset Library path : ' + pipeAssetLibPath+"xml/"+"pipeAssetLibrary.xml"


# Check if the Asset Type is Valid
    tempAssetTypes = pipeListAssetTypes()
    tempAssetTypeCheck = 0
    for tempAssetType in tempAssetTypes:
	    if tempAssetType==newAssetType:
	        tempAssetTypeCheck = 1
    if tempAssetTypeCheck == 0:
        print '  - Asset Type "' + newAssetType + '" is not a valid Asset Type'
	print '  - Aborting Asset Creation: Try again'
	return
# Get current Asset list
    listAssets = []
    listAssets= pipeListAssets()
    if listAssets[0] == "*N/A*":
        tempLen=0
        listAssets = []
        print listAssets
        print tempLen
    else:
        tempLen = len(listAssets)
# Check if an asset with the name of the new asset already exists
    if pipeAssetExists(newAssetName):
                print  '  - Create Asset Fail:  PipeAsset named"' + newAssetName + '" already exists!!!'
                return
# Check if Library is locked
    if os.path.exists(pipeAssetLibPath+"xml/"+"pipeAssetLibrary.xml.lock")==True:
        print '  - Asset Library Currently Locked'
	print '  - Aborting Asset Creation: Try again'
	return
# Try to Lock the Asset Lib
    libXmlpath = pipeAssetLibPath+"xml/"+"pipeAssetLibrary.xml"
    try:
        file = open(libXmlpath+".lock",'w')
        file.write("X")
        file.close()
        shutil.copy(libXmlpath,libXmlpath+".back")
        if verbosity == 1:
            print "  - Asset Library Locked"
    except:
        print '  - Cannot Lock Asset Library Currently'
        print '  - Aborting Asset Creation . . .'
        return
# Determine New ID Number
###    newAssetID = str(tempLen)
###    while len(newAssetID)<6:
###        newAssetID="0" + newAssetID
###    print "  - New Asset ID = " + newAssetID
# Update Asset Library XML    
    assetLibRoot = xmlT.Element('pipeAssets')
    print listAssets
    if listAssets!= "*N/A*":
        for asset in listAssets:
 ###           id = pipeGetAssetInfoName(asset,"Id")
            assetNameObj = xmlT.SubElement(assetLibRoot,asset)
            tempNewAssetIDObj = xmlT.SubElement(assetNameObj,asset+"Name")
            tempNewAssetIDObj.text = asset
    assetNameObj = xmlT.SubElement(assetLibRoot,newAssetName)
    tempNewAssetIDObj = xmlT.SubElement(assetNameObj,newAssetName+"Name")
    tempNewAssetIDObj.text = newAssetName
    file = open(libXmlpath + ".new", 'w')
    xmlT.ElementTree(assetLibRoot).write(file)
    file.close()
    shutil.copy(libXmlpath + ".new",pipeAssetLibPath+"xml/"+"pipeAssetLibrary.xml")
    os.remove(libXmlpath+".new")

# Create Asset Based XML File
    xmlPath = pipeAssetLibPath + "assets/" + newAssetName + "/xml/" + newAssetName + ".asset.xml"
    assetAssetLibRoot = xmlT.Element('pipeAsset')
    assetNewNameObj = xmlT.SubElement(assetAssetLibRoot,newAssetName)
    assetNewTypeObj = xmlT.SubElement(assetNewNameObj,newAssetName+"Type")
    assetNewTypeObj.text = newAssetType
    assetNewNoteObj = xmlT.SubElement(assetNewNameObj,newAssetName+"Note")
    assetNewNoteObj.text = newNotes
    assetNewCreatorObj = xmlT.SubElement(assetNewNameObj,newAssetName+"Creator")
    assetNewCreatorObj.text =  os.environ['USER']
    assetNewVarsObj = xmlT.SubElement(assetNewNameObj,newAssetName+"Variations")

# Make directories for Asset
    if os.path.exists(pipeAssetLibPath+"assets/"+ newAssetName + "/xml/")!=True:
        os.makedirs(pipeAssetLibPath+"assets/"+ newAssetName + "/xml/", 0777)
    if os.path.exists(pipeAssetLibPath+"assets/"+ newAssetName + "/data/")!=True:
        os.makedirs(pipeAssetLibPath+"assets/"+ newAssetName + "/data/", 0777)
    if os.path.exists(pipeAssetLibPath+"assets/"+ newAssetName + "/data/definition/")!=True:
        os.makedirs(pipeAssetLibPath+"assets/"+ newAssetName + "/data/definition/", 0777)
    if os.path.exists(pipeAssetLibPath+"assets/"+ newAssetName + "/data/variations/")!=True:
        os.makedirs(pipeAssetLibPath+"assets/"+ newAssetName + "/data/variations/", 0777)
    if os.path.exists(pipeAssetLibPath+"assets/"+ newAssetName + "/data/textures/")!=True:
        os.makedirs(pipeAssetLibPath+"assets/"+ newAssetName + "/data/textures/", 0777)
# Write Asset XML File
    file = open(xmlPath, 'w')
    xmlT.ElementTree(assetAssetLibRoot).write(file)
    file.close()

    if verbosity == 1:
        print "  - Asset Library Updated"
# Make directories for variations and representations
    tempVars = pipeListAssetVars(newAssetName)
    if tempVars[0] != "*N/A*":
         for tempVar in tempVars:
            os.makedirs(pipeAssetLibPath+"assets/"+ newAssetName + "/data/variations/" + tempVar + "/", 0777)
            tempReps = pipeListAssetVarReps(newAssetType, tempVar)
            for tempRep in tempReps:
                os.makedirs(pipeAssetLibPath+"assets/"+ newAssetName + "/data/variations/" + tempVar + "/" + tempRep, 0777)
# Remove the Lock
    os.remove(libXmlpath+".lock")
    if verbosity == 1:
        print "  - Asset Library Lock Removed"
    print '  - Asset Placeholder for "' + newAssetName + '" had been completed\n'


#############################
# Edit An Asset Placeholder #
#############################

# Add Variations / pipeEditAsset(AssetName,[variationName],"addVar")
# Add Rep to a Variation / pipeEditAsset(AssetName,[variationName,representation],"addRep")
def pipeEditAsset(assetName,input,tempCommand):
# Begin Edit Asset Placeholder Process
    if verbosity == 1:
        print "\n---------------------------------"
        print " PIPE: Edit an  Asset Placeholder"
        print "---------------------------------"
        print '  - Get Asset List'

# Declare Variables
    pipeAssetLibXMLPath = pipeAssetLibPath+"xml/"+"pipeAssetLibrary.xml"
    tempDecs = 5
    newAssetID = ""
    tempTest = ""
    assetVariations = []
    if verbosity == 1:
        print '  - Asset Library path : ' + pipeAssetLibXMLPath

# Get a list of all of the current Representation types for the current Show
    tempAllRepTypes = pipeListRepTypes()

# Get a list of all the assets
    assets = pipeListAssets()

# Check if an asset with the name of the new asset already exists
    if pipeAssetExists(assetName) ==False:
            print  '  - Edit Placeholder Failed:  PipeAsset named "' + assetName + '" does not exist!!!'
            return

# Check if an asset variation with that name already exists
    if tempCommand=="addVar" and pipeAssetVariationExists(assetName,input[0])==True:
            print  '  - Edit Placeholder Failed:  PipeAsset Variation named "' + input[0] + '" already exists!!!'
            return

# Check if an asset variation rep exists with that name
    if tempCommand=="addRep" and pipeAssetVarRepExists(assetName,input[0],input[1])==True:
            print  '  - Edit Placeholder Failed:  PipeAsset Variation Representation named "' + input[1] + '" already exists!!!'
            return

# Loop through existing Assets
# Get Info
##    tempID = pipeGetAssetInfoName(assetName,"Id")
    tempType = pipeGetAssetInfoName(assetName,"Type")
    tempNote = pipeGetAssetInfoName(assetName,"Note")
    tempCreator = pipeGetAssetInfoName(assetName,"Creator")
    tempVariations = pipeListAssetVars(assetName)
    assetXMLPath = pipeBasePath + pipeShow + "/lib/assets/"  + assetName + "/xml/" + assetName + ".asset.xml"

# Create New Virtual Doc
    xmlRoot = xmlT.Element('pipeAssets')

# Get Variations
#       Get variations Representations
    assetVariations = pipeListAssetVars(assetName)
    tempName = assetName
# Add Infor and Asset to the New Virtual XML Doc
    tempNewAssetNameObj = xmlT.SubElement(xmlRoot,tempName)
    tempNewAssetTypeObj = xmlT.SubElement(tempNewAssetNameObj,tempName+"Type")
    tempNewAssetTypeObj.text = tempType
    tempNewAssetNotesObj = xmlT.SubElement(tempNewAssetNameObj,tempName+"Note")
    tempNewAssetNotesObj.text = tempNote
    tempNewAssetNotesObj = xmlT.SubElement(tempNewAssetNameObj,tempName+"Creator")
    tempNewAssetNotesObj.text = tempCreator
    tempNewAssetVarsObj = xmlT.SubElement(tempNewAssetNameObj,tempName+"Variations")
    tempVariations = pipeListAssetVars(assetName)
    if tempVariations[0]!="*N/A*":
            for tempVar in tempVariations:
                tempNewAssetVarObj = xmlT.SubElement(tempNewAssetVarsObj,tempVar)
                tempVarReps = pipeListAssetVarReps(tempName,tempVar)
                for tempVarRep in tempVarReps:
                    tempNewVarRepObj = xmlT.SubElement(tempNewAssetVarObj,tempName+"Var" + tempVar+"Reps")
                    tempNewVarRepObj.attrib['type']= tempVarRep
                if tempName==assetName and tempCommand=="addRep" and tempVar == input[0]:
                    tempNewVarRepObj = xmlT.SubElement(tempNewAssetVarObj,assetName+"Var" + tempVar+"Reps")
                    tempNewVarRepObj.attrib['type']= input[1]
                    tempTypeTester="NoMatch"
                    for tempRepType in tempAllRepTypes:
                        print tempRepType + "\n"
                        if tempRepType == input[1]:
                            tempTypeTester="Match"
                    if os.path.exists(pipeAssetLibPath+"assets/"+ tempName + "/data/variations/" + input[0] +"/" + input[1] + "/")!=True:
                        os.makedirs(pipeAssetLibPath+"assets/"+ tempName + "/data/variations/" + input[0] +"/" + input[1] + "/", 0777)
                    if tempTypeTester!="Match":
                        print '  - **Warning**: Representation "' + input[1] + '" is not registered'
# Add Variation
    if tempCommand=="addVar" and tempName==assetName:
            tempNewVarName = input[0]
            tempNewAssetVarObj = xmlT.SubElement(tempNewAssetVarsObj,tempNewVarName)
            if os.path.exists(pipeAssetLibPath+"assets/"+ assetName + "/data/variations/"+ tempNewVarName)!=True:
                os.makedirs(pipeAssetLibPath+"assets/"+ assetName + "/data/variations/"+ tempNewVarName, 0777)
                os.makedirs(pipeAssetLibPath+"assets/"+ assetName + "/data/definition/"+ tempNewVarName, 0777)
            tempAssetTypes = pipeGetAssetInfoName(assetName,"Type")
            tempDefVars = pipeListAssetTypeReps(tempAssetTypes)
            for tempInput in tempDefVars:
#                print (pipeAssetLibPath+"assets/"+ tempID + "/data/variations/" + tempNewVarName +"/" + tempInput + "/")
                if tempNewVarName != tempInput:
                    tempTypeTester="NoMatch"
                    for tempRepType in tempAllRepTypes:
                        if tempRepType == tempInput:
                            tempTypeTester="Match"
                    tempNewVarRepObj = xmlT.SubElement(tempNewAssetVarObj,tempName +"Var" + tempNewVarName+"Reps")
                    tempNewVarRepObj.attrib['type']= tempInput
                    tempNewSubdir = pipeGetRepDataType(tempInput,"SubDir")
                    if os.path.exists(pipeAssetLibPath+"assets/"+ tempName + "/data/variations/" + tempNewVarName +"/" + tempInput + "/" + tempNewSubdir)!=True:
                        os.makedirs(pipeAssetLibPath+"assets/"+ tempName + "/data/variations/" + tempNewVarName +"/" + tempInput + "/" + tempNewSubdir, 0777)
                    if tempTypeTester!="Match":
                        print '  - Warning: Representation "' + tempInput + '" is not registered'
# Write the New Asset Library File
    file = open(assetXMLPath, 'w')
    xmlT.ElementTree(xmlRoot).write(file)
    file.close()
    if verbosity == 1:
        print '  - Asset Placeholder for "' + tempName + '" has been edited\n'



#############################
# Query Tools For Pipe XMLs #
#############################

# Test If Asset Type Exist
def pipeAssetTypeExists(type):
 if verbosity == 1:
     print "\n------------------------"
     print "PIPE: ASSET TYPE EXISTS?"
     print "------------------------"
     print '  - Does '  + type + '  Type Exist?'
 tempAssetTypes=[]
 xmlAssTypes = "pipeAssetTypes.xml"
 xmlAssTypesPath = pipeXMLConfigPath+xmlAssTypes
 if os.path.exists(xmlAssTypesPath)==True:
     tempAssetTypes=pipeListAssetTypes()
     for tempAssetType in tempAssetTypes:
         if tempAssetType == type:
             return 1
     return 0

# Test If Data Type Exist
def pipeDataTypeExists(type):
 if verbosity == 1:
     print "\n-----------------------"
     print "PIPE: DATA TYPE EXISTS?"
     print "-----------------------"
     print '  - Does Data Type'  + type + ' Exist?'
 tempAssetTypes=[]
 xmlDataTypes = "pipeDataTypes.xml"
 xmlAssTypesPath = pipeXMLConfigPath+xmlDataTypes
 if os.path.exists(xmlAssTypesPath)==True:
     tempDataTypes=pipeListDataTypes()
     for tempDataType in tempDataTypes:
         if tempDataTypes == type:
             return 1
     return 0


# Test If An Asset Exists
def pipeAssetExists(name):
 if verbosity == 1:
     print "\n-------------------"
     print "PIPE: ASSET EXISTS?"
     print "-------------------"
     print '  - Does '  + name + ' Exist?'
 tempAssets=[]
 tempXmlPath=pipeAssetLibPath+"xml/"+"pipeAssetLibrary.xml"
 if os.path.exists(tempXmlPath)==True:
     tempAssets=pipeListAssets()
     for tempAsset in tempAssets:
         if tempAsset == name:
             return 1
     return 0


# Test If An Asset Variation Exists
def pipeAssetVariationExists(asset,variation):
 if verbosity == 1:
     print "\n-----------------------------"
     print "PIPE: ASSET VARIATION EXISTS?"
     print "-----------------------------"
     print '  - Does '  + variation + '  Variation Exist For Asset ' + asset + '?'
 tempVars=[]
 tempXmlPath=pipeAssetLibPath+"xml/"+"pipeAssetLibrary.xml"
 if os.path.exists(tempXmlPath)==True:
     temps=pipeListAssetVars(asset)
     for temp in temps:
         if temp == variation:
             return 1
     return 0
 else:
     return 0


# Test If An Asset Variation Representation Exist
def pipeAssetVarRepExists(assetName,varType, representation):
 if verbosity == 1:
     print "\n-------------------------------------------"
     print "PIPE: ASSET VARIATION REPRESENTAION EXISTS?"
     print "-------------------------------------------"
     print '  - Does representation ' + representation + ' for '  + varType + '   exist for asset ' + assetName + '?'
 tempVars=[]
 tempXmlPath=pipeAssetLibPath+"xml/"+"pipeAssetLibrary.xml"
 if os.path.exists(tempXmlPath)==True:
     temps=pipeListAssetVarReps(assetName,varType)
     for temp in temps:
         if temp == representation:
             return 1
     return 0
 else:
     return 0

# Test if a Representation Type Exists
def pipeRepExists(representation):
 if verbosity == 1:
     print "\n---------------------------------"
     print "PIPE: REPRESENTAION TYPE EXISTS?"
     print "--------------------------------"
     print '  - Does representation type' + representation + ' exist?'
 tempVars=[]
 tempXmlPath = pipeXMLConfigPath + "pipeDataTypes.xml"
 if os.path.exists(tempXmlPath)==True:
     temps=pipeListRepTypes()
     for temp in temps:
         if temp == representation:
             return 1
     return 0
 else:
     return 0

# Test if an Asset Type Representation Type Exists
def pipeAssetTypeRepExists(type, representation):
 if verbosity == 1:
     print "\n---------------------------------"
     print "PIPE: ASSET TYPE REPRESENTAION TYPE EXISTS?"
     print "--------------------------------"
     print '  - Does representation type' + representation + ' exist for asset type ' + type +'?'
 tempVars=[]
 xmlAssTypes = "pipeAssetTypes.xml"
 tempXmlPath = pipeXMLConfigPath+xmlAssTypes
 if os.path.exists(tempXmlPath)==True:
     temps=pipeListAssetTypeReps(type)
     for temp in temps:
         if temp == representation:
             return 1
     return 0
 else:
     return 0

# Get the "show" name
def pipeGetPipeShow():
 global pipeShow
 temp=pipeShow
 return temp

# Get the pipe path
def pipeGetPipePath():
 temp=pipeBasePath
 return temp

# Get all the Asset Types
def pipeListAssetTypes():
    if verbosity == 1:
        print "\n-----------------------"
        print " PIPE: Get Asset Types "
        print "-----------------------"
        print '  - Get Asset Types'
    tempXmlPath = pipeXMLConfigPath + "pipeAssetTypes.xml"
    tree = xmlT.ElementTree(file=tempXmlPath)
    assetTypesObj = tree.getroot()
    assetTypes = []
    for temp in assetTypesObj:
        assetTypes.append(temp.tag)
    if len(assetTypes)==0:
        assetTypes.append('*N/A*')
    for x in assetTypes:
        if verbosity == 1:
            print "     " + x
    assetTypes.sort()
    return assetTypes

# Get Asset Info by Name
def pipeGetAssetInfoName(tempName,info):
    if verbosity == 1:
        print "\n-----------------------------"
        print " PIPE: Get Asset Info By Name"
        print "-----------------------------"
        print '  - Get Asset ' + info + ' for "' +tempName +'"'
    tempValues = []
    tempXmlPath=pipeAssetLibPath+"xml/"+"pipeAssetLibrary.xml"


    xmldoc = minidom.parse(tempXmlPath)
    data = xmldoc.getElementsByTagName(tempName+ "Name")
    if info == "Id":
        data = xmldoc.getElementsByTagName(tempName+ "Id")
    x= " ".join(t.nodeValue for t in data[0].childNodes if t.nodeType == t.TEXT_NODE)
    tempID=x
    if info != "Id":
	xmldoc2 = minidom.parse(pipeAssetLibPath + "assets/" + tempID + "/xml/"+tempName + ".asset.xml")
	data = xmldoc2.getElementsByTagName(tempName+ info)
	x= " ".join(t.nodeValue for t in data[0].childNodes if t.nodeType == t.TEXT_NODE)
    if len(x)==0:
        x="*N/A*"
    if verbosity == 1:
        print "     " +  x + "\n"
    return x

# List the Asset Type Representations
def pipeListAssetTypeReps(type):
    if verbosity == 1:
        print "\n----------------------------"
        print " PIPE: Get Asset Types Reps "
        print "----------------------------"
        print '  - Get Asset Type Reps for "' + type + '"'
    tempXmlPath = pipeXMLConfigPath + "pipeAssetTypes.xml"
    tree = xmlT.ElementTree(file=tempXmlPath)
    assetTypesObj = tree.getroot()
    tempValues = []
    for temp in assetTypesObj:
        if type == temp.tag:
                assetChildren = temp.getchildren()
                for temp2 in assetChildren:
                    tempValues.append(temp2.tag)
    if len(tempValues)==0:
        tempValues.append('*N/A*')
    if verbosity == 1:
        for x in tempValues:
            print "     " + x +"\n"
    return tempValues

# List all assets in the Show
def pipeListAssets():
    if verbosity == 1:
        print "\n------------------"
        print " PIPE: Get Assets "
        print "------------------"
        print '  - Get Assets in show "' +  pipeShow + '":'

    tempXmlPath=pipeAssetLibPath+"xml/"+"pipeAssetLibrary.xml"
    tempAssets = []
    tree = xmlT.ElementTree(file=tempXmlPath)
    assetsObj = tree.getroot()
    for temp in assetsObj:
        tempAssets.append(temp.tag)
    if len(tempAssets)==0:
        tempAssets.append('*N/A*')
    if verbosity == 1:
        for x in tempAssets:
            print "     " + x +"\n"
    return tempAssets

# Get variations of an asset
def pipeListAssetVars(assetName):
    if verbosity == 1:
        print "\n----------------------------"
        print " PIPE: Get Asset Variations "
        print "----------------------------"
        print '  - Get Variations for Asset "' +  assetName + '"'

    tempXmlPath =  (pipeAssetLibPath + "assets/" + assetName + "/xml/"+assetName + ".asset.xml")
    tempValues = []
    tree = xmlT.ElementTree(file=tempXmlPath)
    assetObj = tree.getroot()
    for temp in assetObj:
        if temp.tag == assetName:
            assetChildren = temp.getchildren()
            for temp2 in assetChildren:
                if temp2.tag == assetName+"Variations":
                    assetVariationsChildren = temp2.getchildren()
                    for temp3 in assetVariationsChildren:
                        tempValues.append(temp3.tag)
    if len(tempValues)==0:
        tempValues.append('*N/A*')
    if verbosity == 1:
        for x in tempValues:
            print "     " + x +"\n"
    return tempValues

# Get the representations of a variation of an asset
def pipeListAssetVarReps(assetName,varType):
    if verbosity == 1:
        print "\n--------------------------------------------"
        print " PIPE: Get Asset Variation Representations "
        print "--------------------------------------------"
        print '  - Get Representations for Variation "' +varType + '" for Asset Name "' + assetName +'":'

    tempXmlPath =  (pipeAssetLibPath + "assets/" + assetName + "/xml/"+assetName + ".asset.xml")

    tempValues = []
    xmldoc = minidom.parse(tempXmlPath)
    itemlist = xmldoc.getElementsByTagName(assetName +"Var"+ varType + "Reps")
    for s in itemlist:
        x=s.attributes['type'].value
        tempValues.append(str(x))
    if len(tempValues)==0:
        tempValues.append("*N/A*")
    for x in tempValues:
        if verbosity == 1:
            print "     " + x
    tempValues.sort()
    if verbosity == 1:
        print "     " + x +"\n"
    return tempValues

# Get all Data Types
def pipeListDataTypes():
    if verbosity == 1:
        print "\n-----------------------"
        print " PIPE: Get Data Types "
        print "-----------------------"
        print '  - Get Data Types:'
    tempXmlPath = pipeXMLConfigPath + "pipeDataTypes.xml"
    if os.path.exists(tempXmlPath)!=True:
        dataTypes=[]
        return dataTypes
    tree = xmlT.ElementTree(file=tempXmlPath)
    dataTypesObj = tree.getroot()
    dataTypes = []
    for temp in dataTypesObj:
        dataTypes.append(temp.tag)
    if len(dataTypes)==0:
        dataTypes.append('*N/A*')
    for temp in dataTypes:
        if verbosity == 1:
                print "     " + temp
    dataTypes.sort()
    if verbosity == 1:
        print "\n"
    return dataTypes

# get Data Type Info
def pipeGetDataTypeInfo(dataType,Tag):
    if verbosity == 1:
        print "\n--------------------------"
        print " PIPE: Get Data Type Info "
        print "--------------------------"
        print '  - Get Editor Application for Data Type "' +dataType + Tag + '"'
    tempValues = []
    tempXmlPath = pipeXMLConfigPath+"pipeDataTypes.xml"
    xmldoc = minidom.parse(tempXmlPath)
    data = xmldoc.getElementsByTagName(dataType+ Tag)
    x= " ".join(t.nodeValue for t in data[0].childNodes if t.nodeType == t.TEXT_NODE)
    if len(x)==0:
        x="*N/A*"
    if verbosity == 1:
        print "     " + x
        print "\n"
    return x

# Get all Rep Types
def pipeListRepTypes():
    if verbosity == 1:
        print "\n----------------------"
        print " PIPE: Get Data Types"
        print "----------------------"
        print '  - Get Rep Types:'
    tempXmlPath = pipeXMLConfigPath + "pipeRepTypes.xml"
    if os.path.exists(tempXmlPath)!=True:
        repTypes=[]
        return repTypes
    tree = xmlT.ElementTree(file=tempXmlPath)
    repTypesObj = tree.getroot()
    repTypes = []
    for temp in repTypesObj:
        repTypes.append(temp.tag)
    if len(repTypes)==0:
        repTypes.append('*N/A*')
    for temp in repTypes:
        if verbosity == 1:
                print "     " + temp
    repTypes.sort()
    if verbosity == 1:
         print "\n"
    return repTypes

# get Rep Info
def pipeGetRepDataType(repType, Tag):
    if verbosity == 1:
        print "\n-------------------------"
        print " PIPE: Get Rep Data Type "
        print "-------------------------"
        print '  - Get Data Type for Representation "' +repType +Tag + '"'
    tempValues = []
    tempXmlPath = pipeXMLConfigPath+"pipeRepTypes.xml"
    xmldoc = minidom.parse(tempXmlPath)
    data = xmldoc.getElementsByTagName(repType+ Tag)
    x= " ".join(t.nodeValue for t in data[0].childNodes if t.nodeType == t.TEXT_NODE)
    if len(x)==0:
        x="*N/A*"
    if verbosity == 1:
        print "     " + x + "\n"
    return x
    
#################################
# Debugging Tools For Pipe XMLs #
#################################

# Reinitiate the Asset Library  - Destructive
def pipeCreateNewLib():
    xmlAssLib = "pipeAssetLibrary.xml"
    if os.path.exists(pipeAssetLibPath+"assets/")==True:
        shutil.rmtree(pipeAssetLibPath+"assets/")
    if os.path.exists(pipeAssetLibPath+"xml/")==True:
        shutil.rmtree(pipeAssetLibPath+"xml/")
    os.makedirs(pipeAssetLibPath+"xml/")
    xmlAssLibPath = pipeAssetLibPath+"xml/"+xmlAssLib
    XMLroot = xmlT.Element("pipeAssets")
    file = open(xmlAssLibPath, 'w')
    xmlT.ElementTree(XMLroot).write(file)
    file.close()
