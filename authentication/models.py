import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password

# Create your models here.
from authentication.managers import UserManager

class User(AbstractUser):
    RH = 'RH'
    EMPLOYEE = 'EMPLOYEE'
    RESPONSIBLE = 'RESPONSIBLE'
    ADMIN = 'ADMIN'

    ROLE_CHOICES = [
        (EMPLOYEE, 'EMPLOYE'),
        (RESPONSIBLE, 'RESPONSABLE'),
        (RH, 'RH'),
        (ADMIN, 'ADMIN'),
    ]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    responsible = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Responsable'))
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=EMPLOYEE, verbose_name=_('Role'))
    first_name = models.CharField(max_length=150, verbose_name=_('Nom de famille'))
    last_name = models.CharField(max_length=150, verbose_name=_('Prenom.s'))
    email = models.EmailField(unique=True, verbose_name=_('Adresse email'))
    phone = models.CharField(max_length=50, verbose_name=_('Telephone'))
    address = models.CharField(max_length=255, verbose_name=_('Adresse'), blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phone']

    objects = UserManager()

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Utilisateur')
        verbose_name_plural = _('Utilisateurs')
        ordering = ['last_name', 'first_name']

