from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import Mock

from account.authentication import EmailAuthBackend, create_profile
from account.models import Profile


class EmailAuthBackendTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.backend = EmailAuthBackend()

    def test_authenticate_with_valid_credentials(self):
        """Test that authenticate returns the user with valid credentials."""
        user = self.backend.authenticate(
            request=None,
            username='testuser@example.com',
            password='testpassword'
        )
        self.assertEqual(user, self.user)

    def test_authenticate_with_invalid_email(self):
        """Test that authenticate returns None if the email doesn't exist."""
        user = self.backend.authenticate(
            request=None,
            username='invalid@example.com',
            password='testpassword'
        )
        self.assertIsNone(user)

    def test_authenticate_with_invalid_password(self):
        """Test that authenticate returns None for incorrect password."""
        user = self.backend.authenticate(
            request=None,
            username='testuser@example.com',
            password='wrongpassword'
        )
        self.assertIsNone(user)

    def test_get_user_with_valid_id(self):
        """Test that get_user returns the user for a valid ID."""
        user = self.backend.get_user(self.user.id)
        self.assertEqual(user, self.user)

    def test_get_user_with_invalid_id(self):
        """Test that get_user returns None for an invalid ID."""
        user = self.backend.get_user(999)
        self.assertIsNone(user)


class CreateProfileTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    def test_create_profile_creates_new_profile(self):
        """Test that create_profile creates a profile for the user."""
        backend = 'google-oauth2'  # Mock backend
        create_profile(backend=backend, user=self.user)
        
        # Check if the profile exists
        profile = Profile.objects.filter(user=self.user).first()
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user, self.user)

    def test_create_profile_does_not_create_duplicate_profile(self):
        """Test that create_profile doesn't create duplicate profiles."""
        backend = 'google-oauth2'  # Mock backend

        # Create the first profile
        create_profile(backend=backend, user=self.user)

        # Create the second profile
        create_profile(backend=backend, user=self.user)

        # Assert only one profile exists
        profiles = Profile.objects.filter(user=self.user)
        self.assertEqual(profiles.count(), 1)
