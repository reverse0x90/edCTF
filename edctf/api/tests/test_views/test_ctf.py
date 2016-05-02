from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from edctf.api.models import Team
from random import randint
import json


class CtfViewTestCase(TestCase):
    def setUp(self):
        """
        Creates admin user session
        """
        self.admin = Client()

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

    def test_create_online_ctf(self):
        """
        Creates/edits/deletes a ctf
        """
        admin = self.admin

        # create a new online ctf
        create_ctf = json.dumps({
            'ctf': {
                'name': 'ctfname',
                'online': True,
            }
        })
        response = admin.post('/api/ctfs/', data=create_ctf, content_type='application/json')
        ctf = response.data
        id = ctf['ctf']['id']

        self.assertEqual(200, response.status_code)
        self.assertEqual('ctfname', ctf['ctf']['name'])
        self.assertTrue(ctf['ctf']['online'])


        # edit ctf to offline
        ctf['ctf']['online'] = False
        edit_ctf = json.dumps(ctf)
        url = '/api/ctfs/{id}'.format(id=id)
        response = admin.put(url, data=edit_ctf, content_type='application/json')
        ctf2 = response.data

        self.assertEqual(200, response.status_code)
        self.assertEqual('ctfname', ctf['ctf']['name'])
        self.assertEqual(id, ctf2['ctf']['id'])
        self.assertFalse(ctf2['ctf']['online'])


        # delete the ctf
        response = admin.delete(url)
        self.assertEqual(200, response.status_code)

    def test_create_online_offline_ctfs(self):
        """
        Creates/edits/deletes multiple ctfs
        """
        admin = self.admin

        nctfs = 10
        # create n ctfs, randomly online
        for i in range(nctfs):
            ctfname = 'ctfname{i}'.format(i=i)
            online = bool(randint(0,1))
            create_ctf = json.dumps({
                'ctf': {
                    'name': ctfname,
                    'online': online,
                }
            })
            response = admin.post('/api/ctfs/', data=create_ctf, content_type='application/json')
            ctf = response.data['ctf']

            self.assertEqual(200, response.status_code)
            self.assertEqual(ctfname, ctf['name'])
            self.assertEqual(online, ctf['online'])


        # update local ctfs, only one max should be online
        ctfs = []
        response = admin.get('/api/ctfs/',)
        self.assertEqual(200, response.status_code)

        remote_ctfs = response.data['ctfs']
        self.assertEqual(nctfs, len(remote_ctfs))

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
            response =  admin.put(url, data=edit_ctf, content_type='application/json')
            self.assertEqual(200, response.status_code)
            self.assertEqual(True, ctf['online'])


        # update local ctfs, only one max should be online
        ctfs = []
        response =  admin.get('/api/ctfs/',)
        self.assertEqual(200, response.status_code)

        remote_ctfs = response.data['ctfs']
        nonline = 0
        for rctf in remote_ctfs:
            if rctf['online']:
               nonline += 1
            self.assertGreaterEqual(1, nonline) 
            ctfs.append(rctf)

    def test_same_ctfname(self):
        """
        Checks if multiple ctfs can have the same name
        """
        admin = self.admin

        # register two ctfs with same name
        create_ctf = json.dumps({
            'ctf': {
                'name': 'ctfname',
                'online': True,
            }
        })
        response =  admin.post('/api/ctfs/', data=create_ctf, content_type='application/json')
        self.assertEqual(200, response.status_code)
        response =  admin.post('/api/ctfs/', data=create_ctf, content_type='application/json')
        self.assertEqual(400, response.status_code)

        create_ctf = json.dumps({
            'ctf': {
                'name': 'ctfname1',
                'online': True,
            }
        })
        response =  admin.post('/api/ctfs/', data=create_ctf, content_type='application/json')
        self.assertEqual(200, response.status_code)

        # edit two ctfs to have the same name
        response =  admin.get('/api/ctfs/',)
        self.assertEqual(200, response.status_code)
        ctfs = response.data['ctfs']

        ctfs[0]['name'] = ctfs[1]['name'] = 'somectfname'
        url0 = '/api/ctfs/{id}'.format(id=ctfs[0]['id'])
        url1 = '/api/ctfs/{id}'.format(id=ctfs[1]['id'])
        response =  admin.put(url0, data=json.dumps({'ctf': ctfs[0]}), content_type='application/json')
        self.assertEqual(200, response.status_code)
        response =  admin.put(url1, data=json.dumps({'ctf': ctfs[1]}), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_get_online_ctf(self):
        """
        Tests whether a user can view an online ctf
        """
        admin = self.admin

        # create online ctf
        create_ctf = json.dumps({
            'ctf': {
                'name': 'ctfname',
                'online': True,
            }
        })
        response =  admin.post('/api/ctfs/', data=create_ctf, content_type='application/json')
        ctf = response.data
        id = ctf['ctf']['id']

        self.assertEqual(200, response.status_code)
        self.assertEqual('ctfname', ctf['ctf']['name'])
        self.assertTrue(ctf['ctf']['online'])


        # get online ctf
        c = Client()
        response =  admin.get('/api/ctfs/?online=true')
        online_ctf = response.data['ctfs'][0]
        
        self.assertEqual(200, response.status_code)
        self.assertEqual(online_ctf['name'], ctf['ctf']['name'])
        self.assertTrue(online_ctf['online'])

