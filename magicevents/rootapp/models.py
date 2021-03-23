from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from random import randint
import datetime


# QUESTION: where to put remove_atendee? it does not use self so...
#           staticmethod? classmethod?

class Event(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    thumbnail = models.ImageField(upload_to="images/")

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.title

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("End date should not be before start date.")

    def add_atendee(self, user, code):
        EventRegistration.objects.create(event=self,
                                         user=user,
                                         registration_code=code)

    @staticmethod
    def remove_atendee_from_code(user, code):
        try:
            registration = EventRegistration.objects.get(user=user,
                                                         registration_code=code)
        except MultipleObjectsReturned:
            raise ValidationError('Uncanny.')
        except ObjectDoesNotExist:
            raise ValidationError('This code does not match any registrations.')

        event = registration.event

        # check if this event starts after two days
        today = datetime.date.today()
        days_difference = (event.start_date - today).days

        if days_difference < 2:
            raise ValidationError('You cannot cancel an event after two days \
                                  before the start date')

        # check if this event's duration does not exceed two days
        event_duration = (event.end_date - event.start_date).days

        if event_duration > 2:
            raise ValidationError('You cannot cancel an event that is longer \
                                  than two days.')

        registration.delete()


class EventRegistration(models.Model):
    event = models.ForeignKey(Event,
                              verbose_name='Event',
                              on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                            verbose_name='Attendee',
                            on_delete=models.CASCADE)

    registration_code = models.PositiveIntegerField(
                                default=randint(111111, 999999))

    class Meta:
        verbose_name = "Event registration"
        verbose_name_plural = "Event registrations"

    def __str__(self):
        return f'User {self.user.username} registered for {self.event.title}'

    @staticmethod
    def already_registered(event, user):
        return bool(EventRegistration.objects.filter(event=event,
                                                     user=user).count())
