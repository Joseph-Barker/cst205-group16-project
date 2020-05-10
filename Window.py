"""
Boris Marin, Joseph Barker, Joseph Rivera, Rogelio Rodriguez, Ramiro Soto
CST 205 Project: Group 16
Window.py
5/4/2020
	This class handles the GUI display, button press, event slots, file selection.
"""

# Import required packages
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QComboBox, QMessageBox, QInputDialog, QLineEdit, QFileDialog, QTextEdit, QSlider, QAction, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5 import QtCore, Qt
from Image import Image


class Window(QWidget):
	"""Manages PyQt window"""

	# Initialises the window (object of the class)
	def __init__(self):
		super().__init__()
		self.setGeometry(350, 100, 1000, 700)
		self.setWindowTitle("Text Recognition")
		self.grid = QGridLayout(self)

		label = QLabel(self)
		label.setText("Image input")
		self.grid.addWidget(label, 0, 0)

		label1 = QLabel(self)
		label1.setText("Text output")
		self.grid.addWidget(label1, 0, 1)
		# Creates the check box
		box = QCheckBox("Output to the file")
		self.grid.addWidget(box, 2, 1)
		box.stateChanged.connect(self.check_box_change)
		# A string in case user wantes to output text to the file
		self.text_file_link = ""
		#setting for Image OTSU
		self.kernel_size = 20

	# handles the check box so the user may choose to output text to the file, and does not trigger then user unselects
	# the box
	def check_box_change(self):
		global box_change
		box_change = box_change + 1
		if box_change%2 != 0:
			options = QFileDialog.Options()
			options = QFileDialog.DontUseNativeDialog
			self.text_file_link = QFileDialog.getOpenFileName(self,"File dialog", "" , "Text files (*.txt)", options=options)

	# Creates the text box for the Kernel size setting
	def text_box(self, text):
		global kernel_change
		if (kernel_change == 0):
			self.label = QLabel(self)
		self.label.clear()
		self.label.setText(text)
		self.grid.addWidget(self.label, 4, 0)

	# Create text edit for to display extracted text output
	def text_edit(self, text, x_c, y_c, replace):
		if(replace == False):
			self.label_edit = QTextEdit(self)
		self.label_edit.setText(text)
		self.grid.addWidget(self.label_edit, x_c, y_c)

	# Creaes the slider for kernel ajustment
	def slider_nob(self, x_c, y_c):
		slider = QSlider(self)
		slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
		slider.setMinimum(10)
		slider.setMaximum(75)
		slider.setValue(self.kernel_size)
		slider.setTickPosition(QSlider.TicksBelow)
		slider.setTickInterval(5)
		global kernel_change
		kernel_change = kernel_change + 1
		slider.valueChanged.connect(self.valuechange)
		self.grid.addWidget(slider, x_c, y_c)

	# Outputs the text to the file or to the text edit box in the program.
	def text_output(self, text, replace):
		global box_change
		if box_change%2 != 0:
			self.text_file = open(str(self.text_file_link[0]), "w+")
			self.text_file.write(text)
			self.text_file.close()
		self.text_edit(text, 1, 1, replace)

	# Places the image to its spot in the program.
	def place_im(self, text):
		im = QPixmap(text)
		try:
			# Calulates the ratio, so the image can be slaced with proper ratio
			ratio = im.height()/im.width()

			if(im.height() > 400 and im.width() > 600):
				im = im.scaled(600, (600*ratio))
			else:
				im = im.scaled(400, (400*ratio))
			global event
			if event == 1:
				self.label_im = QLabel()
			self.label_im.clear()
			self.label_im.setPixmap(im)
			self.grid.addWidget(self.label_im,1,0)
		except:
			print("No image selected")

	# Allows user to open the image file, without a need to write a path for the file
	def openFileNameDialog(self):
		global link
		global event
		options = QFileDialog.Options()
		options = QFileDialog.DontUseNativeDialog
		fileName = QFileDialog.getOpenFileName(self,"File dialog", "" , "Image files (*.jpg)", options=options)
		if fileName:
			# records the path to the image
			link = fileName[0]
			# Counts the events so images do not stack on top of each other
			event = event + 1
			self.place_im(link)
			ImageFile = Image(link, self, self.kernel_size)
			ImageFile.process_image()
			ImageFile.produce_results()

	# Method called when slider state change
	def valuechange(self, state):
		self.kernel_size = state
		self.text_box("Kernel size: " + str(window.kernel_size))

	# Called when the exit button is pressed so the program exits
	def exit(self):
		QApplication.quit()

	# The function that crates Quit and Open file buttons
	def button(self, text, x_c, y_c):
		button = QPushButton(text)
		self.grid.addWidget(button, x_c, y_c)
		if(text == "Open file"):
			button.clicked.connect(self.openFileNameDialog)
		else:
			button.clicked.connect(self.exit)

app = QApplication(sys.argv)
# Counts the changes of the check box, so the file diolog will not be triggered on unselection of the check box
box_change = 0
# Counts the events for image replacement, so the images do not stack on top of each other
event = 0
# Counts the events of the change of the kernel veriable, so the numbers do not stack on top of each other
kernel_change = 0
# Stores the link to the image
link = ""

window = Window()
window.button("Open file", 5, 0)
window.button("Quit", 5, 1)
window.text_box("Kernel size: " + str(window.kernel_size))
window.text_edit("Text output here", 1, 1, replace = False)
window.slider_nob(3,0)

window.show()
sys.exit(app.exec())
