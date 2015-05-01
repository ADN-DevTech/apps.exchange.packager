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
'''
bt_zeroTransforms.py
adrian.graham@autodesk.com
02/18/2014

Description: Utility for freezing transforms on objects, including flushing
local pivot information into worldspace, which is essential for geo preparation
for systems such as Bullet.

Mode can be one of 'center', 'offset' or 'origin'
'''

import maya.cmds
MODES=['center', 'offset', 'origin']
ATTRS = [ 'tx', 'ty', 'tz', 'rz', 'ry', 'rz', 'sx', 'sy', 'sz' ]

def zero( node, translate=True, rotate=False, scale=True, mode='center' ):

    # There are a limited number of modes.
    if mode not in MODES:
        raise Exception( '\'mode\' arg must be one of %s.' % ', '.join(MODES) )
    # end if

    # If any attrs are locked, skip.
    for attr in ATTRS:
        if maya.cmds.getAttr( node+'.'+attr, l=True ):
            maya.cmds.warning( '%s has locked attributes. Skipping.' % node )
            return
        # end if
    # end for

    # If user specifies mode=origin, zero rotation as well.
    if mode == 'origin':
        rotate=True
    # end if

    # Retain parent name.
    parent = None
    try:
        parent = maya.cmds.listRelatives( node, p=True )[0]
    except:
        pass
    # end try
        
    # Unparent, if not already under worldspace. Capture new name, in case node
    # is renamed on unparent.
    if parent:
        node = maya.cmds.parent( node, w=True )[0]
    # end if

    # Flush pivot info into worldspace.
    if mode == 'center':
        maya.cmds.xform( node, ztp=True )
    # end if

    # Query node type.
    shape_type = shapeType( node )

    # Find original location of object.
    old_pos = maya.cmds.xform( 
        node, 
        q=True, 
        ws=True, 
        rp=True 
    )

    # If centering pivot, we need to find the correct center of the bounding box.
    if mode == 'center':
        old_pos = findCenter( node )

        # Center pivot.
        maya.cmds.xform( node, cp=True )
    # end if

    # Move object back to the origin.
    maya.cmds.move( 0, 0, 0, node, rpr=True )

    # Freeze node.
    maya.cmds.makeIdentity(
        node,
        apply=True,
        t=translate,
        r=rotate,
        s=scale
    )

    # Move back to original position.
    maya.cmds.xform( 
        node,
        t=old_pos,
        ws=True,
    )

    # If freezing at origin, place pivot at 0,0,0 and zero.
    if mode == 'origin':
        maya.cmds.xform( 
            node,
            piv=[0, 0, 0],
            ws=True,
        )

        # Freeze node.
        maya.cmds.makeIdentity(
            node,
            apply=True,
            t=True,
            r=True,
            s=True
        )

    # end if

    if parent:
        maya.cmds.parent( node, parent )
    # end if

# end def zero


def shapeType( node ):
    '''
    Returns the shape type of specified node. Be careful to return correct data
    for empty nulls and nodes with duplicate node names.
    '''

    if maya.cmds.objectType( node ) != 'transform':
        return node_type
    # end if

    # Query shapes.
    shapes = maya.cmds.listRelatives( node, s=True, f=True )

    # If no shapes, just return transform (ie it's an empty null).
    # If there are shapes, return the type of the zeroth shape.
    if not shapes:
        return 'transform'
    else:
        return maya.cmds.objectType( shapes[0] )
    # end if

# end def shapeType


def findCenter( node ):
    '''
    Query bounding box and calculate the center. This is necessary as the
    'objectCenter' command doesn't always work properly.
    '''

    bbx = maya.cmds.xform( node, q=True, bb=True )
    xl = bbx[0];
    xh = bbx[3];
    yl = bbx[1];
    yh = bbx[4];
    zl = bbx[2];
    zh = bbx[5];

    # Calculate averages.
    x = (xh + xl) / 2;
    y = (yh + yl) / 2;
    z = (zh + zl) / 2;

    # Return position.
    return [x, y, z]

# end def findCenter


# Interactive method. Iterates over list of nodes.
def run( mode='center' ):

    node_list = maya.cmds.ls( sl=True )
    if not node_list:
        maya.cmds.error( 'Select one or more nodes to zero its transforms.' )
    # end if

    for node in node_list:
        zero( node=node, mode=mode )
    # end for

    # Re-select original selection.
    maya.cmds.select( node_list, r=True )

# end def run
