# Copyright (C) 1997-2013 Autodesk, Inc., and/or its licensors.
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

import shutil
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import pipe
reload(pipe)
import os
import re
import sys

#pipeBasePath2 = pipe.pipeGetPipePath()
#pipeBasePath=pipeBasePath2
pipeBasePath2 = ""
pipeBasePath=""
pipeDir = ""
show = ""
hideableRowLayout=""
zzzxx=""

def nameToNode( name ): 
    """
    Get the MObject for a node name
    """
    selectionList = OpenMaya.MSelectionList() 
    selectionList.add( name ) 
    node = OpenMaya.MObject() 
    selectionList.getDependNode( 0, node )
    return node 


def PAMApproveFixOldDatabase():
    pipePath = pipe.pipeGetPipePath()
    pipeShow = pipe.pipeGetPipeShow()
    assetIDDirs = os.listdir(pipePath + pipeShow + "/lib/assets/")
    assetIDDirs.sort(key=lambda y: y.lower()) 
    if assetIDDirs[0]=="000001" or assets[0]=="000000":
        diaResult = cmds.confirmDialog(message= 'Show "' + pipeShow + '" uses IDs. IDs are not used by this version of Assembly Manager.\n\nPress "Convert" to update the Show.\n\nIt is recommneded that you backup your Show first.\n\n'+ pipePath + pipeShow,button=['Convert', 'Cancel'],defaultButton='Cancel',cancelButton='Cancel', dismissString='Cancel')
        if diaResult=="Convert":
            PAMFixOldDatabase()
        if diaResult=="Cancel":
            cmds.confirmDialog(message= 'Terminating Assembly Manager\n', button=["OK"])
            if cmds.window("pipeAssetManager",q=1, exists=1)==True:
                cmds.deleteUI("pipeAssetManager", window=True)
            sys.exit()


def PAMFixOldDatabase():
    import xml.etree.ElementTree as xmlT
    pipePath = pipe.pipeGetPipePath()
    pipeShow = pipe.pipeGetPipeShow()
    xmlPath = pipePath + pipeShow + "/lib/xml/pipeAssetLibrary.xml"
    assets = pipe.pipeListAssets()
# Go through assets one by one
    for asset in assets:
        tempID = pipe.pipeGetAssetInfoName(asset,"Id")
        tempOldPath = pipePath + pipeShow + "/lib/assets/" + str(tempID)
        tempNewPath = pipePath + pipeShow + "/lib/assets/" + asset
        os.rename(tempOldPath,tempNewPath)
    # create new PipeAssetXML
    os.rename(xmlPath, xmlPath + ".IDs")
    assetLibRoot = xmlT.Element('pipeAssets')
    for asset in assets:
        assetNameObj = xmlT.SubElement(assetLibRoot,asset)
        tempNewAssetIDObj = xmlT.SubElement(assetNameObj,asset+"Name")
        tempNewAssetIDObj.text = asset
    file = open(xmlPath, 'w')
    xmlT.ElementTree(assetLibRoot).write(file)
    file.close()


def PAMAssetManagerBuild(pipeDir,show):
 if os.path.exists(pipeDir):
    if pipeDir.endswith("/")!=True:
        pipeDir=pipeDir +"/"
    rmbLoad = "" 
    rmbImp = ""
    loadState=0
    impState=0
    assetTypeControls = []
    pipe.pipeInitPipe(pipeDir,show,0)
    assets = pipe.pipeListAssets()
    assets.sort(key=lambda y: y.lower())
    assetTypes = pipe.pipeListAssetTypes()
    assetsTypes = []
    if assets[0] != "*N/A*":
        gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
        cmds.progressBar( gMainProgressBar, edit=True,beginProgress=True,isInterruptable=True,status='"Building Assembly Manager ...',maxValue=len(assets) )
        for xx in assets:
            if cmds.progressBar(gMainProgressBar, query=True, isCancelled=True ) :
                cmds.confirmDialog(message= 'Assembly Manager Creation Cancelled!!!!.\n', button=["OK"])
                cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
                sys.exit()
            cmds.progressBar(gMainProgressBar, edit=True, step=1)
            zz=pipe.pipeGetAssetInfoName(xx,"Type")
            assetsTypes.append(xx+"%"+zz)
        cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
    txScrlLst=""
    mel.eval('setProject "' + pipeDir + show + '/"') 
    if cmds.window("pipeAssetManager",q=1, exists=1)==True:
        cmds.deleteUI("pipeAssetManager", window=True)
    cmds.window("pipeAssetManager", wh=[290,405], title = "Pipe AM", sizeable=False, mb=True, mbv=True)
    cmds.menu( label='Options', tearOff=True )
    cmds.radioMenuItemCollection()
    rmbLoad = cmds.menuItem(label='Load Data Files', radioButton=True )
    rmbImp = cmds.menuItem(label='Import Data Files', radioButton=False )
    rmbSav = cmds.menuItem(label='Save Data Files', radioButton=False )
    hideCB = cmds.menuItem("PipeAMShowTB",label='Show Authoring Toolbar', cb=True )
    cmds.menuItem("PipeAMShowTB",e=1, cb=True )
    viewMenu = cmds.menu( label='View', tearOff=True )
    toolsMenu = cmds.menu( label='Tools', tearOff=True )
    itemAssemblify = cmds.menuItem(label='Assemblify', enable=True, c="PIPEAM.PAMAssemblifyUI()" )
    itemSaveSelectAsRep = cmds.menuItem(label='Save Representation', enable=True, c="PIPEAM.PAMAssetSaveRepUI()")
    itemBuildAssDef = cmds.menuItem(label='Build Assembly Definition', c='PIPEAM.PAMAssetBuildAssetUI', enable=True )
    pipeMenu = cmds.menu( label='Pipe', tearOff=True )
    itemCreatePipeAsset = cmds.menuItem(label='New Pipe Asset', c='PIPEAM.PAMAssetNewAssetUI()')
    itemEditPipeAsset = cmds.menuItem(label='Edit Pipe Asset', c='PIPEAM.PAMAssetEditAssetUI()', enable=True)
    cmds.menuItem( divider=True )
    itemAddAssetType = cmds.menuItem(label='Add Asset/Representation Type', c="PIPEAM.PAMAssetAddTypeUI",enable=True)
    cmds.menuItem( divider=True )
    itemRedirectPipeShow = cmds.menuItem(label='Set New Repository Location', c='PIPEAM.PAMRedirectRepo()')
    cmds.menuItem( divider=True )
    itemNewPipeShow = cmds.menuItem(label='Create New Pipe Show', c='PIPEAM.PAMAssetEditNewShow()')
    itemSetPipeShow = cmds.menuItem(label='Set Current Show', c='PIPEAM.PAMAssetEditSetShow()')
    aboutMenu = cmds.menu( label='About', tearOff=True )
    aboutPipeAss = cmds.menuItem(label='Assembly Manager v. 2.0')
    cmds.columnLayout(cat=["both",5], adjustableColumn=True)
    tempIconPath = cmds.about(pd=True) + '/prefs/icons/'
    tempIconFiles = ["add-Type","Assemblify","Build-Asset","Edit-Asset","New-Asset","Save-Rep"]
    hideableRowLayout = cmds.rowLayout("PipeAMHideable", nc=6,visible=True)
    cmds.columnLayout()
    cmds.frameLayout(lv=False,bs="out")
    cmds.columnLayout()
    butNA = cmds.iconTextButton(ann="Create Asset Placeholder",c = "PIPEAM.PAMAssetNewAssetUI()", h=34, w=38,style='iconOnly', image1=tempIconPath+tempIconFiles[4], label='New Asset' )
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.text(l="New",w=38)
    cmds.setParent('..')
    cmds.columnLayout()
    cmds.frameLayout(lv=False,bs="out")
    cmds.columnLayout()
    butSR = cmds.iconTextButton(ann="Save Representation File", c = "PIPEAM.PAMAssetSaveRepUI()", h=34, w=38,style='iconOnly', image1=tempIconPath+tempIconFiles[5], label='Save Rep' )
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.text(l="Reps",w=38)
    cmds.setParent('..')
    cmds.columnLayout()
    cmds.frameLayout(lv=False,bs="out")
    cmds.columnLayout()
    butBA = cmds.iconTextButton(ann="Build Asset Assembly", c = "PIPEAM.PAMAssetBuildAssetUI()", h=34, w=38,style='iconOnly', image1=tempIconPath+tempIconFiles[2], label='Build Assembly' )
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.text(l="Build",w=38)
    cmds.setParent('..')
    cmds.columnLayout()
    cmds.frameLayout(lv=False,bs="out")
    cmds.columnLayout()
    butAS = cmds.iconTextButton(ann="Assemblify Selected", c = "PIPEAM.PAMAssemblifyUI()",h=34, w=38,style='iconOnly', image1=tempIconPath+tempIconFiles[1], label='Assemblify' )
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.text(l="Assemb",w=38)
    cmds.setParent('..')
    cmds.columnLayout()
    cmds.frameLayout(lv=False,bs="out")
    cmds.columnLayout()
    butEA = cmds.iconTextButton(ann="Edit Asset Placeholder", c = "PIPEAM.PAMAssetEditAssetUI()", h=34, w=38, style='iconOnly', image1=tempIconPath+tempIconFiles[3], label='Edit Asset' )
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.text(l="Config",w=38)
    cmds.setParent('..')
    cmds.columnLayout()
    cmds.frameLayout(lv=False,bs="out")
    cmds.columnLayout()
    butAT = cmds.iconTextButton(ann="Add Asset Types to Show", c = "PIPEAM.PAMAssetAddTypeUI()", h=34, w=38,style='iconOnly', image1=tempIconPath+tempIconFiles[0], label='Add Type' )
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.text(l="Types",w=38)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.menuItem(hideCB,e=1,c='import maya.cmds as cmds;zzzz=(cmds.menuItem("' + hideCB+ '", q=1,cb=1));cmds.rowLayout("' + hideableRowLayout + '",e=1,visible=zzzz);cmds.window("pipeAssetManager", e=1, h=(405+(zzzz* 50 )))')
    cmds.separator(h=10,style="none")
    txScrlLst = cmds.textScrollList("PipeAMMainList", numberOfRows=20, allowMultiSelection=True)
    def PAMAssetPopup(*args):
       global TempCurrent;
       listSelection = []
       loadState=0
       impState=0
       savState=0
       loadState = cmds.menuItem(rmbLoad,q=True, radioButton=True)
       impState = cmds.menuItem(rmbImp, q=True, radioButton=True)
       savState = cmds.menuItem(rmbSav, q=True, radioButton=True)
       tempSelection = cmds.textScrollList(txScrlLst,q=True, si=True)
       if cmds.textScrollList(txScrlLst,q=1,nsi=1) > 0:
            if impState==0:
                 cmds.textScrollList(txScrlLst,e=1,da=1)
                 cmds.textScrollList(txScrlLst,e=1,si=tempSelection[0])
                 tempSelection = cmds.textScrollList(txScrlLst,q=True, si=True)
            cmds.popupMenu(HSM_Popup,e=True, deleteAllItems=True)
            cmds.setParent(HSM_Popup, menu=True)
            tempSelection = cmds.textScrollList(txScrlLst,q=True, si=True)
            if tempSelection==None:
            	return
            asset=tempSelection[0]
            assetType = pipe.pipeGetAssetInfoName(asset,"Type")
            tempPipePath = pipe.pipeGetPipePath()
            tempPipeShow = pipe.pipeGetPipeShow()
            tempPipeAssVarList=pipe.pipeListAssetVarReps(asset,'initial')
