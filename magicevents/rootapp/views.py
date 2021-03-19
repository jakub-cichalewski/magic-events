from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from rootapp.forms import RegistrationForm
from rootapp.models import EventRegistration, Event

from random import randint

def start(request):
    user = request.user
    if user.is_authenticated:
        user_registrations = EventRegistration.objects.filter(user=user)

        return render(request, 'users/start.html',
                        {'registrations': user_registrations})
    else:
        return render(request, 'users/start.html')

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

def events(request):
    if not request.user.is_authenticated:
        return redirect('start')
    events = Event.objects.all()
    return render(request, 'users/events.html',
                  {'events': events})

def register_for_event(request):
    if request.method == 'POST':
        event = Event.objects.get(pk=request.POST['pk'])
        user = request.user

        already_registered = \
            EventRegistration.objects.filter(
                event=event, user=user).count() != 0

        if not already_registered:
            event.add_atendee(user=user, code=randint(111111, 999999))

    return redirect('start')


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




def unregister_from_event(request):
    if request.method != 'POST': redirect('start')

    message = get_message_from_code(request.POST['code'], request.user)

    return render(request, 'users/event_unregister.html',
                  {'message': message})
