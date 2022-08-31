from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from feedback.models import Review


REVIEW_URL = reverse('feedback:review-list')
REVIEW_GLOBAL_URL = reverse('feedback:all-review-list')


def review_detail(review_id):
    return reverse('feedback:review-detail', args=[review_id])


def create_review(user, **params):
    defaults = {
        'rating': 5,
        'description': 'Cool review description',
    }
    defaults.update(**params)
    review = Review.objects.create(user=user, **defaults)
    return review


class FeedbackApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpassword123',
        )
        self.another_user = get_user_model().objects.create(
            email='another@example.com',
            password='testpassword123',
        )

    def test_auth_required(self):
        res = self.client.get(REVIEW_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_global_reviews(self):
        r1 = create_review(self.user, rating=3)
        r2 = create_review(self.another_user, rating=5)
        r3 = create_review(self.another_user, rating=1)

        res = self.client.get(REVIEW_GLOBAL_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, r1.rating)
        self.assertContains(res, r2.rating)
        self.assertContains(res, r3.rating)


class AuthorizedFeedbackApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpassword123',
        )
        self.another_user = get_user_model().objects.create(
            email='another@example.com',
            password='testpassword123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_review(self):
        r1 = create_review(self.user, description='Override description')
        r2 = create_review(self.another_user)

        res = self.client.get(REVIEW_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, r1.description)
        self.assertNotContains(res, r2.description)

    def test_create_review(self):
        data = {
            'rating': 4,
            'description': 'Description test',
        }

        res = self.client.post(REVIEW_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        review = Review.objects.get(id=res.data['id'])
        self.assertEqual(review.description, data['description'])

    def test_create_review_rating_out_of_range(self):
        data = {
            'rating': 11,
            'description': 'Description test',
        }

        res = self.client.post(REVIEW_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_full_review_update(self):
        review = create_review(self.user)
        data = {
            'rating': 1,
            'description': 'updated description',
        }

        url = review_detail(review.id)
        res = self.client.put(url, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertEqual(data['description'], review.description)
        self.assertEqual(data['rating'], review.rating)

    def test_partial_review_update(self):
        review = create_review(self.user)
        data = {
            'rating': 1,
            'description': 'updated description',
        }

        url = review_detail(review.id)
        res = self.client.patch(url, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertEqual(data['description'], review.description)
