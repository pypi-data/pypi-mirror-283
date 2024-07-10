def format_float(value:float, precision:int=3) -> str:
    """Return formatted float.
    
    Args:
        value: A `float`. Float value to be formatted.
        precision: An `Integer`. Desired precision of the float value. Defaults to `3`.
    """
    return str(round(value,precision)).rstrip('0').rstrip('.')