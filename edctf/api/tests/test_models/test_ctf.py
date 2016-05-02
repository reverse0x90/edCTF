from django.db import IntegrityError
from django.db import transaction
from django.test import TestCase
from edctf.api.models import Ctf
from edctf.api.models import Challengeboard
from edctf.api.models import Scoreboard


class CtfModelTestCase(TestCase):
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

    def test_online_ctf(self):
        """
        Tests online ctf
        """
        Ctf.objects.get(online=True)

    def test_create_multiple_ctf(self):
        """
        Tests creating multiple ctfs
        """

        try:
            with transaction.atomic():
                ctf = Ctf.objects.create(name=self.ctfname, online=self.online)
            self.assertTrue(0, 'Duplicate ctf allowed.')
        except IntegrityError:
            pass

        with transaction.atomic():
           ctf = Ctf.objects.create(name='ctf1', online=False)
        challengeboard = Challengeboard.objects.create()
        scoreboard = Scoreboard.objects.create()
        ctf.challengeboard = challengeboard
        ctf.scoreboard = scoreboard
        ctf.save()
        Ctf.objects.get(online=False)

        with transaction.atomic():
            ctf = Ctf.objects.create(name='ctf2', online=False)
        challengeboard = Challengeboard.objects.create()
        scoreboard = Scoreboard.objects.create()
        ctf.challengeboard = challengeboard
        ctf.scoreboard = scoreboard
        ctf.save()
        self.assertEqual(2, len(Ctf.objects.filter(online=False)))
