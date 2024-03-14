from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from buyokapp.yandex_api import get_content
import buyokapp.design as design
import sys
from buyokapp.model import Metrics, session
from PyQt5 import QtCore
from sqlalchemy import create_engine, text
import buyokapp.config as config
import sys


class MyApp(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show_table()
        self.pushButton_search.clicked.connect(self.search_metric)
        self.pushButton_search.clicked.connect(self.show_map)

    def show_map(self):
        ll = f'{self.lineEdit_long.text()},{self.lineEdit_latt.text()}'
        url = 'http://static-maps.yandex.ru/1.x/'
        radios = [self.radioButton_scheme, self.radioButton_sat, self.radioButton_hybr]
        radio_dict = {'Схема': 'map', 'Спутник': 'sat', 'Гибрид': 'sat,skl'}
        for r in radios:
            if r.isChecked():
                l = radio_dict[r.text()]
                break
        params = {
            'll': ll,
            'l': l,
            'z': self.lineEdit_scale.text(),
            'size': '600,400'
        }
        response = get_content(url, params).content
        with open("response.jpg", "wb") as f:
            f.write(response)
        pixmap = QPixmap("response.jpg")
        pixmap = pixmap.scaled(600, 400)
        self.label_map.setPixmap(pixmap)

    def search_metric(self):
        self.tableWidget.itemChanged.disconnect()
        input_year = self.lineEdit_search.text()
        self.show_table(input_year)

    def show_table(self, update=False): #filter=None
        engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
        connect = engine.connect()
        # if filter:  # новое название, изменить везде
        #     all_rows = connect.execute(f'SELECT * FROM metrics where year = {filter}').all()
        # else:
        all_rows = connect.execute(text('SELECT * FROM metrics')).all()
        self.tableWidget.setRowCount(len(all_rows))
        self.tableWidget.setColumnCount(4)
        for i, row in enumerate(all_rows):
            id_ = QTableWidgetItem(str(row[0]))
            id_.setFlags(QtCore.Qt.ItemIsEnabled)
            time = QTableWidgetItem(str(row[1]))
            ll = QTableWidgetItem(row[2])
            depth = QTableWidgetItem(str(row[3]))
            self.tableWidget.setItem(i, 0, id_)
            self.tableWidget.setItem(i, 1, time)
            self.tableWidget.setItem(i, 2, ll)
            self.tableWidget.setItem(i, 3, depth)
        self.tableWidget.resizeColumnsToContents()
    #     self.tableWidget.itemChanged.connect(self.update_db)
    #
    # def update_db(self):
    #     row = self.tableWidget.currentRow()
    #     row = [self.tableWidget.item(row, col).text() for col in range(4)]
    #     engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    #     connect = engine.connect()
    #     connect.execute(f'UPDATE metrics SET time = {row[1]}, ll = "{row[2]}", depth = "{row[2]}" where id = {row[0]}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())

# 59.57
# 30.18
