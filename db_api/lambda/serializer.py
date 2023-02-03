from decimal import Decimal


def to_serializable(val):
    if isinstance(val, Decimal):
        return str(val)
    return val
