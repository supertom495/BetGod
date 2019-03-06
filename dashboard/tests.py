from django.test import TestCase
from django.http import HttpRequest
from django.urls import reverse
from . import views
from django.contrib.auth.models import User
from .models import Event, Team, Admin
# Create your tests here.
#
# class RegisterTest(TestCase):
#     def setUp(self):
#         User.objects.create(username='Admin', password='Admin')
#
#     def test_userName_content(self):
#         user = User.objects.get(id=1)
#         expected_object_name = f'{user.username}'
#         self.assertEquals(expected_object_name, 'Admin')
#         self.assertEquals(f'{user.password}', 'Admin')
class event_test(TestCase):
    def setUp(self):
        a = Team.objects.create(team_name='Royal Never Give Up', team_description='a')
        b = Team.objects.create(team_name='Team Aster', team_description='b')
        c = Admin.objects.create(admin_email='aaaa', admin_nickname='bbbb', admin_password='cccc', admin_privilege='0')
        Event.objects.create(event_name='DOTA2', event_result='0', event_create_date='2013-01-01', event_odds_a='3',
                             event_odds_b='0.3', event_team_a=a,
                             event_team_b=b, event_admin=c)
    def test_team1_content(self):
        team = Team.objects.get(id=1)
        expected_object_name = f'{team.team_name}'
        self.assertEquals(expected_object_name, 'Royal Never Give Up')
    def test_team2_content(self):
        team = Team.objects.get(id=2)
        expected_object_name = f'{team.team_name}'
        self.assertEquals(expected_object_name, 'Team Aster')
    def test_admin_content(self):
        admin = Admin.objects.get(id=1)
        expected_object_name = f'{admin.admin_email}'
        self.assertEquals(expected_object_name, 'aaaa')
    def test_event_content(self):
        event = Event.objects.get(event_id=1)
        expected_object_name = f'{event.event_name}'
        self.assertEquals(expected_object_name, 'DOTA2')
    def test_event_list_view(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Royal Never Give Up')
        self.assertContains(response, 'Team Aster')
        self.assertTemplateUsed(response, 'HomePage.html')
class LoginPageTests(TestCase):
    # def test_profile_page_status_code(self):
    #     response = self.client.get('login/')
    #     self.assertEquals(response.status_code, 200)
    def test_view_url_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
class HomePageTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('')
        self.assertEquals(response.status_code, 200)
    def test_view_url_by_name(self):
        response = self.client.get(reverse('homepage'))
        self.assertEquals(response.status_code, 200)



