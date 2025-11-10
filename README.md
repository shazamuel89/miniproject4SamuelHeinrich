### INF601 - Advanced Programming in Python
### Samuel Heinrich
### Mini Project 4
 
 
# Spotify Playlist Maker
 
A simple Django web app that allows users to register, log in, and create personalized playlists. Users can add songs, view other users’ playlists, and manage their own content through a clean Bootstrap-styled interface.
 
## Description
 
This project demonstrates how to build a small but functional web application using Django. It includes user authentication, form handling, database models, an admin interface, and dynamic rendering of templates. The web app focuses on playlist management - each user can create and view playlists with song entries, while administrators can manage all data through Django’s admin panel.

The site uses Bootstrap for layout and styling, including modals for playlist creations.
 
## Getting Started
 
### Dependencies
 
* Python 3.11 or higher
* Django 5.0 or higher
* Bootstrap 5 (loaded via CDN)
* OS: Works on Windows, macOS, or Linux
* Required Pip packages (instructions below)

 
### Installing
 
* Clone the GitHub repository to your local machine:
```
git clone https://github.com/shazamuel89/miniproject4SamuelHeinrich.git
cd miniproject4SamuelHeinrich
```
* Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate         # On Windows
```
* Install required packages:
```
pip install -r requirements.txt
```
* Verify that Django is installed correctly:
```
python -m django --version
```
 
### Executing program
 
* Make database migrations and apply them:
```
python manage.py makemigrations
python manage.py migrate
```
* Create an admin (superuser) account:
```
python manage.py createsuperuser
```
* Run the development server:
```
python manage.py runserver
```
* Open your browser and navigate to on 2 separate tabs:
```
http://127.0.0.1:8000/
```
* On the second tab, replace the text after :8000/ with:
```
admin/
```
* Log in with the admin superuser account credentials you just created
 
## Help
 
Any advise for common problems or issues.
```
command to run if program contains helper info
```
 
## Authors
 
Samuel Heinrich
 
## Version History

* 0.1
    * Initial Release
 
## Acknowledgments
 
Inspiration, code snippets, etc.
* [Django Documentation](https://docs.djangoproject.com/en/5.2/)
* [Bootstrap Documentation](https://getbootstrap.com/docs/5.1/getting-started/introduction/)
* [Django Allauth Github](https://github.com/pennersr/django-allauth/)