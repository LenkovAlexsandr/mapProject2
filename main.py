import os
import sys
import requests
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit
from functions_geocode import get_toponym, get_coordinates

SCREEN_SIZE = [850, 500]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.coordinates = [44.269772, 46.307847]
        self.zoom = 15
        self.mod = ['map', 'sat', 'sat,skl']
        self.option = 0
        self.points = []
        self.map_file = "map.png"
        self.get_image()
        self.initUI()

    def get_image(self):
        map_params = {
            "ll": ','.join(list(map(str, self.coordinates))),
            "z": self.zoom,
            "l": self.mod[self.option],
            "pt": '~'.join(map(lambda x: x + ',vkbkm', self.points))
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def search(self):
        point = get_coordinates(get_toponym(self.search_value.text()))
        if point:
            if point not in self.points:
                self.points.append(point)
            self.coordinates = list(map(float, point.split(',')))
            self.get_image()
            self.image.setPixmap(QPixmap(self.map_file))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_PageUp:
            self.zoom += 1 if self.zoom < 19 else 0
        elif event.key() == QtCore.Qt.Key_PageDown:
            self.zoom -= 1 if self.zoom > 1 else 0
        elif event.key() == QtCore.Qt.Key_Left:
            self.coordinates[0] -= (0.0025 * 2 ** (17 - self.zoom)) / 2
        elif event.key() == QtCore.Qt.Key_Up:
            self.coordinates[1] += (0.0025 * 2 ** (17 - self.zoom)) / 2
        elif event.key() == QtCore.Qt.Key_Right:
            self.coordinates[0] += (0.0025 * 2 ** (17 - self.zoom)) / 2
        elif event.key() == QtCore.Qt.Key_Down:
            self.coordinates[1] -= (0.0025 * 2 ** (17 - self.zoom)) / 2
        if event.key() == QtCore.Qt.Key_Insert:
            self.option = (self.option + 1) % 3
        if self.coordinates[0] > 180:
            self.coordinates[0] = -360 + self.coordinates[0]
        elif self.coordinates[0] < -180:
            self.coordinates[0] = 360 + self.coordinates[0]
        if self.coordinates[1] > 85:
            self.coordinates[1] = -170 + self.coordinates[1]
        elif self.coordinates[1] < -85:
            self.coordinates[1] = 170 + self.coordinates[1]
        self.get_image()
        self.image.setPixmap(QPixmap(self.map_file))

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        # Изображение
        self.image = QLabel(self)
        self.image.resize(600, 450)
        self.image.setPixmap(QPixmap(self.map_file))

        #self.search_value = QLineEdit(self)
        #self.search_value.move(605, 10)
        #self.search_value.resize(240, 25)

        #self.search_button = QPushButton('Искать', self)
        #self.search_button.resize(80, 30)
        #self.search_button.move(765, 40)
        #self.search_button.clicked.connect(self.search)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
