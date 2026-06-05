import json
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='student1',
            email='student1@unza.zm',
            password='Str0ngPassword!'
        )

    def test_register_success(self):
        payload = {
            'username': 'student2',
            'email': 'student2@unza.zm',
            'password1': 'Str0ngPassword!',
            'password2': 'Str0ngPassword!'
        }
        response = self.client.post(reverse('accounts:register'), json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['status'], 'success')
        created = self.user_model.objects.filter(email='student2@unza.zm').first()
        self.assertIsNotNone(created)
        self.assertNotEqual(created.password, payload['password1'])
        self.assertTrue(created.check_password(payload['password1']))

    def test_register_duplicate_email(self):
        payload = {
            'username': 'student3',
            'email': 'student1@unza.zm',
            'password1': 'Str0ngPassword!',
            'password2': 'Str0ngPassword!'
        }
        response = self.client.post(reverse('accounts:register'), json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json()['errors'])

    def test_login_success(self):
        payload = {'identifier': 'student1', 'password': 'Str0ngPassword!'}
        response = self.client.post(reverse('accounts:login'), json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_wrong_password(self):
        payload = {'identifier': 'student1', 'password': 'WrongPassword123'}
        response = self.client.post(reverse('accounts:login'), json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid credentials', response.json()['errors']['__all__'][0])

    def test_login_nonexistent_user(self):
        payload = {'identifier': 'unknown', 'password': 'DoesNotExist123'}
        response = self.client.post(reverse('accounts:login'), json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid credentials', response.json()['errors']['__all__'][0])

    def test_logout_clears_session(self):
        login_payload = {'identifier': 'student1', 'password': 'Str0ngPassword!'}
        self.client.post(reverse('accounts:login'), json.dumps(login_payload), content_type='application/json')
        response = self.client.post(reverse('accounts:logout'), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_dashboard_api_requires_auth(self):
        response = self.client.get(reverse('accounts:dashboard_api'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['status'], 'error')

    def test_dashboard_api_authenticated(self):
        self.client.login(username='student1', password='Str0ngPassword!')
        response = self.client.get(reverse('accounts:dashboard_api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(response.json()['dashboard']['email'], 'student1@unza.zm')
