from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from .forms import RegistrationForm, EventUnregisterForm
from .models import EventRegistration, Event

from random import randint


def start(request):
    user = request.user
    event_registrations = EventRegistration.objects.filter(user=user) \
        if user.is_authenticated else None

    unregister_form = EventUnregisterForm()

    context = {
        'registrations': event_registrations,
        'form': unregister_form,
        }

    return render(request, 'users/start.html', context)

def start_old(request):
    user = request.user

    event_registrations = EventRegistration.objects.filter(user=user) \
        if user.is_authenticated else None

    return render(request, 'users/start.html',
                    {'registrations': event_registrations})

@login_required
def events(request):
    '''
    Lists all events for user to view.
    '''
    events = Event.objects.all()
    return render(request, 'users/events.html', {'events': events})

@login_required
def event_register(request):
    '''
    Retrieves data from POST request to register user for an event.
    Assigns random unregistration code.
    '''
    if request.method != 'POST': return redirect('start')

    event = Event.objects.get(pk=request.POST['pk'])
    user = request.user

    if not EventRegistration.already_registered(event, user):
        # TODO: move the assignment of the unregistration code to models.py 
        #       ensure uniqueness of the code for the user
        unregister_code = randint(111111, 999999)
        event.add_atendee(user=user, code=unregister_code)
        messages.success(request,
                         f'Your unregistration code for {event.title} \
                         is {unregister_code}',
                         extra_tags='unregister-code')

    return events(request)

@login_required
def event_unregister(request):
    '''
    Lets user unregister by retrieving data from a POST request, calling a
    model method and showing appropriate message.
    '''
    if request.method != 'POST': return redirect('start')

    user = request.user
    unregister_form = EventUnregisterForm(request.POST)

    if unregister_form.is_valid():
        code = unregister_form.cleaned_data['unregister_code']

        try:
            Event.remove_atendee_from_code(user, code)
        except ValidationError as error:
            messages.error(request, error.message, extra_tags='unregister')
        else:
            messages.success(request,
                             'You have been successfully unregistered.',
                             extra_tags='unregister')
    else:
        messages.error(request,
                       'Enter a six digit code.',
                       extra_tags='unregister')

    return start(request)

#########################################################################
def register(request):
    '''
    User registration with a default django form.
    '''
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
