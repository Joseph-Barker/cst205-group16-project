"""
Boris Marin, Joseph Barker, Joseph Rivera, Rogelio Rodriguez, Ramiro Soto
CST 205 Project: Group 16
Window.py
5/4/2020
    This class handles the GUI display, button press, event slots, file selection.
"""

# Import required packages
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QComboBox, QMessageBox, QInputDialog, QLineEdit, QFileDialog, QTextEdit, QSlider
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5 import QtCore, Qt
from Image import Image

class Window(QWidget):
	"""Manages PyQt window"""
	
	def __init__(self):
		super().__init__()
		self.setGeometry(350, 100, 1000, 700) 
		self.setWindowTitle("Text Recognition")
		self.grid = QGridLayout(self)

		#setting for Image OTSU
		self.kernel_size = 20

	def text_box(self, text, x_c, y_c):
		label = QLabel(self)
		label.setText(text)
		self.grid.addWidget(label, x_c, y_c)

	def text_edit(self, text, x_c, y_c):
		label = QTextEdit(self)
		label.setText(text)
		self.grid.addWidget(label, x_c, y_c)

	def slider_nob(self, x_c, y_c):
		slider = QSlider(self)
		slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
		slider.setMinimum(10)
		slider.setMaximum(75)
		slider.setValue(self.kernel_size)
		slider.setTickPosition(QSlider.TicksBelow)
		slider.setTickInterval(5)
		slider.valueChanged.connect(self.valuechange)
		self.grid.addWidget(slider, x_c, y_c)


	def text_output(self, text):
		#manipulate text
		self.text_edit(text, 0, 1)

	def openFileNameDialog(self):
		global link
		options = QFileDialog.Options()
		options = QFileDialog.DontUseNativeDialog
		fileName = QFileDialog.getOpenFileName(self,"File dialog", "" , "Image files (*.jpg)", options=options)
		# fileName = QFileDialog.getOpenFileName(self, options=options)
		if fileName:
			link = fileName[0]
			#print_link()
			ImageFile = Image(link, self, self.kernel_size)
			ImageFile.process_image()
			ImageFile.produce_results()

	def valuechange(self, state):
		self.kernel_size = state
		self.text_box("Kernel size: " + str(window.kernel_size), 2, 0)

	def button(self):
		button = QPushButton("Open file")
		self.grid.addWidget(button, 3, 0)
		button.clicked.connect(self.openFileNameDialog)

app = QApplication(sys.argv)
link = "link sting no change"
window = Window()
# file_input_window = FileInput()
window.button()
window.text_box("Image input", 0, 0)
window.text_box("Kernel size: " + str(window.kernel_size), 2, 0)
window.text_edit("Text output", 0, 1)
window.slider_nob(1,0)


# link = window.file_input()

window.show()
sys.exit(app.exec())