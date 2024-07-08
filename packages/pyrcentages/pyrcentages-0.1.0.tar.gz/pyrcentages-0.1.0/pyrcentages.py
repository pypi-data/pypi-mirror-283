import random

def AddByPercentage(a, b):
    return a + (a * (b / 100))

def SubtractByPercentage(a, b):
    return a - (a * (b / 100))

def PercentageChances(a):
    if a > 100:
        a = 100
    if a < 0:
        a = 0
    b = random.randint(0, 100)
    return not a < b
