from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings


class Excursion(models.Model):
    class ExcursionType(models.TextChoices):
        CHILD = 'CH', _('Child')
        ADULT = 'AD', _('Adult')
        FILMING = 'FI', _('Filming')
        EVENT_HOLDING = 'EH', _('Event holding')
        SELF_EXCURSION = 'SE', _('Self excursion')

    type = models.CharField(
        max_length=2,
        choices=ExcursionType.choices,
        default=ExcursionType.SELF_EXCURSION,
    )
    date = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

