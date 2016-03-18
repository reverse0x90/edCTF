from Crypto.Cipher import AES
from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from hashlib import sha256

AES_KEY = sha256(settings.SECRET_KEY).digest()
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]


class CtfUserManager(BaseUserManager):
  def _encrypt(self, message, salt=''):
    aes = AES.new(AES_KEY, AES.MODE_ECB)
    message = pad("{salt}{message}".format(salt=salt, message=message))
    return aes.encrypt(message).encode('hex')

  def _decrypt(self, ciphertext, salt=''):
    aes = AES.new(AES_KEY, AES.MODE_ECB)
    return unpad(aes.decrypt(ciphertext.decode('hex')))[len(salt):]

  def encrypt_username(self, username, ctf):
    """
    Encrypts username with salt ctf.id to allow for duplicate usernames among different ctfs.
    Key is based on django SECRET_KEY, to prevent users from logging with with their encrypted usernames.
    """
    return self._encrypt(username, str(ctf.id))

  def decrypt_username(self, encrypted_username, ctf):
    """
    Decrypts encrypted username with salt ctf.id.
    """
    return self._decrypt(encrypted_username, str(ctf.id))

  def encrypt_email(self, email, ctf):
    """
    Encrypts email with salt ctf.id to allow for duplicate emails among different ctfs.
    Key is based on django SECRET_KEY, to prevent users from logging with with their encrypted usernames.
    """
    return self._encrypt(email, str(ctf.id))

  def decrypt_email(self, encrypted_email, ctf):
    """
    Decrypts encrypted email with salt ctf.id.
    """
    return self._decrypt(encrypted_email, str(ctf.id))

  def _create_user(self, username, email, password, ctf=None, **extra_fields):
      if ctf:
        user = self.model(
          enc_username=self.encrypt_username(username, ctf),
          username=username,
          enc_email=self.encrypt_email(self.normalize_email(email), ctf),
          email=self.normalize_email(email),
          ctf=ctf,
          **extra_fields
        )
      else:
        user = self.model(
          enc_username=username,
          username=username,
          enc_email=self.normalize_email(email),
          email=self.normalize_email(email),
          **extra_fields
        )
      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_user(self, username, ctf, email, password=None, **extra_fields):
    """
    Creates user for a given ctf.
    User has default user access and an encrypted username with `ctf.id` as a salt.
    """
    if not username:
      raise ValueError('The given username must be set')
    if not email:
      raise ValueError('The given email must be set')

    return self._create_user(
      username=username,
      email=email,
      password=password,
      ctf=ctf,
      **extra_fields
    )

  def create_ctfadmin(self, username, ctf, email, password=None, **extra_fields):
    """
    Creates an admin for a given ctf.
    User has staff access and an encrypted username with `ctf.id` as a salt.
    """
    if not username:
      raise ValueError('The given username must be set')

    extra_fields.setdefault('is_staff', True)
    if extra_fields.get('is_staff') is not True:
      raise ValueError('Ctfadmin must have is_staff=True.')

    return self._create_user(
      username=username,
      email=email,
      password=password,
      ctf=ctf,
      **extra_fields
    )

  def create_superuser(self, username, email, password, **extra_fields):
    """
    Creates a superuser admin for ctf framework.
    User has global ctf access and an unencrypted username.
    """
    if not username:
      raise ValueError('The given username must be set')

    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    if extra_fields.get('is_staff') is not True:
      raise ValueError('Superuser must have is_staff=True.')
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must have is_superuser=True.')

    return self._create_user(
      username=username,
      email=email,
      password=password,
      **extra_fields
    )

class CtfUser(AbstractBaseUser):
  ctf = models.ForeignKey('Ctf', null=True, related_name='ctfs', related_query_name='ctf')
  enc_username = models.CharField(
    max_length=256,
    unique=True,
    verbose_name='username',
  )
  username = models.CharField(
    max_length=30,
    unique=False,
    help_text=_('Required. 30 characters or fewer. Letters, digits and ./+/-/_ only.'),
    validators=[
      RegexValidator(
        r'^[\w.+-]+$',
        _('Enter a valid username. This value may contain only '
          'letters, numbers ' 'and ./+/-/_ characters.')
      ),
    ],
    error_messages={
      'unique': _('A user with that username already exists.'),
    },
    verbose_name='unencrypted username',
  )
  enc_email = models.CharField(max_length=256, unique=True, verbose_name='email address')
  email = models.EmailField(max_length=64, unique=False, verbose_name='unencrypted email address')
  is_staff = models.BooleanField(
    default=False,
    help_text=_('Designates whether the user can log into this admin site.'),
  )
  is_superuser = models.BooleanField(
    default=False,
  )
  is_active = models.BooleanField(
    default=True,
    help_text=_(
      'Designates whether this user should be treated as active. '
      'Unselect this instead of deleting accounts.'
    ),
  )
  date_joined = models.DateTimeField(default=timezone.now, verbose_name='date joined')
    
  objects = CtfUserManager()

  USERNAME_FIELD = 'enc_username'
  REQUIRED_FIELDS = ['username', 'enc_email', 'email']

  class Meta:
    verbose_name = 'User'
    verbose_name_plural = 'Users'

  def get_full_name(self):
    return self.username

  def get_short_name(self):
    return self.username

  def __str__(self):
    if self.ctf:
      return "{username} \{ctf {ctf}\}".format(username=username, ctf=self.ctf)
    else:
      return "{username} \{ctf None\}".format(username=username)

  def has_perm(self, perm, obj=None):
    "Does the user have a specific permission?"
    # Simplest possible answer: Yes, always
    return True

  def has_module_perms(self, app_label):
    "Does the user have permissions to view the app `app_label`?"
    # Simplest possible answer: Yes, always
    return True
