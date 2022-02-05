from django.contrib.auth.models import User
from django import forms
from .models import Profile,Post,Comment
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_email(value):
    if value not in [i.email for i in User.objects.all()]:
        raise ValidationError(
            _('%(value)s is not a valid user'),
            params={'value': value},
        )

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	email = forms.EmailField(max_length=254, help_text='Required field')
	class Meta:
		model = User
		fields = ['username','email','password']

class UserLoginForm(forms.Form):
	email = forms.EmailField(max_length=254, help_text='', validators=[validate_email],widget=forms.TextInput(attrs={'class':"form-control"}))
	password = forms.CharField(widget=forms.TextInput(attrs={'type':'password','class':"form-control"}))


class UpdateUserForm(forms.ModelForm):
	email = forms.EmailField(max_length=254, help_text='Required field')

	class Meta:
		model = User
		fields = ['email']


class UpdateProfileForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['status_info','profile_photo']

class CreatePost(forms.ModelForm):
	
	class Meta:
		model = Post
		fields = ['post_text','post_picture']

class CreateComment(forms.ModelForm):
	
	class Meta:
		model = Comment
		fields = ['comment_text']
