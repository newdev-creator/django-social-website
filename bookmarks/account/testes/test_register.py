from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from account.models import Profile  # Assuming Profile is in the `account.models`

class RegisterViewTest(TestCase):
    def test_register_view_get(self):
        """
        Test GET request to the register view.
        """
        response = self.client.get(reverse('register'))  # Replace 'register' with the actual URL name
        self.assertEqual(response.status_code, 200)  # Ensure the page loads
        self.assertTemplateUsed(response, 'account/register.html')  # Check the correct template is used
        self.assertIn('user_form', response.context)  # Ensure the context includes 'user_form'

    def test_register_view_post_valid_data(self):
        """
        Test POST request with valid data to the register view.
        """
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'testuser@example.com'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)  # Ensure the page loads
        self.assertTemplateUsed(response, 'account/register_done.html')  # Check the success template is used
        
        # Check if the user and profile are created
        self.assertTrue(User.objects.filter(username='testuser').exists())
        user = User.objects.get(username='testuser')
        self.assertTrue(Profile.objects.filter(user=user).exists())  # Profile is created for the user

    def test_register_view_post_invalid_data(self):
        """
        Test POST request with invalid data to the register view.
        """
        data = {
            'username': '',  # Invalid username
            'password': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'invalid-email'  # Invalid email format
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)  # Ensure the page loads
        self.assertTemplateUsed(response, 'account/register.html')  # Check the form re-renders
        self.assertIn('user_form', response.context)  # Ensure the context includes 'user_form'
        self.assertTrue(response.context['user_form'].errors)  # Form should have errors
        
        # Check that no user or profile is created
        self.assertFalse(User.objects.exists())
        self.assertFalse(Profile.objects.exists())
