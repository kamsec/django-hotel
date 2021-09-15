from rest_framework import serializers, status
from datetime import datetime, date, timedelta
from hotel.models import Booking

# these validations are used by serializers

class CustomException(serializers.ValidationError):
    def __init__(self, detail, status_code=status.HTTP_400_BAD_REQUEST):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code

def check_availability(room, check_in, check_out, booking_to_exclude=None):
    # making sure that check_in and check_out are date objects, not strings
    check_in, check_out = [datetime.strptime(x, "%Y-%m-%d").date() if isinstance(x, str) else x for x in [check_in, check_out]]
    existing_bookings = Booking.objects.filter(rooms=room)
    if booking_to_exclude is not None:
        existing_bookings = existing_bookings.exclude(id=booking_to_exclude.id)

    for existing_booking in existing_bookings:  # every date is in date format here, not str
        if (existing_booking.check_in > check_out) or (existing_booking.check_out < check_in):
            # in this case the new booking is not overlapping that single existing booking checked
            continue
        else:
            # in this case it overlaps existing booking, so cannot be accepted
            raise CustomException('At least one of selected rooms is booked')


def check_timespan(check_in, check_out):
    check_in, check_out = [datetime.strptime(x, "%Y-%m-%d").date() if isinstance(x, str) else x for x in [check_in, check_out]]
    if check_in >= check_out:
        raise CustomException('"Check in" date should precede "Check out"')
    if (check_in < date.today()) or (check_out < (date.today() + timedelta(hours=1))):
        raise CustomException('You can only book rooms in future dates')