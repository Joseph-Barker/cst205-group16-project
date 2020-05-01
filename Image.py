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

# Mention the installed location of Tesseract-OCR in your system 
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

class Image:
	"""Image class to which text is extracted"""

	def __init__( self, file_path ):
		
		# instance variables unique to each instance
		self.file_path = file_path
		
		# Read image from which text needs to be extracted 
		self.file = cv2.imread( self.file_path )

	# A method for processing data members 
	def process_image(self):		  

		# Convert the image to gray scale 
		self.gray = cv2.cvtColor( self.file, cv2.COLOR_BGR2GRAY )		


		# Performing OTSU threshold 
		self.ret, self.thresh1 = cv2.threshold(self.gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

		# Specify structure shape and kernel size.  
		# Kernel size increases or decreases the area  
		# of the rectangle to be detected. 
		# A smaller value like (10, 10) will detect  
		# each word instead of a sentence. 
		self.rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))  


		# Appplying dilation on the threshold image 
		self.dilation = cv2.dilate( self.thresh1, self.rect_kernel, iterations = 1) 
		  
		# Finding contours 
		self.contours, self.hierarchy = cv2.findContours( self.dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	# A method for testing output text
	def output_text(self):		

		# Creating a copy of image
		self.file2 = self.file.copy() 
		  
		# A text file is created and flushed 
		self.text_file = open("./output/recognized.txt", "w+") 
		self.text_file.write("") 
		self.text_file.close()

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
		      
		    # Open the file in append mode 
		    self.text_file = open("./output/recognized.txt", "a") 
		      
		    # Apply OCR on the cropped image 
		    self.text = pytesseract.image_to_string(self.cropped) 
		      
		    # Appending the text into file 
		    self.text_file.write( self.text ) 
		    self.text_file.write("\n") 
		      
		    # Close the file 
		    self.text_file.close
