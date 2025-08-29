from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update_view, name='profile_update'),
    path('travel-options/', views.travel_options_list, name='travel_options_list'),
    path('book/<int:option_id>/', views.book_travel_option, name='book_travel_option'),

    path('bookings/', views.bookings_list_view, name='bookings_list'),
    path('bookings/cancel/<int:booking_id>/', views.cancel_booking_view, name='cancel_booking'),
    path('travel-options/add/', views.add_travel_option, name='add_travel_option'),
]