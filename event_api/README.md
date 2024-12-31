# Event Management System

The **Event Management System** is a Django-based web application designed to allow users to view and register for events. The application includes user authentication, event registration, and an administrative backend for managing events. This project is hosted on [PythonAnywhere](https://www.pythonanywhere.com/).

---

## Features

### For Visitors
- View a list of all available events without logging in.
- Click on an event to see detailed information.

### For Registered Users
- Log in to register for events.
- After registration, users can see their profile page with event registration details.

### Authentication System
- User registration form with password confirmation.
- Login/logout functionality.
- Redirect to the last visited event detail page after login or signup.

---

## Project Structure

### Directory Layout

event_management_api/
├── event_api/
│   ├── events/
│   │   ├── migrations/
│   │   ├── templates/
│   │   │   ├── events/
│   │   │   │   ├── base.html
│   │   │   │   ├── event_list.html
│   │   │   │   ├── event_detail.html
│   │   │   │   ├── login.html
│   │   │   │   ├── register.html
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   ├── style.css
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── manage.py
├── README.md


---

### Technologies Used
Backend: Django
Frontend: HTML, CSS (with Django Templates)
Hosting: PythonAnywhere
Database: mySQL


### Installation
1. Clone the repository:
git clone https://github.com/Vanparie/event_management_api.git
cd event_api

2. Create a virtual environment and activate it:
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Apply migrations:
python manage.py makemigrations
python manage.py migrate

5. Create a superuser:
python manage.py createsuperuser

6. Run the development server:
python manage.py runserver



### Usage
- Access the application at http://127.0.0.1:8000/ (local development).
- Navigate to the homepage to view all available events.
- Click on an event to see details and register.
- Log in or sign up to register for an event.
- After logging in, you'll be redirected to the event details page.


### Project Goals and Progress
## Current Goals:

- Allow visitors to view and register for events.
- Build a user-friendly interface with Django Templates.
- Implement authentication for secure event registration.


## Completed Tasks:

- Basic project and app setup.
- Event list and detail views.
- User registration and login system.
- Form validation for registration.
- Integration with Django's auth system.



### Contributions
Feel free to contribute! Submit a pull request or create an issue to report bugs or suggest improvements.

### License
This project is open-source and available under the MIT License.

### Author
Leparie
Aiming to become a backend developer with expertise in Django and Python.