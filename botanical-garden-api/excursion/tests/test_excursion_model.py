from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware

from datetime import datetime

from excursion.models import  Excursion


class ExcursionTest(TestCase):
    def test_successfully_created(self):
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpassword123',
        )
        Excursion.objects.create(
            user=user,
            type='AD',
            date=make_aware(datetime.now()),
        )

        self.assertEqual(Excursion.objects.count(), 1)
