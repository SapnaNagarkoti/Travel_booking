from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from .forms import UserRegister
from .models import TravelOption, Booking


def register(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegister()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'profile.html')


@login_required
def profile_update_view(request):
    user = request.user
    profile = request.user

    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if email:
            user.email = email
            user.save()
        if phone is not None:
            profile.phone = phone
        if address is not None:
            profile.address = address
        profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return render(request, 'profile_update.html', {'user': user})


@login_required
def bookings_list_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'bookings_list.html', {'bookings': bookings})

@login_required
def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status != Booking.CANCELLED:
        booking.status = Booking.CANCELLED
        booking.save()
        messages.success(request, "Booking cancelled successfully.")
    else:
        messages.info(request, "Booking was already cancelled.")
    return redirect('bookings_list')


def travel_options_list(request):
    travel_options = TravelOption.objects.all()

    travel_type = request.GET.get('type')
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    date = request.GET.get('date')

    if travel_type:
        travel_options = travel_options.filter(travel_type=travel_type)
    if source:
        travel_options = travel_options.filter(source__icontains=source)
    if destination:
        travel_options = travel_options.filter(destination__icontains=destination)
    if date:
        travel_options = travel_options.filter(datetime__date=date)

    return render(request, 'travel_options_list.html', {'travel_options': travel_options})

@login_required
def book_travel_option(request, option_id):
    travel_option = get_object_or_404(TravelOption, id=option_id)
    if request.method == 'POST':
        seats = int(request.POST.get('seats', 1))
        if seats <= 0:
            messages.error(request, 'Number of seats must be positive.')
        elif seats > travel_option.available_seats:
            messages.error(request, 'Not enough seats available.')
        else:
            total_price = seats * travel_option.price
            booking = Booking.objects.create(
                user=request.user,
                travel_option=travel_option,
                number_of_seats=seats,
                total_price=total_price,
            )
            travel_option.available_seats -= seats
            travel_option.save()
            messages.success(request, 'Booking confirmed.')
            return redirect('bookings_list')
    return render(request, 'book_travel_option.html', {'travel_option': travel_option})

def is_staff_user(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_staff_user)
def add_travel_option(request):
    if request.method == 'POST':
        form = TravelOptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('travel_options_list')
    else:
        form = TravelOptionForm()
    return render(request, 'add_travel_option.html', {'form': form})