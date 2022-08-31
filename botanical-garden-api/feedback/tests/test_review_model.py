from django.test import TestCase
from django.contrib.auth import get_user_model

from feedback.models import Review


class ReviewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='testpassword123',
            first_name='Dima',
        )

    def test_successfully_create(self):
        review = Review.objects.create(
            user=self.user,
            rating=5,
            description='Description',
        )

        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(review.rating, 5)