###            tempID = pipe.pipeGetAssetInfoName(asset,"Id")
            tempPath = tempPipePath + tempPipeShow + "/lib/assets/" + asset + "/data/variations/initial"
            if cmds.textScrollList(txScrlLst,q=1,nsi=1) == 1:
                 cmds.menuItem(label="Name: " + asset, bld=True, enable=False)
                 cmds.menuItem(label="Type: " + assetType, bld=True, enable=False)
###                 cmds.menuItem(label="ID: " + tempID, bld=True, enable=False)
            if cmds.textScrollList(txScrlLst,q=1,nsi=1) > 1:
                 cmds.menuItem(label="Multiple Items Selected", bld=True, enable=False)
            cmds.menuItem(divider=True)
            rawReps = pipe.pipeListAssetVarReps(asset,'initial')
            for tempRep in rawReps:
            	tempData = pipe.pipeGetRepDataType(tempRep,"Data")
            	tempExt = pipe.pipeGetDataTypeInfo(tempData,"Extension")
            	tempSubDir = pipe.pipeGetRepDataType(tempRep,"SubDir")
            	tempFileName = pipe.pipeGetRepDataType(tempRep,"Filename")
            	testPath = tempPath + "/"+ tempRep + "/"  + tempSubDir + "/" + asset +".initial." + tempRep + tempExt
            	if os.path.exists(testPath):
            	     if loadState==True:
            	         cmds.menuItem(label="Load Data File: " + tempRep, command = 'PIPEAM.PAMAssetPopupImpLoad("' + txScrlLst + '","' + str(loadState) +'","'+ str(impState) +'","'+ str(savState)  + '","' + tempRep + '")')
            	     if impState==True:
            	         cmds.menuItem(label="Import Data File: " + tempRep, command = 'PIPEAM.PAMAssetPopupImpLoad("' + txScrlLst + '","' + str(loadState) +'","'+ str(impState) +'","'+ str(savState)  + '","' + tempRep + '")')
            	     if savState==True:
            	         cmds.menuItem(label="Save Data File: " + tempRep, command = 'PIPEAM.PAMAssetPopupImpLoad("' + txScrlLst + '","' + str(loadState) +'","'+ str(impState) +'","'+ str(savState) + '","' + tempRep + '")')
            cmds.menuItem(divider=True)
            tempDefLoadPath = tempPipePath + tempPipeShow + '/lib/assets/' + asset + '/data/definition/initial/'
            if os.path.exists(tempDefLoadPath + asset + '.AD.ma'):
                cmds.menuItem(label="Load Assembly Definition File: " + asset+ ".AD.ma", command = 'import maya.cmds as cmds;cmds.file("' + tempDefLoadPath + asset + '.AD.ma",o=True,f=True,options="v=0;",typ="mayaAscii")')
            elif os.path.exists(tempDefLoadPath + asset + '.ma'):
                cmds.menuItem(label="Load Assembly Definition File: " + asset+ ".ma", command = 'import maya.cmds as cmds;cmds.file("' + tempDefLoadPath + asset + '.ma",o=True,f=True,options="v=0;",typ="mayaAscii")')
       elif cmds.textScrollList(txScrlLst,q=1,nsi=1)==0:
            cmds.popupMenu(HSM_Popup,e=True, deleteAllItems=True)
            cmds.setParent(HSM_Popup, menu=True)
            cmds.menuItem(label="  Please select only 1 item   ", bld=True, enable=False)
    HSM_Popup = cmds.popupMenu("HSM_Popoup", button=3)
    cmds.popupMenu(HSM_Popup,e=True, postMenuCommand =PAMAssetPopup)
    cmds.menuItem(label="True")
    cmds.separator(h=10,style="none")
    def PAMAssetNotes(*args):
        item=[]
        item=cmds.textScrollList(txScrlLst,q=1,si=True)
        if item==None:
            cmds.textField("assetNotes",e=1,text="")
        elif len(item)==1:
            tempNotes = pipe.pipeGetAssetInfoName(item[0],"Note")
            cmds.textField("assetNotes",e=1,text=tempNotes)
        elif len(item)>1:
            cmds.textField("assetNotes",e=1,text= "* MUTLIPLE ASSETS SELECTED *")
    cmds.textField("assetNotes",text="",editable=False)
    cmds.textScrollList(txScrlLst,e=1,sc=PAMAssetNotes)
    cmds.separator(h=10,style="none")
    loadButton=cmds.button(label="Create Assembly Reference")
    def loadPipeAssets(*args):
        selected=[]
        selected = cmds.textScrollList(txScrlLst,q=True, si=True)
        if selected==None:
            cmds.confirmDialog(message= 'No Assets selected.\n\nSelect at least one asset and try again.\n', button=["OK"])
        elif len(selected)>0:
            for name in selected:
                tempPipePath = pipe.pipeGetPipePath()
                tempPipeShow = pipe.pipeGetPipeShow()
                tempPipeAssVarList=pipe.pipeListAssetVarReps(name,'initial')
##                tempID = pipe.pipeGetAssetInfoName(name,"Id")
                tempPath = tempPipePath + tempPipeShow + "/lib/assets/" + name + "/data/definition/initial/" + name + ".ma"
                tempPathAD = tempPipePath + tempPipeShow + "/lib/assets/" + name + "/data/definition/initial/" + name + ".AD.ma"
                if os.path.exists(tempPath):
                    feedback=cmds.assembly(name=name, type='assemblyReference')
                    cmds.setAttr(feedback + ".definition", tempPath, type="string")
                elif os.path.exists(tempPathAD):
                    feedback=cmds.assembly(name=name, type='assemblyReference')
                    cmds.setAttr(feedback + ".definition", tempPathAD, type="string")
                else:
                    cmds.confirmDialog(message= 'Assembly Definition does not exist for ' + name+ '.\n\n', button=["Skip"])
    cmds.button(loadButton,e=True, command=loadPipeAssets)
    cmds.separator(h=10,style="none")
    cmds.textScrollList(txScrlLst, e=1, dcc= loadPipeAssets)
    #cmds.setParent(viewMenu)
    def refreshTextList(*args):
        cmds.textScrollList(txScrlLst,e=1, ra=1)
        for temp in assetsTypes:
            x_assetType = temp.split("%")
            if cmds.menuItem('cb_'+x_assetType[1],q=True,cb=True):
                cmds.textScrollList(txScrlLst, e=1, append=x_assetType[0])
    if assetTypes[0] !="*N/A*":
        for tempAssetTypes in assetTypes:
            x= cmds.menuItem('cb_'+tempAssetTypes,checkBox=True, label=tempAssetTypes,p=viewMenu)
            cmds.menuItem(x, e=1, c=refreshTextList)
            assetTypeControls.append(x)
    refreshTextList(txScrlLst)
    cmds.showWindow("pipeAssetManager")

def PAMAssetPopupImpLoad(txScrlLst,loadState,impState,savState, tempRep):
     tempSelection = cmds.textScrollList(txScrlLst,q=True, si=True)
     tempData = pipe.pipeGetRepDataType(tempRep,"Data")
     tempExt = pipe.pipeGetDataTypeInfo(tempData,"Extension")
     tempSubDir = pipe.pipeGetRepDataType(tempRep,"SubDir")
     tempFileName = pipe.pipeGetRepDataType(tempRep,"Filename")
     for temp in tempSelection:
          assetType = pipe.pipeGetAssetInfoName(temp,"Type")
          tempPipePath = pipe.pipeGetPipePath()
          tempPipeShow = pipe.pipeGetPipeShow()
          tempPipeAssVarList=pipe.pipeListAssetVarReps(temp,'initial')
##          tempID = pipe.pipeGetAssetInfoName(temp,"Id")
          tempPath = tempPipePath + tempPipeShow + "/lib/assets/" + temp + "/data/variations/initial"
          testPath = tempPath + "/"+ tempRep + "/"  + tempSubDir + "/" + temp +".initial." + tempRep + tempExt
          if os.path.exists(testPath):
               if loadState=="True":
                     if tempExt==".abc":
                         tempResult = cmds.createNode("gpuCache", name=temp+"Shape")
                         cmds.setAttr(tempResult+".cacheFileName", testPath, type="string")
                     else:
                         cmds.file(testPath ,o=True, f=True, options="v=0;",typ="mayaAscii")
               if impState=="True":
                     if tempExt==".abc":
                         tempResult = cmds.createNode("gpuCache", name=temp+"Shape")
                         cmds.setAttr(tempResult+".cacheFileName", testPath, type="string")
                     else:
                         cmds.file(testPath,mergeNamespacesOnClash=False, rpr=True,pr=True, i=True, options="v=0;",typ="mayaAscii")
               if savState=="True":
                     if temp==tempSelection[0]:
                         cmds.textScrollList(txScrlLst,w=True, si=temp)
                         currentFrame = cmds.currentTime(q=1)
                         if tempData=='gpuCache':
                             diaResult = cmds.confirmDialog(message= 'Asset: ' + temp + '\n\nAbout to overwrite the representation file:\n\n' + testPath + '\n\nvia an Export GPU Cache All.\n\nPress OK to continue.\n', button=['OK', 'Cancel'],defaultButton='OK',cancelButton='Cancel', dismissString='Cancel')
                             if diaResult=="OK":
                                 cmds.gpuCache(st=currentFrame,et=currentFrame,o=True,ot=40000, ado=True, omb=False, wm=True, dir=tempPath + "/"+ tempRep + "/"  + tempSubDir + "/", fileName = temp +".initial." + tempRep)
                         elif tempData=='alembic' or tempData=='bBoxC':
                             diaResult = cmds.confirmDialog(message= 'Asset: ' + temp + '\n\nAbout to overwrite the representation file:\n\n' + testPath + '\n\nvia an Alembic Export All.\n\nPress OK to continue.\n', button=['OK', 'Cancel'],defaultButton='OK',cancelButton='Cancel', dismissString='Cancel')
                             if diaResult=="OK":
                                 cmds.AbcExport(j= "-frameRange " + str(currentFrame) + " " +  str(currentFrame) + " -file " + testPath)
                         elif tempData=='bBoxB' or tempData=='mayaBinary' or tempData=='bBoxA' or tempData=='mayaAscii':
                             diaResult = cmds.confirmDialog(message= 'Asset: ' + temp + '\n\nAbout to overwrite the representation file:\n\n' + testPath + '\n\nvia a Maya File Save.\n\nPress OK to continue.\n', button=['OK', 'Cancel'],defaultButton='OK',cancelButton='Cancel', dismissString='Cancel')
                             if diaResult=="OK":
                                 cmds.file(rename=testPath)
                                 cmds.file(f=True,save=True)

