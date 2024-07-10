from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenuBar, QMenu, QAction,
                             QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox,
                             QComboBox, QListWidget, QWidget,
                             QAbstractItemView, QCompleter,
                             QSizePolicy, QMessageBox, QPushButton, QFileDialog, QListWidgetItem, QToolButton, QDialog,
                             QTextEdit, QSpacerItem)

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtCore import QAbstractListModel, QItemSelectionModel
from rbpop import *


class UISupport:
    def __init__(self):
        self.app = QApplication([])

    def __del__(self):
        self.app.quit()


