from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailUsernameBackend(ModelBackend):
    #Authenticate with email instead of username
    def authenticate(self, **credentials):
        if 'username' in credentials:
            return super(EmailUsernameBackend, self).authenticate(**credentials)
        try:
            user = User.objects.get(email=credentials.get('email'))
            if user.check_password(credentials.get('password')):
                return user
        except User.DoesNotExist:
            return None