import sys
from PyQt5 import *
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication


app = QApplication(sys.argv)
web = QWebEngineView()
web.load(QUrl("http://127.0.0.1:8000/TaskManager/"))
web.resize(800, 900)
web.setWindowTitle("Task manager")
web.show()
sys.exit(app.exec_())
