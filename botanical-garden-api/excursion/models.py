from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError


WORKDAY_START = (8, 30)
WORKDAY_END = (16, 15)
FRIDAY_END = (15, 0)



def validate_excursion_date(value):
    if value.weekday() in [5, 6]:
        raise ValidationError(
            _('We do not work at weekends'),
            params={'value': value},
        )

    too_early1 = value.hour < WORKDAY_START[0]
    too_early2 = value.hour == WORKDAY_START[0] and value.minute < WORKDAY_START[1]
    if too_early1 or too_early2:
        raise ValidationError(
            _('Too early for excursion'),
            params={'value': value},
        )

    if value.weekday() != 4:
        too_late1 = value.hour > WORKDAY_END[0]
        too_late2 = value.hour == WORKDAY_END[0] and value.minute > WORKDAY_END[1]
        if too_late1 or too_late2:
            raise ValidationError(
                _('Too late for excursion'),
                params={'value': value},
            )
    else:
        too_late_friday = value.hour > FRIDAY_END[0]
        if too_late_friday:
            raise ValidationError(
                _('Too late for excursion'),
                params={'value': value},
            )


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
    date = models.DateTimeField(validators=[validate_excursion_date])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

