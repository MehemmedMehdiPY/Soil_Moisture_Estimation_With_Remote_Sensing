from PyQt5.QtWidgets import QApplication
from gui import LaunchWIndow
import sys

app = QApplication(sys.argv)
window = LaunchWIndow()
window.show()
app.exec()