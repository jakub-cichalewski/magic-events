from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from random import randint
import datetime

class Event(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    thumbnail = models.ImageField()

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

    def remove_atendee(self, user, code):
        registration = EventRegistration.objects.get(user=user,
                                                    event=self,
                                                    registration_code=code)
        registration.delete()


    def get_days_to_start(self):
        today = datetime.date.today()
        diff_days = (self.start_date - today).days
        return diff_days if diff_days >= 0 else -1

    def get_duration(self):
        return (self.end_date - self.start_date).days




class EventRegistration(models.Model):
    event = models.ForeignKey(Event,
                              verbose_name='Event',
                              on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                            verbose_name='Attendee',
                            on_delete=models.CASCADE)

    registration_code = models.PositiveIntegerField(
                                default=randint(111111, 999999))
    def __str__(self):
        return f'User {self.user.username} registered for {self.event.title}'
