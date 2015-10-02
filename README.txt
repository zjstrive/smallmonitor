========================
django-smallmonitor-project
========================

A project template for Django 1.8.2

To use this project follow these steps:

#. Install Django
#. Create the new project using the django-two-scoops template
#. Install additional dependencies
#. Install static file dependencies
#. Run server
Installing Django
============================

To install Django in the new virtual environment, run the following command::

    $ pip install django

Installation of Dependencies
=============================

Depending on where you are installing dependencies:

    $ pip install -r requirements.txt


#set version
=============================
    smallmonitor.__init__.py 


#. Install static file dependencies
=============================
  bower update

Run server 
==============================
test
python manage.py test --settings=smallmonitor.test_settings

development
python manage.py runserver --settings=smallmonitor.development_settings 0.0.0.0:2332
production   add --insecure  close debug can't find static file
python manage.py runserver --insecure 0.0.0.0:2332
