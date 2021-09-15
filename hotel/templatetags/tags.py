from django import template
from django.contrib.auth.models import User

register = template.Library()

@property
def is_hotel_client(self):
    return self.groups.filter(name='Client').exists()

@property
def is_hotel_staff(self):  # to not be confused with django .is_staff
    return self.groups.filter(name='Staff').exists()


setattr(User, 'is_hotel_client', is_hotel_client)
setattr(User, 'is_hotel_staff', is_hotel_staff)


