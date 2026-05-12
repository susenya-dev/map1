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
