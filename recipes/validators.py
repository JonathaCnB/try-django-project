import pint
from django.core.exceptions import ValidationError
from pint.errors import UndefinedUnitError


def validate_unit_of_measure(value):
    ureg = pint.UnitRegistry()
    try:
        single_unit = ureg[value]
    except UndefinedUnitError as e:
        print(e)
        raise ValidationError(f"'{value}' não é uma unidade de medida valida")
    except Exception as e:
        print(e)
        raise ValidationError(f"'{value}' não é uma unidade de medida valida")
