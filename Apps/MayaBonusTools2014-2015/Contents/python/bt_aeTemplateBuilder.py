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
# Author : Rob Skiena
# Last Update: 02/01/12
#

import maya.cmds as cmds
import os
import re
import maya.mel as mel
import sys

def simpleTemplateEditorUI():

 startupViews = ["Anim", "Effects", "Lighting"]
 tempStr = ""
 currentNode=""
 currentType=""
 dictCallbacks = {}
 verbMode = "False"

 if cmds.window('bt_aeTemplateBuilder',q=1, exists=1) ==True:
 	cmds.deleteUI('bt_aeTemplateBuilder',window=True)
 window = cmds.window('bt_aeTemplateBuilder', sizeable=False, title = "Attribute Editor Template Builder", mb=True, wh=[666,596])
 cmds.menu( label='Options')
 verbMenuI = cmds.menuItem( label='Feedback', checkBox=False )
 cmds.menu( label='Help', helpMenu=True )
 cmds.menuItem(label='Version 000.000.1' )
#
# Main UI Column Layout
 col1 = cmds.columnLayout(cat=["both",10], adj=True)
 cmds.columnLayout(cat=["both",80], adj=True) 
 cmds.separator(style="none", h=5)
#
# Path Text Field
 txtFldButGrp1 = cmds.textFieldButtonGrp(label = "Template Path: ", buttonLabel = "Browse", cw3 = [100,300,100], text=(os.getenv("MAYA_LOCATION") + "/scripts/AETemplates/"))
 cmds.rowLayout(nc=2, cw2=[145, 135])
#
# Add to Templates Path Checkbox
 chkBox1 = cmds.checkBoxGrp(label="", cw= [1,125])
 cmds.text(l='Add to "MAYA_CUSTOM_TEMPLATES"  path   ')
 cmds.setParent('..')
 cmds.separator(style="none", h=5)
#
# Named Type Text Field
 txtFld1 = cmds.textFieldGrp(label = "Node Type: ", cw = [1,100], editable=False)
 cmds.rowLayout(nc=3, cw3=[145, 135, 150])
#
# Named based Checkbox
 chkBox2 = cmds.checkBoxGrp(label="", cw= [1,125])
 text1 = cmds.text(l=" Name-Based Template:    ", en=True)
#
# Named based Object Name
 textFld2 = cmds.textField(editable=True, en=False)
 cmds.setParent('..')
 cmds.setParent('..')
 cmds.separator(style="none", h=15)
#
# Frame Layout
 cmds.frameLayout(labelVisible=0)
# col2 = cmds.columnLayout(cat=["both",5], adj=True)
 cmds.rowLayout(nc=3, cw3=[290, 55, 290], adj=2, ct3 = ["both","both","both"], co3=[5,0,5])
 col31 = cmds.columnLayout(cat=["both",2], adj=True)
 cmds.text(l="Attributes")
 cmds.separator(style="none", h=10)
#
# Attributes Text Scroll List
 txtScrl1 = cmds.textScrollList(nr=25, ams=True)
 cmds.setParent('..')
 col32 = cmds.columnLayout(cat=["both",0], adj=True)
 cmds.separator(style="none", h=10)
 cmds.text(l="")
 col32 = cmds.columnLayout(cat=["both",5], adj=True)
 #cmds.separator(style="none", h=0)
#
# Icon Button1: Add to View
 cmds.frameLayout(lv=False, borderStyle = "out")
 iconButt1 = cmds.iconTextButton( style='iconAndTextVertical',ebg = 1, bgc=[0.265625,0.265625,0.265625],image1='setEdAddCmd.png', annotation='Add Attribute To View' )
 cmds.setParent('..')
 cmds.separator(style="none", h=5)
#
# Icon Button2: Remove From View
 cmds.frameLayout(lv=False, borderStyle = "out")
 iconButt2 = cmds.iconTextButton( style='iconAndTextVertical',ebg = 1, bgc=[0.265625,0.265625,0.265625],image1='removeRenderable.png', annotation='Remove Selected Item From View' )
 cmds.setParent('..')
 cmds.separator(style="none", h=20)
