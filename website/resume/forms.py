from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import UserProfile, UserJobExperience
from django.forms import modelformset_factory, inlineformset_factory


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'summary',
            'phone',
            'alt_phone',
            'alt_email',
            'experience',
            'current_ctc',
            'expected_ctc'
        ]


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password'
        ]
        exclude = [
            'username'
        ]


class UserJobExperienceForm(forms.ModelForm):
    class Meta:
        model = UserJobExperience
        fields = [
            'company_name',
            'duration',
            'designation',
            'contribution',
        ]


UserJobExperienceFormSet = modelformset_factory(UserJobExperience, fields=(
    'company_name',
    'duration',
    'designation',
    'contribution'
))
