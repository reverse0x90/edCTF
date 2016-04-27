from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from edctf.api.models import Team
from random import randint
import json


class CtfTestCase(TestCase):
    def setUp(self):
        self.username = 'admin'
        self.teamname = 'admin'
        self.email = 'admin@localhost'
        self.password = 'admin'
        user = get_user_model().objects.create_superuser(self.username, self.email, self.password)
        team = Team.objects.create_team(self.teamname, user)

    def test_create_online_ctf(self):
        login = json.dumps({
            'username': self.username,
            'password': self.password
        })

        c = Client()

        # login as admin
        response = c.post('/api/session/', data=login, content_type='application/json')
        self.assertEqual(200, response.status_code)


        # create a new online ctf
        create_ctf = json.dumps({
            'ctf': {
                'name': 'ctfname',
                'online': True,
            }
        })
        response = c.post('/api/ctfs/', data=create_ctf, content_type='application/json')
        ctf = response.data
        id = ctf['ctf']['id']

        self.assertEqual(200, response.status_code)
        self.assertEqual('ctfname', ctf['ctf']['name'])
        self.assertTrue(ctf['ctf']['online'])


        # edit ctf to offline
        ctf['ctf']['online'] = False
        edit_ctf = json.dumps(ctf)
        url = '/api/ctfs/{id}'.format(id=id)
        response = c.put(url, data=edit_ctf, content_type='application/json')
        ctf2 = response.data

        self.assertEqual(200, response.status_code)
        self.assertEqual('ctfname', ctf['ctf']['name'])
        self.assertEqual(id, ctf2['ctf']['id'])
        self.assertFalse(ctf2['ctf']['online'])


        # delete the ctf
        response = c.delete(url)
        self.assertEqual(200, response.status_code)

    def test_create_online_offline_ctfs(self):
        login = json.dumps({
            'username': self.username,
            'password': self.password
        })

        c = Client()

        # login as admin
        response = c.post('/api/session/', data=login, content_type='application/json')
        self.assertEqual(200, response.status_code)


        # create 100 ctfs, randomly online
        for i in range(100):
            ctfname = 'ctfname{i}'.format(i=i)
            online = bool(randint(0,1))
            create_ctf = json.dumps({
                'ctf': {
                    'name': ctfname,
                    'online': online,
                }
            })
            response = c.post('/api/ctfs/', data=create_ctf, content_type='application/json')
            ctf = response.data['ctf']

            self.assertEqual(200, response.status_code)
            self.assertEqual(ctfname, ctf['name'])
            self.assertEqual(online, ctf['online'])


        # update local ctfs, only one max should be online
        ctfs = []
        response = c.get('/api/ctfs/',)
        self.assertEqual(200, response.status_code)

        remote_ctfs = response.data['ctfs']
        nonline = 0
        for rctf in remote_ctfs:
            if rctf['online']:
               nonline += 1
            self.assertGreaterEqual(1, nonline) 
            ctfs.append(rctf)


        # change all ctfs to online
        for ctf in ctfs:
            ctf['online'] = True
            edit_ctf = json.dumps({'ctf': ctf})
            url = '/api/ctfs/{id}'.format(id=ctf['id'])
            response = c.put(url, data=edit_ctf, content_type='application/json')
            self.assertEqual(200, response.status_code)
            self.assertEqual(True, ctf['online'])


        # update local ctfs, only one max should be online
        ctfs = []
        response = c.get('/api/ctfs/',)
        self.assertEqual(200, response.status_code)

        remote_ctfs = response.data['ctfs']
        nonline = 0
        for rctf in remote_ctfs:
            if rctf['online']:
               nonline += 1
            self.assertGreaterEqual(1, nonline) 
            ctfs.append(rctf)

