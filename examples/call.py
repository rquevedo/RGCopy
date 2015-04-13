from ui_RQCopy import Ui_MainWindow
import sys
import gtk
import signal
import os
from subprocess import PIPE, Popen
from threading  import Thread
from PyQt4 import QtCore, QtGui
from process import Process
import gobject

class Copy():

	def __init__(self, direction):
		self.dir = direction
		self.dest = None
		self.porcent = 0
		self.process = Process(self)


class MyForm(QtGui.QMainWindow):
       
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


copy1 = Copy('/home/reisy/Videos/nuevos/El Club de la Comedia 1x01.avi')
copy1.dest = '/home/reisy/Desktop'

def update(data):
	f.ui.pb_single_file.setValue(copy1.porcent)

	return True

def handleButton(self):
	copy1.process.start()

if __name__ == "__main__":
	
	
	app = QtGui.QApplication(sys.argv)
	f = MyForm()

	f.ui.btn_copy_to.clicked.connect(handleButton)

	# f.ui.pb_single_file.setValue(copy1.porcent)
	# gobject.idle_add(update, 1)

	f.show()
	sys.exit(app.exec_())
