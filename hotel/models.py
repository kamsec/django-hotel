from django.db import models
from django.conf import settings
from django.utils import timezone
from .config import ROOM_CATEGORIES, ROOM_PRICES

class Room(models.Model):
    number = models.IntegerField(unique=True, primary_key=True)
    category = models.PositiveSmallIntegerField(choices=ROOM_CATEGORIES)

    def __str__(self):
        return f'Room {self.number}, class {ROOM_CATEGORIES[self.category - 1][1]}'

    @property
    def get_category(self):
        return ROOM_CATEGORIES[self.category - 1][1]


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    surname = models.CharField(max_length=30)
    rooms = models.ManyToManyField(Room)
    check_in = models.DateField()
    check_out = models.DateField()
    created = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f'{self.user}, {self.surname} has booked {[x for x in self.rooms.all()]}, from {self.check_in} to {self.check_out}'

    @property
    def get_rooms(self):
        return f'{[x for x in self.rooms.values_list("number", flat=True)]}'[1:-1]

    def get_booking_time(self):
        return int((self.check_out - self.check_in).days)

    def get_booking_price(self):
        rooms_categories = [x.get_category for x in self.rooms.all()]
        return sum([self.get_booking_time() * ROOM_PRICES[x] for x in rooms_categories])
