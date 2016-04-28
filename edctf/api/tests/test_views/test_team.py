from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from edctf.api.models import Team
import json


class TeamViewTestCase(TestCase):
    def setUp(self):
        """
        Creates admin user session and ctf
        """
        self.admin = Client()
        self.ctf = {}

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

    def test_edit_team(self):
        """
        Tests user edit profile
        """
        # register user
        c = Client()
        register = json.dumps({
            'email': 'a@a.com',
            'username': 'newuser',
            'teamname': 'newuser',
            'password': 'newuser'
        })
        response = c.post('/api/teams/', data=register, content_type='application/json')
        self.assertEqual(200, response.status_code)
        response = c.get('/api/session/')
        self.assertEqual(200, response.status_code)
        id = response.data['team']


        # edit profile
        team = json.dumps({
            'team': {
                'position': None,
                'teamname': 'newuser',
                'username': 'newuser',
                'password': 'newpassword',
                'email':'a@a.com',
                'hidden': False,
                'points': 0,
                'correctflags': 0,
                'wrongflags': 0,
                'lasttimestamp': 0,
                'solves': [],
            }
        })
        response = c.put('/api/teams/{id}'.format(id=id), data=team, content_type='application/json')
        self.assertEqual(200, response.status_code)

        c = Client()
        login = json.dumps({
            'username': 'newuser',
            'password': 'newpassword'
        })
        response = c.post('/api/session/', data=login, content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_edit_team_as_admin(self):
        """
        Registers new user and edits as admin
        """
        # add user
        c = Client()
        register = json.dumps({
            'email': 'a@a.com',
            'username': 'newuser',
            'teamname': 'newuser',
            'password': 'newuser'
        })
        response = c.post('/api/teams/', data=register, content_type='application/json')
        self.assertEqual(200, response.status_code)
        response = c.get('/api/session/')
        self.assertEqual(200, response.status_code)
        id = response.data['team']


        # edit user as admin
        team = json.dumps({
            'team': {
                'position': None,
                'teamname': 'newuser',
                'username': 'newuser',
                'password': 'newpassword',
                'email':'a@a.com',
                'hidden': False,
                'points': 0,
                'correctflags': 0,
                'wrongflags': 0,
                'lasttimestamp': 0,
                'solves': [],
            }
        })
        response = self.admin.put('/api/teams/{id}'.format(id=id), data=team, content_type='application/json')
        self.assertEqual(200, response.status_code)

        c = Client()
        login = json.dumps({
            'username': 'newuser',
            'password': 'newpassword'
        })
        response = c.post('/api/session/', data=login, content_type='application/json')
        self.assertEqual(200, response.status_code)


        # delete user as admin
        response = self.admin.delete('/api/teams/{id}'.format(id=id), data=team, content_type='application/json')
        self.assertEqual(200, response.status_code)

        c = Client()
        login = json.dumps({
            'username': 'newuser',
            'password': 'newpassword'
        })
        response = c.post('/api/session/', data=login, content_type='application/json')
        self.assertEqual(403, response.status_code)
