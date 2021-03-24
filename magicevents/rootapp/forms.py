from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields


class UnregisterCodeField(forms.CharField):
    def validate(self, value):
        super().validate(value)


# QUESTION: does this code really have to be an integer?
class EventUnregisterForm(forms.Form):
    unregister_code = forms.CharField(label='Unregistration Code',
                                      max_length=6,
                                      validators=[RegexValidator(r'^\d{6}$')]
                                      )
