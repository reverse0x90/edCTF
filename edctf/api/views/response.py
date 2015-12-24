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
