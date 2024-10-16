from django.contrib.auth import get_user,get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.db.models.base import Model

User = get_user_model()


class UsernameOrEmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in with either their email or username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Check if user is logging in with email or username
            user = User.objects.get(Q(user_name__iexact=username) | Q(email__iexact=username))
        except User.DoesNotExist:
            User().set_password(password)
            return
        
        except User.MultipleObjectsReturned:
            user = User.objects.filter(Q(user_name__iexact=username) | Q(email__iexact=username)).order_by('id').first()

        # Check the password
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
      
