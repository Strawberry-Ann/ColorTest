from PIL import Image
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
from PIL import Image


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)  # Загружаем дизайн
        # Обратите внимание: имя элемента такое же как в QTDesigner
        self.x = 4
        self.name = 1
        self.run()
        self.color = (255, 255, 155)

    def run(self):
        self.look_picture(self.name)
        # self.im = Image.open(f'data/{self.name}.jpg')
        # self.pixels = self.im.load()  # список с пикселями
        # self.x, self.y = self.im.size  # ширина (x) и высота (y) изображения
        # for i in range(self.x):
        #     for j in range(self.y):
        #         if self.pixels[i, j] != (0, 0, 0):
        #             self.pixels[i, j] = (255, 255, 255)
        # self.im.save(f'user/{self.name}.jpg')
        # Имя элемента совпадает с objectName в QTDesigner

    def mousePressEvent(self, event):
        self.coords = event.x() - 9, event.y()
        if 763 >= event.x() >= 9 and 541 >= event.y() >= 9:
            self.im = Image.open(f'user/{self.name}.bmp')
            self.pixels = self.im.load()  # список с пикселями
            self.x, self.y = self.im.size  # ширина (x) и высота (y) изображения
            self.fill(self.pixels, self.coords, self.color)
            self.im.save(f'user/{self.name}.bmp')
            self.look_picture(self.name)

    def look_picture(self, name):
        self.pic = QPixmap(f'user/{name}.bmp')
        # self.pic = self.pic.scaled(764, 520, 1)
        self.label.setPixmap(self.pic)

    def fill(self, data, start_coords, fill_value):
        xsize, ysize = self.x, self.y
        orig_value = data[start_coords[0], start_coords[1]]
        stack = {(start_coords[0], start_coords[1])}
        if orig_value == fill_value:
            return None
        while stack:
            x, y = stack.pop()
            if data[x, y] == (0, 0, 0):
                continue
            elif data[x, y] == orig_value:
                data[x, y] = fill_value
                if x > 0:
                   stack.add((x - 1, y))
                if x < (xsize - 1):
                    stack.add((x + 1, y))
                if y > 0:
                    stack.add((x, y - 1))
                if y < (ysize - 1):
                    stack.add((x, y + 1))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

