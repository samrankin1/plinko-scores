from django.core.validators import RegexValidator, MaxValueValidator
from django.core.exceptions import ValidationError

SCORE_MAXIMUM			 = 2147483647
BALLS_DROPPED_MAXIMUM	 = 2147483647

score_max_validator = MaxValueValidator(
	SCORE_MAXIMUM
)

balls_dropped_max_validator = MaxValueValidator(
	BALLS_DROPPED_MAXIMUM
)

def run_validator(validator, test_string):
	"""Runs a validator on a given test string, returns success"""
	try:
		validator(test_string)
	except ValidationError:
		return False
	else:
		return True
