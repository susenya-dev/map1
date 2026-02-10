import os
import sys

import requests
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt6.QtCore import Qt
SCREEN_SIZE = [600, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)
        self.num = 18
        self.ll = [37, 55]
        self.delta = 0.1
        self.getImage()
        self.setWindowTitle('Отображение карты')

    def getImage(self):
        map_params = {
            "apikey": 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13',
            "ll": ','.join(str(x) for x in self.ll),
            "z": self.num
        }
        server_address = 'https://static-maps.yandex.ru/v1?'
        response = requests.get(server_address, params=map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            # print()
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp and self.num < 21:
            self.num += 1
        if event.key() == Qt.Key.Key_PageDown and self.num > 0:
            self.num -= 1
        if event.key() == Qt.Key.Key_Right:
            self.ll[0] += self.delta * (20 - self.num)
            self.getImage()
        if event.key() == Qt.Key.Key_Left:
            self.ll[0] -= self.delta * (20 - self.num)
        if event.key() == Qt.Key.Key_Up:
            self.ll[1] += self.delta * (20 - self.num)
        if event.key() == Qt.Key.Key_Down:
            self.ll[1] -= self.delta * (20 - self.num)
        self.getImage()

    def update(self):
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())