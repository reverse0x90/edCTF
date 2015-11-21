from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status


# Create your views here.
class sessionView(APIView):
    """
    Manages sessions
    """
    permission_classes = (AllowAny,)
    error_messages = {
        'invalid': 'Invalid username or password',
        'disabled': 'This account is suspended',
        'isloggedin': 'Already logged in',
    }

    def send_error_response(self, message_key):
        data = {
            'success': False,
            'message': self.error_messages[message_key],
            'team': None,
        }
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            try:
                return Response({
                    'success': True,
                    'team': request.user.teams.id,
                })
            # Temporary: Django admin doesnt have a team..
            except:
                return Response({
                    'success': True,
                    'team': None,
                })
        return Response({
            'success': False,
            'team': None,
        })

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)
        #    return self.send_error_response('isloggedin')
        
        # Login
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    return Response({
                        'success': True,
                        'team': user.teams.id,
                    })
                # Temporary: Django admin doesnt have a team..
                except:
                    return Response({
                        'success': True,
                        'team': None,
                    })
            return self.send_error_response('disabled')
        return self.send_error_response('invalid')

    def delete(self, request, *args, **kwargs):
        # Logout
        if request.user.is_authenticated():
            logout(request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
