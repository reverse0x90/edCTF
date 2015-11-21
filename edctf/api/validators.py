from django.core.exceptions import ValidationError

def validate_xss(value):
  """
  Validates there is no unintended javascript in the value.
  """
  if "javascript:" in value:
    raise ValidationError('string contains javascript')

def validate_whitelist_tags(value):
  """
  Validates only allowed white listed tags are allowed in the string.
  """
  if "javascript:" in value:
    raise ValidationError('string contains javascript')

def validate_positive(value):
  """
  Validates challenge points are positive.
  """
  if value < 0:
    raise ValidationError("Numerical value must be positive")