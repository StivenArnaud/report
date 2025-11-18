import uuid
from datetime import datetime, timedelta, timezone

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Create your models here.


class Report(models.Model):
    RQ = 'RQ'
    RH = 'RH'
    JRA = 'JRA'
    QUIZ = 'QUIZ'
    REPORT_TYPES_CHOICES = (
        (RQ, 'Rapport Quotidien'),
        (RH, 'Rapport Hebdomadaire'),
        (JRA, 'Justificatif'),
        (QUIZ, 'Evaluation'),
    )
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Utilisateur'), related_name='reports')
    title = models.CharField(max_length=255, verbose_name=_('Titre du rapport'))
    type = models.CharField(max_length=5, choices=REPORT_TYPES_CHOICES, default=RQ, verbose_name=_('Type de rapport'))
    published = models.BooleanField(default=False)
    date_start = models.DateField(verbose_name=_('Date de debut'), blank=True, null=True)
    date_end = models.DateField(verbose_name=_('Date de fin'), blank=True, null=True)
    marks = models.PositiveBigIntegerField(default=0, verbose_name=_("Note"))
    admin_marks = models.PositiveBigIntegerField(default=0, verbose_name=_("Note administrateur"))
    marks_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name=_('Utilisateur'), related_name='reports_marks', blank=True, null=True)
    responsible_comments = models.TextField(blank=True, null=True, verbose_name=_('Commentaires'))
    employee_comments = models.TextField(blank=True, null=True, verbose_name=_('Commentaires'))
    admin_comments = models.TextField(blank=True, null=True, verbose_name=_('Commentaires administrateur'))
    admin_marks_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name=_('Utilisateur'), related_name='reports_admin_marks', blank=True, null=True)
    file = models.FileField(upload_to='tasks/files/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Rapport')
        verbose_name_plural = _('Rapports')
        ordering = ['-created']

    def temps_restant_jour(self):
        temps_restant = None
        maintenant = self.created.astimezone()

        # Calculer le début du jour suivant (minuit)
        debut_demain = (maintenant + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        if datetime.now().astimezone() >= debut_demain:
            temps_restant = None
            return temps_restant

        # Calculer la différence
        temps_restant = debut_demain - datetime.now().astimezone()

        return temps_restant


class Task(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, verbose_name=_('Rapport'), related_name='tasks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Utilisateur'))
    title = models.TextField(max_length=1500, verbose_name=_('Nom de la tache'))
    is_completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Tache')
        verbose_name_plural = _('Taches')
        ordering = ['created']


