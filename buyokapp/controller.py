from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import buyokapp.depthmap_design as depthmap_design
from buyokapp.model import Metrics, session
from sqlalchemy import create_engine, text
import buyokapp.config as config
import sys
import buyokapp.controller_design as controller_design


class MyAppController(QMainWindow, controller_design.Ui_Controller):
    def __init__(self, parent=None):
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.setupUi(self)
        self.navigation_map.triggered.connect(self.show_navigationmap)
        self.depth_map.triggered.connect(self.show_depthmap)
        self.controller.triggered.connect(self.show_controller)

    def show_controller(self):
        window_controller = MyAppController(self)
        self.hide()
        window_controller.show()

    def show_depthmap(self):
        from buyokapp.depthmap import MyAppDepthMap
        window_depthmap = MyAppDepthMap(self)
        self.hide()
        window_depthmap.show()

    def show_navigationmap(self):
        from buyokapp.navigation import MyApp
        window_navigationmap = MyApp(self)
        self.hide()
        window_navigationmap.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyAppController()
    window.show()
    sys.exit(app.exec())