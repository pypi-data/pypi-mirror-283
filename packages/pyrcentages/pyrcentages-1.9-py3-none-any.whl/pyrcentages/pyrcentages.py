import random

def add_by_percentage(a, b):
    return a + (a * (b / 100))

def subtract_by_percentage(a, b):
    return a - (a * (b / 100))

def percentage_chances(a):
    if a > 100:
        a = 100
    if a < 0:
        a = 0
    b = random.randint(0, 100)
    return a >= b

def percentage_difference_from_mean(a, b):
    if a == 0 and b == 0:
        return "Error: Both values are zero."
    return abs(a - b) / ((a + b) / 2) * 100

def percentage_difference(a, b):
    try:
        difference = ((b - a) / a) * 100
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    return difference

def is_within_percentage(a, b, percentage):
    return abs(a - b) <= (b * (percentage / 100))

def get_percents(a, total):
    if total == 0:
        return "Error: Division by zero is not allowed."
    return (a / total) * 100
