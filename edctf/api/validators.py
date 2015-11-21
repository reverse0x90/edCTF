from django.core.exceptions import ValidationError
from bs4 import BeautifulSoup

def validate_xss(value):
  """
  Validates there is no unintended javascript in the value.
  """
  if "javascript:" in value:
    raise ValidationError('string contains javascript')

def validate_attributes(value):
  """
  Validates only white listed attributes are allowed in the string.
  """
  VALID_ATTRS = ['href','title']
  valid = True

  soup = BeautifulSoup(value, 'html.parser')

  for tag in soup.findAll(True):
    for attr in soup.find(tag.name).attrs:
        if attr not in VALID_ATTRS:
            valid = False
            break
    if not valid:
      break

  if not valid:
    raise ValidationError('Field may only contain valid html attributes: %s' %(", ".join(VALID_ATTRS)))

def validate_tags(value):
  """
  Validates only white listed tags are allowed in the string.
  """
  VALID_TAGS = ['a', 'br']
  valid = True

  # Make the string into a soup
  soup = BeautifulSoup(value, 'html.parser')

  # Parse all the tags in the soup
  for tag in soup.findAll(True):
    if tag.name not in VALID_TAGS:
        valid = False
        break

  if not valid:
    raise ValidationError('Field may only contain valid html tags: %s' %(", ".join(VALID_TAGS)))

def validate_positive(value):
  """
  Validates challenge points are positive.
  """
  if value < 0:
    raise ValidationError("Value must be positive")