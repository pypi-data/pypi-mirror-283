Voici la version en anglais des descriptions et des exemples :

---

# Pyrcentages

This Python module provides functions to perform calculations based on percentages.

## Usage

```python
from pyrcentages import *
```

## Functions

### `add_by_percentage(a, b)`
Adds a percentage of `b` to `a`.

#### Parameters
- `a`: The initial value.
- `b`: The percentage value to add.

#### Returns
- The result of adding `b` percent of `a` to `a`.

#### Example
```python
result = add_by_percentage(100, 20)
print(result)  # Output: 120
```

### `subtract_by_percentage(a, b)`
Subtracts a percentage of `b` from `a`.

#### Parameters
- `a`: The initial value.
- `b`: The percentage value to subtract.

#### Returns
- The result of subtracting `b` percent of `a` from `a`.

#### Example
```python
result = subtract_by_percentage(100, 20)
print(result)  # Output: 80
```

### `percentage_chances(a)`
Determines the likelihood of an event based on a given percentage. (boolean)

#### Parameters
- `a`: The percentage chance of the event happening.

#### Returns
- `True` if the event occurs based on the given percentage; `False` otherwise.

#### Example
```python
result = percentage_chances(75)
print(result)  # Output: True (75% chance of occurrence)
```

### `percentage_difference_from_mean(a, b)`
Calculates the percentage difference from mean between two values `a` and `b`.

#### Parameters
- `a`: The first value.
- `b`: The second value.

#### Returns
- The percentage difference from mean between `a` and `b`.

#### Example
```python
result = percentage_difference(100, 120)
print(result)  # Output: 18.18
```

### `percentage_difference(a, b)`
Calculates the percentage difference between two values `a` and `b`.

#### Parameters
- `a`: The first value.
- `b`: The second value.

#### Returns
- The percentage difference between `a` and `b`.

#### Example
```python
result = percentage_difference(2, 1500)
print(result)  # Output: 74900.0
```

### `is_within_percentage(a, b, percentage)`
Checks if `a` is within a certain percentage range of `b`.

#### Parameters
- `a`: The value to check.
- `b`: The reference value.
- `percentage`: The tolerance percentage.

#### Returns
- `True` if `a` is within the percentage range of `b`; `False` otherwise.

#### Example
```python
result = is_within_percentage(105, 100, 5)
print(result)  # Output: True
```

### `get_percentage(a, b)`
Calculates the percentage of `a` with respect to `b`.

#### Parameters
- `a`: The part value.
- `b`: The whole value.

#### Returns
- The percentage of `a` with respect to `b`.

#### Example
```python
result = get_percentage(50, 200)
print(result)  # Output: 25
```

---