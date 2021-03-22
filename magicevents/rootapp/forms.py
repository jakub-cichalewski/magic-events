from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields


class EventUnregisterForm(forms.Form):
    unregister_code = forms.CharField(label='Registration Code:', max_length=6)