def PAMAssetNewAssetUI():
    if cmds.window("HSM_AssetCreator", q=1, ex=True):
        cmds.deleteUI("HSM_AssetCreator", window=True)
    window = cmds.window("HSM_AssetCreator", title="ADD PIPE ASSET", sizeable=False, wh=[360,250])
    cmds.columnLayout(columnAttach=['both', 20], adj=True, cal="center")
    cmds.separator(style="none", h=20)
    assetNameFieldGroup = cmds.textFieldGrp( label='Name', ed=True, text='New Asset Name', cw2 = [70, 100] )
    cmds.separator(style="none", h=5)
    assetTypeMenu = cmds.optionMenuGrp(label='Type', w=1, cw = [1,70])
    tempTypes = pipe.pipeListAssetTypes()
    for temp in tempTypes:
        cmds.menuItem(label=temp)
    cmds.separator(style="none", h=5)
    assetNoteFieldGroup = cmds.textFieldGrp(label='Description', text='Enter Note Here', adj=2, cw = [1,70]  )
    cmds.separator(style="none", h=30)
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 1, 125), adjustableColumn=2,ct3=["both","both","both"])
    assetCreateButton = cmds.button(l="Create Asset", command='PIPEAM.PAMAssetNewAssetCreate("' + window + '","' + assetNameFieldGroup +'","' + assetTypeMenu + '","' + assetNoteFieldGroup + '")')
    cmds.separator(style="none")
    assetCancelButton = cmds.button(l="Cancel", c='import maya.cmds as cmds;cmds.deleteUI("HSM_AssetCreator", window=True)')
    cmds.setParent('..')
    cmds.columnLayout(columnAttach=['both', 20], adj=True, cal="center")
    cmds.separator(style="none", h=20)
    cmds.setParent('..')
    cmds.showWindow(window)

def PAMAssetNewAssetCreate(window,assetNameFieldGroup,assetTypeMenu,assetNoteFieldGroup):
    newName = cmds.textFieldGrp(assetNameFieldGroup,q=1,text=True)
    newType = cmds.optionMenuGrp(assetTypeMenu,q=1,v=1)
    newNote = cmds.textFieldGrp(assetNoteFieldGroup,q=1,text=True)
    newName=newName.replace("."," ")
    newName=newName.replace("-"," ")
    newName=newName.replace("_"," ")
    pattern = re.compile('([^\s\w]|_)+')
    newName = pattern.sub('', newName) 
    newName=newName.replace(" ","_")
    if pipe.pipeAssetExists(newName)==True:
    	cmds.confirmDialog(message= 'Asset with name "' + newName + '" exists.')
    else:
        pipe.pipeAddAsset(newName,newType,newNote)
        pipe.pipeEditAsset(newName,['initial'],'addVar')
        PAMAssetEditInitialize()
    if cmds.window(window, q=1, ex=True):
        cmds.deleteUI(window, window=True)

def PAMAssemblifyUI():
    result = cmds.promptDialog(title='Assemblify',message='New Assemblified Asset Name:', button=['OK', 'Cancel'],defaultButton='OK',cancelButton='Cancel', dismissString='Cancel')
    if result == 'OK':
        tempName = cmds.promptDialog(query=True, text=True)
        tempName=tempName.replace("."," ")
        tempName=tempName.replace("-"," ")
        tempName=tempName.replace("_"," ")
        pattern = re.compile('([^\s\w]|_)+')
        tempName = pattern.sub('', tempName) 
        tempName=tempName.replace(" ","_")
        PAMAssemblify(tempName,1,1,1,0)

def PAMAssemblify(newAssetName,makeGeo,makeGPU,makeBBox,makeGPULo):
    show = pipe.pipeGetPipeShow()
    lowestAssetInfo=[]
    assetDic={}
    xyzTup=()
    tempNewAssets = []
    tempSels = ""
    selAssets=[]
    lowestAssetValue=999999999
# Get assets selected list
    tempSelAssets = cmds.ls(sl=True)
    for tempAsset in tempSelAssets:
        if cmds.nodeType(tempAsset) == "assemblyReference" and cmds.listRelatives(tempAsset,ap=True) == None:
            selAssets.append(tempAsset)
    if len(selAssets)==0:
            cmds.confirmDialog(message="There are no Top Level Assemblby References selected.", button=["Abort"])
            return
    selAssets.sort()
# Create a string for the selected list
    for t in selAssets:
        t=tempSels + " " + t
