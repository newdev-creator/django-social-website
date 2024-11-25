from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User



class DashboardViewTest(TestCase):
    def setUp(self):
        """
        Create a test user to simulate login.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_dashboard_redirects_if_not_logged_in(self):
        """
        Test that the dashboard view redirects to the login page if not logged in.
        """
        response = self.client.get(reverse('dashboard'))  # 'dashboard' is the name of the view
        self.assertEqual(response.status_code, 302)  # 302 is the HTTP status code for a redirect
        self.assertIn('/login/', response.url)  # Ensure the redirect URL includes '/login/'

    def test_dashboard_renders_if_logged_in(self):
        """
        Test that the dashboard view renders properly for a logged-in user.
        """
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)  # 200 means the page loads successfully
        self.assertTemplateUsed(response, 'account/dashboard.html')  # Check the correct template is used
        self.assertContains(response, '<h1>Dashboard</h1>')  # Ensure 'Dashboard' header is present
        self.assertContains(response, 'Welcome to your Dashboard.')  # Ensure welcome text is present

