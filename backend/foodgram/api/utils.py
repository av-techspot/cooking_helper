from rest_framework.serializers import ValidationError

LOW_INGREDIENT_LIMIT = 0
LOW_COOKING_LIMIT = 0


def validate_low_limit(value, error):
    if value <= LOW_INGREDIENT_LIMIT:
        raise ValidationError(error)
