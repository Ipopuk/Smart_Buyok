from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import buyokapp.depthmap_design as depthmap_design
from buyokapp.model import Metrics, session
from sqlalchemy import create_engine, text
import buyokapp.config as config
import sys


class MyAppDepthMap(QMainWindow, depthmap_design.Ui_MainWindow):
    def __init__(self, parent=None):
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.setupUi(self)
        self.actionmain.triggered.connect(self.show_navigationmap)
        self.actiondepth_map.triggered.connect(self.show_depthmap)

    def show_navigationmap(self):
        from buyokapp.navigation import MyApp
        window_depthmap = MyApp(self)
        self.hide()
        window_depthmap.show()

    def show_depthmap(self):
        window_depthmap = MyAppDepthMap(self)
        self.hide()
        window_depthmap.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyAppDepthMap()
    window.show()
    sys.exit(app.exec())
