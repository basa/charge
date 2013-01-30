*******************************************************************************
charge web application
*******************************************************************************

getting ready
===============================================================================

Python is a prerequisite should be already installed.
Python 2.7.3 or above (2.7.x) is recommended.
To keep it simple for the database SQLite is used, as it doesn't require
running a separate server.

To bootstrap the project run following commands:

    python bootstrap.py
    ./bin/buildout


run development server
-------------------------------------------------------------------------------

To run development server at http://127.0.0.1:8000/ use following command:

    ./bin/django runserver


project structure
===============================================================================

    |-- bin/    => scripts and binaries
    |   |-- buildout    => software build tool (primarily download/set up)
    |   |-- django      => Django’s command-line utility for administrative tasks
    |-- lib/    => libraries
    |   |-- buildout/eggs/    => bundles of used Python modules
    |-- src/    => developed source code
    |   |-- charge/    => main project
    |       |-- models.py      =>
    |       |-- settings.py    => project settings
    |       |-- urls.py        => URL configuration
    |       |-- views.py       =>
    |       |-- static/        =>
    |       |-- templates/     =>
    |-- patches/        =>
    |-- var/            => data
    |-- bootstrap.py    => copy of the zc.buildout bootstrap script
    |-- buildout.cfg    => buildout configuration
    |-- README          => minimal information about product


update database structure
===============================================================================

    ./bin/django syncdb


Translation
===============================================================================

Update all po files
---------------------
    cd src/charge
    ../../bin/django makemessages -a

Compile po files
----------------
    cd src/charge
    ../../bin/django compilemessages


links
===============================================================================

- Django 1.4 documentation
  https://docs.djangoproject.com/en/1.4/

- Python v2.7.3 documentation
  http://docs.python.org/2.7/

- Google Python Style Guide
  http://google-styleguide.googlecode.com/svn/trunk/pyguide.html