from rest_framework.serializers import ValidationError

LOW_INGREDIENT_LIMIT = 0
LOW_COOKING_LIMIT = 0


def is_greater_than_zero(value, error):
    if value <= 0:
        raise ValidationError(error)
