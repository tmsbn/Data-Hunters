____________________________________

PLEASE FOLLOW THE INSTRUCTIONS TO RUN THE HOUSE PRICE PREDICTOR DJANGO APPLICATION
____________________________________

Requirements:

1. Python 3.4.3
2. pip 9.0.1 or newer
3. Django 1.11 or newer
4. Numpy 1.12.1 or newer
5. Pandas 0.19.2 or newer
6. Sklearn 0.18.1 or newer

_____________________________________

Instructions to Run:

1. Please install all python packages listed in the requirements section.
2. On the terminal/command-prompt navigate to the the HousePricePredictor folder.
3. Run the command 'python manage.py runserver'.
4. The website will be accessible on 'localhost:8000/predictor' on your browser.
5. For portability, this application is setup to use sql_lite by default, although the
application can be configured to use MYSQL.

_____________________________________

Instructions to Use:

1. Choose "Land Use".
2. Choose "Sold as Vacant".
3. Choose "City".
4. Enter "Square Footage" to a maximum of 1,000,000 sq. ft.
5. Choose "Tax District".
6. Choose "Neighborhood".
7. Enter "Land Value" to a maximum $1,000,000.
8. Click the "Submit" button.
9. The predicted value will be displayed in the white box bellow.

_____________________________________

ADDITIONAL INFORMATION
_____________________________________

How to start a new Django App:

1. Run command 'django-admin startproject <mysite>'.
2. Run command 'python manage.py runserver' on the root manage.py directory.
3. Site will be accesssible on <localhost:8000>.
4. Run command 'python manage.py startapp <myapp>' to create an application within the project.
5. In the <myapp> directory, create the views in 'views.py'.
6. In the <myapp> directory, configure the Urls in 'urls.py' after creating that file.
7. In the <mysite> directory, configure the site to point to <myapp> using 'urls.py' file.
7. Run 'python3 manage.py makemigrations <myapp>' to setup migrations.
8. Run the command 'python manage.py runserver' to start the server.
