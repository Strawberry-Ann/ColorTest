class MyColor:
    def __init__(self, h, s, v):
        self.h, self.s, self.v = h, s, v

    def get_combinations(self):
        return

    def triada(self):
        colors = [((self.h + 120 * i) % 360, self.s, self.v) for i in range(3)]
        return colors

    def opposite(self):
        colors = [((self.h + 180 * i) % 360, self.s, self.v) for i in range(2)]
        return colors

    def square(self):
        colors = [((self.h + 90 * i) % 360, self.s, self.v) for i in range(4)]
        return colors

    def analogy(self):
        colors = [((self.h + 15 * i) % 360, self.s, self.v) for i in range(5)]
        return colors

    def opposite_analogy(self):
        colors = [((self.h + 60 * i) % 360, self.s, self.v) for i in [-1, 0, 1]]
        return colors

    def tetrada(self):
        colors = [((self.h + 15 * i) % 360, self.s, self.v) for i in [0, 2, 6, 8]]
        return colors