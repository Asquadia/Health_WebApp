def bmi(weight, height):
    """Calculates BMI given weight and height.

    Args:
        weight: Weight in kilograms (float).
        height: Height in meters (float).

    Returns:
        The calculated BMI (float) or None if inputs are invalid.
    """
    if not isinstance(weight, (int, float)):
        raise TypeError("Weight must be a number.")
    if not isinstance(height, (int, float)):
        raise TypeError("Height must be a number.")
    if weight <= 0:
        raise ValueError("Weight must be a positive value.")
    if height <= 0:
        raise ValueError("Height must be a positive value.")
    return weight / (height * height)