#
# Icon Button3: Move Item Uo
 cmds.frameLayout(lv=False, borderStyle = "out")
 iconButt3 = cmds.iconTextButton( style='iconAndTextVertical',ebg = 1, bgc=[0.265625,0.265625,0.265625],image1='moveButtonUp.png', annotation='Move Item Up in View List' )
 cmds.setParent('..')
 cmds.separator(style="none", h=5)
#
# Icon Button4: Move Item Down
 cmds.frameLayout(lv=False, borderStyle = "out")
 iconButt4 = cmds.iconTextButton( style='iconAndTextVertical',ebg = 1, bgc=[0.265625,0.265625,0.265625],image1='moveButtonDown.png', annotation='Move Item Down in View List' )
 cmds.setParent('..')
 cmds.separator(style="none", h=20)
#
# Icon Button5: Start Group
 cmds.frameLayout(lv=False, borderStyle = "out")
 iconButt5 = cmds.iconTextButton( style='iconAndTextVertical',ebg = 1, bgc=[0.265625,0.265625,0.265625],image1='publishAttributes.png', annotation='Insert New Attribute Group' )
 cmds.setParent('..')
 cmds.separator(style="none", h=5)
 cmds.setParent('..')
 cmds.setParent('..')
 cmds.columnLayout(cat=["both",2], adj=True)
 col33 = cmds.columnLayout(cat=["both",2], adj=True)
 cmds.separator(style="none", h=2)
 cmds.text(l="Views")
 cmds.separator(style="none", h=2)
#
# Views Tab Layout
 tabs1 = cmds.tabLayout("simpleTemplateEditorUITabsLayout")
 for tempStr in startupViews:
	cmds.columnLayout(tempStr,cat=["both",5], adj=True)
 	cmds.separator(style="none", h=8)
	tmptxtScrl = cmds.textScrollList(nr=21, ams=True)
 	cmds.separator(style="none", h=5)
	cmds.setParent('..')
 cmds.setParent('..')
 cmds.setParent('..')
 cmds.columnLayout(cat=["both",2], adj=True)
 cmds.rowLayout(nc=3,cw3=[89,89,91], ct3=["both", "both", "both"], co3=[2,2,2])
#
# Button2: Add View
 butt2 = cmds.button(l="Add View", annotation = "Add a view for this template")
#
# Button3: Create Template
 butt3 = cmds.button(l="Copy View", annotation = "Copy the current view as a unique one")
#
# Button4: Create Template
 butt4 = cmds.button(l="Delete View", annotation = "Delete the current view")
 cmds.setParent('..')
 cmds.setParent('..')
 cmds.setParent('..')
 cmds.setParent('..')
 cmds.setParent('..')
 cmds.separator(style="none", h=15)
 cmds.rowLayout(nc=3,cw3=[222, 222, 222], ct3=["both", "both","both"], co3 = [20,20,20] )
#
# Button4: Create Template
 butt5 = cmds.button(l="Create Template", annotation = "Writes out the Template File")
#
# Button5: Reset Template
 butt6 = cmds.button(l="Reset Editor", annotation = "Re-initiates the Simple Template Editor using the selected node to populate the UI")
#
# Button6: Cancel
 butt7 = cmds.button(l="Quit", annotation = "Quit the Simple Template Editor")
#
# Set VerbMode
 def simpleTemplateVerbMode( *args):
  verbMode = str(cmds.menuItem(verbMenuI, q=1, checkBox = True))
  print "  - Verbosity Mode Set to: " + verbMode
