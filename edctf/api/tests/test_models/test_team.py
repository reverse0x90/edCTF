from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from edctf.api.models import Ctf
from edctf.api.models import Challengeboard
from edctf.api.models import Scoreboard
from edctf.api.models import Team


class TeamModelTestCase(TestCase):
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

    def create_ctf_team(self, offset=''):
        """
        Creates a new ctf team and user
        """
        User = get_user_model()

        username = 'username' + offset
        teamname = 'teamname' + offset
        email =  offset + 'a@a.com'
        password = 'password' + offset

        # check if email exists for ctf or global
        enc_email = User.objects.encrypt_email(email, self.ctf)
        check = User.objects.filter(enc_email__iexact=enc_email) or User.objects.filter(enc_email__iexact=email)
        self.assertFalse(check)

        # check if teamname exists for ctf or global
        enc_teamname = Team.objects.encrypt_teamname(teamname, self.ctf)
        check = Team.objects.filter(enc_teamname__iexact=enc_teamname) or Team.objects.filter(enc_teamname__iexact=teamname)
        self.assertFalse(check)

        # check if username exists for ctf or global
        enc_username = User.objects.encrypt_username(username, self.ctf)
        check = User.objects.filter(enc_username__iexact=enc_username) or User.objects.filter(enc_username__iexact=username)
        self.assertFalse(check)

        # create user/team
        new_user = User.objects.create_user(username, self.ctf, email, password)
        new_team = Team.objects.create_team(teamname, new_user, self.ctf)

        Team.objects.get(id=new_team.id)


    def test_create_multiple_ctf_team(self):
        """
        Creates multiple ctf team and user
        """
        for i in range(10):
            self.create_ctf_team(offset=str(i))

    def test_create_multiple_ctf_team_with_dup_name(self):
        """
        Attempts to create multiple ctf teams with the same name
        """
        self.create_ctf_team()
        try:
            self.create_ctf_team()
            self.assertTrue(0, 'Duplicate ctf team allowed.')
        except AssertionError:
            pass
