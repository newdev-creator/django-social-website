from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from account.models import Profile
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile

class EditViewTest(TestCase):
    def setUp(self):
        """
        Set up a test user and profile for the tests.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )
        # Create a profile for the user
        self.profile = Profile.objects.create(
            user=self.user,
            date_of_birth=date(1990, 1, 1),
            photo=None  # Initially, no photo
        )

    def test_edit_view_get(self):
        """
        Test GET request to the edit view.
        """
        # Log in as the test user
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('edit'))  # Replace 'edit' with the correct URL name
        self.assertEqual(response.status_code, 200)  # Ensure the page loads
        self.assertTemplateUsed(response, 'account/edit.html')  # Check the correct template is used
        self.assertIn('user_form', response.context)  # Ensure user_form is in the context
        self.assertIn('profile_form', response.context)  # Ensure profile_form is in the context
        self.assertEqual(response.context['profile_form'].instance, self.profile)  # Profile instance should match

    def test_edit_view_post_valid_data(self):
        """
        Test POST request with valid data to the edit view.
        """
        # Log in as the test user
        self.client.login(username='testuser', password='testpassword')

        # Simulate uploading a photo
        photo = SimpleUploadedFile(
            'test_photo.jpg',
            content=b'This is a test photo.',
            content_type='image/jpeg'
        )

        # Send valid form data
        data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'date_of_birth': '1995-05-20'
        }
        files = {'photo': photo}

        response = self.client.post(reverse('edit'), data, files=files)
        self.assertEqual(response.status_code, 200)  # Ensure the page loads

        # Check that the user's data is updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updateduser@example.com')

        # Check that the profile's data is updated
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.date_of_birth, date(1995, 5, 20))
        self.assertIsNotNone(self.profile.photo)  # Photo should be updated

    def test_edit_view_post_invalid_data(self):
        """
        Test POST request with invalid data to the edit view.
        """
        # Log in as the test user
        self.client.login(username='testuser', password='testpassword')

        # Send invalid form data (e.g., invalid email format)
        data = {
            'username': 'updateduser',
            'email': 'invalid-email',  # Invalid email format
            'date_of_birth': 'not-a-date'  # Invalid date format
        }
        response = self.client.post(reverse('edit'), data)
        self.assertEqual(response.status_code, 200)  # Ensure the page reloads
        self.assertTemplateUsed(response, 'account/edit.html')  # Check the form is re-rendered
        self.assertTrue(response.context['user_form'].errors)  # Ensure user_form has errors
        self.assertIn('email', response.context['user_form'].errors)  # Check email field has an error
        self.assertIn('date_of_birth', response.context['profile_form'].errors)  # Check date_of_birth has an error

        # Ensure no changes were made to the database
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'testuser@example.com')  # Email remains unchanged
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.date_of_birth, date(1990, 1, 1))  # Date of birth remains unchanged
