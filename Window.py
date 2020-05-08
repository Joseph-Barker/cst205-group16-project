"""
Boris Marin, Joseph Barker, Joseph Rivera, Rogelio Rodriguez, Ramiro Soto
CST 205 Project: Group 16
Window.py
5/4/2020
    This class handles the GUI display, button press, event slots, file selection.
"""

# Import required packages
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QComboBox, QMessageBox, QInputDialog, QLineEdit, QFileDialog, QTextEdit, QSlider, QAction
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
		label = QLabel(self)
		label.setText("Image input")
		self.grid.addWidget(label, 0, 0)
		label1 = QLabel(self)
		label1.setText("Text output")
		self.grid.addWidget(label1, 0, 1)

		#setting for Image OTSU
		self.kernel_size = 20

	def text_box(self, text):
		global kernel_change
		if (kernel_change == 0):
			self.label = QLabel(self)
		self.label.clear()
		self.label.setText(text)
		self.grid.addWidget(self.label, 3, 0)

	def text_edit(self, text, x_c, y_c):
		self.label_edit = QTextEdit(self)
		self.label_edit.setText(text)
		self.grid.addWidget(self.label_edit, x_c, y_c)

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


	def text_output(self, text):
		#manipulate text
		self.text_edit(text, 1, 1)

	def place_im(self, text):
		print(text)
		im = QPixmap(text)
		try:
			petio = im.height()/im.width()

			if(im.height() > 400 and im.width() > 600):
				im = im.scaled(600, (600*petio))
			else:
				im = im.scaled(400, (400*petio))
			global event
			if event == 1:
				self.label_im = QLabel()
			self.label_im.clear()
			self.label_im.setPixmap(im)
			self.grid.addWidget(self.label_im,1,0)
		except:
			print("No image selected")

	def openFileNameDialog(self):
		global link
		global event
		options = QFileDialog.Options()
		options = QFileDialog.DontUseNativeDialog
		fileName = QFileDialog.getOpenFileName(self,"File dialog", "" , "Image files (*.jpg)", options=options)
		# fileName = QFileDialog.getOpenFileName(self, options=options)
		if fileName:
			link = fileName[0]
			#print_link()
			event = event + 1
			self.place_im(link)
			print(link)
			ImageFile = Image(link, self, self.kernel_size)
			ImageFile.process_image()
			ImageFile.produce_results()

	def valuechange(self, state):
		self.kernel_size = state
		self.text_box("Kernel size: " + str(window.kernel_size))

	def exit(self):
		QApplication.quit()

	def button(self, text, x_c, y_c):
		button = QPushButton(text)
		self.grid.addWidget(button, x_c, y_c)
		if(text == "Open file"):
			button.clicked.connect(self.openFileNameDialog)
		else:
			button.clicked.connect(self.exit)

app = QApplication(sys.argv)
event = 0
kernel_change = 0
text_change = 0
link = "test.jpg"
window = Window()
# file_input_window = FileInput()
window.button("Open file", 4, 0)
window.button("Quit", 4, 1)
window.place_im(link)
#window.text_box("Image input", 0, 0)
window.text_box("Kernel size: " + str(window.kernel_size))
window.text_edit("Text output here", 3, 1)
window.slider_nob(2,0)


# link = window.file_input()

window.show()
sys.exit(app.exec())
