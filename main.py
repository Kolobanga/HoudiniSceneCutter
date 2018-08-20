import sys

from PyQt5.QtWidgets import QApplication

from panel import SceneCutterPanel

if __name__ == '__main__':
    def my_excepthook(type, value, tback):
        sys.__excepthook__(type, value, tback)


    sys.excepthook = my_excepthook

    app = QApplication([])
    window = SceneCutterPanel()
    window.show()
    sys.exit(app.exec_())
