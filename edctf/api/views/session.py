from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
import json


class sessionView(APIView):
    """
    Manages server side user sessions
    """
    permission_classes = (AllowAny,)
    
    def form_response(self, isauthenticated, username='', email='', teamid='', error=''):
        """
        Returns the login form response.
        """
        # Create return data dictionary.
        data = {
            'isauthenticated': isauthenticated,
        }
        # If error during login, return the error else return login data.
        if error:
            data['error'] = error
        else:
            data['username'] = username
            data['email'] = email
            data['team'] = teamid
        return Response(data)


    def get(self, request, *args, **kwargs):
        """
        Returns authentication data.
        """
        # If user is authenticated, return authentication data else 
        # return a "not authenticated" error.
        if request.user.is_authenticated():
            try:
                return self.form_response(True, username=request.user.username, email=request.user.email, teamid=request.user.teams.id)
            # This is temporary the django admin user doesn't have a team
            except:
                return self.form_response(True, username=request.user.username, email=request.user.email, teamid=None)
        return self.form_response(False, error='Not authenticated')


    def post(self, request, *args, **kwargs):
        """
        Uses provided json data to authenticate and login a user.
        """
        # If user is already authenticated, logout the user.
        if request.user.is_authenticated():
            logout(request)

        # Serialize the provided login json data to a python object. 
        login_data = request.data

        # Sanity check the json data to make sure all required parameters 
        # are included.
        if not ('username' in login_data  and 'password' in login_data):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # Authenticate the user.
        username = login_data['username']
        password = login_data['password']
        user = authenticate(username=username, password=password)

        # If user authentication was sucessful, login the user else 
        # return an error message. 
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    return self.form_response(True, username=request.user.username, email=request.user.email, teamid=request.user.teams.id)
                # This is temporary the django admin user doesn't have a team.
                except:
                    return self.form_response(True, username=request.user.username, email=request.user.email, teamid=None)
            return self.form_response(False, error='Acount disabled')
        return self.form_response(False, error='Invalid username or password')


    def delete(self, request, *args, **kwargs):
        """
        Logout the user
        """
        # If user is authenticated, logout the user else return a 401 
        # error message.
        if request.user.is_authenticated():
            logout(request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
