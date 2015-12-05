from django.core.exceptions import ValidationError
from bs4 import BeautifulSoup


def validate_no_xss(value):
  """
  Validates there is no unintended javascript in the value.
  """
  if "javascript:" in value:
    raise ValidationError('Field may not contain javascript')


def validate_attributes(value):
  """
  Validates only white listed html tag attributes are allowed in the string.
  """
  # List of valid html tag attributes
  VALID_ATTRS = ['href', 'title']
  valid = True

  # Parse the input string
  soup = BeautifulSoup(value, 'html.parser')

  # Verify only valid tag attributes are in the input
  for tag in soup.findAll(True):
    for attr in soup.find(tag.name).attrs:
        if attr not in VALID_ATTRS:
            valid = False
            break
    if not valid:
      break

  # Raise an error if invalid tag attributes were found
  if not valid:
    raise ValidationError('Field may only contain valid html attributes: %s' % (", ".join(VALID_ATTRS)))


def validate_tags(value):
  """
  Validates only white listed html tags are allowed in the string.
  """
  # List of valid html tags
  VALID_TAGS = ['a', 'br']
  valid = True

  # Parse the input string
  soup = BeautifulSoup(value, 'html.parser')

  # Verify only valid tags are in the input
  for tag in soup.findAll(True):
    if tag.name not in VALID_TAGS:
        valid = False
        break

  # Raise an error if invalid tags were found
  if not valid:
    raise ValidationError('Field may only contain valid html tags: %s' % (", ".join(VALID_TAGS)))


def validate_no_html(value):
  """
  Validates only white listed attributes are allowed in the string.
  """
  valid = True

  # Parse the input string
  soup = BeautifulSoup(value, 'html.parser')

  # Verify only valid tags are in the input
  for tag in soup.findAll(True):
    if tag.name:
        valid = False
        break

  # Raise an error if invalid tags were found
  if not valid:
    raise ValidationError('Field may not contain html')


def validate_positive(value):
  """
  Validates challenge points are positive.
  """
  if value < 0:
    raise ValidationError("Value must be positive")
