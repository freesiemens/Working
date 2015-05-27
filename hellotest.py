# -*- coding: utf-8 -*-
"""
Created on Wed May 20 15:08:09 2015

@author: rbanderson
"""
import sys

sys.stdout = open("my_stdout.log", "w")
sys.stderr = open("my_stderr.log", "w")

import PySide.QtGui
from PySide.QtGui import QApplication
from PySide.QtGui import QMessageBox


# Create the application object
app = QApplication(sys.argv)

# Create a simple dialog box
msgBox = QMessageBox()
msgBox.setText("Hello World - using PySide version " + PySide.__version__)
msgBox.exec_()