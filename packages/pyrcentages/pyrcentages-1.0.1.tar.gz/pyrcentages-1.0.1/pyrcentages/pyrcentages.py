import random

def add_by_percentage(value1, value2): # Add a percentage to value1. Example: subtract_by_percentage(100, 10) = 110.
    return value1 + (value1 * (value2 / 100))

def subtract_by_percentage(value1, value2): # Subtract a percentage from value1. Example: subtract_by_percentage(100, 10) = 90.
    return value1 - (value1 * (value2 / 100))

def percentage_chances(chances): # Percents of chance to occur an event. Example: percentage_chances(30) = 30% of chances to return True.
    if chances > 100:
        chances = 100
    if chances < 0:
        chances = 0
    b = random.randint(0, 100)
    return chances >= b

def percentage_difference_from_mean(value1, value2): # Return the difference from mean between 2 values. Example: percentage_difference_from_mean(1300, 1500) = 14.28.
    if value1 == 0 and value2 == 0:
        return "Error: Both values are zero."
    return abs(value1 - value2) / ((value1 + value2) / 2) * 100

def percentage_difference(value1, value2): # Return the difference between two values. Example: percentage_difference(1300, 1500) = 15.38.
    try:
        difference = ((value2 - value1) / value1) * 100
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    return difference

def is_within_percentage(value, target_value, margin_percentage): # Return True if value is within percentage. Example: is_within_percentage(100, 150, 20) = False. is_within_percentage(130, 150, 20) = True.
    return abs(value - target_value) <= (target_value * (margin_percentage / 100))

def get_percents(value, total): # Return the percentage of a value. Example: get_percents(100, 10) = 10.
    if total == 0:
        return "Error: Division by zero is not allowed."
    return (value / total) * 100
