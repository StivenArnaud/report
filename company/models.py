from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Raison sociale"))
    address = models.CharField(max_length=255, verbose_name=_("Adresse"), blank=True, null=True)
    phone = models.CharField(max_length=255, verbose_name=_("Telephone"), blank=True, null=True)
    email = models.EmailField(max_length=255, verbose_name=_("Adresse email"), blank=True, null=True)
    logo = models.ImageField(upload_to='company/logo/', null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Compagnie")
        verbose_name_plural = _("Compagnies")
        ordering = ['name']
