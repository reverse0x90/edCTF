from rest_framework.permissions import BasePermission


class EdctfPermission(BasePermission):
  """
  Base permissions for edCTF
  """
  PUBLIC_METHODS = []
  AUTHENTICATED_METHODS = ['GET']
  ADMIN_METHODS = ['POST', 'PUT', 'DELETE']

  def has_permission(self, request, view):
    if request.method in self.PUBLIC_METHODS:
      return True
    if request.user and request.user.is_authenticated():
      if request.method in self.AUTHENTICATED_METHODS:
        return True
      if request.user.is_staff and request.method in self.ADMIN_METHODS:
        return True
    return False


class CtfPermission(EdctfPermission):
  """
  Permissions for the ctf route
  """
  PUBLIC_METHODS = ['GET']
  AUTHENTICATED_METHODS = []
  ADMIN_METHODS = ['POST']


class CtfPermissionDetail(EdctfPermission):
  """
  Permissions for the ctf route
  """
  PUBLIC_METHODS = ['GET']
  AUTHENTICATED_METHODS = []
  ADMIN_METHODS = ['PUT', 'DELETE']


class ChallengeboardPermission(EdctfPermission):
  """
  Permissions for the challengeboard route
  """
  PUBLIC_METHODS = []
  AUTHENTICATED_METHODS = []
  ADMIN_METHODS = ['GET']


class ChallengeboardPermissionDetail(EdctfPermission):
  """
  Permissions for the challengeboard route
  """
  PUBLIC_METHODS = []
  AUTHENTICATED_METHODS = ['GET']
  ADMIN_METHODS = []


class CategoryPermission(EdctfPermission):
  """
  Permissions for the category route
  """
  PUBLIC_METHODS = []
  AUTHENTICATED_METHODS = ['GET']
  ADMIN_METHODS = ['POST']


class CategoryPermissionDetail(EdctfPermission):
  """
  Permissions for the category route
  """
  PUBLIC_METHODS = []
  AUTHENTICATED_METHODS = ['GET']
  ADMIN_METHODS = ['PUT', 'DELETE']


class ChallengePermission(EdctfPermission):
  """
  Permissions for the challenge route
  """
  PUBLIC_METHODS = []
  AUTHENTICATED_METHODS = ['GET']
  ADMIN_METHODS = ['POST']


class ChallengePermissionDetail(EdctfPermission):
  """
  Permissions for the challenge route
  """
  PUBLIC_METHODS = []
  AUTHENTICATED_METHODS = ['GET']
  ADMIN_METHODS = ['PUT', 'DELETE']


class FlagPermission(EdctfPermission):
  """
  Permissions for the flag route
  """
  PUBLIC_METHODS = []
  AUTHENTICATED_METHODS = []
  ADMIN_METHODS = ['GET']


class FlagPermissionDetail(EdctfPermission):
  """
  Permissions for the flag route
  """
  PUBLIC_METHODS = []
  AUTHENTICATED_METHODS = ['POST']
  ADMIN_METHODS = ['GET']


class ScoreboardPermission(EdctfPermission):
  """
  Permissions for the scoreboard route
  """
  PUBLIC_METHODS = ['GET']
  AUTHENTICATED_METHODS = []
  ADMIN_METHODS = ['POST', 'PUT', 'DELETE']


class TeamPermission(EdctfPermission):
  """
  Permissions for the team route
  """
  PUBLIC_METHODS = ['GET', 'POST']
  AUTHENTICATED_METHODS = ['PUT']
  ADMIN_METHODS = ['DELETE']


class SessionPermission(EdctfPermission):
  """
  Permissions for the session route
  """
  PUBLIC_METHODS = ['GET', 'POST']
  AUTHENTICATED_METHODS = ['DELETE']
  ADMIN_METHODS = []


class CtftimePermission(EdctfPermission):
  """
  Permissions for the ctftime route
  """
  PUBLIC_METHODS = ['GET']
  AUTHENTICATED_METHODS = []
  ADMIN_METHODS = []
