# MOVIES_FOREST
This project has improved version [movies forest](https://github.com/hitesh911/modified_moviesforest)
## Introduction

The goal of this project is to provide  django project template with many added features that everyone can use.

Template is written with django 3.2.1 and python 3 in mind.


### Main features

* Separated dev and production settings

* Example app with custom user model

* Bootstrap static files included

* User registration and logging in as demo

* Procfile for easy deployments

* Separated requirements files

* Push notification implemented already

* Message framwork , Whitenoise and many more are already implemented

# Usage

To use this template to start your own project:

### Existing virtualenv

If your project is already in an existing python3 virtualenv first install django by running

    $ pip install django
    
And then run the `django-admin.py` command to start the new project:

    $ django-admin.py startproject \
      --template=https://github.com/hitesh911/modified-moviesforest \
      --extension=py,md \
      <project_name>
      
### No virtualenv

This assumes that `python3` is linked to valid installation of python 3 and that `pip` is installed and `pip3`is valid
for installing python 3 packages.

Installing inside virtualenv is recommended, however you can start your project without virtualenv too.

If you don't have django installed for python 3 then run:

    $ pip3 install django
    
And then:

    $ python3 -m django startproject \
      --template=https://github.com/hitesh911/movies_forest.git \
      --extension=py,md \
      <project_name>
      
      
After that just install the local dependencies, run migrations, and start the server.


# MoviesForest

# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/hitesh911/movies_forest.git
    $ cd movies_forest
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver

