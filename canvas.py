from PIL import Image
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QButtonGroup
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
from PIL import Image, ImageDraw
import os
import shutil
import pygame
from color import MyColor


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
        self.paint = False

    def initUI(self):
        self.bg.buttonClicked.connect(self.check_color)
        self.widget.hide()
        # кнопка начала раскрашивания картинки
        self.pb_start = QPushButton(self)
        self.pb_start.move(100, 0)
        self.pb_start.setMinimumSize(200, 800)
        self.pb_start.setText("Начать подборку цветов")
        self.pb_start.clicked.connect(self.run_picture)
        # кнопка для показа теории
        self.teory = QPushButton(self)
        self.teory.move(300, 0)
        self.teory.setMinimumSize(200, 800)
        self.teory.setText("Start teory")
        self.teory.clicked.connect(self.run_teory)
        # кнопка показа результата
        self.results = QPushButton(self)
        self.results.move(500, 0)
        self.results.setMinimumSize(200, 800)
        self.results.setText("Get Result")

        # группа кнопок меню
        self.group_buts_menu = QButtonGroup(self)
        self.group_buts_menu.addButton(self.pb_start)
        self.group_buts_menu.addButton(self.teory)
        self.group_buts_menu.addButton(self.results)
        self.results.clicked.connect(self.run_results)

        # кнопки на виджете
        self.pb_to_begin.clicked.connect(self.to_begin)
        self.pb_end_fill.clicked.connect(self.end_fill)
        self.pb_check_picture.clicked.connect(self.check_picture)

    def copy_files(self):
        # функция копирования изображений из папки data в папку user
        # с использованием библиотек shutil и os
        lst_of_files_in_user = os.listdir(path="user")
        for file in lst_of_files_in_user:
            os.remove(f'user/{file}')
        lst_of_files_in_data = list(filter(lambda x: '.bmp' == x[-4:], os.listdir(path="data")))
        for file in lst_of_files_in_data:
            shutil.copyfile(f'data/{file}', f'user/{file}')

    def run_picture(self):
        for button in self.group_buts_menu.buttons():
            button.hide()
        self.check_picture()
        self.widget.show()

    def check_picture(self):
        self.name, ok_pressed = QInputDialog.getItem(
            self, "Выберите комнату", "С какой комнаты начнём подборку цветов?",
            ("Ванная комната", "Гостиная", "Кухня", "Спальня"), 0, False)
        self.look_picture(self.name)

    def run_teory(self):
        # функция показа теории
        for button in self.group_buts_menu.buttons():
            button.hide()
        self.widget.show()

    def to_begin(self):
        # начать закрашивать изображение сначала
        result = QMessageBox.question(self.widget, "Начать сначала",
                                      "Вы действительно хотите начать раскрашивать картинку сначала?",
                                      buttons=QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                      defaultButton=QMessageBox.Cancel)
        if result == 16384:
            os.remove(f'user/{self.name}.bmp')
            shutil.copyfile(f'data/{self.name}.bmp', f'user/{self.name}.bmp')
            self.look_picture(self.name)

    def show_menu(self):
        self.widget.hide()
        for button in self.group_buts_menu.buttons():
            button.show()

    def end_fill(self):
        self.paint = False
        self.show_menu()
        self.run_results()

    def run_results(self):
        # !!!!!!!!!!!!!!!!!!!!!!!#
        for button in self.group_buts_menu.buttons():
            button.hide()
        colors = self.analize_pictures()
        for color in colors:
            pass
        self.show_menu()

    def analize_pictures(self):
        colors = list()
        lst_of_files_in_user = os.listdir(path="user")
        for name in lst_of_files_in_user:
            im = Image.open(f'user/{name}')
            im = im.convert('HSV')
            pixels = im.load()
            x, y = im.size
            dct = dict()
            for i in range(x):
                for j in range(y):
                    c = pixels[i, j]
                    if c not in dct.keys():
                        dct[c] = 1
                    else:
                        dct[c] +=1
            cs = sorted(dct.keys(), key=lambda k: -dct[k])
            colors.append((name[:-4], MyColor(cs[0][0], cs[0][1], cs[0][2])))
        return colors

    def check_color(self, btn):
        # функция смены цвета заливки по нажатию кнопки
        color = btn.palette().button().color()
        r = color.red()
        g = color.green()
        b = color.blue()
        self.color = (r, g, b)

    def mousePressEvent(self, event):
        # функция нажатия кнопки мыши
        self.coords = event.x() - 9, event.y() - 9
        if 772 >= event.x() >= 9 and 550 >= event.y() >= 9 and self.paint:
            # заливаем область на картинке с помощью функции self.fill
            # здесь используется библиотека для работы с изображениями PIL
            self.im = Image.open(f'user/{self.name}.bmp')
            self.pixels = self.im.load()  # список с пикселями
            self.x, self.y = self.im.size  # ширина (x) и высота (y) изображения
            self.fill(self.pixels, self.coords, self.color)
            self.im.save(f'user/{self.name}.bmp')
            self.look_picture(self.name)

    def look_picture(self, name):
        self.paint = True
        self.pic = QPixmap(f'user/{name}.bmp')
        self.label.setPixmap(self.pic)

    def fill(self, data, start_coords, fill_value):
        # функция заливки области
        xsize, ysize = self.x, self.y
        # узнаём какого цвета сейчас пиксель
        orig_value = data[start_coords[0], start_coords[1]]
        # создаём множество из координат пикселей, которые необходимо проверить на совместимость цвета
        # и закрасить
        stack = {(start_coords[0], start_coords[1])}
        if orig_value == fill_value:
            # если цвет стартового пикселя совпадает с тем, в который нужно закрасить область,
            # то выходим из функции
            return None
        while stack:
            x, y = stack.pop()
            if data[x, y] == (0, 0, 0):
                # если цвет пикселя чёрный, тоо не обращаем на него внимания,
                # т.к. это линия рисунка
                continue
            elif data[x, y] == orig_value:
                data[x, y] = fill_value
                # добавляем все соседние пиксели в множество
                if x > 0:
                   stack.add((x - 1, y))
                if x < (xsize - 1):
                    stack.add((x + 1, y))
                if y > 0:
                    stack.add((x, y - 1))
                if y < (ysize - 1):
                    stack.add((x, y + 1))

    def keyPressEvent(self, e):
        # функция закрытия окна по нажатию клавиши Escape
        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

