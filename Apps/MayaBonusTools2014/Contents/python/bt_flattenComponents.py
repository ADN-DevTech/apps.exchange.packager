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
# Last Update: 02/01/12
#

from pymel.core import *
import string


def bt_getAvgVertPosition():
    
    vertList = filterExpand (ex=1,sm=31) 
        
    select (vertList,r=1)
    verts = ls (sl=1,fl=1)
    
    totalPos = [0,0,0]
    count = 0
    
    for vert in verts:
        count = count + 1
        totalPos = totalPos + vert.getPosition(space='world')
    
    print totalPos
    print count
    
    select (vertList,r=1)
    
    if (count == 0):
        print 'No verts selected'
        return [0,0,0]
    else:
        avgPosition = totalPos[0]/count, totalPos[1]/count, totalPos[2]/count
    return avgPosition
    
    
def bt_getAvgVertNormal():
    
    vertList = filterExpand (ex=1,sm=31) 
        
    select (vertList,r=1)
    verts = ls (sl=1,fl=1)
    
    totalNormal = [0,0,0]
    count = 0
    
    for vert in verts:
        count = count + 1
        totalNormal = totalNormal + vert.getNormal()
    
    print totalNormal
    print count

    select (vertList,r=1)
    
    if (count == 0):
        print 'No verts selected'
        return [0,0,0]
    else:
        avgNormal = totalNormal[0]/count, totalNormal[1]/count, totalNormal[2]/count
    return avgNormal

    #move (avgNormal[0], avgNormal[1], avgNormal[2], 'locator1', r=1)


def bt_flattenComponents():

    componentList = filterExpand (ex=1, sm=(31,32,34))
    select ( polyListComponentConversion(componentList, tv=True), r=1)
    vertList = filterExpand (ex=1,sm=31)
        
    vertsObjectName = string.split (vertList[0], '.')[0]
    
    #vertsObject = ls (vertsObjectName)
    #select (vertsObject)

    #vertsObject = pickWalk (d='up')
    if (nodeType(vertsObjectName) == 'mesh'):    
        vertsObject = listRelatives(vertsObjectName,p=1)
    else:
        vertsObject = vertsObjectName
    
    #select (vertsObject)


    #calculate avg position and normals for selected verts
    select (vertList)
    avgNormal = bt_getAvgVertNormal()
    avgPosition = bt_getAvgVertPosition()
    
    #create snapping plane
    snapPlane = polyPlane(sx=1,sy=1)[0]
    snapPlaneParent = group(name="snapPlane")
    snapPlaneParent.setTranslation(avgPosition, a=1)
    snapPlaneParent.setScale([10,10,10])

    
    #break shader connection
    disconnectAttr (snapPlane.getShape().outputs(plugs=1)[0])
    
    #create temporary locator for origenting plane
    orientLocator = spaceLocator()
    orientLocator.setTranslation(avgPosition)
    delete (orientConstraint(vertsObject, orientLocator, offset=(0,0,0)))
    #parent (orientLocator, vertsObject, r=1)
    
    move (avgNormal[0], avgNormal[1], avgNormal[2], orientLocator, r=1, os=1)
    #move ((avgNormal[0] * 1000000), (avgNormal[1] * 1000000), (avgNormal[2] * 1000000), orientLocator, r=1, ws=1)
    #move (0, 10, 0, orientLocator, r=1, os=1)
    
    #temporay orientation contraint
    delete (aimConstraint(orientLocator, snapPlaneParent, aimVector=[0,1,0]), orientLocator)

    #parent plane to object
    #parent (snapPlaneParent, vertsObject)    
    
    #snap verts to plane
    select (snapPlane,vertList, r=1)
    transferAttributes (pos=1,nml=0,uvs=0,col=0)
    
    #snapPlane = (`pPlane1`)
    
    setAttr(snapPlaneParent.displayHandle, 1)
    setAttr(snapPlaneParent.displayLocalAxis, 1)
    setAttr(snapPlane.overrideEnabled, 1)
    setAttr(snapPlane.overrideDisplayType, 2)
    

    select (snapPlaneParent, r=1)
    
    print ('Components flattened.  Use manipulator to interactively change angle, distance and area with translate, rotate and scale')
    headsUpMessage ('Components flattened.  Use manipulator to interactively change distance and orientation.  Scale can be used to expand snap area',t=4)

bt_flattenComponents()


