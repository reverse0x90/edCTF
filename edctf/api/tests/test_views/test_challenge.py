from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from edctf.api.models import Team
import json


class ChallengeViewTestCase(TestCase):
    def setUp(self):
        """
        Creates admin user session, ctf, and normal user session
        """
        self.admin = Client()
        self.user = Client()
        self.ctf = {}
        self.challengeboard = None


        # create admin session
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
        self.challengeboard = self.ctf['challengeboard']


        # create user session
        register = json.dumps({
            'email': 'a@a.com',
            'username': 'newuser',
            'teamname': 'newuser',
            'password': 'newuser'
        })
        response = self.user.post('/api/teams/', data=register, content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_challenge(self):
        """
        Tests adding, editing, and deleting a challenge
        """
        # create challenge
        category = json.dumps({
            'category': {
                'name': 'categoryname',
                'challengeboard': self.challengeboard
            }
        })
        response = self.admin.post('/api/categories', data=category, content_type='application/json')
        self.assertEqual(200, response.status_code)
        categoryid = response.data['category']['id']

        challenge = json.dumps({
            'challenge': {
                'title': 'title',
                'points': 1337,
                'description': 'desc',
                'flag': 'flag\{1337\}', # regex
                'category': categoryid
            }
        })
        response = self.admin.post('/api/challenges/', data=challenge, content_type='application/json')
        self.assertEqual(200, response.status_code)
        challengeid = response.data['challenge']['id']

        flag = json.dumps({
            'flag': 'wrong'
        })
        response = self.user.post('/api/flags/{id}'.format(id=challengeid), data=flag, content_type='application/json')
        self.assertEqual(400, response.status_code)

        flag = json.dumps({
            'flag': 'flag{1337}'
        })
        response = self.user.post('/api/flags/{id}'.format(id=challengeid), data=flag, content_type='application/json')
        self.assertEqual(200, response.status_code)

        response = self.user.get('/api/session/')
        self.assertEqual(200, response.status_code)
        teamid = response.data['team']

        response = self.user.get('/api/teams/{id}'.format(id=teamid))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1337, response.data['team']['points'])


        # edit challenge
        challenge = json.dumps({
            'challenge': {
                'title': 'newtitle',
                'points': 10000,
                'description': 'newdesc',
                'flag': 'newflag\{1337\}',
                'category': categoryid
            }
        })
        response = self.admin.put('/api/challenges/{id}'.format(id=challengeid), data=challenge, content_type='application/json')
        self.assertEqual(200, response.status_code)

        response = self.user.get('/api/teams/{id}'.format(id=teamid))
        self.assertEqual(200, response.status_code)
        self.assertEqual(10000, response.data['team']['points'])


        # delete challenge
        response = self.admin.delete('/api/challenges/{id}'.format(id=challengeid), data=challenge, content_type='application/json')
        self.assertEqual(200, response.status_code)
        
        response = self.user.get('/api/teams/{id}'.format(id=teamid))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.data['team']['points'])
