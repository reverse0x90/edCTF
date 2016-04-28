from django.test import Client
from django.test import TestCase
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage


class StaticViewTestCase(TestCase):
    def test_index(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(200, response.status_code)
