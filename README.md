#  Engineer ROI Challenge [![Build Status](https://travis-ci.org/lalvarezguillen/eng-roi-challenge.svg?branch=master)](https://travis-ci.org/lalvarezguillen/eng-roi-challenge) [![codecov](https://codecov.io/gh/lalvarezguillen/eng-roi-challenge/branch/master/graph/badge.svg)](https://codecov.io/gh/lalvarezguillen/eng-roi-challenge)
This is my solution for the code challenge set by  Engineer ROI.

It consists of a Django app that serves a VueJS app.

This is my first rodeo with VueJS.

The Python code styling decisions were deferred to [Black](https://black.readthedocs.io/en/stable/).

### Requirements:

* Python 3.6+


### Running the app:

* Create a virtual environemnt
```sh
virtualenv .env
```

* Install dependencies
```sh
pip install -r requirements.dist.txt
```

* Create and apply migrations
```sh
python manage.py makemigrations tweeter
python manage.py migrate
```

* Run the app
```sh
python manage.py runserver
```

### Hacking on the application

* Create a virtual environemnt
```sh
virtualenv .env
```

* Install development and dist dependencies
```sh
pip install -r requirements.dist.txt -r requirements.dev.txt
```

* Run the tests to make sure everything is working
```sh
python manage.py test
```

* Break things up.