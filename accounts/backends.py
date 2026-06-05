from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        credential = username or kwargs.get('email') or kwargs.get('email_or_username')
        if credential is None or password is None:
            return None
        try:
            user = UserModel.objects.get(
                Q(username__iexact=credential) | Q(email__iexact=credential)
            )
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
