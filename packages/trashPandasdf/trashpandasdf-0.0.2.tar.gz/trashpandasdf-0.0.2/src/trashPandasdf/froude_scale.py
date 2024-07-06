def getFroudeCoeff(unit) :
    """
    Calculates the Froude coefficient for a given unit.

    Parameters:
    unit (str): The unit for which the Froude coefficient needs to be calculated.

    Returns:
    float: The Froude coefficient for the given unit.

    """
    if '/' in unit:
        a, b = unit.split('/')
        return getFroudeCoeff(a) - getFroudeCoeff(b)
    elif '-' in unit:
        a, b = unit.split('-')
        return getFroudeCoeff(a) + getFroudeCoeff(b)
    elif '^' in unit:
        a, n = unit.split('^')
        return getFroudeCoeff(a)*int(n)
    else:
        coefficients = {
            'm': 1,
            's': 0.5,
            'Hz': -0.5,
            'N': 3,
            'kg': 3,
            'deg':0,
            'rad':0
        }
        if unit in coefficients.keys() :
            return coefficients[unit]
        else:
            raise ValueError(f"Invalid unit: {unit} for froude scaling, consider changing to SI units first")