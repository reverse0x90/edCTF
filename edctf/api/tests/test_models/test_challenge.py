from django.test import TestCase
from edctf.api.models import Ctf
from edctf.api.models import Challengeboard
from edctf.api.models import Scoreboard
from edctf.api.models import Category
from edctf.api.models import Challenge
from random import randint


class ChallengeModelTestCase(TestCase):
    def setUp(self):
        """
        Creates ctf model with challengeboard and scoreboard
        """
        self.ctfname = 'ctfname'
        self.online = True
        self.ctf = Ctf.objects.create(name=self.ctfname, online=self.online)
        self.challengeboard = Challengeboard.objects.create()
        self.scoreboard = Scoreboard.objects.create()

        self.ctf.challengeboard = self.challengeboard
        self.ctf.scoreboard = self.scoreboard
        self.ctf.save()

    def tearDown(self):
        """
        Deletes ctf
        """
        self.ctf.delete()

    def create_category(self, offset=''):
        """
        Creates a category
        """
        categoryname = 'categoryname' + offset
        return Category.objects.create(name=categoryname, challengeboard=self.challengeboard)

    def create_challenge(self, category, offset='', points=1):
        """
        Creates a challenge under with given category
        """
        title = 'title' + offset
        points = points
        description = 'description' + offset
        flag = 'flag' + offset
        return Challenge.objects.create(category=category, title=title, points=points, description=description, flag=flag)

    def test_create_multiple_challenges(self):
        """
        Tests creating multiple challenges and categories
        """
        for i in range(5):
            category = self.create_category(offset=str(i))
            for j in range(i):
                self.create_challenge(category, offset=str(i), points=1+i)

    def test_create_multiple_challenges_with_same_info(self):
        """
        Tests creating multiple challenges with the same info
        """
        for i in range(5):
            category = self.create_category(offset=str(i))
            for j in range(i):
                self.create_challenge(category)
