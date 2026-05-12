import os
import sys

import requests
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow

SCREEN_SIZE = [600, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("untitled.ui", self)

        self.dark.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.light.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.z = 15
        self.ll = [37.530887, 55.703118]
        self.delt = 0.001
        self.getImage()

    def getImage(self):
        param = {"apikey": 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13',
                 "ll": f"{self.ll[0]},{self.ll[1]}",
                 "z": self.z}

        server_address = 'https://static-maps.yandex.ru/v1?'
        response = requests.get(server_address, params=param)

        if not response:
            print("Ошибка выполнения запроса:")
            # print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.update()

    def keyPressEvent(self, event):

        d = {"0": 8, "1": 6, "2": 5, "3": 4, "4": 3, "5": 0.6, "6": 0.5, "7": 0.4, "8": 0.3, "9": 0.2, "10": 0.1,
             "11": 0.04,
             "12": 0.03, "13": 0.02, "14": 0.002, "15": 0.001, "16": 0.0001, "17": 0.0001, "18": 0.0001, "19": 0.0001,
             "20": 0.0001, "21": 0.0001}

        if event.key() == Qt.Key.Key_PageUp and self.z <= 21:
            self.z += 1

        if event.key() == Qt.Key.Key_PageDown and self.z > 0:
            self.z -= 1

        if event.key() == Qt.Key.Key_Left:
            self.ll[0] -= d[f'{self.z}']

        if event.key() == Qt.Key.Key_Right:
            self.ll[0] += d[f'{self.z}']

        if event.key() == Qt.Key.Key_Up:
            self.ll[1] += d[f'{self.z}']

        if event.key() == Qt.Key.Key_Down:
            self.ll[1] -= d[f'{self.z}']
        self.getImage()

    def closeEvent(self, event):
        os.remove(self.map_file)

    def update(self):
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
