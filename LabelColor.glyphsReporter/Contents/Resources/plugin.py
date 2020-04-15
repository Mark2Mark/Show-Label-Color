#!/usr/bin/env python
# encoding: utf-8
from __future__ import division, print_function, unicode_literals

'''
• See OPTION below to either use Label Size or Whole Glyph Body.
'''

# TODO:
#	add clipping path https://developer.apple.com/library/mac/documentation/Cocoa/Reference/ApplicationKit/Classes/NSBezierPath_Class/#//apple_ref/doc/uid/20000339-SW27

import objc
from GlyphsApp.plugins import *
from math import tan, pi
import traceback

#### OPTIONS +++++++++++++++++++++++++++++++++++++++++
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
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Label Color',
			'de': 'Etikettenfarbe',
			'fr': 'couleur d’etiquette',
			'es': 'color de etiqueta',
		})
	
	@objc.python_method
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

	@objc.python_method
	def LabelColor( self, Layer ):
		try:
			glyphColor = None
			layerColor = None
				
			try:
				glyphColor = Layer.parent.colorObject
			except:
				pass
				
			try:
				layerColor = Layer.colorObject # Layer.color()
			except:
				# Glyphs 1.x or no layerColor:
				pass

			if layerColor and not glyphColor:
				glyphColor = layerColor
				layerColor = None

			if glyphColor is None:
				return
			try:
				thisWidth = Layer.width
				thisGlyph = Layer.parent
				thisFont = thisGlyph.parent
				thisMaster = Layer.master
				thisDescender = thisMaster.descender
				thisXHeight = thisMaster.xHeight
				thisAngle = thisMaster.italicAngle
				if abs(thisAngle) > 0.001:
					transform = NSAffineTransform.alloc().init()
					slant = tan(thisAngle * pi / 180.0)
					transform.shearXBy_atCenter_(slant, thisXHeight*0.5)
				else:
					transform = None

				glyphColor.colorWithAlphaComponent_(alpha).set()

				if drawingOption == "Label Size":
					rectangle = NSMakeRect(0, 0, thisWidth, -40)
				elif drawingOption == "Label Size Descender":
					rectangle = NSMakeRect(0, thisDescender - 40, thisWidth, 40)
					rectangleLeft = NSMakeRect(0, thisDescender - 40, thisWidth/2, 40)
					rectangleRight = NSMakeRect(thisWidth/2, thisDescender - 40, thisWidth/2, 40)
				elif drawingOption == "Full Glyph Body":
					rectangle = NSMakeRect(0, thisDescender, thisWidth, thisMaster.ascender - thisDescender)

				if not layerColor is None:
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
				print(traceback.format_exc())
		except:
			print(traceback.format_exc())

	@objc.python_method
	def background( self, layer ):
		"""
		Whatever you draw here will be displayed BEHIND the paths.
		"""
		try:
			self.LabelColor( layer )
			# self.BlockOutGlyph( Layer )
		except:
			print(traceback.format_exc())

	@objc.python_method
	def inactiveLayerBackground(self, layer):
		"""
		Whatever you draw here will be displayed behind the paths, but for inactive masters.
		"""
		try:
			self.LabelColor( layer )
			# self.BlockOutGlyph( Layer )
		except:
			print(traceback.format_exc())

	@objc.python_method
	def preview( self, layer ):
		"""
		Whatever you draw here will be displayed BEHIND the paths.
		"""
		try:
			self.LabelColor( layer )
			# self.BlockOutGlyph( Layer )
		except:
			print(traceback.format_exc())

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
	# 	# print(myLog)
	# 	NSLog( myLog )

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
