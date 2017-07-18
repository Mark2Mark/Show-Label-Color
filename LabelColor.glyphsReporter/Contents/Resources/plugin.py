#!/usr/bin/env python
# encoding: utf-8

'''
• See OPTION below to either use Label Size or Whole Glyph Body.
'''

# TODO:
#	add clipping path https://developer.apple.com/library/mac/documentation/Cocoa/Reference/ApplicationKit/Classes/NSBezierPath_Class/#//apple_ref/doc/uid/20000339-SW27

from GlyphsApp.plugins import *
import objc
# from Foundation import *
from AppKit import *
import sys, os, re
import math
import traceback

#### OTIONS ++++++++++++++++++++++++++++++++++++++++++
#### #######++++++++++++++++++++++++++++++++++++++++++
# drawingOption = "Label Size"
drawingOption = "Label Size Descender"
# drawingOption = "Full Glyph Body"
#### #######++++++++++++++++++++++++++++++++++++++++++
#### #######++++++++++++++++++++++++++++++++++++++++++

alpha = 0.9
if drawingOption == "Full Glyph Body":
	alpha = 0.5

class LabelColor (ReporterPlugin):
	def settings(self):
		self.menuName = Glyphs.localize({'en': u'Label Color', 'de': u'Label Farbe'})

	def BlockOutGlyph( self, Layer ):
		if drawingOption == "Label Size":
			pass
		elif drawingOption == "Full Glyph Body":
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 1, 1, 1, 1 ).set()
			try:
				thisGlyphPath = Layer.copyDecomposedLayer().bezierPath()
			except:
				thisGlyphPath = Layer.copyDecomposedLayer().bezierPath
			if thisGlyphPath:
				thisGlyphPath.fill()
	
	def LabelColor( self, Layer ):
		try:
			try:
				glyphColor = Layer.parent.colorObject
			except:
				glyphColor = None
			try:
				layerColor = Layer.colorObject # Layer.color()
			except:
				# Glyphs 1.x or no layerColor:
				layerColor = None
			
			if layerColor and not glyphColor:
				glyphColor = layerColor
				layerColor = None
			
			try:
				thisWidth = Layer.width
				thisGlyph = Layer.parent
				thisFont = thisGlyph.parent
				thisMaster = thisFont.selectedFontMaster
				thisDescender = thisMaster.descender
				thisXHeight = thisMaster.xHeight
				thisAngle = thisMaster.italicAngle
				if abs(thisAngle) > 0.001:
					transform = NSAffineTransform.alloc().init()
					slant = math.tan(thisAngle * math.pi / 180.0)
					transform.shearXBy_atCenter_(slant, thisXHeight / -2.0)
				else:
					transform = False
				
				glyphColor.colorWithAlphaComponent_(alpha).set()
				
				if drawingOption == "Label Size":
					rectangle = NSMakeRect(0, 0, thisWidth, -40)
				elif drawingOption == "Label Size Descender":
					rectangle = NSMakeRect(0, thisDescender - 40, thisWidth, 40)
					rectangleLeft = NSMakeRect(0, thisDescender - 40, thisWidth/2, 40)
					rectangleRight = NSMakeRect(thisWidth/2, thisDescender - 40, thisWidth, 40)
				elif drawingOption == "Full Glyph Body":
					rectangle = NSMakeRect(0, thisDescender, thisWidth, thisMaster.ascender - thisDescender)
				
				if layerColor != None:
					'''
					LEFT = Glyph-Color
					'''
					pathRectLeft = NSBezierPath.bezierPathWithRect_(rectangleLeft)
					if transform:
						pathRectLeft.transformUsingAffineTransform_(transform)
					pathRectLeft.fill()
					
					'''
					RIGHT = Layer-Color
					'''
					layerColor.colorWithAlphaComponent_(alpha).set()
					pathRectRight = NSBezierPath.bezierPathWithRect_(rectangleRight)
					if transform:
						pathRectRight.transformUsingAffineTransform_(transform)
					pathRectRight.fill()
				else:
					pathRect = NSBezierPath.bezierPathWithRect_(rectangle)
					if transform:
						pathRect.transformUsingAffineTransform_(transform)
					pathRect.fill()
			except:
				print traceback.format_exc()
		except:
			print traceback.format_exc()
			
	def background( self, layer ):
		"""
		Whatever you draw here will be displayed BEHIND the paths.
		"""
		try:
			self.LabelColor( layer )
			# self.BlockOutGlyph( Layer )
		except:
			print traceback.format_exc()
	
	def inactiveLayers(self, layer):
		"""
		Whatever you draw here will be displayed behind the paths, but for inactive masters.
		"""
		try:
			self.LabelColor( layer )
			# self.BlockOutGlyph( Layer )
		except:
			print traceback.format_exc()
	
	def needsExtraMainOutlineDrawingForInactiveLayer_( self, Layer ):
		return True
	
	# def setController_( self, Controller ):
	# 	"""
	# 	Use self.controller as object for the current view controller.
	# 	"""
	# 	try:
	# 		self.controller = Controller
	# 	except Exception as e:
	# 		self.logToConsole( "Could not set controller" )
	
	# def logToConsole( self, message ):
	# 	"""
	# 	The variable 'message' will be passed to Console.app.
	# 	Use self.logToConsole( "bla bla" ) for debugging.
	# 	"""
	# 	myLog = "Show %s plugin:\n%s" % ( self.title(), message )
	# 	# print myLog
	# 	NSLog( myLog )
