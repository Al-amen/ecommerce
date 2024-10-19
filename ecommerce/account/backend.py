from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

class UsernameOrEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(f"Authenticating user: {username}")  # Debugging info
        try:
            user = User.objects.get(Q(user_name__iexact=username) | Q(email__iexact=username))
        except User.DoesNotExist:
            print("User not found")  # Debugging info
            return None
        except User.MultipleObjectsReturned:
            user = User.objects.filter(Q(user_name__iexact=username) | Q(email__iexact=username)).first()

        if user.check_password(password) and self.user_can_authenticate(user):
            print("Authentication successful")  # Debugging info
            return user
        else:
            print("Password incorrect or user can't authenticate")  # Debugging info
            return None
