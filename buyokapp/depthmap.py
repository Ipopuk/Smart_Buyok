from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import buyokapp.depthmap_design as depthmap_design
from buyokapp.model import Metrics, session
from sqlalchemy import create_engine, text
import buyokapp.config as config
import sys
from PyQt5 import QtCore



class MyAppDepthMap(QMainWindow, depthmap_design.Ui_MainWindow):
    def __init__(self, parent=None):
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.setupUi(self)
        self.show_table()
        self.navigation_map.triggered.connect(self.show_navigationmap)
        self.depth_map.triggered.connect(self.show_depthmap)
        self.controller.triggered.connect(self.show_controller)


    def show_navigationmap(self):
        from buyokapp.navigation import MyApp
        window_navigationmap = MyApp(self)
        self.hide()
        window_navigationmap.show()

    def show_depthmap(self):
        window_depthmap = MyAppDepthMap(self)
        self.hide()
        window_depthmap.show()

    def show_controller(self):
        from buyokapp.controller import MyAppController
        window_controller = MyAppController(self)
        self.hide()
        window_controller.show()


    def search_metric(self):
        # self.tableWidget.itemChanged.disconnect()
        id = self.lineEdit.text()
        self.show_table(id)

    def show_table(self, filter=None, update=False):  # filter=None
        engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
        connect = engine.connect()
        if filter:  # новое название, изменить везде
            all_rows = connect.execute(text(f'SELECT * FROM metrics where id = {filter}')).all()
        else:
            all_rows = connect.execute(text('SELECT * FROM metrics')).all()
        self.tableWidget_2.setRowCount(len(all_rows))
        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setHorizontalHeaderLabels(['id', 'll', 'depth'])
        for i, row in enumerate(all_rows):
            id_ = QTableWidgetItem(str(row[0]))
            id_.setFlags(QtCore.Qt.ItemIsEnabled)
            ll = QTableWidgetItem(row[2])
            depth = QTableWidgetItem(str(row[3]))
            self.tableWidget_2.setItem(i, 0, id_)
            self.tableWidget_2.setItem(i, 1, ll)
            self.tableWidget_2.setItem(i, 2, depth)

        self.tableWidget_2.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyAppDepthMap()
    window.show()
    sys.exit(app.exec())
