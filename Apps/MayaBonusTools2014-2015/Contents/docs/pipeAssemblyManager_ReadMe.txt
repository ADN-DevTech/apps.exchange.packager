pipeAssemblyManager.py, pipe.py


------------------------------
What is Pipe Assembly Manager
------------------------------
Pipe Assembly Manager is a UI-based Scene Assembly Authoring system. It greatly simplifies the process of creating Scene Assembly definitions and representation, while providing a simple UI to manage and bring in Assembly Representations.

Scene Assembly is an inherently complex feature in Maya. Note that this tool is not a substitute for learning how to use Scene Assembly. Read the Maya documentation on Scene Assembly to get an understanding for how the feature works to get the most out of this tool.

The UI is built on top of a simple XML-based Asset database that is described in more detail later.  Advanced users can adapt the Asset Database to suit their own needs using the source code that is included.



-------------------------------
 Quick Start Instructions 
-------------------------------
Follow the on-screen instructions to:

   a. Browse to a directory for the Pipe repository
   b. Enter a "Show" name

The repository resides on a local drive or it can exist on a network drive. On a network, multiple users can work collaboratively using the same repository and assets.

During the installation process, a directory called "pipe" is created in your [HOME] directory.  Inside this new directory a text file called "pipe.cfg" is created, which  contains the location of the Repository and the current Show.  If you want to "reinstall" Pipe Assembly Manager, delete the [HOME]/pipe directory.


------------------------------
 Basic Trouble Shooting Guide
------------------------------
If you suddenly find that this script is not working properly, here are somethings you might want to check.

Does not work at all
  - Ensure the pipe.py script and the pipeAssemblyManager.py file are both in your scripts directory

Problems with Pipe.cfg
  - Ensure that file [HOME]/pipe/pipe.cfg has two lines of text
  - The first line should the path to the Pipe repository
  - The second line is the current Pipe show
  
Unable to save Assets/Library Locked message
  - If you are getting a message in the script editor that the Library is locked, you will need to delete the lock file
  - in the repository directory pipe/[show]/lib/xml there may be a file with .lock extension.  This can be deleted.

Unable to create representations/assemblify/etc
  - Ensure that you have the Assembly Reference node selected, and not the assembly members

Linux is not supported
  - This may change in the future
  - If someone fixes the Linux issue, please send let us know.


----------------------
 Basic Data Structure
----------------------
  Pipe Repository
   Show
     Asset
      Assembly Definition
        Representation Files
     Asset
      Assembly Definition
        Representation Files


------------------------------
 Basic UI Operation Checklist
------------------------------
To go through the general steps and create Assemblies with the default settings of Pipe Assembly Manager, do the following:

   1. Create an Asset
     - Click "New".
     - Enter an asset name, choose a type and add a note.
     - Click the "Create Asset" button.
     - The new asset is added to the Assembly Manager list.

   2. Create Representations
     - Select the asset in the Assembly Manger UI.
     - Load or create a model.
     - Make sure it is a single hierarchy (grouped, etc).
     - Select the top node of the hierarchy.
     - Click the "Reps" button.
     - Click the "Save Selected Representations" button.
     - The representation files for the specific asset are created.
   
   2.5 To Overwrite a Single Representation File (eg Character Rig) .
     - Load or create the Rigged Character in Maya.
     - From the Options menu in the Pipe Assembly Manager, select Options>> Save Data Files.
     - Select the asset in the Assembly Manger UI.
     - From the Right Mouse Button menu, select representation you want to overwrite.
     - The individual representation file is overwritten

   3. Build Assembly Definition
     - Select the asset in the Assembly Manger UI.
     - Click "Build".
     - An Assembly Definition is created using Asset's representations.

   4. Create Assembly References
     - Select one or more assets in the Assembly Manger UI.
     - Click "Create Assembly Reference".
     - An Assembly Reference of the asset is created if a Definition of it exists.
 
   5. Assemblify Hierarchical Assemblies
     - Select more than one top-level assembly referenced asset in Maya.
     - Click "Assemb".
     - Enter a new asset name for the "Assemblified" new asset.
     - Click "Ok".
     - The selected assemblies are replaced by a hierarchical assembly.
   


------------------------
 1. Creating an Asset
------------------------
An Asset is technically a placeholder for data files. While it is what representations and assembly definitions refer to, an asset is actually a holding pen for Data.

To Create an asset, click "NEW" in the UI or use the Pipe >Create Asset menu item.

This will present a UI where you can:

   - Enter a name for your asset.
      Two assets cannot have the same name, so trying to enter an existing asset name will fail.
      Illegal characters are automatically converted to acceptable ones (eg, Empty spaces will become "_").
   - Choose an Asset Type for your asset:
      There are 4 standard asset types: char, envir, hier, prop.
      Different asset types have different representation profiles.
      Advanced users can add new asset types to a show with the "TYPES" button.
   - Provide a description about the asset:
      This is available when the asset is selected in the Pipe Assembly Manager. You can use to provide any information about the asset you think will be helpful.

