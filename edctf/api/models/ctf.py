from django.db import models


DEFAULT_HOME = """<h1 class="text-center">Welcome to edCTF!</h1>
"""
DEFAULT_ABOUT = """<h1>What is CTF?</h1>
<p>Capture the Flag (CTF) is a computer security competition. CTF contests are usually designed to serve as an educational exercise to give participants experience in securing a machine, as well as conducting and reacting to the sort of attacks found in the real world. Reverse-engineering, network sniffing, protocol analysis, system administration, programming, and cryptanalysis are all skills which have been required by prior CTF contests at DEF CON. There are two main styles of capture the flag competitions: attack/defense and jeopardy.</p>

<p>In an attack/defense style competition, each team is given a machine (or a small network) to defend on an isolated network. Teams are scored on both their success in defending their assigned machine and on their success in attacking other team's machines. Depending on the nature of the particular CTF game, teams may either be attempting to take an opponent's flag from their machine or teams may be attempting to plant their own flag on their opponent's machine. One of the more prominent attack/defense CTF's is held every year at the hacker conference DEF CON.</p>

<p>Jeopardy-style competitions usually involve multiple categories of problems, each of which contains a variety of questions of different point values. Teams race to be the first to solve the most number of points, but do not directly attack each other.</p>

<br/>
<br/>
"""


class Ctf(models.Model):
  """
  Ctf model class.
  """
  name = models.CharField(max_length=100, unique=True)
  online = models.BooleanField(default=False)
  home_page = models.CharField(max_length=10000, default=DEFAULT_HOME)
  about_page = models.CharField(max_length=10000, default=DEFAULT_ABOUT)
  challengeboard = models.OneToOneField('Challengeboard', on_delete=models.CASCADE, null=True, related_name='ctf', related_query_name='ctf')
  scoreboard = models.OneToOneField('Scoreboard', on_delete=models.CASCADE, null=True, related_name='ctf', related_query_name='ctf')
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'Ctfs'

  def __unicode__(self):
    return '{}'.format(self.name)

  def delete(self, *args, **kwargs):
    self.challengeboard.delete()
    self.scoreboard.delete()
    super(Ctf, self).delete(*args, **kwargs)

  def home(self):
    return self.id

  def about(self):
    return self.id

  def ctftime(self):
    return '/api/ctftime/{id}'.format(id=self.id)
