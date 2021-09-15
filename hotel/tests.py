from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from .models import Booking, Room
from datetime import datetime
from json import dumps, loads
import base64

# codes cheatsheet
# 200 - OK
# 201 - Created
# 204 - No Content
# 301 - Moved Permamently (make sure to add '/' at the end of url) (api)
# 302 - Found (Redirected)
# 400 - Bad Request
# 401 - Unauthorized
# 403 - Forbidden
# 404 - Not Found
# 415 - Unsupported media type (for PUT method use dumps(data) and add ..., content_type='application/json',) (api)


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%% API TESTS %%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class RoomTest(TestCase):
    def setUp(self):
        self.client = Client()

        group_client, _ = Group.objects.get_or_create(name='Client')
        self.user_client = User.objects.create_user('user_client', 'test1.test@gmail.com', 'password')
        self.c_headers = {'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(b'user_client:password').decode("ascii")}
        group_client.user_set.add(self.user_client)

        group_staff, _ = Group.objects.get_or_create(name='Staff')
        self.user_staff = User.objects.create_user('user_staff', 'test2.test@gmail.com', 'password')
        self.s_headers = {'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(b'user_staff:password').decode("ascii")}
        group_staff.user_set.add(self.user_staff)

        self.room_101 = Room.objects.create(number=101, category=1)

    def test_anon_get_rooms(self):
        Room.objects.create(number=102, category=1)
        Room.objects.create(number=103, category=4)
        response = self.client.get('/api/rooms/')
        self.assertEqual(response.status_code, 200)  # OK
        self.assertEqual(len(loads(response.content)), 3)

    def test_client_not_auth_add_room(self):
        response = self.client.post('/api/rooms/', data={"number": 101, "category": 1})
        self.assertEqual(response.status_code, 401)  # Unauthorized

    def test_client_auth_add_room(self):
        response = self.client.post('/api/rooms/', data={"number": 102, "category": 1}, **self.c_headers)
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_staff_auth_add_room(self):
        response = self.client.post('/api/rooms/', data={"number": 102, "category": 1}, **self.s_headers)
        self.assertEqual(response.status_code, 201)  # Created

    def test_staff_auth_add_room_duplicate(self):
        response = self.client.post('/api/rooms/', data={"number": 101, "category": 1}, **self.s_headers)
        self.assertEqual(response.status_code, 400)  # Created
        self.assertEqual(loads(response.content)['number'][0], "room with this number already exists.")

    def test_staff_auth_update_room(self):
        Room.objects.create(number=102, category=1)
        response = self.client.put(f'/api/rooms/{102}/', data=dumps({"number": 103, "category": 4}),
                                   content_type='application/json', **self.s_headers)
        self.assertEqual(response.status_code, 200)  # OK

    def test_staff_auth_update_room_to_duplicate(self):
        Room.objects.create(number=102, category=1)
        response = self.client.put(f'/api/rooms/{102}/', data=dumps({"number": 101, "category": 1}),
                                   content_type='application/json', **self.s_headers)
        self.assertEqual(response.status_code, 400)  # Bad Request

    def test_staff_auth_delete_room(self):
        Room.objects.create(number=102, category=1)
        response = self.client.delete(f'/api/rooms/{102}/', data=dumps({"number": 102, "category": 1}),
                                      content_type='application/json', **self.s_headers)
        self.assertEqual(response.status_code, 204)  # No Content


# equivalent to Booking.objects.create, just converts dates and therefore reduces number of lines
def create_booking(_id, user, surname, rooms, check_in, check_out):
    return Booking.objects.create(id=_id,  # id required only in tests
                                  user=user,
                                  surname=surname,
                                  rooms=rooms,
                                  check_in=datetime.strptime(check_in, "%Y-%m-%d").date(),
                                  check_out=datetime.strptime(check_out, "%Y-%m-%d").date())


class BookingSimpleTest(TestCase):
    def setUp(self):
        self.client = Client()

        group_client, _ = Group.objects.get_or_create(name='Client')
        self.user_client = User.objects.create_user('user_client', 'test1.test@gmail.com', 'password')
        self.c_headers = {'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(b'user_client:password').decode("ascii")}
        group_client.user_set.add(self.user_client)

        group_staff, _ = Group.objects.get_or_create(name='Staff')
        self.user_staff = User.objects.create_user('user_staff', 'test2.test@gmail.com', 'password')
        self.s_headers = {'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(b'user_staff:password').decode("ascii")}
        group_staff.user_set.add(self.user_staff)

        self.room_101 = Room.objects.create(number=101, category=1)

    def test_anon_get_bookings(self):
        create_booking(1, self.user_staff, 'Staff', [self.room_101], '3021-09-01', '3021-09-03')
        create_booking(2, self.user_staff, 'Staff', [self.room_101], '3021-09-05', '3021-09-06')
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(loads(response.content)), 2)  # loads (dict) or response.data (objects)

    def test_client_not_auth_add_booking(self):
        data = {"user": self.user_client.id, "surname": "user_client", "rooms": [101], "check_in": "3021-09-15",
                "check_out": "3021-09-17"}
        response = self.client.post('/api/bookings/', data=data)
        self.assertEqual(response.status_code, 401)  # Unauthorized

    def test_client_auth_add_booking(self):
        data = {"user": self.user_client.id, "surname": "user_client", "rooms": [101], "check_in": "3021-09-15",
                "check_out": "3021-09-17"}
        response = self.client.post('/api/bookings/', data=data, **self.s_headers)
        self.assertEqual(response.status_code, 201)  # Created

    def test_client_auth_update_own_booking(self):  # i dont want clients to be able to edit bookings, even their own
        create_booking(1, self.user_client, 'user_client', [self.room_101], '3021-09-01', '3021-09-03')
        data = {"user": self.user_client.id, "surname": "user_client", "rooms": [101], "check_in": "3021-09-15",
                "check_out": "3021-09-17"}
        response = self.client.put(f'/api/bookings/{1}/', data=dumps(data), content_type='application/json',
                                   **self.c_headers)
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_client_auth_delete_own_booking(self):  # i dont want clients to be able to delete bookings, even their own
        create_booking(1, self.user_client, 'user_client', [self.room_101], '3021-09-01', '3021-09-03')
        response = self.client.delete(f'/api/bookings/{1}/', **self.c_headers)
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_staff_auth_add_booking(self):
        data = {"user": self.user_staff.id, "surname": "user_staff", "rooms": [101], "check_in": "3021-09-15",
                "check_out": "3021-09-17"}
        response = self.client.post('/api/bookings/', data=data, **self.s_headers)
        self.assertEqual(response.status_code, 201)  # Created

    def test_staff_auth_update_any_booking(self):
        create_booking(1, self.user_client, 'user_client', [self.room_101], '3021-09-01', '3021-09-03')
        data = {"user": self.user_client.id, "surname": "edited", "rooms": [101], "check_in": "3021-09-15",
                "check_out": "3021-09-17"}
        response = self.client.put(f'/api/bookings/{1}/', data=dumps(data), content_type='application/json',
                                   **self.s_headers)
        self.assertEqual(response.status_code, 200)  # OK

    def test_staff_auth_delete_any_booking(self):
        create_booking(1, self.user_client, 'user_client', [self.room_101], '3021-09-01', '3021-09-03')
        response = self.client.delete(f'/api/bookings/{1}/', **self.s_headers)
        self.assertEqual(response.status_code, 204)  # No Content


class BookingAdvancedTest(TestCase):
    def setUp(self):
        self.client = Client()
        group_staff, _ = Group.objects.get_or_create(name='Staff')
        self.user_staff = User.objects.create_user('user_staff', 'test2.test@gmail.com', 'password')
        self.s_headers = {'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(b'user_staff:password').decode("ascii")}
        group_staff.user_set.add(self.user_staff)
        self.room_101 = Room.objects.create(number=101, category=1)
        self.room_102 = Room.objects.create(number=102, category=1)

    def test_bookings_post_single_non_overlapping(self):
        create_booking(1, self.user_staff, 'Staff', [self.room_101], '3021-09-01', '3021-09-03')
        data = {"user": self.user_staff.id, "surname": "Staff", "rooms": [101], "check_in": "3021-09-05",
                "check_out": "3021-09-06"}
        response = self.client.post('/api/bookings/', data=data, **self.s_headers)
        self.assertEqual(response.status_code, 201)  # Created
        self.assertEqual(loads(response.content)['rooms'], [101])

    def test_bookings_post_single_overlapping(self):
        create_booking(1, self.user_staff, 'Staff', [self.room_101], '3021-09-01', '3021-09-03')
        data = {"user": self.user_staff.id, "surname": "Staff", "rooms": [101], "check_in": "3021-09-02",
                "check_out": "3021-09-06"}
        response = self.client.post('/api/bookings/', data=data, **self.s_headers)
        self.assertEqual(response.status_code, 400)  # Bad Request
        self.assertEqual(loads(response.content)['rooms'], "At least one of selected rooms is booked")

    def test_bookings_post_many_non_overlapping(self):
        create_booking(1, self.user_staff, 'Staff', [self.room_101], '3021-09-01', '3021-09-03')
        create_booking(2, self.user_staff, 'Staff', [self.room_102], '3021-09-05', '3021-09-08')
        create_booking(3, self.user_staff, 'Staff', [self.room_102], '3021-09-21', '3021-09-24')
        data = {"user": self.user_staff.id, "surname": "Staff", "rooms": [101, 102], "check_in": "3021-09-12",
                "check_out": "3021-09-15"}
        response = self.client.post('/api/bookings/', data=data, **self.s_headers)
        self.assertEqual(response.status_code, 201)  # Created
        self.assertEqual(loads(response.content)['rooms'], [101, 102])

    def test_bookings_post_many_overlapping(self):
        create_booking(1, self.user_staff, 'Staff', [self.room_101], '3021-09-01', '3021-09-03')
        create_booking(2, self.user_staff, 'Staff', [self.room_102], '3021-09-05', '3021-09-08')
        create_booking(3, self.user_staff, 'Staff', [self.room_102], '3021-09-21', '3021-09-24')
        data = {"user": self.user_staff.id, "surname": "Staff", "rooms": [101, 102], "check_in": "3021-09-18",
                "check_out": "3021-09-21"}
        response = self.client.post('/api/bookings/', data=data, **self.s_headers)
        self.assertEqual(response.status_code, 400)  # Bad Request
        self.assertEqual(loads(response.content)['rooms'], "At least one of selected rooms is booked")

    def test_bookings_post_wrong_timespan(self):
        data = {"user": self.user_staff.id, "surname": "Staff", "rooms": [101], "check_in": "3021-09-15",
                "check_out": "3021-09-13"}
        response = self.client.post('/api/bookings/', data=data, **self.s_headers)
        self.assertEqual(response.status_code, 400)  # Bad Request
        self.assertEqual(loads(response.content)['rooms'], '"Check in" date should precede "Check out"')

    def test_bookings_update_single_extending(self):
        create_booking(1, self.user_staff, 'Staff', [self.room_101], '3021-09-01', '3021-09-05')
        data = {"user": self.user_staff.id, "surname": "Staff", "rooms": [101], "check_in": "3021-09-01",
                "check_out": "3021-09-07"}
        response = self.client.put(f'/api/bookings/{1}/', data=dumps(data), content_type='application/json',
                                   **self.s_headers)
        self.assertEqual(response.status_code, 200)  # OK



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%% FRONTEND TESTS %%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class FrontendBookingSimpleTest(TestCase):
    def setUp(self):
        self.client = Client()

        group_client, _ = Group.objects.get_or_create(name='Client')
        self.user_client = User.objects.create_user('user_client', 'test1.test@gmail.com', 'password')
        self.c_headers = {'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(b'user_client:password').decode("ascii")}
        group_client.user_set.add(self.user_client)

        group_staff, _ = Group.objects.get_or_create(name='Staff')
        self.user_staff = User.objects.create_user('user_staff', 'test2.test@gmail.com', 'password')
        self.s_headers = {'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(b'user_staff:password').decode("ascii")}
        group_staff.user_set.add(self.user_staff)

        self.room_101 = Room.objects.create(number=101, category=1)

    def test_anon_get_bookings(self):
        create_booking(1, self.user_staff, 'Staff', [self.room_101], '3021-09-01', '3021-09-03')
        create_booking(2, self.user_staff, 'Staff', [self.room_101], '3021-09-05', '3021-09-06')
        response = self.client.get('/bookings/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['bookings']), 2)

    def test_client_not_auth_add_booking(self):
        data = {"user": self.user_client.id, "surname": "user_client", "rooms": [101], "check_in": "3021-09-15",
                "check_out": "3021-09-17"}
        response = self.client.post('/book/', data=data)
        self.assertEqual(response.status_code, 401)  # Unauthorized

    def test_client_auth_add_booking(self):
        data = {"user": self.user_client.id, "surname": "user_client", "rooms": [101], "check_in": "3021-09-15",
                "check_out": "3021-09-17"}
        response = self.client.post('/book/', data=data, **self.s_headers)
        self.assertEqual(response.status_code, 302)  # Found (Redirected)
        bookings = Booking.objects.all()
        self.assertEqual(len(bookings), 1)

    def test_client_auth_update_own_booking(self):  # i dont want clients to be able to edit bookings, even their own
        create_booking(1, self.user_client, 'user_client', [self.room_101], '3021-09-01', '3021-09-03')
        data = {"user": self.user_client.id, "surname": "user_client", "rooms": [101], "check_in": "3021-09-15",
                "check_out": "3021-09-17", "method": "PUT"}
        response = self.client.post(f'/bookings/{1}/', data=data, **self.c_headers)
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_client_auth_delete_own_booking(self):  # i dont want clients to be able to delete bookings, even their own
        create_booking(1, self.user_client, 'user_client', [self.room_101], '3021-09-01', '3021-09-03')
        data = {"user": self.user_client.id, "surname": "user_client", "rooms": [101], "check_in": "3021-09-01",
                "check_out": "3021-09-03", "method": "DELETE"}
        response = self.client.post(f'/bookings/{1}/', data=data, **self.c_headers)
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_staff_auth_add_booking(self):
        data = {"user": self.user_staff.id, "surname": "user_staff", "rooms": [101], "check_in": "3021-09-15",
                "check_out": "3021-09-17"}
        response = self.client.post('/book/', data=data, **self.s_headers)
        self.assertEqual(response.status_code, 302)  # Found (Redirected)
        bookings = Booking.objects.all()
        self.assertEqual(len(bookings), 1)

    def test_staff_auth_update_any_booking(self):
        create_booking(1, self.user_client, 'user_client', [self.room_101], '3021-09-01', '3021-09-03')
        data = {"user": self.user_client.id, "surname": "edited", "rooms": [101], "check_in": "3021-09-15",
                "check_out": "3021-09-17", "method": "PUT"}
        response = self.client.post(f'/bookings/{1}/', data=data, **self.s_headers)
        self.assertEqual(response.status_code, 302)  # Found (Redirected)
        bookings = Booking.objects.all()
        self.assertEqual(len(bookings), 1)

    def test_staff_auth_delete_any_booking(self):
        create_booking(1, self.user_client, 'user_client', [self.room_101], '3021-09-01', '3021-09-03')
        data = {"user": self.user_client.id, "surname": "user_client", "rooms": [101], "check_in": "3021-09-01",
                "check_out": "3021-09-03", "method": "DELETE"}
        response = self.client.post(f'/bookings/{1}/', data=data, **self.s_headers)
        self.assertEqual(response.status_code, 302)  # Found (Redirected)
        bookings = Booking.objects.all()
        self.assertEqual(len(bookings), 0)


class BookingAdvancedTest(TestCase):
    def setUp(self):
        self.client = Client()
        group_staff, _ = Group.objects.get_or_create(name='Staff')
        self.user_staff = User.objects.create_user('user_staff', 'test2.test@gmail.com', 'password')
        self.s_headers = {'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(b'user_staff:password').decode("ascii")}
        group_staff.user_set.add(self.user_staff)
        self.room_101 = Room.objects.create(number=101, category=1)
        self.room_102 = Room.objects.create(number=102, category=1)

    def test_bookings_post_single_non_overlapping(self):
        create_booking(1, self.user_staff, 'Staff', [self.room_101], '3021-09-01', '3021-09-03')
        data = {"user": self.user_staff.id, "surname": "Staff", "rooms": [101], "check_in": "3021-09-05",
                "check_out": "3021-09-06"}
        response = self.client.post('/book/', data=data, **self.s_headers)
        self.assertEqual(response.status_code, 302)  # Found (Redirected)
        bookings = Booking.objects.all()
        self.assertEqual(len(bookings), 2)

    def test_bookings_post_single_overlapping(self):
        create_booking(1, self.user_staff, 'Staff', [self.room_101], '3021-09-01', '3021-09-03')
        data = {"user": self.user_staff.id, "surname": "Staff", "rooms": [101], "check_in": "3021-09-02",
                "check_out": "3021-09-06"}
        response = self.client.post('/book/', data=data, **self.s_headers)
        self.assertEqual(response.status_code, 200)  # OK
        bookings = Booking.objects.get(id=1)
        self.assertEqual(datetime.strftime(getattr(bookings, 'check_in'), "%Y-%m-%d"), '3021-09-01')  # not changed

    def test_bookings_post_many_non_overlapping(self):
        create_booking(1, self.user_staff, 'Staff', [self.room_101], '3021-09-01', '3021-09-03')
        create_booking(2, self.user_staff, 'Staff', [self.room_102], '3021-09-05', '3021-09-08')
        create_booking(3, self.user_staff, 'Staff', [self.room_102], '3021-09-21', '3021-09-24')
        data = {"user": self.user_staff.id, "surname": "Staff", "rooms": [101, 102], "check_in": "3021-09-12",
                "check_out": "3021-09-15"}
        response = self.client.post('/book/', data=data, **self.s_headers)
        self.assertEqual(response.status_code, 302)  # Found (Redirected)
        bookings = Booking.objects.all()
        self.assertEqual(len(bookings), 4)

    def test_bookings_post_many_overlapping(self):
        create_booking(1, self.user_staff, 'Staff', [self.room_101], '3021-09-01', '3021-09-03')
        create_booking(2, self.user_staff, 'Staff', [self.room_102], '3021-09-05', '3021-09-08')
        create_booking(3, self.user_staff, 'Staff', [self.room_102], '3021-09-21', '3021-09-24')
        data = {"user": self.user_staff.id, "surname": "Staff", "rooms": [101, 102], "check_in": "3021-09-18",
                "check_out": "3021-09-21"}
        response = self.client.post('/book/', data=data, **self.s_headers)
        bookings = Booking.objects.all()
        self.assertEqual(len(bookings), 3)

    def test_bookings_post_wrong_timespan(self):
        data = {"user": self.user_staff.id, "surname": "Staff", "rooms": [101], "check_in": "3021-09-15",
                "check_out": "3021-09-13"}
        response = self.client.post('/book/', data=data, **self.s_headers)
        self.assertEqual(response.status_code, 200)  # OK
        bookings = Booking.objects.all()
        self.assertEqual(len(bookings), 0)  # booking not created

    def test_bookings_update_single_extending(self):
        create_booking(1, self.user_staff, 'Staff', [self.room_101], '3021-09-01', '3021-09-05')
        data = {"user": self.user_staff.id, "surname": "Staff", "rooms": [101], "check_in": "3021-09-01",
                "check_out": "3021-09-07", "method": "PUT"}
        response = self.client.post(f'/bookings/{1}/', data=data, **self.s_headers)
        self.assertEqual(response.status_code, 302)  # Found (Redirected)
        bookings = Booking.objects.get(id=1)
        self.assertEqual(datetime.strftime(getattr(bookings, 'check_out'), "%Y-%m-%d"), '3021-09-07')  # changed