After you click "CREATE ASSET", the new asset is listed in the Pipe Assembly Manager UI.  As noted above, the asset is devoid of Scene Assembly data or representations.  You can see if any representations exist for an asset by using the right mouse button menu of an Asset.  Any available representation data files are listed.

-----------------------------
 2. Create Representations
-----------------------------
Representations need to be created in order to create a viable Assembly Definition. You can have the Pipe Assembly Manager automatically derive a set of representations base on a model, or you can save a representation as is.

To Save/Create Representations of an Asset, click "REPS" or use the TOOLS > Save Representation menu.

The Save Representations UI has 3 primary columns:

   - Representation Check Boxes:
      This column lists the potential representations of your current asset, and lets you select which representations you want to derive.
   - Preparation Step Option Menus:
      This defines the "Prep Step" of the scene data prior to be written to disk.
   - Save Action Option Menus:
      This defines how the data will be externalized as a representation data file.
   
There are also 3 Options check boxes that are self-explanatory after you become familiar with the Save Representation UI.

The Maya data you want to write out as a representation(s) must be a single DAG hierarchy in Maya (e.g., under a single group node) and it must be selected.

All Reps
 The simplest way to create representations is to start with a model that all the representations will be derived from.  Make sure it is grouped under a single node and select it. Then bring up the Save Representations UI, and then click Save Selected Representations.  All the representations of that Asset will then have a representation data file saved.

Single Rep
 Some representations cannot be derived from a polygoin model, such an animateable character rig representation from a simple polygon model. For these types of representations you need to create/overwrite a single representation file. There are two ways to accomplish this:

   I - Use the Save Representations UI.
    1. Load or create a character rig in Maya.
    2. Click Reps.
    3. Uncheck all of the representations you do not want to save.
    4. Click Save Selected Representations.
  
  II - Overwrite an existing representation file
    1. Load/Create the Maya Scene you want to use a representation data file
    2. From the Options menu of the Pipe Assembly Manager, select Options >Save Data File
    3. In the Asset List select the desired asset
    4. Press the Right Mouse button
    5. Choose the Variation you wish to overwrite
    6. Click "OK" to confirm Representation overwrite

It is important to note that when a representation is saved, the associated textures will be copied and repathed so they are within the Show data structure.  This way, you should be able to move a show to a different disk location and still have it work when you adjust the location of the repository in the HOME]/pipe/pipe.cfg file.


--------------------------------
 3. Build Assembly Definition
--------------------------------
After representation files have been created, it is possible to Build an Assembly Definition.  This process creates an Assembly Definition in Maya, assigns the existing representation for it, and saves the assembly definition to disk.  After an Assembly Definition has been "built", you can create an Assembly Reference of an asset.

To build an assembly definition, select an Asset in the Pipe Assembly Manager UI and click "Build".

After an Assembly Definition has been built you do not need to rebuild it if you overwrite existing representation files.  Assembly Definitions must be rebuilt if you add a new representation type to an asset, or create a new representation file to an asset that has an existing Assembly Definition.


--------------------------------
 4. Create Assembly References
--------------------------------
After an Assembly Definition has been built for an Asset, it is possible to then use the Pipe Assembly Manager to bring in Assembly References of it. Users can either double click on an asset in the main UI list, or select one or more assets in the UI and then press the "Create Assembly Reference" button.


-----------------------------------------
 5. Assemblify Hierarchical Assemblies
-----------------------------------------
It is possible to create nested hierarchical assemblies automatically using the Assemblify tool.  This enables an organic workflow where you bring in a series of assets as world level assembly references, and then create a single hierarchical assembly from them.  The only representations types that are created by the Assemblify tool are the "geo", "bBox" and "gpu" representations.

To Assemblify, in Maya, select two or more Top Level scene assembly references, then click "Assemb" button.  You are prompted to provide a name for the new Hierarchical asset.  Enter a name and click "OK."  Maya processes your request and replaces the selected assembly references with an assembly reference of a newly created asset.


------------------------
 Advanced Use: Config
------------------------
The Config tool allows you to add show-defined representations to an existing asset.  For example, if a representation type is available  and it has not yet been associated to an asset, you can associate it to that asset here.  This does not create any representations for your asset, but allows for representation files for that representation type to be creatable.

Note that once you add support for a representation for an asset you cannot remove support for that asset.  This is specifically to prevent data loss.

To Config an asset, select the asset in the Main Pipe Assembly Manager UI and click Config.

