import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.conf import settings

# Create your models here.
from authentication.managers import UserManager
from company.models import Company

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
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name=_('Entreprise'), related_name='users', blank=True, null=True)
    responsible = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Responsable'))
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=EMPLOYEE, verbose_name=_('Role'))
    first_name = models.CharField(max_length=150, verbose_name=_('Nom de famille'))
    last_name = models.CharField(max_length=150, verbose_name=_('Prenom.s'))
    email = models.EmailField(unique=True, verbose_name=_('Adresse email'))
    phone = models.CharField(max_length=50, verbose_name=_('Telephone'))
    address = models.CharField(max_length=255, verbose_name=_('Adresse'), blank=True, null=True)
    identifier = models.CharField(max_length=100, verbose_name=_('Identifiant'), blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name=_('Photo de profil'))

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


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Utilisateur'), related_name='profile')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name=_('Entreprise'))
    cv = models.FileField(upload_to='cvs/', blank=True, null=True, verbose_name=_('CV'))
    gender = models.CharField(max_length=10, choices=(('male', 'Homme'), ('female', 'Femme')), default='male', verbose_name=_('Genre'))
    birth_date = models.DateField(verbose_name=_('Date de naissance'), blank=True, null=True)
    job_title = models.CharField(max_length=150, verbose_name=_('Poste occupe'), blank=True, null=True)
    job_file = models.FileField(upload_to='job_files/', verbose_name=_('Fiche de poste'), blank=True, null=True)
    cni = models.FileField(upload_to='cnis/', blank=True, null=True, verbose_name=_('CNI'))
    salary = models.DecimalField(verbose_name=_('Salaire'), blank=True, null=True, decimal_places=2, max_digits=15)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = _('Profil')
        verbose_name_plural = _('Profils')
        ordering = ['created']
