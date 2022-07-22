from sympy import Point
from writeutilities import *


def color(r, g, b):
    return bytes([b, g, r])


BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)


class Render(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_color = WHITE
        self.vertex_color = BLACK
        self.clear()

    def createWindow(self, width, height):
        self.width = width
        self.height = height

    def clear(self):
        self.framebuffer = [
            [self.current_color for x in range(self.width)]
            for y in range(self.height)
        ]

    def write(self, filename):
        f = open(filename, 'bw')

        # pixel header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(word(0))
        f.write(word(0))
        f.write(dword(14 + 40))

        # info header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # pixel data
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])

        f.close()

    def point(self, x, y):
        self.framebuffer[x][y] = self.vertex_color

    def line(self, x1, y1, x2, y2):

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        steep = dy > dx

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)

        offset = 0
        threshold = dx

        y = y1
        for x in range(x1, x2 + 1):
            if steep:
                self.point(y, x)
            else:
                self.point(x, y)

            offset += dy * 2
            if offset >= threshold:
                y += 1 if y1 < y2 else -1
                threshold += dx * 2


r = Render(1000, 1000)


def fill_supder(x, y):
    if r.framebuffer[x][y] == BLACK:
        return
    else:
        r.point(x, y)
        fill_supder(x+1, y)
        fill_supder(x, y+1)


def fill_infder(x, y):
    if r.framebuffer[x][y] == BLACK:
        return
    else:
        r.point(x, y)
        fill_infder(x-1, y)
        fill_infder(x, y+1)


def fill_supizq(x, y):
    if r.framebuffer[x][y] == BLACK:
        return
    else:
        r.point(x, y)
        fill_supizq(x+1, y)
        fill_supizq(x, y-1)


def fill_infizq(x, y):
    if r.framebuffer[x][y] == BLACK:
        return
    else:
        r.point(x, y)
        fill_infizq(x-1, y)
        fill_infizq(x, y-1)


def fill_all(x, y):
    fill_supder(x, y)
    fill_infder(x-1, y)
    fill_supizq(x, y-1)
    fill_infizq(x-1, y-1)


def fill_calc_center(x_max, y_max, x_min, y_min):
    x_mid = int((x_max+x_min)/2)
    y_mid = int((y_max+y_min)/2)
    fill_all(x_mid, y_mid)


# estrella
r.line(165, 380, 185, 360)
r.line(185, 360, 180, 330)
r.line(180, 330, 207, 345)
r.line(207, 345, 233, 330)
r.line(233, 330, 230, 360)
r.line(230, 360, 250, 380)
r.line(250, 380, 220, 385)
r.line(220, 385, 205, 410)
r.line(205, 410, 193, 383)
r.line(193, 383, 165, 380)

# cuadrado
r.line(321, 335, 288, 286)
r.line(288, 286, 339, 251)
r.line(339, 251, 374, 302)
r.line(374, 302, 321, 335)

# triangulo
r.line(377, 249, 411, 197)
r.line(411, 197, 436, 249)
r.line(436, 249, 377, 249)

# tetera
r.line(413, 177, 448, 159)
r.line(448, 159, 502, 88)
r.line(502, 88, 553, 53)
r.line(553, 53, 535, 36)
r.line(535, 36, 676, 37)
r.line(676, 37, 660, 52)
r.line(660, 52, 750, 145)
r.line(750, 145, 761, 179)
r.line(761, 179, 672, 192)
r.line(672, 192, 659, 214)
r.line(659, 214, 615, 214)
r.line(615, 214, 632, 230)
r.line(632, 230, 580, 230)
r.line(580, 230, 597, 215)
r.line(597, 215, 552, 214)
r.line(552, 214, 517, 144)
r.line(517, 144, 466, 180)
r.line(466, 180, 413, 177)
# hoyo
r.line(682, 175, 708, 120)
r.line(708, 120, 735, 148)
r.line(735, 148, 739, 170)
r.line(739, 170, 682, 175)

# estrella
fill_calc_center(250, 410, 165, 330)
# cuadrado
fill_calc_center(374, 335, 288, 251)
# triangulo
fill_calc_center(436, 249, 377, 197)
# tetera
fill_calc_center(761, 230, 413, 36)
fill_calc_center(750, 150, 750, 150)
fill_calc_center(590, 227, 590, 227)
r.write('imagen.bmp')
