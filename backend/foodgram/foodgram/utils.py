from rest_framework.serializers import ValidationError

LOW_INGREDIENT_LIMIT = 1
LOW_COOKING_LIMIT = 1


def is_greater_than_zero(value, error):
    if value < 1:
        raise ValidationError(error)
