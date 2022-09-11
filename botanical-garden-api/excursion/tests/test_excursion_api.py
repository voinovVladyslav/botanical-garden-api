from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware

from datetime import datetime

from rest_framework.test import APIClient
from rest_framework import status

from excursion.models import Excursion
from excursion.serializers import ExcursionSerializer


EXCURSIONS_URL = reverse('excursion:excursion-list')


def excursion_detail(excursion_id):
    return reverse('excursion:excursion-detail', args=[excursion_id])


def create_datetime(**params):
    defaults = {
        'year': 2111,
        'month': 1,
        'day': 5,
        'hour': 12,
        'minute': 0,
    }
    defaults.update(**params)
    dt = make_aware(datetime(**defaults))
    return dt


MONDAY_MIDDAY = create_datetime()
MONDAY_LATE_EVENING = create_datetime(hour=19)
SUNDAY_MIDDAY = create_datetime(day=4)
MONDAY_PAST_YEAR = create_datetime(year=2020, month=1, day=6)


def create_excursion(user, **params):
    defaults = {
        'type': 'AD',
        'date': MONDAY_MIDDAY,
    }
    defaults.update(**params)
    excursion = Excursion.objects.create(user=user, **defaults)
    return excursion


class ExcursionApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpassword123',
        )

    def test_auth_required(self):
        res = self.client.get(EXCURSIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedExcursionApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpassword123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_excursions(self):
        create_excursion(self.user)

        res = self.client.get(EXCURSIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        excursions = Excursion.objects.filter(user=self.user)
        serializer = ExcursionSerializer(excursions, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_retvieve_excursions_for_current_user_only(self):
        another_user = get_user_model().objects.create_user(
            email='another@example.com',
            password='testpassword123',
        )
        create_excursion(another_user, type='CH', date=create_datetime(hour=11))
        create_excursion(self.user)

        res = self.client.get(EXCURSIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        excursions = Excursion.objects.filter(user=self.user)
        serializer = ExcursionSerializer(excursions, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_create_excursion_success(self):
        data = {
            'type': 'SE',
            'date': MONDAY_MIDDAY,
        }
        res = self.client.post(EXCURSIONS_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        excursion = Excursion.objects.get(user=self.user)
        self.assertEqual(excursion.type, data['type'])
        self.assertEqual(excursion.date, data['date'])

    def test_create_excursion_invalid_time(self):
        data = {
            'type': 'SE',
            'date': MONDAY_LATE_EVENING,
        }
        res = self.client.post(EXCURSIONS_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Excursion.objects.count(), 0)

    def test_create_excursion_invalid_data(self):
        data = {
            'type': 'SE',
            'date': SUNDAY_MIDDAY,
        }

        res = self.client.post(EXCURSIONS_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Excursion.objects.count(), 0)

    def test_excursion_partial_update(self):
        excursion = create_excursion(self.user)
        data = {
            'type': 'AD',
        }

        url = excursion_detail(excursion.id)
        res = self.client.patch(url, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        excursion.refresh_from_db()
        self.assertEqual(data['type'], excursion.type)

    def test_excursion_full_update(self):
        excursion = create_excursion(self.user)
        data = {
            'type': 'AD',
            'date': create_datetime(hour=13)
        }

        url = excursion_detail(excursion.id)
        res = self.client.put(url, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        excursion.refresh_from_db()
        self.assertEqual(data['type'], excursion.type)
        self.assertEqual(data['date'], excursion.date)

    def test_delete_excursion(self):
        excursion = create_excursion(self.user)
        url = excursion_detail(excursion.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        excursion = Excursion.objects.filter(user=self.user)
        self.assertFalse(excursion.exists())

    def test_excursion_past_year_date(self):
        data = {
            'type': 'AD',
            'date': MONDAY_PAST_YEAR,
        }

        res = self.client.post(EXCURSIONS_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
