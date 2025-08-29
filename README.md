Travel Booking Django Project - Simple Setup & Usage Guide
1. Set up your Python environment

Create a virtual environment
python -m venv env
Activate the virtual environment:
env\Scripts\activate

Install required packages
pip install -r requirements.txt


2. Prepare the database
Run Django migrations to create database tables:
python manage.py makemigrations
python manage.py migrate
3. 
3. Create admin user
Run this command
python manage.py createsuperuser
4. Run the development server
python manage.py runserver
Open your browser:
http://127.0.0.1:8000

5. Add Travel Options
Go to admin panel:
http://127.0.0.1:8000/admin/

Login with admin username/password
Add Flights, Trains, or Buses as Travel Options with available seats and other details

6. Use the web app as user
Register a new user or login with existing account
Visit Travel Options page to view available travel options
Click Book Now button beside each option to book seats
Manage your bookings in My Bookings page
Update your details in Profile page
Logout when done

7. Templates location
HTML template files are located at:
travelbooking/Templates/
 files include base.html, login.html, register.html, etc.