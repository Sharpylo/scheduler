# Scheduler
## Scheduler is an application designed to help users organize their lives and increase their efficiency.

## Installation
### To get started with Scheduler, you'll need to perform the following steps:
1. Clone the repository to your local machine:
```
git clone https://github.com/Sharpylo/scheduler.git
```
3. Activate the virtual environment:
```
myvenv\Scripts\activate
```
4. Install the dependencies:
```
pip install -r requirements.txt
```
5. Navigate into the project directory:
```
cd project
```
6. Create a new MySQL database and configure the parameters in the .env file using the env-options file
7. Create the database:
```
python manage.py migrate
```
8. Run the development server:
```
python manage.py runserver
```
9. Open your web browser and navigate to ```http://localhost:8000``` to access the application.

## Testing
### Scheduler includes unit tests for views, models, and forms. To run the tests, use the following command:

```
python manage.py test
```

## Features
### Project Scheduler includes the following features:
- User registration and login
- User profile management, including the ability to update profile information such as name, email, phone number, and profile picture
- Adding, deleting, and updating notes
- Unit tests for views, models, and forms

## Using
### To use the Scheduler, you must create an account or log in to an existing account. Once logged in, you will be able to:
- View a list of notes, which displays your current notes
- Add new notes 
- Update existing notes as needed
- Delete notes that are no longer relevant.
- You can also update your profile information at any time via the profile settings in the top bar




