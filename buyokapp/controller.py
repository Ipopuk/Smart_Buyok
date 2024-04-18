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
        self.pushButton_grid_up.clicked.connect(self.grid_up)
        self.pushButton_grid_down.clicked.connect(self.grid_down)
        self.pushButton_turn_up.clicked.connect(self.turn_up)
        self.pushButton_turn_down.clicked.connect(self.turn_down)
    def grid_up(self):
        x = int(self.grid_line_edit.text()[:-1])
        if x < 100:
            self.grid_line_edit.setText(str(x+20) + '%')
        else:
            self.grid_line_edit.setText(str(x) + '%')


    def grid_down(self):
        x = int(self.grid_line_edit.text()[:-1])
        if x > 0:
            self.grid_line_edit.setText(str(x-20) + '%')
        else:
            self.grid_line_edit.setText(str(x) + '%')

    def turn_up(self):
        x = int(self.turn_line_edit.text()[:-1])
        self.turn_line_edit.setText(str(x + 45)+'°')

    def turn_down(self):
        x = int(self.turn_line_edit.text()[:-1])
        self.turn_line_edit.setText(str(x - 45) +'°')


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
