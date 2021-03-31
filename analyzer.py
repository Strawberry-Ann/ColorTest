from PIL import Image, ImageDraw
import colorsys


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))


im = Image.new("RGB", (500, 600), (9, 27, 96))
width, height = im.width, im.height
color = hsv2rgb(9, 0.27, 0.96)
draw = ImageDraw.Draw(im)
draw.rectangle(((0, 0), (int(width * 0.1), int(height * 0.1))), color)
im.convert('RGB')
im.save('1.jpg')