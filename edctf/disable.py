class DisableCSRF(object):
  """
  Disables CSRF checks in django.
  """
  def process_request(self, request):
    setattr(request, '_dont_enforce_csrf_checks', True)
