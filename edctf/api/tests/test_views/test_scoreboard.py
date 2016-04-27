from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from edctf.api.models import Team
import json


class ChallengeboardViewTestCase(TestCase):
    def setUp(self):
        """
        Creates admin user session, ctf, and normal user session
        """
        self.admin = Client()
        self.user = Client()
        self.urls = '/api/scoreboards/'
        self.url = '/api/scoreboards/{id}'
        self.ctf = {}

        # get admin session
        self.username = 'admin'
        self.teamname = 'admin'
        self.email = 'admin@localhost'
        self.password = 'admin'
        user = get_user_model().objects.create_superuser(self.username, self.email, self.password)
        team = Team.objects.create_team(self.teamname, user)
        
        login = json.dumps({
            'username': self.username,
            'password': self.password
        })
        response = self.admin.post('/api/session/', data=login, content_type='application/json')
        self.assertEqual(200, response.status_code)

        # create online ctf
        create_ctf = json.dumps({
            'ctf': {
                'name': 'ctfname',
                'online': True,
            }
        })
        response = self.admin.post('/api/ctfs/', data=create_ctf, content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.ctf = response.data['ctf']
        self.url = self.url.format(id=self.ctf['scoreboard'])

        # register normal user
        register = json.dumps({
            "email": "a@a.com",
            "username": "a",
            "teamname": "a",
            "password": "a"
        })
        response = self.user.post('/api/teams/', data=register, content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_nonauth_get_scoreboard(self):
        c = Client()
        response = c.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_auth_get_scoreboard(self):
        response = self.user.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.ctf['scoreboard'], response.data['scoreboard']['id'])
        

        
