from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):
    def test_create_user(self):
        email='test@example.com'
        password='testpassword134'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_manager, False)

    def test_create_manager(self):
        email='test@example.com'
        password='testpassword134'
        manager = get_user_model().objects.create_manager(
            email=email,
            password=password,
        )

        self.assertEqual(email, manager.email)
        self.assertTrue(manager.check_password(password))
        self.assertEqual(manager.is_staff, False)
        self.assertEqual(manager.is_manager, True)


    def test_create_superuser(self):
        email='test@example.com'
        password='testpassword134'
        superuser = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )

        self.assertEqual(email, superuser.email)
        self.assertTrue(superuser.check_password(password))
        self.assertEqual(superuser.is_staff, True)
        self.assertEqual(superuser.is_manager, True)
        self.assertEqual(superuser.is_superuser, True)
