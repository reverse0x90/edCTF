from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
import json


# Create your views here.
class sessionView(APIView):
    """
    Manages sessions
    """
    permission_classes = (AllowAny,)
    

    def form_response(self, isauthenticated, username='', email='', teamid='', error=''):
        data = {
            'isauthenticated': isauthenticated,
        }
        if error:
            data['error'] = error
        else:
            data['username'] = username
            data['email'] = email
            data['team'] = teamid
        return Response(data)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            try:
                return self.form_response(True, username=request.user.username, email=request.user.email, teamid=request.user.teams.id)
            # Temporary: Django admin doesnt have a team..
            except:
                return self.form_response(True, username=request.user.username, email=request.user.email, teamid=None)
        return self.form_response(False, error='Not authenticated')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)
            #return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        login_data = json.loads(request.body)
        if not ('username' in login_data  and 'password' in login_data):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        username = login_data['username']
        password = login_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    return self.form_response(True, username=request.user.username, email=request.user.email, teamid=request.user.teams.id)
                # Temporary: Django admin doesnt have a team..
                except:
                    return self.form_response(True, username=request.user.username, email=request.user.email, teamid=None)
            return self.form_response(False, error='Acount disabled')
        return self.form_response(False, error='Invalid username or password')

    def delete(self, request, *args, **kwargs):
        # Logout
        if request.user.is_authenticated():
            logout(request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
