import colorsys
import numpy as np
from math import modf


class MyColor:
    def __init__(self, r, g, b):
        self.h, self.s, self.v, = self.rgb2hsv(r, g, b)

    def get_comb(self):
        return [self.opposite(), self.analogy(), self.opposite_analogy(), self.square(), self.tetrada(), self.triada()]

    def rgb2hsv(self, r, g, b):
        r, g, b = r / 255, g / 255, b / 255
        v = max(r, g, b)
        temp = min(r, g, b)
        if v == 0:
            s = 0
        else:
            s = (v - temp) / v
        if s == 0:
            h = 0
        else:
            if r == v and g >= b:
                h = 60 * ((g - b) / (v - temp))
            elif r == v and g < b:
                h = 60 * ((g - b) / (v - temp)) + 360
            elif v == g:
                h = 60 * ((b - r) / (v - temp)) + 120
            elif v == b:
                h = 60 * ((r - g) / (v - temp)) + 240
            if h < 0:
                h = h + 360
        return h, s, v

    def hsv2rgb(self, h, s, v):
        h, s, v = round(h), round(s * 100), round(v * 100)
        hi = (h / 60) % 6
        v_min = (100 - s) * v / 100
        a = (v - v_min) * (h % 60) / 60
        v_inc = v_min + a
        v_dec = v - a
        if 1 >= hi >= 0:
            r, g, b = v, v_inc, v_min
        elif 2 >= hi >= 1:
            r, g, b = v_dec, v, v_min
        elif 3 >= hi >= 2:
            r, g, b = v_min, v, v_inc
        elif 4 >= hi >= 3:
            r, g, b = v_min, v_dec, v
        elif 5 >= hi >= 4:
            r, g, b = v_inc, v_min, v
        else:
            r, g, b = v, v_min, v_dec
        return int(r / 100 * 255), int(g / 100 * 255), int(b / 100 * 255)

    def triada(self):
        colors = [self.hsv2rgb((self.h + 120 * i) % 360, self.s, self.v) for i in range(3)]
        return colors

    def opposite(self):
        colors = [self.hsv2rgb((self.h + 180 * i) % 360, self.s, self.v) for i in range(2)]
        print(colors)
        return colors

    def square(self):
        colors = [self.hsv2rgb((self.h + 90 * i) % 360, self.s, self.v) for i in range(4)]
        return colors

    def analogy(self):
        colors = [self.hsv2rgb((self.h + 15 * i) % 360, self.s, self.v) for i in range(5)]
        return colors

    def opposite_analogy(self):
        colors = [self.hsv2rgb((self.h + 60 * i) % 360, self.s, self.v) for i in [0, -1, 1]]
        return colors

    def tetrada(self):
        colors = [self.hsv2rgb((self.h + 15 * i) % 360, self.s, self.v) for i in [0, 2, 6, 8]]
        return colors