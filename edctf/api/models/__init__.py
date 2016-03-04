from category import Category
from challenge import Challenge
from challengeboard import Challengeboard
from challengetimestamp import ChallengeTimestamp
from ctf import Ctf
from scoreboard import Scoreboard
from team import Team

from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from Crypto.Cipher import AES
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core import validators

def encrypt_username(username, salt=''):
  aes = AES.new(settings.SECRET_KEY, AES.MODE_CBC)
  message = "{salt}{username}".format(salt=salt, username=username)
  return aes.encrypt(image_string)

def decrypt_username(encrypted_username, salt=''):
  aes = AES.new(settings.SECRET_KEY, AES.MODE_CBC)
  return aes.decrypt(encrypted_username)[len(salt):]

class CtfUserManager(BaseUserManager):
  def _create_user(self, username, raw_username, email, password, **extra_fields):
      if not username or not raw_username:
          raise ValueError('The given username must be set')
      user = self.model(
        username=username,
        raw_username=raw_username,
        email=self.normalize_email(email),
        **extra_fields
      )
      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_user(self, raw_username, email, password=None, ctf=None, **extra_fields):
    if not raw_username:
      raise ValueError('The given username must be set')
    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_superuser', False)
    if ctf:
      try:
        salt = str(ctf.id)
      except:
        raise
    else:
      salt = ''
    extra_fields.setdefault('salt', salt)
    username = encrypt_username(raw_username, salt=salt)
    return self._create_user(username, raw_username, email, password, **extra_fields)

  def create_superuser(self, username, email, password, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    if extra_fields.get('is_staff') is not True:
      raise ValueError('Superuser must have is_staff=True.')
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must have is_superuser=True.')
    return self._create_user(username, username, email, password, **extra_fields)

class CtfUser(AbstractBaseUser):
  username = models.CharField(
    _('encrypted username'),
    max_length=256,
    unique=True,
  )
  raw_username = models.CharField(
    max_length=150,
    unique=False,
    help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    validators=[
      validators.RegexValidator(
        r'^[\w.@+-]+$',
        _('Enter a valid username. This value may contain only '
          'letters, numbers ' 'and @/./+/-/_ characters.')
      ),
    ],
    error_messages={
      'unique': _('A user with that username already exists.'),
    },
  )
  email = models.EmailField(max_length=255,blank=True, verbose_name='email address',)
  is_staff = models.BooleanField(
    default=False,
    help_text=_('Designates whether the user can log into this admin site.'),
  )
  is_admin = models.BooleanField(
    default=False,
    help_text=_('Designates whether the user can log into this admin site.'),
  )
  is_active = models.BooleanField(
    default=True,
    help_text=_(
        'Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.'
    ),
  )
  date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
  objects = CtfUserManager()

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['raw_username', 'email']

  def get_full_name(self):
    return self.raw_username

  def get_short_name(self):
    return self.raw_username

  def __str__(self):
    return self.raw_username

  def has_perm(self, perm, obj=None):
    "Does the user have a specific permission?"
    # Simplest possible answer: Yes, always
    return True

  def has_module_perms(self, app_label):
    "Does the user have permissions to view the app `app_label`?"
    # Simplest possible answer: Yes, always
    return True
