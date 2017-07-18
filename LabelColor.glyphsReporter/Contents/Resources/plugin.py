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


alpha = .9
labelColorsDict = {
	0 : (0.93, 0.57, 0.47, alpha), # red
	1 : (0.98, 0.79, 0.51, alpha), # orange
	2 : (0.84, 0.76, 0.62, alpha), # brown
	3 : (0.98, 0.98, 0.51, alpha), # yellow
	4 : (0.80, 0.96, 0.63, alpha), # light green
	5 : (0.48, 0.76, 0.46, alpha), # dark green
	6 : (0.47, 0.82, 0.96, alpha), # light blue
	7 : (0.60, 0.61, 0.91, alpha), # dark blue
	8 : (0.71, 0.52, 0.89, alpha), # purple
	9 : (0.98, 0.63, 0.82, alpha), # magenta
	10 : (0.86, 0.86, 0.86, alpha), # light gray
	11 : (0.56, 0.56, 0.56, alpha), # charcoal
	9223372036854775807 : (1, 1, 1, 0), # not colored, white
}

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

	### Italic Angle Stuff
	def angle(self, yPos, thisXHeight, thisAngle):
		# rotation point is half of x-height
		offset = math.tan(math.radians(thisAngle)) * thisXHeight/2
		shift = math.tan(math.radians(thisAngle)) * yPos - offset
		return shift

	
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
				upm = thisFont.upm
				thisAngle = thisMaster.italicAngle

				glyphColor.colorWithAlphaComponent_(alpha).set()

				if drawingOption == "Label Size":
					rectangle = [0, 0, thisWidth, -40]
				elif drawingOption == "Label Size Descender":
					rectangle = [0, thisDescender, thisWidth, thisDescender-40]
					rectangleLeft = [0, thisDescender, thisWidth/2, thisDescender-40]
					rectangleRight = [thisWidth/2, thisDescender, thisWidth, thisDescender-40]
				elif drawingOption == "Full Glyph Body":
					ySize = upm+thisDescender
					rectangle = [0, thisDescender, thisWidth, ySize]
				
				if layerColor != None:
					'''
					LEFT = Glyph-Color
					'''
					pathRectLeft = NSBezierPath.bezierPath()
					pathRectLeft.moveToPoint_( (rectangleLeft[0] + self.angle(rectangleLeft[1], thisXHeight, thisAngle), rectangleLeft[1]) )
					pathRectLeft.lineToPoint_( (rectangleLeft[0] + self.angle(rectangleLeft[3], thisXHeight, thisAngle), rectangleLeft[3]) )
					pathRectLeft.lineToPoint_( (rectangleLeft[2] + self.angle(rectangleLeft[3], thisXHeight, thisAngle), rectangleLeft[3]) )
					pathRectLeft.lineToPoint_( (rectangleLeft[2] + self.angle(rectangleLeft[1], thisXHeight, thisAngle), rectangleLeft[1]) )
					pathRectLeft.closePath()

					pathRectLeft.fill()

					'''
					RIGHT = Layer-Color
					'''
					pathRectRight = NSBezierPath.bezierPath()
					pathRectRight.moveToPoint_( (rectangleRight[0] + self.angle(rectangleRight[1], thisXHeight, thisAngle), rectangleRight[1]) )
					pathRectRight.lineToPoint_( (rectangleRight[0] + self.angle(rectangleRight[3], thisXHeight, thisAngle), rectangleRight[3]) )
					pathRectRight.lineToPoint_( (rectangleRight[2] + self.angle(rectangleRight[3], thisXHeight, thisAngle), rectangleRight[3]) )
					pathRectRight.lineToPoint_( (rectangleRight[2] + self.angle(rectangleRight[1], thisXHeight, thisAngle), rectangleRight[1]) )
					pathRectRight.closePath()

					layerColor.colorWithAlphaComponent_(alpha).set()
					pathRectRight.fill()
				else:
					## using a bezier path instead of an NSRect for transforming ability
					pathRect = NSBezierPath.bezierPath()
					pathRect.moveToPoint_( (rectangle[0] + self.angle(rectangle[1], thisXHeight, thisAngle), rectangle[1]) )
					pathRect.lineToPoint_( (rectangle[0] + self.angle(rectangle[3], thisXHeight, thisAngle), rectangle[3]) )
					pathRect.lineToPoint_( (rectangle[2] + self.angle(rectangle[3], thisXHeight, thisAngle), rectangle[3]) )
					pathRect.lineToPoint_( (rectangle[2] + self.angle(rectangle[1], thisXHeight, thisAngle), rectangle[1]) )
					pathRect.closePath()

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
