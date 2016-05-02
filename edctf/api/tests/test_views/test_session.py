from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from edctf.api.models import Team
import json


class SessionViewNoCtfTestCase(TestCase):
    def setUp(self):
        """
        Creates admin user
        """
        self.username = 'admin'
        self.teamname = 'admin'
        self.email = 'admin@localhost'
        self.password = 'admin'
        user = get_user_model().objects.create_superuser(self.username, self.email, self.password)
        team = Team.objects.create_team(self.teamname, user)

    def test_admin_user_session(self):
        """
        Tests sessions for admin user
        """
        c = Client()
        login = json.dumps({
            'username': self.username,
            'password': self.password
        })
        response = c.post('/api/session/', data=login, content_type='application/json')
        self.assertEqual(200, response.status_code)
        response = c.get('/api/session/')
        self.assertEqual(200, response.status_code)
        response = c.delete('/api/session/')
        self.assertEqual(200, response.status_code)
        response = c.get('/api/session/')
        self.assertEqual(403, response.status_code)

    def test_invalid_creds_session(self):
        """
        Registers a new user and tests session api
        """
        c = Client()
        login = json.dumps({
            'username': self.username,
            'password': self.password+'a'
        })
        response = c.post('/api/session/', data=login, content_type='application/json')
        self.assertEqual(403, response.status_code)
        response = c.get('/api/session/')
        self.assertEqual(403, response.status_code)
        response = c.delete('/api/session/')
        self.assertEqual(403, response.status_code)

    def test_new_user_session(self):
        """
        Attempts to register a new user and login
        """
        c = Client()
        register = json.dumps({
            'email': 'a@a.com',
            'username': 'newuser',
            'teamname': 'newuser',
            'password': 'newuser'
        })
        response = c.post('/api/teams/', data=register, content_type='application/json')
        self.assertEqual(403, response.status_code)
        response = c.get('/api/session/')
        self.assertEqual(403, response.status_code)
        
        login = json.dumps({
            'username': 'newuser',
            'password': 'newuser'
        })
        response = c.post('/api/session/', data=login, content_type='application/json')
        self.assertEqual(403, response.status_code)


class SessionViewCtfTestCase(TestCase):
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

    def test_admin_user_session(self):
        """
        Tests sessions for admin user
        """
        c = Client()
        login = json.dumps({
            'username': self.username,
            'password': self.password
        })
        response = c.post('/api/session/', data=login, content_type='application/json')
        self.assertEqual(200, response.status_code)
        response = c.get('/api/session/')
        self.assertEqual(200, response.status_code)
        response = c.delete('/api/session/')
        self.assertEqual(200, response.status_code)
        response = c.get('/api/session/')
        self.assertEqual(403, response.status_code)

    def test_invalid_creds_session(self):
        """
        Tests invalid credentials
        """
        c = Client()
        login = json.dumps({
            'username': self.username,
            'password': self.password+'a'
        })
        response = c.post('/api/session/', data=login, content_type='application/json')
        self.assertEqual(403, response.status_code)
        response = c.get('/api/session/')
        self.assertEqual(403, response.status_code)
        response = c.delete('/api/session/')
        self.assertEqual(403, response.status_code)

    def create_new_user_session(self, offset=''):
        """
        Registers a new user and tests session api
        """
        c = Client()
        register = json.dumps({
            'email': offset + 'a@a.com',
            'username': 'newuser' + offset,
            'teamname': 'newuser' + offset,
            'password': 'newuser' + offset
        })
        response = c.post('/api/teams/', data=register, content_type='application/json')
        self.assertEqual(200, response.status_code)
        response = c.get('/api/session/')
        self.assertEqual(200, response.status_code)
        response = c.delete('/api/session/')
        self.assertEqual(200, response.status_code)
        response = c.get('/api/session/')
        self.assertEqual(403, response.status_code)
        
        login = json.dumps({
            'username': 'newuser' + offset,
            'password': 'newuser' + offset + 'a'
        })
        response = c.post('/api/session/', data=login, content_type='application/json')
        self.assertEqual(403, response.status_code)

        login = json.dumps({
            'username': 'newuser' + offset,
            'password': 'newuser' + offset
        })
        response = c.post('/api/session/', data=login, content_type='application/json')
        self.assertEqual(200, response.status_code)
        response = c.get('/api/session/')
        self.assertEqual(200, response.status_code)
        response = c.delete('/api/session/')
        self.assertEqual(200, response.status_code)
        response = c.get('/api/session/')
        self.assertEqual(403, response.status_code)

    def test_multiple_new_user_session(self):
        """
        Attempts to register multiple new users and login
        """
        for i in range(10):
            self.create_new_user_session(offset=str(i))
