from rest_framework import status
from rest_framework.response import Response


def error_response(error, errorfields={}):
  """
  Handles error messages
  """
  return Response({
    'errors': {
      'message': error,
      'fields': errorfields,
    },
  }, status=status.HTTP_400_BAD_REQUEST)

def success_response(message):
    """
    Handles successful message responses
    """
    return Response({
      'success': {
        'message': message,
      },
    })

def registration_response(isauthenticated, user=None, error='', errorfields={}, status=status.HTTP_200_OK):
    """
    Returns the registration form response.
    """
    # Create return data dictionary.
    data = {
        'isauthenticated': isauthenticated,
    }
    # If error during registration, return the error else return
    # the registration data.
    if error:
      data['error'] = error
      data['errorfields'] = errorfields
    if user:
      data['username'] = user.username
      data['email'] = user.email
      data['isadmin'] = user.is_superuser
      try:
        data['team'] = user.teams.id
      except:
        data['team'] = None
    return Response(data, status=status)
