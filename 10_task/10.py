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
        self.theme = 'light'

        self.dark.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.light.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.clear.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.search.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEdit.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.m = 2
        self.z = 15
        self.ll = [37.530887, 55.703118]
        self.delt = 0.001
        self.marker = None

        self.getImage()

        self.light.clicked.connect(lambda:self.theme_func('light'))
        self.dark.clicked.connect(lambda:self.theme_func('dark'))

        self.search.clicked.connect(lambda:self.search_func())
        self.clear.clicked.connect(lambda:self.clear_func())
        self.pushButton.clicked.connect(lambda:self.f())

    def f(self):
        if self.m % 2 == 0:
            self.m += 1
            try:
                text = self.label.text()
                server_address = 'http://geocode-maps.yandex.ru/1.x/?'
                api_key = '8013b162-6b42-4997-9691-77b7074026e0'
                geocode = self.lineEdit.text()
                geocoder_request = f'{server_address}apikey={api_key}&geocode={geocode}&format=json'

                response = requests.get(geocoder_request)
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                toponym_coodrinates = toponym["Point"]["pos"]
                try:
                    t = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]['postal_code']
                except Exception:
                    t = "Индекс отсутствует"

                self.label.setText(f"{text} -- {t}")
            except Exception:
                self.label.setText(f"найдите место")
        else:
            self.m += 1
            try:

                text = self.label.text()
                server_address = 'http://geocode-maps.yandex.ru/1.x/?'
                api_key = '8013b162-6b42-4997-9691-77b7074026e0'
                geocode = self.lineEdit.text()
                geocoder_request = f'{server_address}apikey={api_key}&geocode={geocode}&format=json'

                response = requests.get(geocoder_request)
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                toponym_coodrinates = toponym["Point"]["pos"]
                self.label.setText(f"{text.split(' -- ')[0]}")
            except Exception:
                self.label.setText(f"найдите место")

    def clear_func(self):
        self.lineEdit.clear()
        self.label.clear()
        self.label_2.clear()
        self.marker = None
        self.lineEdit.clearFocus()
        self.setFocus()
        self.getImage()

    def theme_func(self, n: str):
        self.theme = n
        self.getImage()

    def search_func(self):
        try:
            server_address = 'http://geocode-maps.yandex.ru/1.x/?'
            api_key = '8013b162-6b42-4997-9691-77b7074026e0'
            geocode = self.lineEdit.text()
            geocoder_request = f'{server_address}apikey={api_key}&geocode={geocode}&format=json'

            response = requests.get(geocoder_request)
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]

            coords = toponym_coodrinates.split()
            self.ll[0] = float(coords[0])
            self.ll[1] = float(coords[1])
            self.marker = [float(coords[0]), float(coords[1])]


            self.label.setText(toponym["metaDataProperty"]["GeocoderMetaData"]["text"])
            self.lineEdit.clearFocus()
            self.setFocus()

            self.getImage()

        except Exception as e:
            print(e)

    def getImage(self):
        param = {"apikey": 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13',
                 "ll": f"{self.ll[0]},{self.ll[1]}",
                 "z": self.z,
                 "theme": self.theme
                 }
        if self.marker:
            param["pt"] = f"{self.marker[0]},{self.marker[1]},pm2dgl"
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
        if self.lineEdit.hasFocus():
            super().keyPressEvent(event)
            return
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