#
#Add Callbacks to Selected items in the current View
 def simpleTemplateEditorAddCallbacks( *args):
  currTab = str(cmds.tabLayout(tabs1,q=1, st=1))
  currColChld = cmds.columnLayout(str(cmds.tabLayout(tabs1,q=1, st=1)),q=1, ca=1)
  curList = ""
  for temp in currColChld:
  	if cmds.textScrollList(temp, exists=True):
  		curList= temp
  tempSelAttrs = cmds.textScrollList(curList, q=1, si=True)
  tempSelIndAttrs = cmds.textScrollList(curList, q=1, sii=True)
  
  if cmds.textScrollList(curList, q=1, nsi=True)!=0:
  	result = cmds.promptDialog(title='Add Callback', message='Enter The Callback command for the selected attributes:',button=['OK', 'Cancel'],defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
  	if result == 'OK':
  		text = str(cmds.promptDialog(query=True, text=True))
  		if text != "":
  			for tempAttrI in tempSelIndAttrs:
  				cmds.textScrollList(curList, e=1, sii=tempAttrI)
  				tempAttrs = cmds.textScrollList(curList, q=1, si=True)
  				tempAttr =  tempAttrs[0]
  				tempAttrStrp = tempAttr.replace("      ","")
  				tempAttrStrp = tempAttrStrp.replace(" *","")
  				dictCallbacks[currTab + "_" + tempAttrStrp] = text
				if (cmds.menuItem(verbMenuI, q=1, checkBox = True)) == True:
		  			print ('  - Callback created for ' + tempAttrStrp + ' in view "' + currTab + '"')
  				cmds.textScrollList(curList, e=1, rii=tempAttrI)
				cmds.textScrollList(curList, e=1, ap=[tempAttrI,"      " + tempAttrStrp+ " *"])

# List callbacks in Current View
 def simpleTemplateEditorPrintCallbacks( *args):
  currTab = str(cmds.tabLayout(tabs1,q=1, st=1))
  tempkeys = dictCallbacks.keys()
  print '\n-------------------------------------\n Callbacks list in the "' + currTab + '" View\n-------------------------------------'
  for temp in tempkeys:
  	if temp.startswith(currTab):
  		tempCB = dictCallbacks[temp]
  		temp = temp.replace(currTab + "_","")
  		print temp + ":  " + tempCB

# List all callbacks
 def simpleTemplateEditorPrintAllCallbacks( *args):
  currTab = str(cmds.tabLayout(tabs1,q=1, st=1))
  tempkeys = dictCallbacks.keys()
  tempkeys.sort()
  print '\n-------------------------------------\n Callbacks list in all views\n-------------------------------------'
  for temp in tempkeys:
  	tempCB = dictCallbacks[temp]
  	tSplit = temp.split("_")
	temp = temp.replace(tSplit[0] + "_","")
	print tSplit[0] + " View " + temp + ":  " + tempCB


#
#ReReset the Template UI
 def simpleTemplateEditorResetTemplate( *args):
  feedback = ""
  if cmds.textFieldGrp(txtFld1, q=1,text=True) == "":
  	feedback="Reset Editor"
  else:
  	feedback = cmds.confirmDialog(button=["Reset Editor","Continue Editing"], defaultButton = "Continue Editing",cancelButton="Continue Editing", message="Reset Template Editor?\n\nYou will lose any unsaved template editing.\n\n")
  if feedback == "Reset Editor":
	  if (cmds.menuItem(verbMenuI, q=1, checkBox = True)) == True:
	  	print "  - Template Editor Reset"
	  temp2= []
	  temp2= cmds.ls(sl=True)
	  if len(temp2)!=1:
		cmds.confirmDialog(button="OK", message="\n\nThere is no node selected.\n\nSelect a node and Reset the \nEditor to start creating views.\n\n")
	  else:
		currentNode=temp2[0]
		currentType = cmds.nodeType(currentNode)
		cmds.textScrollList(txtScrl1, e=1, ra=1)
		cmds.textFieldGrp(txtFld1, e=1, text=currentType)
		cmds.textField(textFld2, e=1, text=currentNode)
	  	tempAllAttrs = cmds.listAttr()
	  	tempAllAttrs.sort()
	  	for temp in tempAllAttrs:
			try:
		  		name = cmds.attributeQuery(temp, n=currentNode, ln=True)
				tempDType = cmds.getAttr (currentNode+'.'+temp, type=True)
				if tempDType != None:
					cmds.textScrollList(txtScrl1, e=1, append=temp)
			except:
				if (cmds.menuItem(verbMenuI, q=1, checkBox = True)) == True:
				  	print ("  - " + currentNode+'.'+temp + ' was skipped')
	  cmds.deleteUI("simpleTemplateEditorUITabsLayout", layout=True)
	  cmds.setParent(col33)
	  cmds.tabLayout("simpleTemplateEditorUITabsLayout")
	  for tempStr in startupViews:
		cmds.columnLayout(tempStr,cat=["both",5], adj=True)
 		cmds.separator(style="none", h=8)
		tmptxtScrl = cmds.textScrollList(nr=21, ams=True)
		cmds.popupMenu()
		cmds.menuItem(label= '                - -=Callbacks=- -')
		cmds.menuItem( divider=True )
		cmds.menuItem(label= 'Add a Callback to selected Attributes in the "' + tempStr + '" view', command = simpleTemplateEditorAddCallbacks)
		cmds.menuItem( divider=True )
		cmds.menuItem(label= 'List Attributes with Callbacks in Current View', command = simpleTemplateEditorPrintCallbacks)
		cmds.menuItem( divider=True )
		cmds.menuItem(label= 'List Attributes with Callbacks in ALL Views', command = simpleTemplateEditorPrintAllCallbacks)
		cmds.setParent('..')
	  dictCallbacks.clear()
	
#
# Add View to the Template UI
 def simpleTemplateEditorAddView( *args):
 
  result = cmds.promptDialog(title='New View Name ', message='Enter New View Name (Non-alpha characters will be stripped):',button=['OK', 'Cancel'],defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
  if result == 'OK':
        text = cmds.promptDialog(query=True, text=True)
	zz=""
	for c in text:
		if c.isalpha()==True:
			zz=zz+c
	if zz=="":
		cmds.confirmDialog(title = 'Invalid View Name',button="Retry", message='View names may only be text -- no numbers or other characters.\n\nTry a different name.\n')
		simpleTemplateEditorAddView()
	text=zz
        tabsList = cmds.tabLayout(tabs1,q=1, ca=1)
	test=""
	for temp in tabsList:
		if temp == text:
			test="Match"
	if test=="Match" :
		cmds.confirmDialog(title = 'View Exists',button="OK", message='The view "' + text + '" already exists.\n\nTry a different name.\n')
		simpleTemplateEditorAddView()		
	elif text=="" :
		return		
	else:
		tabsList.append(text)
		tabsList.sort(lambda x, y: cmp(x.lower(),y.lower()))
		tempC = 0
		counter = 1
		for tempX in tabsList:
			if tempX == text:
				tempC=counter
			counter=counter+1
		cmds.setParent(tabs1)
		cmds.columnLayout(text ,cat=["both",5], adj=True)
 		cmds.separator(style="none", h=8)
		cmds.textScrollList(nr=21, ams=True)
 		cmds.popupMenu()
		cmds.menuItem( bld=True, label= '                - -=Callbacks=- -')
		cmds.menuItem( divider=True )
		cmds.menuItem(label= 'Add a Callback to selected Attributes in the "' + text + '" view', command = simpleTemplateEditorAddCallbacks)
		cmds.menuItem( divider=True )
		cmds.menuItem( label= 'List Attributes with Callbacks in Current View', command = simpleTemplateEditorPrintCallbacks)
		cmds.menuItem( divider=True )
		cmds.menuItem( label= 'List Attributes with Callbacks in ALL Views', command = simpleTemplateEditorPrintAllCallbacks)
		cmds.separator(style="none", h=5)
		cmds.setParent('..')
		cmds.tabLayout(tabs1, e=1, mt = [len(tabsList), tempC])
		if (cmds.menuItem(verbMenuI, q=1, checkBox = True)) == True:
		  	print ('  - Added View "' + text +  '"')
		
#
# Dupe View to the Template UI
 def simpleTemplateEditorDupeView( *args):
  currView = str(cmds.tabLayout(tabs1,q=1, st=1))
  currColChld = cmds.columnLayout(str(cmds.tabLayout(tabs1,q=1, st=1)),q=1, ca=1)
  result = cmds.promptDialog(title='New View Name ', message='Enter New View Name:',button=['OK', 'Cancel'],defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
  if result == 'OK':
        text = cmds.promptDialog(query=True, text=True)
	zz=""
	for c in text:
		if c.isalpha()==True:
			zz=zz+c
	if zz=="":
		return
	text=zz
        tabsList = cmds.tabLayout(tabs1,q=1, ca=1)
	test=""
	for temp in tabsList:
		if temp == text:
			test="Match"
	if test=="Match" :
		cmds.confirmDialog(title = 'View Exists',button="OK", message='The view "' + text + '" already exists.\n\nTry a different name.\n')
		simpleTemplateEditorDupeView()		
	elif text=="" :
		return		
	else:
		tabsList.append(text)
		tabsList.sort(lambda x, y: cmp(x.lower(),y.lower()))
		tempC = 0
		counter = 1
		for tempX in tabsList:
			if tempX == text:
				tempC=counter
			counter=counter+1
		cmds.setParent(tabs1)
  		curList = ""
		tempContents = []
		cmds.columnLayout(text ,cat=["both",5], adj=True)
 		cmds.separator(style="none", h=8)
		tt = cmds.textScrollList(nr=21, ams=True)
		cmds.popupMenu()
		cmds.menuItem( bld=True, label= '                - -=Callbacks=- -')
		cmds.menuItem( divider=True )
		cmds.menuItem(label= 'Add a Callback to selected Attributes in the "' + text + '" view', command = simpleTemplateEditorAddCallbacks)
		cmds.menuItem( divider=True )
		cmds.menuItem(label= 'List Attributes with Callbacks in Current View', command = simpleTemplateEditorPrintCallbacks)
		cmds.menuItem( divider=True )
		cmds.menuItem(label= 'List Attributes with Callbacks in ALL Views', command = simpleTemplateEditorPrintAllCallbacks)

		for temp in currColChld:
  			if cmds.textScrollList(temp, exists=True):
  				curList= temp
 	 	tempContents=cmds.textScrollList(curList, q=1, ai=True)
 	 	if cmds.textScrollList(curList, q=1, ni=True)>0:
 	 		for t in tempContents:
				cmds.textScrollList(tt, e=1, append=t)		
 		cmds.separator(style="none", h=5)
		cmds.setParent('..')
		cmds.tabLayout(tabs1, e=1, mt = [len(tabsList), tempC])
		if (cmds.menuItem(verbMenuI, q=1, checkBox = True)) == True:
		  	print ('  - Duplicated View "'+ currView + '" as "' + text +  '" View')
		currTab = str(cmds.tabLayout(tabs1,q=1, st=1))
  		tempkeys = dictCallbacks.keys()
		for temp in tempkeys:
		 	if temp.startswith(currView):
		  		tempCB = dictCallbacks[temp]
		  		temp = temp.replace(currView + "_",text+ "_")
		  		dictCallbacks[temp] = tempCB

 
#
# Delete View to the Template UI
 def simpleTemplateEditorDelView( *args):
  currView = str(cmds.tabLayout(tabs1,q=1, st=1))
  x=cmds.tabLayout(tabs1,q=1, ca=1)
  if len(x)==1:
  	cmds.confirmDialog(title='Warning - No Views Left ', message='There must be at least one View!\nCreate a New View before deleting this one!\n\n',button=['OK'])
  else:
  	if cmds.confirmDialog(button=["Delete View","Cancel"], defaultButton = "Cancel",cancelButton="Cancel", message="Delete " +currView + " view?\n\nYou will lose any unsaved template editing.\n\n") == "Delete View":

  		tempkeys = dictCallbacks.keys()
  		for temp in tempkeys:
  			if temp.startswith(currView):
  				del dictCallbacks[temp]
		cmds.deleteUI(currView, layout=True)
		if (cmds.menuItem(verbMenuI, q=1, checkBox = True)) == True:
		  	print ('  - View "'+ currView + '" has been deleted')

#
# Add Attribute(s) to current View List
 def simpleTemplateEditorAddAttrs( *args):
  attrsList = cmds.textScrollList(txtScrl1, q=1, si=1)
  if attrsList==None:
  	return
  currColChld = cmds.columnLayout(str(cmds.tabLayout(tabs1,q=1, st=1)),q=1, ca=1)
  curList = ""
  for temp in currColChld:
  	if cmds.textScrollList(temp, exists=True):
  		curList= temp
  for temp in attrsList:
  	cmds.textScrollList(curList, e=1, append=("      " + temp))
   	if (cmds.menuItem(verbMenuI, q=1, checkBox = True)) == True:
		print ('  - Added "' + temp + '" to the "' + str(cmds.tabLayout(tabs1,q=1, st=1)) +'" View ')
 
#
# Remove Attribute(s) from current View List
 def simpleTemplateEditorRemAttrs( *args):
  currTab = str(cmds.tabLayout(tabs1,q=1, st=1))
  currColChld = cmds.columnLayout(str(cmds.tabLayout(tabs1,q=1, st=1)),q=1, ca=1)
  curList = ""
  for temp in currColChld:
  	if cmds.textScrollList(temp, exists=True):
  		curList= temp
  selAttrs = cmds.textScrollList(curList, q=1, sii=True)
  if selAttrs==None:
  	return
  selAttrs.sort(reverse=True)
  if len(selAttrs) !=0:
  	for temp in selAttrs:
  		cmds.textScrollList(curList, e=1, da=True)
  		cmds.textScrollList(curList, e=1, sii=temp)
  		tempAttrs = cmds.textScrollList(curList, q=1, si=True)
  		tempAttrStrp = tempAttrs[0].replace("      ","")
		tempAttrStrp = tempAttrStrp.replace(" *","")
		tempKey = currTab + "_" + tempAttrStrp
		if tempKey in dictCallbacks:
			del dictCallbacks[tempKey]
  		cmds.textScrollList(curList, e=1, rii=temp)
   		if (cmds.menuItem(verbMenuI, q=1, checkBox = True)) == True:
			print ('  - Removed "' + tempAttrStrp + '" from the "' + currTab +'" View ')

#
# Move Attribute(s) in current Up 
 def simpleTemplateEditorUpAttrs( *args):
  currColChld = cmds.columnLayout(str(cmds.tabLayout(tabs1,q=1, st=1)),q=1, ca=1)
  curList = ""
  for temp in currColChld:
  	if cmds.textScrollList(temp, exists=True):
  		curList= temp
  selAttrs = cmds.textScrollList(curList, q=1, sii=True)
  if selAttrs==None:
  	return
  selAttrs.sort(reverse=False)
  newSelAttrs = []
  if len(selAttrs) !=0:
  	for temp in selAttrs:
  		cmds.textScrollList(curList, e=1, sii=temp)
  		tempText = cmds.textScrollList(curList, q=1, si=True)
  		cmds.textScrollList(curList, e=1, rii=temp)
  		x=temp-1
  		if x==0:
  			x=temp
  		cmds.textScrollList(curList, e=1, ap =[x,str(tempText[0])])
 		newSelAttrs.append(x)
 	cmds.textScrollList(curList, e=1, sii=newSelAttrs)

#
# Move Attribute(s) in current Down 
 def simpleTemplateEditorDownAttrs( *args):
  currColChld = cmds.columnLayout(str(cmds.tabLayout(tabs1,q=1, st=1)),q=1, ca=1)
  curList = ""
  for temp in currColChld:
  	if cmds.textScrollList(temp, exists=True):
  		curList= temp
  selAttrs = cmds.textScrollList(curList, q=1, sii=True)
  if selAttrs==None:
  	return
  selAttrs.sort(reverse=True)
  newSelAttrs = []
  if len(selAttrs) !=0:
  	for temp in selAttrs:
  		cmds.textScrollList(curList, e=1, da=True)
  		cmds.textScrollList(curList, e=1, sii=temp)
  		tempText = cmds.textScrollList(curList, q=1, si=True)
  		x=temp+2
  		cmds.textScrollList(curList, e=1, ap =[x,str(tempText[0])])
 		newSelAttrs.append(x-1)
 		cmds.textScrollList(curList, e=1, rii=temp)
  	cmds.textScrollList(curList, e=1, sii=newSelAttrs)

#
# Add New Group to current View List
 def simpleTemplateEditorNewGrp( *args):
  currColChld = cmds.columnLayout(str(cmds.tabLayout(tabs1,q=1, st=1)),q=1, ca=1)
  curList = ""
  result = cmds.promptDialog(title='Attribute Group Name ', message='Enter Group Name:',button=['OK', 'Cancel'],defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
  if result == 'OK':
  	text = cmds.promptDialog(query=True, text=True)
	zz=""
	for c in text:
		if c.isalnum()==True:
			zz=zz+c
	text=zz
	for temp in currColChld:
	  	if cmds.textScrollList(temp, exists=True):
	  		curList= temp
	selAttrs = cmds.textScrollList(curList, q=1, sii=True)
	if selAttrs==None:
	  	return
	selAttrs.sort(reverse=False)
	insertPt = selAttrs[0]
	if insertPt<1:
	  	insertPt=1
	cmds.textScrollList(curList, e=1, ap=[insertPt, (text + " (Group)")])


#
# Enable Named Templates
 def simpleTemplateEditorNodeNameEnable( *args):
  x = cmds.checkBoxGrp(chkBox2, q=1, v1=1)
  cmds.textField(textFld2, e=1, enable=(cmds.checkBoxGrp(chkBox2, q=1, v1=1)))
  if x == 1:
  	cmds.textField(textFld2, e=1, enable=1)

#
# Quit Editor
 def simpleTemplateEditorCancel( *args):
  feedback = cmds.confirmDialog(button=["Quit Editor","Continue Editing"], defaultButton = "Continue Editing",cancelButton="Continue Editing", message="Quit Template Editing?\n\nYou will lose any unsaved template editing.\n\n")
  if feedback == "Quit Editor":
  	cmds.deleteUI('bt_aeTemplateBuilder',window=True)

#
# File Browser
 def simpleTemplateEditorBrowse( *args):
  tempDir = cmds.textFieldButtonGrp(txtFldButGrp1, q=1, text=1)
  tempBrowse = cmds.fileDialog2(fm=3, cap="Browse to Destination Directory",dir=tempDir)
  if tempBrowse!=None:
  	cmds.textFieldButtonGrp(txtFldButGrp1, e=1, text=tempBrowse[0] +"/")

#
# Create Views
 def simpleTemplateEditorCreateViews( *args):
  if (cmds.menuItem(verbMenuI, q=1, checkBox = True)) == True:
    	print ('  - Create Views Template Initiated')
  allDecAttrs=[]
  allTabs = cmds.tabLayout(tabs1,q=1, ca=1)
  tempPath =  cmds.textFieldButtonGrp(txtFldButGrp1, q=1, text=1)
  if tempPath[len(tempPath)-1] != "/":
  	tempPath=tempPath + "/"
  named = ""
  commit=""
  tempNode = cmds.textField(textFld2, q=1, text=True)
  if cmds.objExists(tempNode) !=1:
 	commit = cmds.confirmDialog(title = "Object Doesn't Exist", message='\nThe named node "' + tempNode + '" does not exist in the current Maya session.\n\nCreate template anyway?\n', button=["Continue","Abort"], defaultButton = "Continue")
	if commit != "Continue":
  		return
  if cmds.textField(textFld2, q=1, en=True):
  	named = "." + tempNode
  tempNodeType = cmds.textFieldGrp(txtFld1, q=1,text=1)
  tempFileName = tempPath + "AE" + tempNodeType + named + "Template.xml"

  for curTab in allTabs:
  	currColChld = cmds.columnLayout(curTab,q=1, ca=1)
  	curList = ""
  	for temp in currColChld:
  		if cmds.textScrollList(temp, exists=True):
  			curList= temp
  	curTabAttrs = cmds.textScrollList(curList, q=1, ai=True)
	if curTabAttrs!=None:
		for tempCutTabAt in curTabAttrs:
			tester="NO"
			tempCutTabAt=tempCutTabAt.replace("      ","")
			for tempDecAttr in allDecAttrs:
				if tempCutTabAt == tempDecAttr:
					tester="YES"
			if tester=="NO":
				allDecAttrs.append(tempCutTabAt)
  tFile = open(tempFileName, "w") 
  tFile.write("<?xml version='1.0' encoding='UTF-8'?>\n")
  tFile.write("<templates>\n\n")
  tFile.write("    <template name='AE" + tempNodeType + "'>")
  for temp in allDecAttrs:
  	if temp[(len(temp)-8):(len(temp)+1)] != " (Group)":
		temp = temp.replace("      ", "")
		temp = temp.replace(" *","")
		name = cmds.attributeQuery(temp, n=tempNode,ln=True)
		
		tempType = cmds.getAttr (tempNode+'.'+temp, type=True)
		if tempType == None:
			tempType = "None"
		tFile.write("\n                <attribute name='" + name + "' type='maya." + tempType+ "'>\n")
		label = re.sub("([a-z])([A-Z])","\g<1> \g<2>",name)
		tmpSplit = label.split(" ")
		tmpLabel = ""
		for tmp in tmpSplit:
			if tmpLabel != "":
				space = " "
			else:
				space=""
			tmpLabel=tmpLabel + space + tmp.capitalize()
		tFile.write("                        <label>" + tmpLabel + "</label>\n")
		tFile.write("                </attribute>\n")
		if (cmds.menuItem(verbMenuI, q=1, checkBox = True)) == True:
			print ('  - Declare Attribute ' + name)

  tFile.write("    </template>\n\n")
  for curTab in allTabs:
   	if (cmds.menuItem(verbMenuI, q=1, checkBox = True)) == True:
		print ('  - Create View ' + curTab)
   	tFile.write('    <view name="' + curTab + '" template="AE' + tempNodeType + '">\n')
    	currColChld = cmds.columnLayout(curTab,q=1, ca=1)
  	curList = ""
  	for temp in currColChld:
  		if cmds.textScrollList(temp, exists=True):
  			curList= temp
  	curTabItems = cmds.textScrollList(curList, q=1, ai=True)
	if curTabItems!=None:
		tempGrp = ""
		for curTabItem in curTabItems:
			if curTabItem[0] == " ":
				curTabItem = curTabItem.replace("      ", "")
				curTabItem = curTabItem.replace(" *","")
				
				tempKey = curTab + "_" + curTabItem
				if tempKey in dictCallbacks:
					tempCallback = dictCallbacks[tempKey]
					tFile.write(tempGrp + "                <property name='" + curTabItem + "'>\n")
					tFile.write(tempGrp + '                       <description language="cb">' + tempCallback + '</description>\n')
					tFile.write(tempGrp + "                </property>\n")
				else:
					tFile.write(tempGrp + "                <property name='" + curTabItem + "'/>\n")
			else:
				curTabItem = curTabItem.replace(" (Group)", "")
				if tempGrp == "       ":
					tFile.write("                </group>\n")
					tFile.write("                <group name='" + curTabItem + "'>\n")
				else:
					tempGrp = "       "
					tFile.write("                <group name='" + curTabItem + "'>\n")
		if tempGrp == "       ":
			tFile.write("                </group>\n")
	tFile.write("    </view>\n\n")
  tFile.write("</templates>\n")
  tFile.close()
  if cmds.checkBoxGrp(chkBox1,q=1,v1=1)==1:
   	if (cmds.menuItem(verbMenuI, q=1, checkBox = True)) == True:
		print ('  - Adding "' +  tempPath + '" to Paths')
	tempTempPaths = mel.eval('getenv MAYA_CUSTOM_TEMPLATE_PATH')
	tmptst=""
	mel.eval('putenv "MAYA_CUSTOM_TEMPLATE_PATH" "' + tempPath + '; ' + tempTempPaths + '"')
	tempTempPaths = mel.eval('getenv MAYA_SCRIPT_PATH')
	mel.eval('putenv "MAYA_SCRIPT_PATH" "' + tempPath + '; ' + tempTempPaths + '"')
	sys.path.append(tempPath)
  cmds.confirmDialog(button="OK", message="\nTEMPLATE SAVED\n\n" + tempFileName + "\n\nYou may need to run a 'refreshCustomTemplate' command\nto see the results of the new template.")
  print "--------------\nTemplate Saved\n--------------"
  print "File: " + tempFileName + "\n"
  

 cmds.menuItem(verbMenuI, e=1, c=simpleTemplateVerbMode)
 cmds.textFieldButtonGrp(txtFldButGrp1,e=1, bc=simpleTemplateEditorBrowse )
 cmds.checkBoxGrp(chkBox2, e=1, cc=simpleTemplateEditorNodeNameEnable)
 cmds.button(butt2, e=1, c=simpleTemplateEditorAddView)
 cmds.button(butt3, e=1, c=simpleTemplateEditorDupeView)
 cmds.button(butt4, e=1, c=simpleTemplateEditorDelView)
 cmds.button(butt5, e=1, c=simpleTemplateEditorCreateViews)
 cmds.button(butt6, e=1, c=simpleTemplateEditorResetTemplate)
 cmds.button(butt7, e=1, c=simpleTemplateEditorCancel)
 cmds.iconTextButton(iconButt1, e=1, command = simpleTemplateEditorAddAttrs)
 cmds.iconTextButton(iconButt2, e=1, command = simpleTemplateEditorRemAttrs)
 cmds.iconTextButton(iconButt3, e=1, command = simpleTemplateEditorUpAttrs)
 cmds.iconTextButton(iconButt4, e=1, command = simpleTemplateEditorDownAttrs)
 cmds.iconTextButton(iconButt5, e=1, command = simpleTemplateEditorNewGrp)
 cmds.window(window, e=True, wh=[666,596])
 simpleTemplateEditorResetTemplate()
 cmds.showWindow(window)
 cmds.tabLayout(tabs1,e=1,sti=1)
#simpleTemplateEditorUI()
