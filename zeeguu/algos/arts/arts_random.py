import random


class ArtsRandom:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def __eq__(self, other):
        return self.a == other.a \
               and self.d == other.d \
               and self.b == other.b \
               and self.r == other.r \
               and self.w == other.w

    def calculate(self, args):
        return random.random()
