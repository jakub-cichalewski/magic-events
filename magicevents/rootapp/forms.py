from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields


class UnregisterCodeField(forms.CharField):
    def validate(self, value):
        super().validate(value)


#TODO: Finish this form

# does this code really have to be an integer?
class EventUnregisterForm(forms.Form):
    unregister_code = forms.CharField(label='Registration Code', max_length=6)

    if unregister_code:
        pass

    # 1. check if it is a digit, and a six-digit number
    # 2. check if it does match registrations
    # 3. check if it does not match more registrations than one
    #    (at least until unregister_code uniqueness is guaranteed)
    # 4. get event and check if reservation is longer than two days
    # 5.           and check if it starts after two days from today

    # if every check is passed return True. (and perhaps call remove_atendee)?
    # idk yet where such actions should be handled
    # MVC - Controller is supposed to modify Model
    #       but in Django Router=Controller
    #       BUT supposedly django follows Model-Template-View
