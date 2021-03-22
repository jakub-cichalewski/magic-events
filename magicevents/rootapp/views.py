from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


from .forms import RegistrationForm, EventUnregisterForm
from .models import EventRegistration, Event

from random import randint


def register(request):
    if request.method == 'GET':
        return render(
            request, 'users/register.html',
            {'form': RegistrationForm}
        )
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('start'))

def start(request):
    user = request.user

    event_registrations = EventRegistration.objects.filter(user=user) \
        if user.is_authenticated else None

    return render(request, 'users/start.html',
                    {'registrations': event_registrations})

@login_required
def events(request):
    events = Event.objects.all()
    return render(request, 'users/events.html', {'events': events})

@login_required
def event_register(request):
    if request.method != 'POST': return redirect('start')

    event = Event.objects.get(pk=request.POST['pk'])
    user = request.user

    already_registered = \
        EventRegistration.objects.filter(
            event=event, user=user).count() != 0

    if not already_registered:
        # TODO: move the assignment of the unregistration code to models (?)
        #       ensure uniqueness of the code for the user
        unregister_code = randint(111111, 999999)
        event.add_atendee(user=user, code=unregister_code)
        messages.success(request,
                         f'Your unregistration code for {event.title} \
                         is {unregister_code}',
                         extra_tags='unregister-code')

    return events(request)

# TODO: move some of this logic to model (?), some to form validation
def get_message_from_code(code: str, user):
    if not (code.isdigit() and len(code) == 6):
        return 'Your code should be a six digit number'

    code = int(code)

    matched_count = EventRegistration.objects.filter(user=user,
                                                registration_code=code).count()

    if matched_count == 0:
        return 'Your code does not match any registrations.'
    elif matched_count > 1:
        return 'Uncanny.'

    # code is matched.
    event = EventRegistration.objects.get(user=user,
                                          registration_code=code).event

    if event.get_duration() > 2:
        return 'You cannot cancel your reservation\
                for an event that is longer than two days.'
    if event.get_days_to_start() < 2:
        return 'You cannot cancel your reservation\
                later than two days before the start of an event.'

    event.remove_atendee(user, code)


# TODO: refactor with django.contrib.messages
@login_required
def event_unregister(request):
    if request.method != 'POST': return redirect('start')

    error_message = get_message_from_code(request.POST['code'], request.user)
    if error_message != None:
        messages.error(request, error_message, extra_tags='unregister')
    else:
        messages.success(request,
                         'You have been succesfully unregistered.',
                         extra_tags='unregister')
    return start(request)
