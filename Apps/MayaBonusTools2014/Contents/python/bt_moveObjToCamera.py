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

# Autodesk non supported Python script
# Author : Steven T. L. Roselle
# Last Update: 02/01/13
#

import maya.cmds as cmds
import maya.mel as mel
import string

def bt_checkCtrFHotkey():
    
    hotkeyExists = cmds.hotkey('f',query=1,ctl=1)
    
    if hotkeyExists == 1:
        print 'CTRL f hotkey already exists.  If you\'d like CTRL f to be associated with this tool simply delete the existing hotkey and rerun the tool to auto create.'
        
    else:
        print 'Automatically setting CTRL f as hotkey for this tool'
        cmds.nameCommand('bt_moveObjToCameraNameCommand',annotation='bt_moveObjToCameraNameCommand', command='bt_moveObjToCamera')
        runtimeCommandExists = cmds.runTimeCommand('bt_moveObjToCamera', exists=1)
        if runtimeCommandExists == 0:
            cmds.runTimeCommand('bt_moveObjToCamera', category='User', command='from bt_moveObjToCamera import *; bt_moveObjToCamera()')
        cmds.hotkey(keyShortcut='f',ctl=1,name='bt_moveObjToCameraNameCommand')
        
#bt_checkCtrFHotkey()


def bt_moveObjToCamera():
    
    #Check for hotkey and make if possible
    bt_checkCtrFHotkey()

    activePanel = cmds.getPanel(wf=1)
    if "model" in activePanel:
        activeCamera = cmds.modelEditor(activePanel,q=1,camera=1)   
    else:
        cmds.error ('No active panel/camera to frame to')    
         
    selected = cmds.ls(sl=1)
    
    locator = cmds.spaceLocator()
    cmds.select(activeCamera,add=1)
    cmds.parent(r=1)
    cmds.move(0,0,-5,locator,r=1,os=1)
    location = cmds.xform(q=1,t=1,ws=1)
    
    for object in selected:
        cmds.move(location[0],location[1],location[2],object,ws=1,a=1)
        #cmds.move(location[0],location[1],location[2],'pCube1',ws=1,a=1)
        
    cmds.delete(locator)   
    cmds.select(selected,r=1)
            
#bt_moveObjToCamera()

###

