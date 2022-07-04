from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from accounts.models import Customer
from .models import Excursion


class UserExcursionsPageTest(TestCase):
    def tearDown(self):
        self.client.logout()
        
    def loginUser(self):
        User = get_user_model()
        self.user = User.objects.create(
            username='pasha',
            email='default@gmail.com',
            password='pavlik135'
        )
        Customer.objects.create(user=self.user)
        self.client.force_login(self.user)

    def loginManager(self):
        User = get_user_model()
        group = Group.objects.get_or_create(name='manager')
        self.manager = User.objects.create(
            username='manager',
            email='default@gmail.com',
            password='pavlik135',
        )
        self.manager.groups.set(group)
        Customer.objects.create(user=self.manager)
        
        self.client.force_login(self.manager)


    def test_anonymuos_user_redirect_to_login_page(self):
        response = self.client.get('/user/excursions/')
        self.assertEqual(response.status_code, 302)

    def test_authorised_user_access_granted(self):
        self.loginUser()
        response = self.client.get('/user/excursions/')
        self.assertEqual(response.status_code, 200)

    def test_displays_users_excursions_only(self):
        self.loginManager()
        self.tearDown()
        self.loginUser()
        excursion = Excursion.objects.create(
            date='2022-07-18', 
            time='11:00', 
            type='Індивідуальні відвідування',
            person=self.user
        )
        excursion2 = Excursion.objects.create(
            date='2022-07-18', 
            time='11:00', 
            type='Індивідуальні відвідування',
            person=self.manager
        )
        response = self.client.get('/user/excursions/')

        self.assertContains(response, excursion)
        self.assertNotContains(response, excursion2)
        

class ExcursionsAllPageTest(TestCase):
    def tearDown(self):
        self.client.logout()
        
    def loginUser(self):
        User = get_user_model()
        self.user = User.objects.create(
            username='pasha',
            email='default@gmail.com',
            password='pavlik135'
        )
        Customer.objects.create(user=self.user)
        self.client.force_login(self.user)

    def loginManager(self):
        User = get_user_model()
        group = Group.objects.get_or_create(name='manager')
        self.manager = User.objects.create(
            username='manager',
            email='default@gmail.com',
            password='pavlik135',
        )
        self.manager.groups.set(group)
        Customer.objects.create(user=self.manager)
        
        self.client.force_login(self.manager)

    
    def test_only_manager_has_access(self):
        response = self.client.get('/user/excursions/all')
        self.assertEqual(response.status_code, 403)
        
        self.loginUser()
        response = self.client.get('/user/excursions/all')
        self.assertEqual(response.status_code, 403)

        self.tearDown()
        self.loginManager()
        response = self.client.get('/user/excursions/all')
        self.assertEqual(response.status_code, 200)
        
    def test_show_all_excursions(self):
        self.loginUser()
        self.tearDown()
        self.loginManager()
        excursion = Excursion.objects.create(
            date='2022-07-18', 
            time='11:00', 
            type='Індивідуальні відвідування',
            person=self.user
        )
        excursion2 = Excursion.objects.create(
            date='2022-07-18', 
            time='11:12', 
            type='Індивідуальні відвідування',
            person=self.manager
        )
        response = self.client.get('/user/excursions/all')

        self.assertContains(response, excursion.time)
        self.assertContains(response, excursion2.time)
        

class DeleteExcursionTest(TestCase):
    def tearDown(self):
        self.client.logout()
        
    def loginUser(self):
        User = get_user_model()
        self.user = User.objects.create(
            username='pasha',
            email='default@gmail.com',
            password='pavlik135'
        )
        Customer.objects.create(user=self.user)
        self.client.force_login(self.user)
    
    def test_can_delete_excursion(self):
        self.loginUser()
        excursion = Excursion.objects.create(
            date='2022-07-18', 
            time='11:00', 
            type='Індивідуальні відвідування',
            person=self.user
        )
        count = Excursion.objects.count()
        self.client.post(f'/user/excursions/delete/{excursion.id}/')
        del_count = Excursion.objects.count()
        self.assertLess(del_count, count)
           