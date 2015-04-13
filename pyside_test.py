# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 15:03:50 2015

@author: rbanderson
"""

import sys
import PySide
from PySide.QtGui import QApplication
from PySide.QtGui import QMessageBox
app=QApplication.instance()
if app is None:
    app=QApplication(sys.argv)
msgBox=QMessageBox()
msgBox.setText("Hello World - using PySide version "+PySide.__version__)
msgBox.exec_()
app.exit()
