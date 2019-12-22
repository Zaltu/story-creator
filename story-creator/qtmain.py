"""
Main entry module for the application.
"""
#pylint: disable=no-name-in-module
import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QIcon
from libs import json_reader
from qtmainframe import MainFrame

APP = QApplication(sys.argv)
APP.setWindowIcon(QIcon(json_reader.buildPath('icon.gif')))
MAINF = MainFrame(APP)
sys.exit(APP.exec_())
