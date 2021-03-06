"""
Boris Marin, Joseph Barker, Joseph Rivera, Rogelio Rodriguez, Ramiro Soto
CST 205 Project: Group 16
Image.py
4/30/2020
    This class handles a given image file from the user.
    The image is analyzed for text and processed by pytesseract
"""
#Main code adapted from AnandhJagadeesan - Text Detection and Extraction using OpenCV and OCR
#https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/

# Import required packages
import cv2
import pytesseract
from Text import Text

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

class Image:
	"""Image class to which text is extracted"""

	def __init__( self, file_path, app_window, kernel_size ):

		# instance variables unique to each instance
		self.file_path = file_path
		self.app_window = app_window
		self.text = ""
		self.kernel_size = kernel_size
		
		# Read image from which text needs to be extracted
		self.file = cv2.imread( self.file_path )

	# A method for processing data members
	def process_image(self):

		try:
			# Convert the image to gray scale
			self.gray = cv2.cvtColor( self.file, cv2.COLOR_BGR2GRAY )

			# Performing OTSU threshold
			self.ret, self.thresh1 = cv2.threshold(self.gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

			# Specify structure shape and kernel size.
			# Kernel size increases or decreases the area
			# of the rectangle to be detected.
			# A smaller value like (10, 10) will detect
			# each word instead of a sentence.
			self.rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.kernel_size, self.kernel_size))


			# Appplying dilation on the threshold image
			self.dilation = cv2.dilate( self.thresh1, self.rect_kernel, iterations = 1)

			# Finding contours
			self.contours, self.hierarchy = cv2.findContours( self.dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
		except:
			print("An exception occurred when processing the image")


	def produce_results(self):
		try:
			# Creating a copy of image
			self.file2 = self.file.copy()

			# Looping through the identified contours
			# Then rectangular part is cropped and passed on
			# to pytesseract for extracting text from it
			# Extracted text is then written into the text file
			for self.cnt in reversed( self.contours ):
				self.x, self.y, self.w, self.h = cv2.boundingRect(self.cnt)

				# Drawing a rectangle on copied image
				self.rect = cv2.rectangle( self.file2, ( self.x, self.y ), ( self.x + self.w, self.y + self.h), (0, 255, 0), 2)

				# Cropping the text block for giving input to OCR
				self.cropped = self.file2[ self.y:self.y + self.h, self.x:self.x + self.w]

				# Apply OCR on the cropped image
				self.text += pytesseract.image_to_string(self.cropped)
				self.text += "\n"

			ImageText = Text( self.text, self.app_window)
		except:
			print("An exception occurred when producing results")
