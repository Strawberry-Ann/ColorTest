from PIL import Image
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
from PIL import Image
import os
import shutil


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)  # Загружаем дизайн
        # Обратите внимание: имя элемента такое же как в QTDesigner
        self.x = 4
        self.name = 3
        self.initUI()
        self.copy_files()
        self.color = (255, 255, 255)

    def initUI(self):
        self.bg.buttonClicked.connect(self.check_color)
        self.widget.hide()
        self.pb_start = QPushButton(self)
        self.pb_start.move(100, 0)
        self.pb_start.setMinimumSize(200, 800)
        self.pb_start.setText("Начать подборку цветов")
        self.pb_start.clicked.connect(self.run_picture)
        self.teory = QPushButton(self)
        self.teory.move(300, 0)
        self.teory.setMinimumSize(200, 800)
        self.teory.setText("Start teory")
        self.teory.clicked.connect(self.run_teory)

    def copy_files(self):
        lst_of_files_in_user = os.listdir(path="user")
        for file in lst_of_files_in_user:
            os.remove(f'user/{file}')
        lst_of_files_in_data = list(filter(lambda x: '.bmp' == x[-4:], os.listdir(path="data")))
        for file in lst_of_files_in_data:
            shutil.copyfile(f'data/{file}', f'user/{file}')

    def run_picture(self):
        self.pb_start.hide()
        self.teory.hide()
        self.name, ok_pressed = QInputDialog.getItem(
            self, "Выберите комнату", "С какой комнаты начнём подборку цветов?",
            ("Гостиная", "Ванная комната", "Спальня", "Кухня"), 0, False)
        self.widget.show()
        self.look_picture(self.name)

    def run_teory(self):
        self.pb_start.hide()
        self.teory.hide()
        self.widget.show()

    def check_color(self, btn):
        color = btn.palette().button().color()
        r = color.red()
        g = color.green()
        b = color.blue()
        self.color = (r, g, b)

    def mousePressEvent(self, event):
        self.coords = event.x() - 9, event.y() - 9
        if 772 >= event.x() >= 9 and 550 >= event.y() >= 9:
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

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

