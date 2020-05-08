"""
Boris Marin, Joseph Barker, Joseph Rivera, Rogelio Rodriguez, Ramiro Soto
CST 205 Project: Group 16
Text.py
5/8/2020
    This class is responsible for handling text extracted from image.
"""

class Text:
	"""A simple class to define text extracted from an image"""

	def __init__( self, text, app_window ):
		# instance variables unique to each instance
		self.text = text
		self.app_window = app_window

		self.app_window.text_output(text)

