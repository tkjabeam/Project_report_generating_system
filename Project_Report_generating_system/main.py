from PySide6.QtWidgets import QApplication
from widget import Mainwindow                   
import sys

app = QApplication(sys.argv)
widget = Mainwindow()
widget.show()
app.exec()