A Small window appears.  Representations that have been associated to the asset are listed in bold, while unassociated representations have checkboxes.  To associate a representation with an asset, activate the checkbox next to the representation and click "Add Representations".


------------------------
 Advanced Use: Types
------------------------
The Types tool allows you to define new Asset Types or Representation Types for the show.  New representation types appear in the View menu, and can be assigned to newly created assets.

To add a new Asset type, select "Asset Type” in the "Add Pipe Types" UI.  Enter a new name for the Asset Type and activate the representation types you want to be associated to the Asset Type when a new asset of this type is created.  Click Add New Asset Type" and this asset type is added to the show.

To add a new Representation Type to the show, select "Representation Type" in the "Add Pipe Types" UI.  Enter a new Representation name and choose the data type for the representation.  You can add a value to the "Metric" field. Note that this information is not used by the Asset Pipe Manage and is available to advanced users if they wish to provide their own support for it.
wn support for it.



---------------------
---------------------
 Pipe Documentation
---------------------
---------------------


---------------
 What is Pipe?
---------------
Pipe is an XML-based asset database that is used by the Pipe Assembly Manager to determine where to save files, the naming convention of those files and the data type of those files.  As such, Pipe is also used to determine where files are loaded from.  While Pipe is used by the Pipe Asset Manager it can also be used independantly.  Since it is XML driven you can potentially integrate it into your own data structure and workflows.

Pipe is a pythyon script that creates, edits and accesses XML files through the use of python procedures that query and write XML data..  It is actually Maya independant, and can easily be customized to coordinate unique and independant data types.  The initial comments in the pipe.py file explain how to use most of the pipe "commands."


----------------------
 Pipe Asset Structure
----------------------
  - Assets are holders of data.  
  - An asset must have at least one Variation.
  - Representations are associated to Asset Variations
  - Different Variations can have completely different Representation associations.

In the directory pipe/[show]/lib/xml there is an xml file tracking the assets in the repository (see Configuring Pipe, below).  This is a list of all the assets in the Show, and their associated Asset IDs.  There is also an individual Asset xml file for each asset that has information about the asset.  

Note: While this Asset XML definition file is simple, this is intentional.  There is nothing stopping you from adding your own XML tags to incorporate it into your own pipeline.


------------------
 Configuring Pipe
------------------
The basic structude of the Pipe is a Pipe Show contained within the Pipe repository.  In the pipe/[show]/config directory there are three XML files that are used to configure the show:

  pipeAssetTypes.xml
  pipeDataTypes.xml
  pipeRepTypes.xml
  
In the pipe/[show]/lib/xml directory there is an xml file tracking the assets in the repository:

  pipeAssetLibrary.xml
  
Each asset has an xml file with information about the specific asset.  These are located in the pipe/[show]/lib/assets/[id]/xml directory.

  [asset].asset.xml
  
Here is how all of these different XML files interrelate with each other.

pipeAssetTypes.xml
  - Lists the different asset types and the Asset Type Representations.
  - These representations are registered to an asset when it is created.
  - Representations must be registered in the pipeRepTypes.xml file to be registered to an asset or asset type.

pipeRepTypes.xml
  - All the possible representation types for a show must be "registered" in this xml file to be available
  - Each rep type has different entries for:
      repData - The datatype of this representation.  This referes to the pipeDataTypes.xml file.
      repSubDir - The subdirectory in the asset directory where this type of representation will reside.
      repFilename - The naming convention of this specific representation type file.
      repNumMetric -  A relative value that rates the "fidelity" of this representation when compared to others.

pipeDataTypes.xml
  - Lists the information about each data type registered in the Pipe show
  - Each data type has different entries for:
       dataEditor - The name/label of an editing application.
       dataAuthor - The name/label of an authoring application.
       dataExtension - The file extension of that data type's data file.

pipeAssetLibrary.xml
  - Lists asset names and asset IDs.
  - IDs are used to figure out the location of the directories for the data files of the asset.

[assetName].asset.xml
  - Has entries for:
       assetType - The asset typ of the asset
       assetNote - The note entered when the asset was created
       assetCreator - The user that created the asset
       assetVariations - While the Pipe Assembly Manager does not seem to use them, the Pipe requires assets to use Variations.
       assetVarVariationReps - The representations associated to this specific asset. This does not mean the rep files exist.


Using different Pipe queries, it is possible to get specific information about an asset directly.


-------------------------
 Pipe Commands Reference
-------------------------

########################
# Start a Pipe Session #
########################

## Import Pipe
import pipe

## Initialize the Pipe
## pipe.pipeInitPipe(basePath,show,verbosity)
pipe.pipeInitPipe("C:/pipe/","TortiseAndHair",0)

