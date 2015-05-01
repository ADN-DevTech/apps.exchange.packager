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
# Last Update: 2008/ 8/ 11
# Author : Hiroyuki Haga
#
# Usage 1:
#  1, Select some UVs in UV shells which you want to align.
#  2, Execute AlignUVShells() with direction like AlignUVShells( 'left'
#
# Usage 2:
#  1, Execute AlignUVShellsWindow()
#  2, Select some UVs in UV shells which you want to align.
#  3, Click direction button where your want align.
#

import maya.OpenMaya as OpenMaya
import maya.cmds as cmds
from sets import Set

def AlignUVShells( direction ):
	originalSelectionList = cmds.ls( sl = True )
	selList = OpenMaya.MSelectionList();
	OpenMaya.MGlobal.getActiveSelectionList( selList );

	path = OpenMaya.MDagPath()
	comp = OpenMaya.MObject()
	selList.getDagPath( 0, path, comp )
	path.extendToShape()

	# Get UV comps
	uvCompFn = OpenMaya.MFnSingleIndexedComponent( comp )
	uvComps = OpenMaya.MIntArray()
	uvCompFn.getElements( uvComps )

	if path.apiType() == OpenMaya.MFn.kMesh:
		meshFn = OpenMaya.MFnMesh(path)
		util = OpenMaya.MScriptUtil();
		uvShellIds = OpenMaya.MIntArray()
		nbUvShells = util.asUintPtr()
		currentUVSet = cmds.polyUVSet( query=True, currentUVSet=True )

		meshFn.getUvShellsIds( uvShellIds, nbUvShells, currentUVSet[0] )

		affectedShellSets = set()
		for i in range( 0, uvComps.length() ):
			affectedShellSets.add( uvShellIds[uvComps[i]] )

		affectedShellIds = list ( affectedShellSets )

	# Get UV values
		u = OpenMaya.MFloatArray()
		v = OpenMaya.MFloatArray()
		meshFn.getUVs( u, v, currentUVSet[0] )

		# Calculate Bounding Box
		bbmins = OpenMaya.MPointArray()
		bbmaxs = OpenMaya.MPointArray()

		for shellId in affectedShellIds:
			umin = 1.0
			umax = 0.0
			vmin = 1.0
			vmax = 0.0
			for j in range ( 0, uvShellIds.length()):
				if uvShellIds[j] == shellId :
					if u[j] < umin : umin = u[j]
					if u[j] > umax : umax = u[j]
					if v[j] < vmin : vmin = v[j]
					if v[j] > vmax : vmax = v[j]
		    	bbmins.append( OpenMaya.MPoint( umin, vmin, 0.0) )
		    	bbmaxs.append( OpenMaya.MPoint( umax, vmax, 0.0) )

		# Calcurate Offset Based on Bounding Box
		minPoint = OpenMaya.MPoint( bbmins[0] )
		maxPoint = OpenMaya.MPoint( bbmaxs[0] )

		# get smallest and largest poss
		for m in range( 0, bbmins.length() ):
			if minPoint.x > bbmins[ m ].x :
				minPoint.x = bbmins[ m ].x
			if minPoint.y > bbmins[ m ].y :
				minPoint.y = bbmins[ m ].y

		for m in range( 0, bbmaxs.length() ):
			if maxPoint.x < bbmaxs[ m ].x :
				maxPoint.x = bbmaxs[ m ].x
			if maxPoint.y < bbmaxs[ m ].y :
				maxPoint.y = bbmaxs[ m ].y

		# Get offset based on direction
 		offsets = OpenMaya.MPointArray()

		if direction == 'top':
			for m in range( 0, bbmaxs.length() ):
				offset = maxPoint.y - bbmaxs[m].y
				offsets.append ( OpenMaya.MPoint(0, offset, 0) )

		elif direction == 'bottom':
			for m in range( 0, bbmins.length() ):
				offset = minPoint.y - bbmins[m].y
				offsets.append ( OpenMaya.MPoint(0, offset, 0) )

		elif direction == 'right':
			for m in range( 0, bbmaxs.length() ):
				offset = maxPoint.x - bbmaxs[m].x
				offsets.append ( OpenMaya.MPoint(offset, 0, 0) )

		elif direction == 'left':
			for m in range( 0, bbmins.length() ):
				offset = minPoint.x - bbmins[m].x
				offsets.append ( OpenMaya.MPoint(offset, 0, 0) )

		# Move UVs

		for i in range( 0, len(affectedShellIds) ):
			selectionList = []
			for j in range ( 0, uvShellIds.length()):
				if uvShellIds[j] == affectedShellIds[i] :
					selectionList.append( path.fullPathName() + '.map[%d] ' % j )

			cmds.select(selectionList)
			cmds.polyEditUVShell( relative=True, uValue= offsets[i].x , vValue= offsets[i].y )

	cmds.select( originalSelectionList )

def AlignUVShellsWindow():

	cmds.window( 'Align UV Shells')
	cmds.columnLayout( adj=True )
	cmds.button( label= 'Left', c='AlignUVShells("left")' )
	cmds.button( label= 'Right', c='AlignUVShells("right")' )
	cmds.button( label= 'Top', c='AlignUVShells("top")' )
	cmds.button( label= 'Bottom', c='AlignUVShells("bottom")' )
	cmds.showWindow();
