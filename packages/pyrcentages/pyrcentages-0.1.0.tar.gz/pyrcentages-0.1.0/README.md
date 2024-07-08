---
# Pyrcentages

This Python module provides functions to perform calculations based on percentages.

## Functions

### `AddByPercentage(a, b)`
Adds a percentage of `b` to `a`.

### Parameters
- `a`: The initial value.
- `b`: The percentage value to add.

### Returns
- The result of adding `b` percent of `a` to `a`.

### Example
```python
result = AddByPercentage(100, 20)
print(result)  # Output: 120
```

### `SubtractByPercentage(a, b)`
Subtracts a percentage of `b` from `a`.

### Parameters
- `a`: The initial value.
- `b`: The percentage value to subtract.

### Returns
- The result of subtracting `b` percent of `a` from `a`.

### Example
```python
result = SubtractByPercentage(100, 20)
print(result)  # Output: 80
```

### `PercentageChances(a)`
Determines the likelihood of an event based on a given percentage. (boolean)

### Parameters
- `a`: The percentage chance of the event happening.

### Returns
- `True` if the event occurs based on the given percentage; `False` otherwise.

### Example
```python
result = PercentageChances(75)
print(result)  # Output: True (75% chance of occurrence)
```

---