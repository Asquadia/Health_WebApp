def bmr(weight, height, age, gender):
    """Calculates BMR given weight, height, age, and gender.

    Args:
        weight: Weight in kilograms (float).
        height: Height in centimeters (float).
        age: Age in years (int).
        gender: Gender ("male" or "female", string).

    Returns:
        The calculated BMR (float) or None if inputs are invalid.
    """
    if not isinstance(weight, (int, float)):
        raise TypeError("Weight must be a number.")
    if not isinstance(height, (int, float)):
        raise TypeError("Height must be a number.")
    if not isinstance(age, int):
        raise TypeError("Age must be an integer.")
    if not isinstance(gender, str):
        raise TypeError("Gender must be a string.")
    if weight <= 0:
        raise ValueError("Weight must be a positive value.")
    if height <= 0:
        raise ValueError("Height must be a positive value.")
    if age <= 0:
        raise ValueError("Age must be a positive value.")

    gender = gender.lower()
    if gender == "male":
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == "female":
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        raise ValueError('Invalid gender. Please specify "male" or "female".')
