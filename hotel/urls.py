
from rest_framework import routers
from django.conf.urls import url, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import HomeView, RoomViewSet, BookingViewSet, BookingList, BookingAdd, BookingEdit, RoomList, RoomAdd,\
    RoomEdit, SearchViewSet, BookingSearch, register


app_name = 'hotel'
router = routers.DefaultRouter()
router.register('rooms', RoomViewSet)
router.register('bookings', BookingViewSet)
router.register('search', SearchViewSet, basename='search')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^register/', register, name="register"),
    url(r'^book/$', BookingAdd.as_view(), name="book"),
    url(r'^bookings/$', BookingList.as_view(), name='bookings'),
    url(r'^bookings/(?P<pk>[0-9]+)/$', BookingEdit.as_view()),
    url(r'^room_add/$', RoomAdd.as_view(), name='room_add'),
    url(r'^rooms/$', RoomList.as_view(), name='rooms'),
    url(r'^rooms/(?P<number>[0-9]+)/$', RoomEdit.as_view()),
    url(r'^search/$', BookingSearch.as_view(), name='search'),
]

