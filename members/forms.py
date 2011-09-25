from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from members.models import Member
from images.models import Photo

class EmailLoginForm(forms.Form):

    email = forms.CharField(label="Email", max_length=50)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(EmailLoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        #alright we have the email and password
        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Please enter a correct email and password. Note that both fields are case-sensitive.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in.")

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
    

class RegistrationForm(forms.Form):
    email=forms.EmailField(label='Email')
    first_name=forms.CharField(min_length=1, max_length=30, label='First Name', )
    last_name=forms.CharField(min_length=1, max_length=30, label='Last Name', )
    password1=forms.CharField(widget=forms.PasswordInput(render_value=False), label='Password')
    password2=forms.CharField(widget=forms.PasswordInput(render_value=False), label='Confirm Password')
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError('Your passwords did not match')
        return self.cleaned_data
    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError('This email address is already being used. Please provide a different email address.')
        return self.cleaned_data['email']

class AuthForm(forms.Form):
    class Meta:
        model=Member
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model=Member
        fields=('about','gender','interests','website')
        
        
