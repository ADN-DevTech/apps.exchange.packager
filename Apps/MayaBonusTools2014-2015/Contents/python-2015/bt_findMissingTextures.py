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

# find missing texture files 


import maya.cmds as cmds
import os.path
import sys


def bt_findMissingTextures():

    selectedAll = []
    selectedMeshes = []
    selectedShaders = []
    selectedFileNodes = []
    shaders = []
    fileNodes = []
    successCount = 0
    failureCount = 0

    #get current project path
    currentProject = cmds.workspace(q=1,fn=1)   
    
    #get current selections
    selectedAll = cmds.ls(sl=1) 
    selectedMeshes = cmds.ls(cmds.filterExpand(sm=12))
    selectedShaders = cmds.ls(sl=1,mat=1)
    selectedFileNodes = cmds.ls(sl=1,type='file')
    
    
    if ((len(selectedMeshes) == 0) and (len(selectedShaders) == 0) and (len(selectedFileNodes) == 0)):
        response = (cmds.confirmDialog( title='Confirm', message='                        No meshes, shaders or textures were selected.\n\nDo you want to search the current project for all missing textures in this scene?  ', button=['Yes','No'],  defaultButton='Yes', cancelButton='No', dismissString='No' ))
        if (response == 'No'):
            cmds.warning('Select a mesh, shader or texture and try again')
            sys.exit()
        else:
            selectedFileNodes = cmds.ls(type='file')


    if (len(selectedMeshes) != 0):    
        #get any connected shaders
        cmds.select(selectedMeshes,r=1)
        connectedShaders = cmds.ls(cmds.listConnections(cmds.listConnections(cmds.ls(sl=True, o=True, dag=True, s=True), t='shadingEngine')), mat=True)
        shaders = selectedShaders + connectedShaders;
    else:
        shaders = selectedShaders
    
    if (len(shaders) != 0):   
        #get any connected file nodes
        connectedFileNodes = cmds.ls(cmds.listConnections(shaders, type='file'), r=1)
        #also check for thing like Secondary/normal maps
        connectedSecondaryNodes = cmds.ls(cmds.listConnections(shaders), r=1)
        connectedSecondaryFileNodes = cmds.ls(cmds.listConnections(connectedSecondaryNodes, type='file'), r=1)
        fileNodes = selectedFileNodes + connectedFileNodes + connectedSecondaryFileNodes
    else:
        fileNodes = selectedFileNodes   

    #remove duplicates
    fileNodes = list(set(fileNodes))   
    
    #print fileNodes
    fileCount = len(fileNodes)
    print ('\n##########################################################################\n')
    print ('Checking ' + str(fileCount) + ' nodes for associated texture/image files\n')


               
    if (len(fileNodes) == 0):
        print('No file nodes found')
      
    else:    
        for fileNode in fileNodes:
            print ('Checking file node -> ' + fileNode + '.fileTextureName')
            #get file names
            pathFileName = (cmds.getAttr(fileNode + '.fileTextureName'))
            if (os.path.isfile(pathFileName) == 0):
                fileName = os.path.basename(pathFileName)
                print ('File does not exist at currently specified path : ' + pathFileName)
                print ('Searching project for : ' + fileName)
                cmds.filePathEditor ((fileNode + '.fileTextureName'),repath=currentProject,recursive=1)
                pathFileName = (cmds.getAttr(fileNode + '.fileTextureName'))   
                if (os.path.isfile(pathFileName) == 1):
                    print ('SUCCESS:  File relocated at: ' + pathFileName + '\n')
                    successCount += 1
                else:
                    print ('FAILURE:  File can not be found in current project: ' + fileName + '\n')  
                    failureCount += 1       
            else:
                print ('File found at existing path: ' + pathFileName + '\n')
    
    if (len(selectedAll) != 0):    
        cmds.select(selectedAll, r=1)
    
    if (successCount > 0):
        print ('SUCCESS:  Relocated ' + str(successCount) + ' missing texture/image files. (See Script Editor for details)')

    if ((successCount == 0) and (failureCount == 0)):
        cmds.warning ('No changes were made. (See Script Editor for details)')

    if (failureCount > 0):
        cmds.warning ('Could not locate ' + str(failureCount) + ' texture/image files.  (See Script Editor for details)')
        
        
        
bt_findMissingTextures()

