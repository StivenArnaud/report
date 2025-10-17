import uuid

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Presence(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Utilisateur'),
                             related_name='presences')
    month = models.CharField(max_length=10, verbose_name=_("Mois"))
    total_hours_of_absence = models.CharField(max_length=63, blank=True, null=True, verbose_name=_("Heures d'absence"))
    total_overtime = models.CharField(max_length=63, blank=True, null=True, verbose_name=_("Heures sup"))
    total_debts = models.CharField(max_length=63, blank=True, null=True, verbose_name=_("Heures dettes"))
    details = models.JSONField(blank=True, null=True, verbose_name=_("Details"), default=list)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = _('Presence')
        verbose_name_plural = _('Presences')
        ordering = ['created']
        unique_together = ('user', 'month')


class PrecenceItem(models.Model):
    IN = "ENTREE"
    OUT = " SORTIE"
    STATE_CHOICES = (
        (IN, "Entree"),
        (OUT, "Sortie"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    presence = models.ForeignKey(Presence, on_delete=models.CASCADE, verbose_name=_('Presence'), related_name='items')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Utilisateur'), blank=True, null=True, related_name='presence_items')
    date = models.DateTimeField(verbose_name=_('Date'))
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default=IN, verbose_name=_('Etat'))
    times = models.TimeField(verbose_name=_('Heure'))
    identifier = models.CharField(max_length=100, verbose_name=_('Identifiant'))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.identifier

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')


