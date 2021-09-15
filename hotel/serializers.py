
from datetime import datetime
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import Room, Booking
from .validations import check_timespan, check_availability

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['number', 'category']

class BookingSerializer(serializers.ModelSerializer):

    get_booking_time = serializers.ReadOnlyField()
    get_booking_price = serializers.ReadOnlyField()  # source='get_booking_price' from Booking, models.py

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    def validate_rooms(self, data):
        check_in = self.initial_data['check_in']
        check_out = self.initial_data['check_out']
        check_timespan(check_in, check_out)
        for room_to_book in data:
            if self.instance is not None:
                # satisfied when the method is PUT (or POST but from frontend views which is treated like PUT)
                check_availability(room_to_book, check_in, check_out, booking_to_exclude=self.instance)
            else:
                check_availability(room_to_book, check_in, check_out)
        return data

    class Meta:
        model = Booking
        fields = ['id', 'user', 'surname', 'rooms', 'check_in', 'check_out', 'created', 'get_booking_time', 'get_booking_price']


class SearchBookingSerializer(serializers.ModelSerializer):
    surname = serializers.CharField(max_length=30, required=False)
    rooms = serializers.ManyRelatedField(required=False,
                                         child_relation=serializers.PrimaryKeyRelatedField(queryset=Room.objects.all()))
    check_in = serializers.DateField(required=False)
    check_out = serializers.DateField(required=False)
    created = serializers.DateTimeField(required=False)  # API and Frontend search accepts Date in format '%Y-%m-%d'

    # because of required = False, always SkipField exception occured and functions like validate_check_in
    # were never called, so everything is in validate() function
    def validate(self, attrs):
        params = self.context['request'].query_params.dict()
        params = {key: value for key, value in params.items() if value != ''}
        if 'rooms' in params:
            for room in params['rooms'].split(','):
                try:
                    int(room)
                except:
                    raise ValidationError('Room can be integer only')
        if 'check_in' in params:
            try:
                datetime.strptime(params['check_in'], '%Y-%m-%d')
            except:
                raise ValidationError('check_in has to be in format %Y-%m-%d')
        if 'check_out' in params:
            try:
                datetime.strptime(params['check_out'], '%Y-%m-%d')
            except:
                raise ValidationError('check_out has to be in format %Y-%m-%d')
        if 'created' in params:
            try:
                datetime.strptime(params['created'], '%Y-%m-%d')
            except:
                raise ValidationError('created has to be in format %Y-%m-%d')
        return attrs

    class Meta:
        model = Booking
        fields = ['surname', 'rooms', 'check_in', 'check_out', 'created']

