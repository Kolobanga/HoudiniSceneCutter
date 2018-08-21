import sys

try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
try:
    import hou
except ImportError:
    pass


class SceneCutterPanel(QWidget):
    def __init__(self, parent=None):
        super(SceneCutterPanel, self).__init__(parent)

        self.setWindowTitle('Scene Cutter')
        self.setProperty("houdiniStyle", True)
        self.__previousFrame = 0

        # Layout
        QGridLayout(self)

        # Buttons
        self.addCutButton = QPushButton('Add Cut')
        self.addCutButton.clicked.connect(self.addCut)
        self.layout().addWidget(self.addCutButton, 0, 0, 1, 1)

        self.runButton = QPushButton('Run')
        self.runButton.clicked.connect(self.run)
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

    def addCut(self):
        itemFrom = QTableWidgetItem(str(self.__previousFrame + 1))
        itemFrom.setFlags(itemFrom.flags() | Qt.ItemIsUserCheckable)
        itemFrom.setCheckState(Qt.Checked)
        itemTo = QTableWidgetItem(str(hou.intFrame()))
        targetRow = self.table.rowCount()
        self.table.insertRow(targetRow)
        self.table.setItem(targetRow, 0, itemFrom)
        self.table.setItem(targetRow, 1, itemTo)
        self.__previousFrame = hou.intFrame()

    def run(self):
        raise NotImplementedError


def onCreateInterface():
    global sceneCutter
    sceneCutter = SceneCutterPanel()
    return sceneCutter


def onDestroyInterface():
    global sceneCutter
    sceneCutter.cleanup()


if __name__ == '__main__':
    def my_excepthook(type, value, tback):
        sys.__excepthook__(type, value, tback)


    sys.excepthook = my_excepthook

    app = QApplication([])
    window = SceneCutterPanel()
    window.show()
    sys.exit(app.exec_())
