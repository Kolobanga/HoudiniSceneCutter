try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *


class SceneCutterPanel(QWidget):
    def __init__(self, parent=None):
        super(SceneCutterPanel, self).__init__(parent)

        self.setWindowTitle('Scene Cutter')
        self.setProperty("houdiniStyle", True)

        # Layout
        QGridLayout(self)

        # Buttons
        self.addCutButton = QPushButton('Add Cut')
        self.layout().addWidget(self.addCutButton, 0, 0, 1, 1)

        self.runButton = QPushButton('Run')
        self.layout().addWidget(self.runButton, 0, 1, 1, 1)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(('From', 'To'))
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.menu)
        self.layout().addWidget(self.table, 1, 0, 1, 2)

        # Commands
        self.removeCutAction = QAction('Remove Cut', self)
        self.removeCutAction.setShortcut(QKeySequence(Qt.Key_Delete))
        self.removeCutAction.triggered.connect(self.removeCut)
        self.addAction(self.removeCutAction)

        # Menus
        self.tableContextMenu = QMenu()
        self.tableContextMenu.addAction(self.removeCutAction)

    def menu(self):
        self.tableContextMenu.exec_(QCursor.pos())

    def removeCut(self):
        index = self.table.currentRow()
        self.table.removeRow(index)

    def cleanup(self):
        self.table.clear()


def onCreateInterface():
    global sceneCutter
    sceneCutter = SceneCutterPanel()
    return sceneCutter


def onDestroyInterface():
    global sceneCutter
    sceneCutter.cleanup()
