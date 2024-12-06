from typing import Optional
from django.contrib.auth.models import User
from django.http import HttpRequest

from .models import Profile


class EmailAuthBackend:
    """
    Authenticate using an e-mail address.
    """
    def authenticate(
        self, request: Optional[HttpRequest], username: Optional[str] = None, password: Optional[str] = None
    ) -> Optional[User]:
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id: int) -> Optional[User]:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def create_profile(backend: str, user: User, *args: object, **kwargs: object) -> None:
    """
    Create user profile for social authentication.
    """
    Profile.objects.get_or_create(user=user)
