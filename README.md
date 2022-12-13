# P11_amelioration
Répo du projet 11 Openclassrooms parcours développeur d'application python

## Table of content
* [Requirements](#Requirements)
* [Django setup](#Django-setup)
* [Running tests](#tests)

## Requirements 
Please install all these :
- [Python](https://www.python.org/downloads/) > = 3.8
- [Git](https://git-scm.com/downloads)


## Django setup

### 1. Change current directory to be where you want the project to be
    cd <future project folder> 
 
### 2. Clone the github project
    git clone git@github.com:Shriukan33/P11_amelioration.git

### 3. Get into the project's folder
    cd P11-Amelioration

### 4. Create a virtual environnement (recommended)
    python -m venv venv

### 5. Activate your virtual environnement (if you went through step 4)
#### Windows
    venv/Scripts/activate
#### Linux / MacOS
    . venv/bin/activate

### 6. Install project's depedencies
    pip install -r requirements.txt

### 7. Set proper env variable in .env file
```
DJANGO_P8_SECRETKEY="whatever-your-secret-is"
DJANGO_P8_ROLE="dev"
STATIC_URL="/static/"
STATIC_ROOT="static_images"
MEDIA_URL="media/"
```

### 8. Create tables in the database using `manage.py migrate`
* If you have your [virtual environment activated](#4-create-a-virtual-environnement-recommended),
move your working directory to the same directory as `manage.py` and use this command : 
`python manage.py migrate` to create the tables in the database.

* You may also create a superuser using `python manage.py createsuperuser`,
this will allow you to login into the admin panel in http://127.0.0.1:8000/admin

### 9. Start the server
Use the following command 
`python manage.py runserver`

## Tests

While having your venv activated, move to migrate.py directory and use: 

`python manage.py test`