## Create a New Show/Project
## pipe.pipeCreateShow(pipeBasePath,pipeShow):
pipe.pipeCreateShow("C:/pipe/","StarWarz")


########################
# Define Data Elements #
########################

## Add an Asset Type to the Current Show
## pipe.pipeAddAssetType(newAssetType)
pipe.pipeAddAssetType("character")

## Add a Representation Type to the Show
## pipe.pipeAddRepType(name,data,subdir,filename,numMetric)
pipe.pipeAddRepType("modelLoRes","mayaAscii","maya","[ASSET].[VAR].[REP]","25")

## Add a Representation to the Asset Type List
## pipe.pipeAddAssetTypeRep(type,repType)
pipe.pipeAddAssetTypeRep("character","preViz")

## Add a Data Type to a show
## pipe.pipeAddDataType(dataType,dataEditor,dataAuthor,dataExt)
pipe.pipeAddDataType("OBJ","maya","maya",".obj")

## Re-Define the Asset Library (Completely Destructive, deletes current library and creates a new empty one)
 pipe.pipeCreateNewLib()


#########################
# Define Asset Elements #
#########################

## Add an Asset to the Show
## pipe.pipeAddAsset(newAssetName,newAssetType,newNotes):
pipe.pipeAddAsset('lukeSkywalker','character','He is the hero'):

## Add a Variation to an Asset
## pipe.pipeEditAsset(AssetName,[variationName],"addVar")
pipe.pipeEditAsset('lukeSkywalker',['pilot'],'addVar')

## Add a Representation to a Variation of an Asset
## pipe.pipeEditAsset(AssetName,[variationName,representation],"addRep")
pipe.pipeEditAsset(lukeSkywalker,['pilot','geoLo'],'addRep')


##################################
# Query Asset Elements Existance #
##################################
## All queries return a True (1) or False (0)

## Query if an Asset exists
## pipe.pipeAssetExists(name)
pipe.pipeAssetExists("lukeSkywalker")

## Query if an Asset Variation exists
## pipe.pipeAssetVariationExists(asset,variation)
pipe.pipeAssetVariationExists('lukeSkywalker','preViz')

## Query if a Representation exists for an Asset Variation
## pipe.pipeAssetVarRepExists(assetName,varType, representation)
pipe.pipeAssetVarRepExists('lukeSkywalker','preViz', 'bBoxLo')

## Query if an Asset Type exists
## pipe.pipeAssetTypeExists(type)
pipe.pipeAssetTypeExists("character")

## Query if a Data Type exists
## pipe.pipeDataTypeExists(type)
pipe.pipeDataTypeExists("OBJ")

## Query if a Representation Type exists for the Show
## pipe.pipeRepExists(representation)
pipe.pipeRepExists('bBoxLo')


#########################
# List Pipe Information #
#########################
## Will return a list of items, or a single item list where list[0]=="*N/A*"
## if there are no items that match the query

## List Assets in Library
pipe.pipeListAssets()

## List Asset Types for Show
pipe.pipeListAssetTypes()

## List the Data Types for the Show
pipe.pipeListDataTypes()

## List the Representation Types for the Show
pipe.pipeListRepTypes()

## List the Varations for an Asset
## pipe.pipeListAssetVars(assetName)
pipe.pipeListAssetVars('lukeSkywalker')

## List the Representations for an Asset Variation
## pipe.pipeListAssetVarReps(assetName,varType)
pipe.pipeListAssetVarReps('lukeSkywalker','preViz')

## List Asset Type Representations
## pipe.pipeListAssetTypeReps(asset)
pipe.pipeListAssetTypeReps('char')


########################
# Get Pipe Information #
########################

## Get the Current Show Name
pipe.pipeGetPipeShow()

## Get the Current Pipe Base Path
pipe.pipeGetPipePath()

## Get Asset Information
## pipe.pipeGetAssetInfoName(tempName,info)
pipe.pipeGetAssetInfoName("lukeSkywalker","Id")
pipe.pipeGetAssetInfoName("lukeSkywalker","Type")
pipe.pipeGetAssetInfoName("lukeSkywalker","Note")
pipe.pipeGetAssetInfoName("lukeSkywalker","Creator")

## Get Data Type Information
## pipe.pipeGetDataTypeInfo(dataType,Tag)
pipe.pipeGetDataTypeInfo('alembic','Editor')
pipe.pipeGetDataTypeInfo('alembic','Author')
pipe.pipeGetDataTypeInfo('alembic','Extension')

## Get Represenation Data Type Information
## pipe.pipeGetRepDataType(repType, Tag)
pipe.pipeGetRepDataType("bBox","Data")
pipe.pipeGetRepDataType("bBox","SubDir")
pipe.pipeGetRepDataType("bBox","Filename")
pipe.pipeGetRepDataType("bBox","NumMetric")
