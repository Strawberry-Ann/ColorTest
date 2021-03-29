import os
from PIL import Image, ImageDraw, ImageColor


def rgb_hsv(image):
    return image.convert('HSV')
