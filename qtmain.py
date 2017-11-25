#--coding:utf-8--
from qtheader import *
import sys
from qtmainframe import MainFrame

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(json_reader.buildPath('icon.gif')))
m = MainFrame(app)
sys.exit(app.exec_())