# Check if Asset with New Asset Name Already Exists
    if pipe.pipeAssetExists(newAssetName):
        result = cmds.confirmDialog( title='Confirm', message="Pipe Asset " + newAssetName+ " exists.  Replace it?", button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if result != "Yes":
             cmds.confirmDialogue(message="Pipe Asset named " + newAssetName + " already exists.", button=["Abort"])
             return
# Turn off background loading of the GPU cache 
    gpuBackgroupCacheOptions = {'gpuCacheAllAuto': 0, 'gpuCacheBackgroundReadingAuto': 1, 'gpuCacheBackgroundReading': 1}
    if cmds.pluginInfo("gpuCache", query = 1, loaded = 1): 
        for optVar in gpuBackgroupCacheOptions: 
            gpuBackgroupCacheOptions[optVar] = cmds.optionVar(query = optVar) 
            cmds.optionVar(intValue = [optVar, 0])
            cmds.gpuCache(e=1, refreshSettings=1)
# Get Lowest values
    for asset in selAssets:
        cmds.assembly(asset, e=1, active="geo")
        tempPos = cmds.xform(asset, q=1,ws=1,rp=True)
        if tempPos[1]< lowestAssetValue:
                lowestAssetInfo = []
                lowestAssetInfo.append(asset)
                lowestAssetInfo.append(tempPos[0])
                lowestAssetInfo.append(tempPos[1])
                lowestAssetInfo.append(tempPos[2])
                lowestAssetValue = tempPos[1]
                tempRots = cmds.getAttr(asset + ".rotate")
                tempX,tempY,tempZ=tempRots[0]
                lowestAssetInfo.append(tempX)
                lowestAssetInfo.append(tempY)
                lowestAssetInfo.append(tempZ)
                tempScale = cmds.getAttr(asset + ".scale")
                tempX,tempY,tempZ=tempScale[0]
                lowestAssetInfo.append(tempX)
                lowestAssetInfo.append(tempY)
                lowestAssetInfo.append(tempZ)
    relX = lowestAssetInfo[1]
    relY = lowestAssetInfo[2]
    relZ = lowestAssetInfo[3]
#Determine Final Positions
    for asset in selAssets:
        x = (cmds.getAttr(asset+".translateX"))-relX
        y = (cmds.getAttr(asset+".translateY"))-relY
        z = (cmds.getAttr(asset+".translateZ"))-relZ
        xr = cmds.getAttr(asset+".rotateX")
        yr = cmds.getAttr(asset+".rotateY")
        zr = cmds.getAttr(asset+".rotateZ")
        xs = cmds.getAttr(asset+".scaleX")
        ys = cmds.getAttr(asset+".scaleY")
        zs = cmds.getAttr(asset+".scaleZ")
        assetDic[str(asset)] = [x,y,z,xr,yr,zr,xs,ys,zs]
#translate all so that the center of the lowest asset is at the origin
        cmds.move(x,y,z, asset, a=True, ws=True)
        cmds.setAttr(asset+".rotateX",xr)
        cmds.setAttr(asset+".rotateY",yr)
        cmds.setAttr(asset+".rotateZ",zr)
        cmds.setAttr(asset+".scaleX",xs)
        cmds.setAttr(asset+".scaleY",ys)
        cmds.setAttr(asset+".scaleZ",zs)
        cmds.assembly(asset, e=1, active="")
        assDefFile =  cmds.getAttr(asset + ".definition")
        assDefSplit = assDefFile.split("/")
        assetBase = assDefSplit[(len(assDefSplit))-1].replace(".ma","")
        tempAssembly = cmds.assembly(name=assetBase,type='assemblyReference')
        tempNewAssets.append(tempAssembly)
        cmds.setAttr(tempAssembly + ".definition", assDefFile, type="string")
        cmds.move(x,y,z, tempAssembly, a=True, ws=True)
        cmds.setAttr(tempAssembly +".rotateX",xr)
        cmds.setAttr(tempAssembly +".rotateY",yr)
        cmds.setAttr(tempAssembly +".rotateZ",zr)
        cmds.setAttr(tempAssembly+".scaleX",xs)
        cmds.setAttr(tempAssembly+".scaleY",ys)
        cmds.setAttr(tempAssembly+".scaleZ",zs)
# Check if Pipe Asset exists
    pipe.pipeAddAsset(newAssetName,'hier','Assemblified: ' + t)
    pipe.pipeEditAsset(newAssetName,['initial'],'addVar')
# Create Assembly Definitions
    newAssDef=cmds.assembly(name=newAssetName, type='assemblyDefinition')         
# Get New Asset Info
    tempPipeDir = pipe.pipeGetPipePath()
###    tempNewAssemblyID = pipe.pipeGetAssetInfoName(newAssetName,"Id")
    tempNewAssemblyBasePath = ""
    tempNewAssemblyBasePath = pipeBasePath + show + "/lib/assets/" + newAssetName + "/data/"
    tempNewAssemblyRepBase = tempNewAssemblyBasePath + "variations/initial/"
    tempNewAssemblyDefPath = tempNewAssemblyBasePath + "definition/initial/" + newAssetName + ".AD.ma"
# Create Geo Rep File
    grpName = ""
    ttt=  ""
    ttt2 = ""
    newAssetDef = ""
    if makeGeo==True:
#        for asset in selAssets:
        for asset in tempNewAssets:
            cmds.assembly(asset, e=1, active="")
        cmds.select(tempNewAssets)
        repPath = tempPipeDir + tempNewAssemblyRepBase + "geo/maya/" + newAssetName + ".initial.geo.ma"
        print repPath
        cmds.file(repPath,force=True, options="v=0;", typ="mayaAscii",pr=True, es=True, constraints=False, constructionHistory=False, expressions=False, channels=False, shader=False)
        repPathLocal = "lib/assets/" +  newAssetName + "/data/variations/initial/geo/maya/" + newAssetName + ".initial.geo.ma"
        tmpType = "Scene"
        tmpLabel = "geo"
        assemblyObj = nameToNode(newAssDef)
        assemblyFn = OpenMaya.MFnAssembly(assemblyObj)
        assemblyFn.createRepresentation(repPathLocal,tmpType, tmpLabel)
        assemblyFn.setRepLabel(tmpLabel,tmpLabel)
# Create GPU Rep File
    if makeGPU==True:
        if grpName =="":
            cmds.select(tempNewAssets)
            grpName = cmds.group()
        for nasset in tempNewAssets:
            tempccd = 0
            listedRepsList = cmds.assembly(nasset, q=1, listRepresentations=True)
            for tempListedRep in listedRepsList:
                if tempListedRep == "gpu":
                    tempccd=1
            if tempccd==1:
                cmds.assembly(grpName+"|" + nasset, e=1, active="gpu")
            else:
                cmds.assembly(grpName+"|" + nasset, e=1, active="geo")
        cmds.select(grpName)
        repPath = tempPipeDir + tempNewAssemblyRepBase + "gpu/cache/" + newAssetName + ".initial.gpu.abc"
        repPathLocal = "lib/assets/" +  newAssetName + "/data/variations/initial/gpu/cache/" + newAssetName + ".initial.gpu.abc"
        cmds.gpuCache(grpName, startTime=1, endTime=1, optimize=True, optimizationThreshold=40000, directory=(tempPipeDir + tempNewAssemblyRepBase + 'gpu/cache/'), fileName=(newAssetName + '.initial.gpu'))
        tmpType = "Cache"
        tmpLabel = "gpu"
        assemblyObj = nameToNode(newAssDef)
        assemblyFn = OpenMaya.MFnAssembly(assemblyObj)
        assemblyFn.createRepresentation(repPathLocal,tmpType, tmpLabel)
        assemblyFn.setRepLabel(tmpLabel,tmpLabel)
# Make BBox Rep
    if makeBBox==True:
        if grpName =="":
            cmds.select(tempNewAssets)
            grpName = cmds.group()
        for nasset in tempNewAssets:
            try:
                cmds.assembly(grpName+"|" + nasset, e=1, active="gpu")
            except:
                cmds.assembly(grpName+"|" + nasset, e=1, active="geo")
        cmds.select(grpName)
        repPath = tempPipeDir + tempNewAssemblyRepBase + "bBox/maya/" + newAssetName + ".initial.bBox.ma"
        repPathLocal = "lib/assets/" +  newAssetName + "/data/variations/initial/bBox/maya/" + newAssetName + ".initial.bBox.ma"
        ttt=cmds.geomToBBox(shaderColor=[0.35,0.35,0.35], combineMesh =True, keepOriginal=True)
#        ttt="|" + ttt[0]
        cmds.select(ttt)
        cmds.file(repPath,force=True, options="v=0;", typ="mayaAscii",pr=True, es=True, constraints=False, constructionHistory=False, expressions=False, channels=False, shader=True)
        tmpType = "Scene"
        tmpLabel = "bBox"
        assemblyObj = nameToNode(newAssDef)
        assemblyFn = OpenMaya.MFnAssembly(assemblyObj)
        assemblyFn.createRepresentation(repPathLocal,tmpType, tmpLabel)
        assemblyFn.setRepLabel(tmpLabel,tmpLabel)
# Save Def
        cmds.select(newAssDef)
        cmds.file(tempPipeDir + tempNewAssemblyDefPath,force=True, options="v=0;", typ="mayaAscii",pr=True, es=True, constraints=False, constructionHistory=False, expressions=False, channels=False, shader=False)
# Delete everything new and move the Originals back to where they belong
        if ttt !="":
             cmds.delete(ttt)
        if grpName !="":
             cmds.delete(grpName)
        cmds.delete(selAssets)
        cmds.delete(newAssDef)
        feedback=cmds.assembly(name=newAssDef, type='assemblyReference')
        tempNewAssemblyDefPath
        cmds.setAttr(feedback + ".definition", ("lib/assets/" +  newAssetName + "/data/definition/initial/" + newAssetName + ".AD.ma"), type="string")
        cmds.select(feedback)
        cmds.move(relX,relY,relZ, feedback, a=True, ws=True)
        cmds.assembly(feedback,e=1, active="gpu")
        PAMAssetEditInitialize()
        print 'Asset "' + newAssetName + '" Assemblified.'
# Turn On and set back old GPU Preference values
    if cmds.pluginInfo("gpuCache", query = 1, loaded = 1):
        for optVar in gpuBackgroupCacheOptions:
            cmds.optionVar(intValue = [optVar, gpuBackgroupCacheOptions[optVar]])
        cmds.gpuCache(e=1, refreshSettings=1)

def PAMAssetEditAssetUI():
    if cmds.window("HSM_EditAsset", q=1, ex=True):
        cmds.deleteUI("HSM_EditAsset", window=True)
    window = cmds.window("HSM_EditAsset", title="EDIT PIPE ASSET", sizeable=False, wh=[211,275])
    selectedAsset=[]
    selectedAsset = cmds.textScrollList("PipeAMMainList", q=1, si=1)
    if selectedAsset==None:
    	cmds.confirmDialog(message= 'No Assets selected.   Select ONLY one Asset and try again.\n', button=["OK"])
    	return
    if len(selectedAsset)>1:
    	cmds.confirmDialog(message= 'Multiple Assets selected.   Select ONLY one Asset and try again.\n', button=["Abort"])
    	return
    allRepTypes = pipe.pipeListRepTypes()
    assetRepTypes = pipe.pipeListAssetVarReps(selectedAsset[0],"initial")
    allRepTypes.sort()
    assetRepTypes.sort()
    cmds.columnLayout(columnAttach=['both', 20], adj=True, cal="center")
    cmds.separator(style="none", h=20)
    cmds.textFieldGrp(label="Asset: ", text = selectedAsset[0],editable=0,cw2=[40,110])
    cmds.separator(style="none", h=10)
    cmds.text(label="Representations List")
    cmds.separator(style="none", h=10)
    cmds.frameLayout(lv=0)
    scrollLayout = cmds.scrollLayout(horizontalScrollBarThickness=16,verticalScrollBarThickness=16, h=160)
    cmds.columnLayout(cat=['left',8])
    cbList = []
    tempCB=""
    for allRepType in allRepTypes:
        bold=0
        for assetRepType in assetRepTypes:
            if assetRepType == allRepType:
    	        bold=1
        if bold==1:
            cmds.text(l = "      " + allRepType, fn='boldLabelFont')
        else:
            tempCB= cmds.checkBox(label = allRepType, value=False)
            cbList.append(tempCB)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.separator(style="none", h=15)
    addRepsButton = cmds.button(l="Add Representations")
    cmds.separator(style="none", h=5)
    cmds.showWindow(window)
    cmds.window(window,e=1, wh=[211,275])
    def PAMAssetAddReps(*args):
      result = cmds.confirmDialog( title='Creating Representations', message="Creating Representations is not undoably. ", button=['Continue','Cancel'], defaultButton='Continue', cancelButton='Cancel', dismissString='Cancel' )
      if result == "Continue":
          for cbTemp in cbList:
              if cmds.checkBox(cbTemp, q=1, value=True):
                  label = cmds.checkBox(cbTemp, q=1, label=True)
                  pipe.pipeEditAsset(selectedAsset[0],['initial', label],'addRep')
          cmds.deleteUI("HSM_EditAsset", window=True)
    cmds.button(addRepsButton,e=1, c=PAMAssetAddReps)

def PAMAssetBuildAssetUI():
# get and check selected asset list
    selectedAssets=[]
    selectedAssets = cmds.textScrollList("PipeAMMainList", q=1, si=1)
    if selectedAssets==None:
        cmds.confirmDialog(message= 'No Assets selected.   Select ONLY one Asset and try again.\n', button=["OK"])
        return
    if cmds.confirmDialog(message= 'WARNING:\n\nBuilding Assets will force a "file -new" operation.\nYou will lose any unsaved work.\n', button=["Continue","Cancel"])!="Continue":
        return
# loop through selected assets
    for asset in selectedAssets:
        cmds.file(force=True, new=True)
        cmds.assembly(name=asset)
        if cmds.assembly(asset, q=1, lr=1)!=True:
            cmds.assembly(asset, e=1, cr="Locator")
# build definition save path
        tempPipePath = pipe.pipeGetPipePath()
        tempPipeShow = pipe.pipeGetPipeShow()
        tempPipeAssVarList=pipe.pipeListAssetVarReps(asset,'initial')
###        tempID = pipe.pipeGetAssetInfoName(asset,"Id")
        tempPath = tempPipePath + tempPipeShow + "/lib/assets/" + asset + "/data/definition/initial/" + asset + ".AD.ma"
# loop through representations of Pipe Asset
        assetRepTypes = pipe.pipeListAssetVarReps(asset,"initial")
        for tempRep in assetRepTypes:
# get Pipe asset info
               tempDataType = pipe.pipeGetRepDataType(tempRep, "Data")
               tempDataTypeExt = pipe.pipeGetDataTypeInfo(tempDataType,'Extension')
               tempSubdir = pipe.pipeGetRepDataType(tempRep,"SubDir")
               tempFileName = pipe.pipeGetRepDataType(tempRep,"Filename")
# create the file name and path
               tempFileName = tempFileName.replace('[ASSET]',asset)
               tempFileName = tempFileName.replace('[REP]',tempRep)
               tempFileName = tempFileName.replace('[VAR]','initial')
               tempFileNameExt = tempFileName + tempDataTypeExt
               tempRepPath = "lib/assets/" + asset + '/data/variations/initial/' + tempRep + '/' + tempSubdir + '/'
               tempRepFullPath = tempRepPath + tempFileNameExt
               if os.path.exists(tempPipePath + tempPipeShow + "/" + tempRepFullPath):
# add ass rep
                   tempRealRepType = ""
                   if tempDataTypeExt ==".ma":
                           tempRealRepType = "Scene"
                   if tempDataTypeExt ==".mb":
                           tempRealRepType = "Scene"
                   elif tempDataTypeExt == ".abc":
                           tempRealRepType = "Cache"
# create a rep
                   assemblyObj = nameToNode(asset)
                   assemblyFn = OpenMaya.MFnAssembly(assemblyObj)
                   assemblyFn.createRepresentation(tempRepFullPath, tempRealRepType, tempRep)
                   assemblyFn.setRepLabel(tempRep, tempRep)
               else:
                   print 'PipeAM:  Skipping representation "' + tempRep + '" of asset "' + asset + '"'
        defSaveFileDir = tempPath + "/data/definition/initial/"
        defSaveFileName = asset +".ma"
        defSavePath = defSaveFileDir + defSaveFileName
        cmds.file(rename=tempPath)
        cmds.file(f=True,type="mayaAscii",save=True)
# Initialize the UI again!
    PAMAssetEditInitialize()

def PAMAssetSaveRepUI():
    if cmds.window("HSM_SaveRepresentations", q=1, ex=True):
        cmds.deleteUI("HSM_SaveRepresentations", window=True)
    selectedAsset = []
    tempPipePath = pipe.pipeGetPipePath()
    tempPipeShow = pipe.pipeGetPipeShow()
    tempTempFullFilePath=""
    selectedAsset = cmds.textScrollList("PipeAMMainList", q=1, si=1)
    if selectedAsset==None:
    	cmds.confirmDialog(message= 'No Assets selected.   Select ONLY one Asset and try again.\n', button=["OK"])
    	return
    if len(selectedAsset)>1:
    	cmds.confirmDialog(message= 'Multiple Assets selected.   Select ONLY one Asset and try again.\n', button=["Abort"])
    	return
    window = cmds.window("HSM_SaveRepresentations", title="SAVE REPRESENTATIONS", sizeable=False)
    cmds.columnLayout(adj=1,cat=["both",5], w=600)
    cmds.separator(style="none", h=20)
    cmds.text(label="Save Representation Files")
    cmds.separator(style="none", h=20)
    cmds.frameLayout(lv=0, borderStyle="etchedOut", w=655)
    cmds.rowLayout(nc=3, cw3=[100,270,100],ct3=['both','both','both'], cl3=["center","center","center"])
    cmds.text(label = "Representation", h=27)
    cmds.text(label = "Preparation")
    cmds.text(label = "Action")
    cmds.setParent('..')
    assetRepTypes = pipe.pipeListAssetVarReps(selectedAsset[0],"initial")
    for repType in assetRepTypes:
        cmds.rowLayout(nc=3, cw3=[100,270,100], h=20,cat=[1,'left',10])
        cmds.checkBox("CB_"+repType,label=repType, value=True)
        cmds.optionMenuGrp("Opt_Prep_"+repType,l="", cw=[1,1])
        cmds.menuItem(label='Use Existing File')
        cmds.menuItem(label='Convert to BBox (Animated, Single)')
        cmds.menuItem(label='Convert to BBox (Animated, Per Shapes)')
        cmds.menuItem(label='Convert to BBox (Static, Single)')
        cmds.menuItem(label='Convert to BBox (Static, Per Shapes)')
        cmds.menuItem(label='Convert to BBox (Static, Per Shapes Combined)')
        cmds.menuItem(label='Poly Reduce by 25%')
        cmds.menuItem(label='Poly Reduce by 50%')
        cmds.menuItem(label='Poly Reduce by 75%')
        cmds.optionMenuGrp("Opt_Act_"+repType,l="", cw=[1,1])
        cmds.menuItem(label='Maya Save')
        cmds.menuItem(label='ALEMBIC Export  (Static)')
        cmds.menuItem(label='ALEMBIC Export  (Animated)')
        cmds.menuItem(label='GPU Export (Static)')
        cmds.menuItem(label='GPU Export (Animated)')
        cmds.menuItem(label='GPU Export (Animated, Optimize for Motion Blur)')
# Set Action Option Menu Values
        tempSubdir = pipe.pipeGetRepDataType(repType,"SubDir")
        tempAssetType = pipe.pipeGetAssetInfoName(selectedAsset[0],"Type")
        if tempSubdir == "cache":
            if tempAssetType=="char" or tempAssetType=="prop":
               cmds.optionMenuGrp("Opt_Act_"+repType,e=1,sl=5)
            else:
               cmds.optionMenuGrp("Opt_Act_"+repType,e=1,sl=4)
        elif tempSubdir == "maya":
# Set Preparation Option Menu Values
               cmds.optionMenuGrp("Opt_Act_"+repType,e=1,sl=1)
        if repType == "bBox":
               cmds.optionMenuGrp("Opt_Prep_"+repType,e=1,sl=6)
        if repType == "bBoxLo":
               cmds.optionMenuGrp("Opt_Prep_"+repType,e=1,sl=4)
        if repType == "col":
               cmds.optionMenuGrp("Opt_Prep_"+repType,e=1,sl=5)
        if repType == "geo":
               cmds.optionMenuGrp("Opt_Prep_"+repType,e=1,sl=1)
        if repType == "geoLo":
               cmds.optionMenuGrp("Opt_Prep_"+repType,e=1,sl=8)
        if repType == "gpu":
               cmds.optionMenuGrp("Opt_Prep_"+repType,e=1,sl=1)
        if repType == "gpuLo":
               cmds.optionMenuGrp("Opt_Prep_"+repType,e=1,sl=6)
        if repType == "rigHigh":
               cmds.optionMenuGrp("Opt_Prep_"+repType,e=1,sl=1)
        if repType == "rigLow":
               cmds.optionMenuGrp("Opt_Prep_"+repType,e=1,sl=1)
        if repType == "rigMed":
               cmds.optionMenuGrp("Opt_Prep_"+repType,e=1,sl=1)
        cmds.setParent('..')
    cmds.separator(style="none", h=5)
    cmds.setParent('..')
    cmds.separator(style="none", h=15)
    cmds.columnLayout(adj=True, cat=['left', 175])
    tmpOverCB = cmds.checkBox(label="Overwrite Exisiting Representation Files", value=True, h=25)
    tmpOverTextCB = cmds.checkBox(label="Overwrite Exisiting Shader/Texture Files", value=True, h=25)
    tmpBuildCB = cmds.checkBox("PAMAssetSaveRepsTexts",label="Build Assembly Definition when completed", value=False)
    cmds.separator(style="none", h=25)
    cmds.setParent('..')
    cmds.rowLayout(nc=3, cw3=[220,100,220],adj=2, ct3=['both','both','both'],co3=[10,5,10])
    makeRepsBut = cmds.button(l="Save Selected Representations")
    cmds.separator(style="none", h=15)
    makeRepsCancelBut = cmds.button(l="Cancel")
    cmds.setParent('..')
    cmds.separator(style="none", h=20)
    def PAMAssetSaveReps(*args):
        asset = selectedAsset[0]
        overTexts = cmds.checkBox("PAMAssetSaveRepsTexts",q=1, value=True)
        if cmds.confirmDialog(title='Save Representation Files', message="You are about derive and save representations of the current\nMaya session.\n\nFor this to be successful all DAG objects must be a single\nhierarchy.  Either parent, or group all objects together.\n\nSelect the Top node of the Hierarchy and press continue.\n", button=['Continue','Cancel'], defaultButton='Continue', cancelButton='Cancel', dismissString='Cancel' ) != "Continue":
            return
# check selection
        selectedObj = ""
        selectedObjects = []
        selectedObjects = cmds.ls(sl=1)
        print selectedObjects
        if len(selectedObjects)==0:
        	cmds.confirmDialog(message= 'No object selected.   Select a single Top-Level object and try again.\n', button=["OK"])
        	return
        if len(selectedObjects)>1:
        	cmds.confirmDialog(message= 'Multiple objects selected.   Select a single Top-Level object and try again.\n', button=["Abort"])
        	return
        if cmds.listRelatives(selectedObjects[0], allParents=True)!= None:
        	cmds.confirmDialog(message= 'The Selected object is not a Top-Level object.Try again.\n', button=["Abort"])
        	return
        selectedObj=selectedObjects[0]
        if cmds.confirmDialog(message= 'WARNING:\n\nSaving Representations will force a "file -new" operation.\nYou will lose any unsaved work.\n', button=["Continue","Cancel"])!="Continue":
                return
        else:
# save Temporary Scene
            print "$$Selected Object" + selectedObj
            tempTempFilePath = tempPipePath + tempPipeShow + '/temp/'
            tempTempFullFilePath = tempTempFilePath + "/temp.ma"
            if os.path.exists(tempTempFilePath)!=True:
                os.makedirs(tempTempFilePath, 0777)
            cmds.file(rename=tempTempFullFilePath)
            cmds.file(save=True, type='mayaAscii')
            print "$$Saved File" + tempTempFullFilePath
            tempPipeAssVarList=pipe.pipeListAssetVarReps(asset,'initial')
###            tempID = pipe.pipeGetAssetInfoName(asset,"Id")
            tempAssetBasePath = tempPipePath + tempPipeShow + "/lib/assets/" + asset + "/data/"
            tempAssetCopyPath = tempAssetBasePath + 'textures/'
            tempAssetRelativeCopyPath = "lib/assets/" + asset + "/data/textures/"
# loop through representations of Pipe Asset
            assetRepTypes = pipe.pipeListAssetVarReps(asset,"initial")
            print "$$Loop through reps"

# Turn off background loading of the GPU cache 
            gpuBackgroupCacheOptions = {'gpuCacheAllAuto': 0, 'gpuCacheBackgroundReadingAuto': 1, 'gpuCacheBackgroundReading': 1}
            if cmds.pluginInfo("gpuCache", query = 1, loaded = 1): 
                for optVar in gpuBackgroupCacheOptions: 
                    gpuBackgroupCacheOptions[optVar] = cmds.optionVar(query = optVar) 
                    cmds.optionVar(intValue = [optVar, 0])
                    cmds.gpuCache(e=1, refreshSettings=1)

            for tempRep in assetRepTypes:
                if cmds.checkBox("CB_"+tempRep,q=1, value=True)!= True:
                    continue
                print "$$Rep to be made: " + tempRep
# get Pipe asset info
                result=""
                cmds.file(tempTempFullFilePath, force=True, o=True )
                tempDataType = pipe.pipeGetRepDataType(tempRep, "Data")
                tempDataTypeExt = pipe.pipeGetDataTypeInfo(tempDataType,'Extension')
                tempSubdir = pipe.pipeGetRepDataType(tempRep,"SubDir")
                tempFileName = pipe.pipeGetRepDataType(tempRep,"Filename")
    # create the file name and path
                tempFileName = tempFileName.replace('[ASSET]',asset)
                tempFileName = tempFileName.replace('[REP]',tempRep)
                tempFileName = tempFileName.replace('[VAR]','initial')
                tempFileNameExt = tempFileName + tempDataTypeExt
                tempRepPath = "lib/assets/" + asset + '/data/variations/initial/' + tempRep + '/' + tempSubdir + '/'
                tempRepPathAbs = tempAssetBasePath + 'variations/initial/' + tempRep + '/' + tempSubdir + '/'
#                tempRepFullPath = tempRepPath + tempFileNameExt
                tempRepFullPath = tempAssetBasePath + 'variations/initial/' + tempRep + '/' + tempSubdir + '/' + tempFileNameExt
                if os.path.exists(tempRepFullPath)==True:
                    if cmds.checkBox(tmpOverCB, q=1, v=1)==False:
                         print "$$DO NOT Over write Rep file"
                         continue
                    print "$$Over write Rep file"
                prepareValue = cmds.optionMenuGrp("Opt_Prep_"+tempRep,q=1,sl=1)
                actionValue = cmds.optionMenuGrp("Opt_Act_"+tempRep,q=1,sl=1)
                print "$$ Prep = " +  str(prepareValue)
                print "$$ Action = " + str(actionValue)
# Preparation Steps
                result=""
                if prepareValue<10 and prepareValue>1:
# Convert to BBox     2-6               
                    if prepareValue<7 and prepareValue>1:
                        if prepareValue == 2:
                            print "$$ Performing Prep " + str(prepareValue)
                            result = cmds.geomToBBox(selectedObj,single=True,shaderColor=[0.5,0.5,0.7],keepOriginal=False, bakeAnimation=True, sampleBy=1)
#                            print "$$ Result = " + result
                        if prepareValue == 3:
                            print "$$ Performing Prep " + str(prepareValue)
                            result = cmds.geomToBBox(selectedObj,shaderColor=[0.5,0.5,0.7],keepOriginal=False, bakeAnimation=True, sampleBy=1)
#                            print "$$ Result = " + result
                        if prepareValue == 4:
                            print "$$ Performing Prep " + str(prepareValue)
                            result = cmds.geomToBBox(selectedObj,single=True,shaderColor=[0.5,0.5,0.7],keepOriginal=False, bakeAnimation=False)
#                            print "$$ Result = " + result
                        if prepareValue == 5:
                            print "$$ Performing Prep " + str(prepareValue)
                            result = cmds.geomToBBox(selectedObj,shaderColor=[0.5,0.5,0.7],keepOriginal=False, bakeAnimation=False)
#                            print "$$ Result = " + result
                        if prepareValue == 6:
                            print "$$ Performing Prep " + str(prepareValue)
                            results = cmds.geomToBBox(selectedObj,shaderColor=[0.5,0.5,0.7],keepOriginal=False, bakeAnimation=False, combineMesh=True)
#                            if type(results)==list:
#                            
#                            if type(results)==str:
#                                result=results
#                            print "$$ Result = " + result
#                        if prepareValue != 3:
#                            print "$$ Selected object = ",
#                            print cmds.ls(sl=True)
#                            print "$$ selectedObj = " + selectedObj
#                            print "$$ does selectedObj exist anymore: " ,
#                            print str(cmds.objExists(selectedObj))
#                            print cmds.ls(sl=True)
#                            cmds.delete(selectedObj)
#                            cmds.rename(str(result),selectedObj)
# Poly Reduce to BBox     7-9               
                    if prepareValue<10 and prepareValue>6:
                        factor = (prepareValue-6) * 25
                        cmds.select(selectedObj)
                        cmds.select(hi=True)
                        selections = cmds.ls(sl=True)
                        for selection in selections:
                            print selection
                            if cmds.nodeType(selection) == "mesh":
                                print "   MESH"
                                cmds.polyReduce(selection, ver=1, trm=0, p=factor, vct=0, tct=0, shp=0, kb=1, kmb=1, kcb=1, kfb=1, khe=1, kce=1, kbw=0.5, kmw=0.5, kcw=0.5, kfw=0.5, khw=0.5, cew=0.5, uvs=0, stl=0.01, sx=0, sy=1,sz=0, sw=0, top=1, kqw=1, vmp="", rpo=1, cr=1, ch=0)
# Prep for Action Steps
                    cmds.select(selectedObj)
                    cmds.file(tempTempFilePath + "/tempExp.ma",force=True, options="v=0;", typ="mayaAscii",pr=True, es=True)
                    cmds.file(tempTempFilePath + "/tempExp.ma", force=True, o=True )
                cmds.select(selectedObj)
# Action Steps
                if actionValue<7 and actionValue>0:

# Add support for any missing or custom file Node types here
#
# copy and repath files
# file node
                    for currentNode in cmds.ls(exactType="file"):
                        file=cmds.getAttr(currentNode + ".fileTextureName")
                        if os.path.exists(file):
                            HSMCPRepath(file, tempAssetCopyPath, currentNode, tempAssetRelativeCopyPath,"fileTextureName",overTexts)
                    for currentNode in cmds.ls(exactType="imagePlane"):
                        file=cmds.getAttr(currentNode + ".imageName")
                        if os.path.exists(file):
                            HSMCPRepath(file, tempAssetCopyPath, currentNode, tempAssetRelativeCopyPath,"imageName",overTexts)
                    for currentNode in cmds.ls(exactType="psdFileTex"):
                        file=cmds.getAttr(currentNode + ".fileTextureName")
                        if os.path.exists(file):
                            HSMCPRepath(file, tempAssetCopyPath, currentNode, tempAssetRelativeCopyPath,"fileTextureName",overTexts)
                    for currentNode in cmds.ls(exactType="movie"):
                        file=cmds.getAttr(currentNode + ".fileTextureName")
                        if os.path.exists(file):
                            HSMCPRepath(file, tempAssetCopyPath, currentNode, tempAssetRelativeCopyPath,"fileTextureName",overTexts)
                    if cmds.pluginInfo("dx11Shader",query=True, loaded=True):
                        for currentNode in cmds.ls(exactType="dx11Shader"):
                            file=cmds.getAttr(currentNode + ".shader")
                            if os.path.exists(file):
                                HSMCPRepath(file, tempAssetCopyPath, currentNode, tempAssetRelativeCopyPath,"shader",overTexts)
                    if cmds.pluginInfo("hlslShader",query=True, loaded=True):
                        for currentNode in cmds.ls(exactType="hlslShader"):
                            file=cmds.getAttr(currentNode + ".shader")
                            if os.path.exists(file):
                                HSMCPRepath(file, tempAssetCopyPath, currentNode, tempAssetRelativeCopyPath,"shader",overTexts)
                    if cmds.pluginInfo("Substance",query=True, loaded=True):
                        mayaLocation = mel.eval('getenv MAYA_LOCATION')
                        substanceLoc =  mayaLocation + "plug-ins/substance/scripts/AEsubstanceTemplate.mel"
                        if os.path.exists(substanceLoc):
                            mel.eval('source "' + substanceLoc + '"')
                            for currentNode in cmds.ls(exactType="substance"):
                                file=mel.eval("sbs_GetPackageFullPathNameFromSubstanceNode " + currentNode)
                                if os.path.exists(file):
                                    parts = file.separate("/")
                                    fileName = parts[(len(parts))-1]
                                    if tempAssetCopyPath+fileName!=file:
                                        shutil.copy(file,tempAssetCopyPath+fileName)
                                        mel.eval('SubstanceFileEntered("' + currentNode + '")')
                                        mel.eval('sbsRemoveAllDynamicAttributes("' + currentNode + '")')
                                        cmds.setAttr(currentNode+".package", tempAssetRelativeCopyPath+fileName, type="string")
                    if cmds.pluginInfo("cgfxShader",query=True, loaded=True):
                        for currentNode in cmds.ls(exactType="cgfxShader"):
                            file = cmds.cgfxShader(currentNode,q=1,fx=1)
                            if os.path.exists(file):
                                parts = file.separate("/")
                                fileName = parts[(len(parts))-1]
                                if tempAssetCopyPath+fileName!=file:
                                    shutil.copy(file,tempAssetCopyPath+fileName)
                                    cmds.cgfxShader(currentNode,e=1,fx=tempAssetCopyPath+fileName)
                    if cmds.pluginInfo("Mayatomr",query=True, loaded=True):
                        for currentNode in cmds.ls(exactType="mentalrayIblShape"):
                            file=cmds.getAttr(currentNode + ".texture")
                            if os.path.exists(file):
                                HSMCPRepath(file, tempAssetCopyPath, currentNode, tempAssetRelativeCopyPath,"texture",overTexts)
                        for currentNode in cmds.ls(exactType="mib_ptex_lookup"):
                            file=cmds.getAttr(currentNode + ".filename")
                            if os.path.exists(file):
                                HSMCPRepath(file, tempAssetCopyPath, currentNode, tempAssetRelativeCopyPath,"filename",overTexts)
                        for currentNode in cmds.ls(exactType="mentalrayTexture"):
                            file=cmds.getAttr(currentNode + ".fileTextureName")
                            if os.path.exists(file):
                                HSMCPRepath(file, tempAssetCopyPath, currentNode, tempAssetRelativeCopyPath,"fileTextureName",overTexts)
                        for currentNode in cmds.ls(exactType="mentalrayLightProfile"):
                            file=cmds.getAttr(currentNode + ".fileName")
                            if os.path.exists(file):
                                HSMCPRepath(file, tempAssetCopyPath, currentNode, tempAssetRelativeCopyPath,"fileName",overTexts)
                        for currentNode in cmds.ls(exactType="mapVizShape"):
                            file=cmds.getAttr(currentNode + ".mapFileName")
                            if os.path.exists(file):
                                HSMCPRepath(file, tempAssetCopyPath, currentNode, tempAssetRelativeCopyPath,"texture",overTexts)

# perform Action
                    tempStartFrame = cmds.playbackOptions(q=1,min=1)
                    tempEndFrame = cmds.playbackOptions(q=1,max=1)
                    currentFrame = cmds.currentTime(q=1)
# Save Scene Representation
                    if actionValue==1:
                        cmds.file(rename=tempRepFullPath)
                        if tempDataTypeExt==".ma":
                            cmds.file(save=True, type='mayaAscii')
                    if actionValue==1:
                        if tempDataTypeExt==".mb":
                            cmds.file(save=True, type='mayaBinary')
# Save Alembic Cache representation
                    if actionValue==2:
                        cmds.AbcExport(j= "-frameRange " + str(tempStartFrame) + " " +  str(tempEndFrame) + " -root " + selectedObj + " -file " + tempRepFullPath)
                    if actionValue==3:
                        cmds.AbcExport(j= "-frameRange " + str(currentFrame) + " " +  str(currentFrame) + " -root " + selectedObj + " -file " + tempRepFullPath)
# Save GPU Cache representation
                    print actionValue
                    if actionValue==4:
                        print tempFileName, tempRepPathAbs
                        cmds.gpuCache(selectedObj,st=currentFrame,et=currentFrame,o=True,ot=40000, omb=False, wm=True, dir=tempRepPathAbs, fileName = tempFileName)
                    if actionValue==5:
                        print tempFileName, tempRepPathAbs
                        cmds.gpuCache(selectedObj,st=tempStartFrame,et=tempEndFrame,o=True,ot=40000, omb=False, wm=True, dir=tempRepPathAbs, fileName = tempFileName)
                    if actionValue==6:
                        print tempFileName,tempRepPathAbs
                        cmds.gpuCache(selectedObj,st=tempStartFrame,et=tempEndFrame,o=True,ot=40000, omb=True, wm=True, dir=tempRepPathAbs, fileName = tempFileName)
# Turn On and set back old GPU Preference values
            if cmds.pluginInfo("gpuCache", query = 1, loaded = 1):
                for optVar in gpuBackgroupCacheOptions:
                    cmds.optionVar(intValue = [optVar, gpuBackgroupCacheOptions[optVar]])
                cmds.gpuCache(e=1, refreshSettings=1)
#
            if cmds.checkBox(tmpBuildCB, q=1,value=1):
                PAMAssetBuildAssetUI()
            cmds.deleteUI("HSM_SaveRepresentations", window=True)
            PAMAssetEditInitialize()
            os.remove(tempTempFullFilePath)
    cmds.button(makeRepsBut,e=1, c=PAMAssetSaveReps)
    cmds.button(makeRepsCancelBut,e=1, c='import maya.cmds as cmds;cmds.deleteUI("HSM_SaveRepresentations", window=True)')
    cmds.showWindow(window)
    cmds.window("HSM_SaveRepresentations",e=1, w=700)




def HSMCPRepath(file, tempAssetCopyPath, currentNode, tempAssetRelativeCopyPath,tempAttr,overTexts):
    print file, tempAssetCopyPath, currentNode, tempAssetRelativeCopyPath,tempAttr
    file=str(file)
    parts = file.split("/")
    fileName = parts[(len(parts))-1]
    if overTexts!=True and os.path.exists(tempAssetCopyPath+fileName):
        return
    if tempAssetCopyPath+fileName!=file:
        shutil.copy(file,tempAssetCopyPath+fileName)
#    mel.eval('SubstanceFileEntered("' + currentNode + '")')
#    mel.eval('sbsRemoveAllDynamicAttributes("' + currentNode + '")')
    cmds.setAttr(currentNode+"." + tempAttr, tempAssetRelativeCopyPath+fileName, type="string")



def PAMAssetAddTypeUI():
    if cmds.window("HSM_AddTypes", q=1, ex=True):
        cmds.deleteUI("HSM_AddTypes", window=True)
    window = cmds.window("HSM_AddTypes", title="ADD PIPE TYPES", sizeable=False, wh=[140,275])
    allRepTypes = pipe.pipeListRepTypes()
    allRepTypes.sort()
    allAssetTypes = pipe.pipeListDataTypes()
    allAssetTypes.sort()
    cmds.columnLayout(columnAttach=['both', 10], adj=True, cal="center")
    cmds.separator(style="none", h=20)
    addTypeRBs = cmds.radioButtonGrp(numberOfRadioButtons=2, label='', labelArray2=['Asset Type', 'Representation Type'], sl=1, cw3 = [10,80,80], ann = "Choose what you would like to Add")
    cmds.separator(style="none", h=20)
#New Rep Type  Column
    addRepTypeCol = cmds.columnLayout(cat=['both',10], adj=1, vis=1)
    addRepTypeTxt = cmds.textFieldGrp(label="Representation Name: ", editable=1,cw2=[120,80], ann="enter the name of the representation you want to add to the show")
    cmds.separator(style="none", h=10)
    addRepTypeOpt = cmds.optionMenuGrp(label="Data Type: ",cw2=[120,50], ann="Choose a Data Type for the representation")
    for tempDataType in allAssetTypes:
        cmds.menuItem( label=tempDataType)
    cmds.separator(style="none", h=10)
    cmds.columnLayout(cat=['both',25], adj=1)
    cmds.frameLayout(lv=0)
    cmds.columnLayout(cat=['both',10], adj=1)
    addRepTypeExtTxt = cmds.textFieldGrp(label="Extension: ", editable=0,cw2=[83,50])
    addRepTypeSubTxt = cmds.textFieldGrp(label="Subdirectory: ", editable=0,cw2=[83,50])
    addRepTypeMetricInt = cmds.intFieldGrp(label="Metric: ", cw2=[83,50])
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.separator(style="none", h=15)
    addRepTypeBut = cmds.button(l="Add New Representation Type")
    cmds.separator(style="none", h=5)
    cmds.setParent('..')
#New AssetType Column
    addAssTypeCol = cmds.columnLayout(cat=['both',20], adj=1)
    addAssTypeTxt = cmds.textFieldGrp(label="New Asset Type: ", editable=1,cw2=[110,80])
    cmds.separator(style="none", h=10)
    cmds.text(label="Representations List")
    cmds.separator(style="none", h=10)
    cmds.frameLayout(lv=0)
    cmds.scrollLayout(horizontalScrollBarThickness=16,verticalScrollBarThickness=16, h=160)
    cmds.columnLayout(cat=['both',20], adj=1)
    cbList = []
    tempCB=""
    for allRepType in allRepTypes:
        tempCB= cmds.checkBox(label = allRepType, value=False)
        cbList.append(tempCB)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.separator(style="none", h=15)
    addAssTypeBut = cmds.button(l="Add New Asset Type")
    cmds.separator(style="none", h=10)
    cmds.showWindow(window)
    cmds.window(window, e=1, wh=[262,329])
    def AddTypeUIMode(*args):
        if cmds.radioButtonGrp(addTypeRBs,q=1,sl=1)==1:
            cmds.columnLayout(addAssTypeCol, e=1, vis=0)
            cmds.columnLayout(addRepTypeCol, e=1, vis=0)
            cmds.columnLayout(addAssTypeCol, e=1, vis=1)
            cmds.window(window, e=1, wh=[262,329])
        if cmds.radioButtonGrp(addTypeRBs,q=1,sl=1)==2:
            cmds.columnLayout(addRepTypeCol, e=1, vis=0)
            cmds.columnLayout(addAssTypeCol, e=1, vis=0)
            cmds.columnLayout(addRepTypeCol, e=1, vis=1)
            cmds.window(window, e=1, wh=[262,243])
    def AddTypeUIDataUp(*args):
        tempDT = cmds.optionMenuGrp(addRepTypeOpt,q=1,v=1)
        tempExt =pipe.pipeGetDataTypeInfo(tempDT,"Extension")
        tempDataDir=""
        if tempExt == ".abc":
            tempDataDir="cache"
        if tempExt == ".ma":
            tempDataDir="maya"
        if tempExt == ".mb":
            tempDataDir="maya"
        cmds.textFieldGrp(addRepTypeExtTxt,e=1, text=tempExt)
        cmds.textFieldGrp(addRepTypeSubTxt,e=1, text=tempDataDir)
    def AddTypeUIAddAssetType(*args):
        newAssetTypeName = cmds.textFieldGrp(addAssTypeTxt,q=1,text=1)
        newAssetTypeName=newAssetTypeName.replace("."," ")
        newAssetTypeName=newAssetTypeName.replace("-"," ")
        newAssetTypeName=newAssetTypeName.replace("_"," ")
        pattern = re.compile('([^\s\w]|_)+')
        newAssetTypeName = pattern.sub('', newAssetTypeName) 
        newAssetTypeName=newAssetTypeName.replace(" ","_")
        if newAssetTypeName != "":
            if pipe.pipeAssetTypeExists(newAssetTypeName) == True:
                cmds.confirmDialog(message='Pipe Asset Type "' + newAssetTypeName + '" already exists.\nTry again.', button=["Abort"])
            else:
                pipe.pipeAddAssetType(newAssetTypeName)
                for cbTemp in cbList:
                    if cmds.checkBox(cbTemp, q=1, value=True):
                        pipe.pipeAddAssetTypeRep(newAssetTypeName,cmds.checkBox(cbTemp, q=1, label=True))
                cmds.deleteUI("HSM_AddTypes", window=True)
                PAMAssetEditInitialize()
    def AddTypeUIAddRepType(*args):
        newRepTypeName = cmds.textFieldGrp(addRepTypeTxt,q=1,text=1)
        newRepTypeName=newRepTypeName.replace("."," ")
        newRepTypeName=newRepTypeName.replace("-"," ")
        newRepTypeName=newRepTypeName.replace("_"," ")
        pattern = re.compile('([^\s\w]|_)+')
        newRepTypeName = pattern.sub('', newRepTypeName) 
        newRepTypeName=newRepTypeName.replace(" ","_")
        if newRepTypeName!= "":
            data = str(cmds.optionMenuGrp(addRepTypeOpt,q=1,v=1))
            subdir = str(cmds.textFieldGrp(addRepTypeSubTxt,q=1,text=True))
            filename= "[ASSET].[VAR].[REP]"
            metric = str(cmds.intFieldGrp(addRepTypeMetricInt,q=1,v=1))
            pipe.pipeAddRepType(newRepTypeName,data,subdir,filename,metric)
            cmds.deleteUI("HSM_AddTypes", window=True)
            PAMAssetEditInitialize()
    cmds.button(addRepTypeBut,e=1, c=AddTypeUIAddRepType)
    cmds.button(addAssTypeBut,e=1, c=AddTypeUIAddAssetType)
    cmds.radioButtonGrp(addTypeRBs,e=1,cc=AddTypeUIMode)
    cmds.optionMenuGrp(addRepTypeOpt,e=1,cc=AddTypeUIDataUp)
    AddTypeUIMode()
    AddTypeUIDataUp()


def PAMAssetEditNewShow():
    result = cmds.promptDialog(title='Create New Show',message='New Show Name:', button=['OK', 'Cancel'],defaultButton='OK',cancelButton='Cancel', dismissString='Cancel')
    if result == 'OK':
        tempShow = cmds.promptDialog(query=True, text=True)
        tempShow=tempShow.replace("."," ")
        tempShow=tempShow.replace("-"," ")
        tempShow=tempShow.replace("_"," ")
        pattern = re.compile('([^\s\w]|_)+')
        tempShow = pattern.sub('', tempShow) 
        tempShow=tempShow.replace(" ","_")
        if os.path.exists(os.environ['HOME']+"/pipe/pipe.cfg")==True:
            file2 = open(os.environ['HOME']+"/pipe/pipe.cfg","r")
            lines = file2.readlines()
            file2.flush()
            file2.close
            lines[0] = lines[0].replace("\r","")
            lines[0] = lines[0].replace("\n","")
            pipeDir = lines[0]
            if os.path.exists(pipeDir + tempShow):
                if cmds.confirmDialog( title='Show Already Exists', message="There is already a show with that name.", button=['Try Again']) == "Try Again":
                    PAMAssetEditNewShow()
            else:
                pipe.pipeInitPipe(pipeDir,tempShow,0)
		file = open(os.environ['HOME']+"/pipe/pipe.cfg","w")
		file.write(pipeDir +"\n")
		file.write(tempShow +"\n")
		file.flush()
		file.close

# Create base Asset Types and Assign Reps
#     char
                pipe.pipeAddAssetType("char")
                pipe.pipeAddAssetTypeRep("char","rig")
                pipe.pipeAddAssetTypeRep("char","bBox")
                pipe.pipeAddAssetTypeRep("char","geo")
                pipe.pipeAddAssetTypeRep("char","geoLo")
                pipe.pipeAddAssetTypeRep("char","gpuLo")
                pipe.pipeAddAssetTypeRep("char","gpu")
#     envir
                pipe.pipeAddAssetType("envir")
                pipe.pipeAddAssetTypeRep("envir","bBox")
                pipe.pipeAddAssetTypeRep("envir","geo")
                pipe.pipeAddAssetTypeRep("envir","geoLo")
                pipe.pipeAddAssetTypeRep("envir","gpuLo")
                pipe.pipeAddAssetTypeRep("envir","gpu")
#     prop
                pipe.pipeAddAssetType("prop")
                pipe.pipeAddAssetTypeRep("prop","rig")
                pipe.pipeAddAssetTypeRep("prop","bBox")
                pipe.pipeAddAssetTypeRep("prop","geo")
                pipe.pipeAddAssetTypeRep("prop","geoLo")
                pipe.pipeAddAssetTypeRep("prop","gpuLo")
                pipe.pipeAddAssetTypeRep("prop","gpu")
#     hier
                pipe.pipeAddAssetType("hier")
                pipe.pipeAddAssetTypeRep("hier","bBox")
                pipe.pipeAddAssetTypeRep("hier","geo")
                pipe.pipeAddAssetTypeRep("hier","gpuLo")
                pipe.pipeAddAssetTypeRep("hier","gpu")

#     create Workspace file 

                file = open(pipeDir + tempShow + "/workspace.mel",'w')
                file.write('//Maya\n\n')
                file.write('workspace -fr "translatorData" "data";\n')
                file.write('workspace -fr "offlineEdit" "scenes/edits";\n')
                file.write('workspace -fr "renderData" "renderData";\n')
                file.write('workspace -fr "scene" "scenes";\n')
                file.write('workspace -fr "3dPaintTextures" "sourceimages/3dPaintTextures";\n')
                file.write('workspace -fr "eps" "data";\n')
                file.write('workspace -fr "mel" "scripts";\n')
                file.write('workspace -fr "furShadowMap" "renderData/fur/furShadowMap";\n')
                file.write('workspace -fr "particles" "cache/particles";\n')
                file.write('workspace -fr "audio" "sound";\n')
                file.write('workspace -fr "scripts" "scripts";\n')
                file.write('workspace -fr "sound" "sound";\n')
                file.write('workspace -fr "furFiles" "renderData/fur/furFiles";\n')
                file.write('workspace -fr "depth" "renderData/depth";\n')
                file.write('workspace -fr "autoSave" "autosave";\n')
                file.write('workspace -fr "alembicCache" "cache/alembic";\n')
                file.write('workspace -fr "diskCache" "data";\n')
                file.write('workspace -fr "furAttrMap" "renderData/fur/furAttrMap";\n')
                file.write('workspace -fr "fileCache" "cache/nCache";\n')
                file.write('workspace -fr "sourceImages" "sourceimages";\n')
                file.write('workspace -fr "movie" "movies";\n')
                file.write('workspace -fr "Alembic" "data";\n')
                file.write('workspace -fr "mayaAscii" "scenes";\n')
                file.write('workspace -fr "iprImages" "renderData/iprImages";\n')
                file.write('workspace -fr "furImages" "renderData/fur/furImages";\n')
                file.write('workspace -fr "furEqualMap" "renderData/fur/furEqualMap";\n')
                file.write('workspace -fr "illustrator" "data";\n')
                file.write('workspace -fr "mayaBinary" "scenes";\n')
                file.write('workspace -fr "move" "data";\n')
                file.write('workspace -fr "images" "images";\n')
                file.write('workspace -fr "fluidCache" "cache/nCache/fluid";\n')
                file.write('workspace -fr "clips" "clips";\n')
                file.write('workspace -fr "OBJ" "data";\n')
                file.write('workspace -fr "templates" "assets";\n')
                file.write('workspace -fr "shaders" "renderData/shaders";\n')
                file.close() 


# Initialize the UI again!
		PAMAssetEditInitialize()

def PAMAssetEditSetShow():
    if os.path.exists(os.environ['HOME']+"/pipe/pipe.cfg")==True:
        file3 = open(os.environ['HOME']+"/pipe/pipe.cfg","r")
        lines = file3.readlines()
        file3.flush()
        file3.close
        lines[0] = lines[0].replace("\r","")
        lines[0] = lines[0].replace("\n","")
        lines[1] = lines[1].replace("\r","")
        lines[1] = lines[1].replace("\n","")
        tempFileList = os.listdir(lines[0])
# create simple window with text scroll list and dbble clikc command
        if cmds.window("pipeAssetManagerShows",q=1, exists=1)==True:
            cmds.deleteUI("pipeAssetManagerShows", window=True)
        cmds.window("pipeAssetManagerShows", wh=[164, 193], sizeable=False, mb=True, mbv=True)
        cmds.columnLayout(cat=["both",5], adjustableColumn=True)
        showScrollList = cmds.textScrollList("pipeAssetManagerShowsList", numberOfRows=10, allowMultiSelection=False, w=150, h=150)
        cmds.separator(h=10, style="none")
        cmds.button(l="Set Current Show",c="PIPEAM.PAMAssetEditDbblClick()")
        for temp in tempFileList:
            cmds.textScrollList(showScrollList,e=True, append=temp)
        cmds.textScrollList(showScrollList,e=1,si=lines[1])
        cmds.showWindow("pipeAssetManagerShows")

def PAMAssetEditDbblClick():
                tt = cmds.textScrollList("pipeAssetManagerShowsList",q=True,si=True)
                file3 = open(os.environ['HOME']+"/pipe/pipe.cfg","r")
                lines = file3.readlines()
                file3.flush()
                file3.close
                lines[0] = lines[0].replace("\r","")
                lines[0] = lines[0].replace("\n","")
                file = open(os.environ['HOME']+"/pipe/pipe.cfg","w")
                file.write(lines[0] +"\n")
                file.write(tt[0] +"\n")
                file.flush()
                file.close
                PAMAssetEditInitialize()

    
def PAMRedirectRepo():
        response = cmds.confirmDialog( title='Redirect Pipe Repository', message="You are about to choose a new location for the Pipe repository.\n\nDo not select the directory called 'Pipe'\n\n Press Continue to choose a directory or Cancel to cancel", button=['Continue','Cancel'], defaultButton='Continue', cancelButton='Cancel', dismissString='Cancel' )
        if response == "Continue":
            repositoryPaths = cmds.fileDialog2(fileMode=3, caption="Choose Directory")
            repositoryPath = str(repositoryPaths[0])
            if os.path.exists(repositoryPath) == True:
                if os.path.exists(repositoryPath + "/pipe") == True:
                    response = cmds.confirmDialog( title='Pipe Repository Already Exists?', message="There may already be a Pipe Repository here.", button=['Continue','Cancel'], defaultButton='Continue', cancelButton='Cancel', dismissString='Cancel' )
                    if response != "Continue":
                        return
                else:
                    os.makedirs(repositoryPath + "/pipe", 0777)
                if os.path.exists(os.environ['HOME']+"/pipe/")!=True:
                     os.makedirs(os.environ['HOME']+"/pipe/", 0777)
                file = open(os.environ['HOME']+"/pipe/pipe.cfg","w")
                file.write(repositoryPath+"/pipe/\n")
                file.write("@NULLSET\n")
                file.write("@NULLSET\n")
                file.flush()
                file.close
        if response == "Cancel":
            return
        pipeBasePath = repositoryPath+"/pipe/"
        result = cmds.confirmDialog(title='Use or Create Show',message='Use an existing show, or create a new one?', button=['Use', 'Create'],defaultButton='Use', dismissString='Cancel')
        if result=="Use":
            PAMAssetEditSetShow()
        if result=="Create":
            created=0
            while created<100:
                PAMAssetEditNewShow()
                if os.path.exists(pipeBasePath + show)== True:
                    created=1000

def PAMAssetEditInitialize():
    if cmds.window("pipeAssetManagerShows",q=1, exists=1)==True:
        cmds.deleteUI("pipeAssetManagerShows", window=True)
    if os.path.exists(os.environ['HOME']+"/pipe/pipe.cfg")!=True:
        response = cmds.confirmDialog( title='Initiate Pipe Repository', message="You are about to initiate the location of the Pipe repository.   \n Press Continue to choose a directory or Cancel to cancel", button=['Continue','Cancel'], defaultButton='Continue', cancelButton='Cancel', dismissString='Cancel' )
        if response == "Continue":
            repositoryPaths = cmds.fileDialog2(fileMode=3, caption="Choose Directory")
            repositoryPath = str(repositoryPaths[0])
            if os.path.exists(repositoryPath) == True:
                if os.path.exists(repositoryPath + "/pipe") == True:
                    response = cmds.confirmDialog( title='Pipe Repository Already Exists?', message="There may already be a Pipe Repository here.", button=['Continue','Cancel'], defaultButton='Continue', cancelButton='Cancel', dismissString='Cancel' )
                    if response != "Continue":
                        return
                else:
                    os.makedirs(repositoryPath + "/pipe", 0777)
                if os.path.exists(os.environ['HOME']+"/pipe/")!=True:
                     os.makedirs(os.environ['HOME']+"/pipe/", 0777)
                file = open(os.environ['HOME']+"/pipe/pipe.cfg","w")
                file.write(repositoryPath+"/pipe/\n")
                file.write("@NULLSET\n")
                file.write("@NULLSET\n")
                file.flush()
                file.close
        if response == "Cancel":
            return
    lines = []
    file4 = open(os.environ['HOME']+"/pipe/pipe.cfg","r")
    lines = file4.readlines()
    file4.flush()
    file4.close
    if len(lines)==2:
            lines[0] = lines[0].replace("\r","")
            lines[0] = lines[0].replace("\n","")
            lines[1] = lines[1].replace("\r","")
            lines[1] = lines[1].replace("\n","")
            if os.path.exists(lines[0] + lines[1])==True:
                pipeBasePath = lines[0]
                show = lines[1]
                tempValue=0
#                PAMApproveFixOldDatabase()
                if os.path.exists(pipeBasePath + "/" + show + "/lib/assets/000000") == True:
                	cmds.confirmDialog( title='Old Database Format', message="Current Database is incompitble with Assembly Manager.\n\nPlease use an earlier version of Assembly Manager", button=['Abort'])
                else:
                    PAMAssetManagerBuild(pipeBasePath,show)
                    if cmds.menuItem("PipeAMShowTB",q=1, exists=True ):
                        tempValue = cmds.menuItem("PipeAMShowTB",q=1, cb=True )
                    cmds.menuItem("PipeAMShowTB",e=1, cb=tempValue)
                    cmds.rowLayout("PipeAMHideable",e=1,visible=tempValue)
                    cmds.window("pipeAssetManager",e=1,title = "PipeAM - Show: " +  show,h=(405+(tempValue * 50 )))
            else:
                if cmds.confirmDialog( title='No Show Found', message="Press 'Continue' to create a new show.\n\nPress 'Cancel' to Cancel.", button=['Continue','Cancel'], defaultButton='Continue', cancelButton='Cancel', dismissString='Cancel' ) == "Continue":
                    PAMAssetEditNewShow()
    elif len(lines)==3:
        PAMAssetEditNewShow()
