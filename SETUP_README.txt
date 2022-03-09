METAR API IN DJANGO:

1) Prerequisite:

    1.1) linux OS (Assignment developed on Ubuntu)

    1.2) Stable internet connection

    1.3) Install python, pip and virtual environment :
        sudo apt-get install python3.8
        sudo apt-get install python3-pip python-dev
        pip install virtualenv

    1.4) Install redis:
        sudo apt install redis-server

2) Setup:

    2.1) Extract metar_api.tar.gz file: (Ignore if you pulled from github)
        tar -xvzf metar_api.tar.gz

    2.2) Create and start python virtual environment:
        python3 -m venv django-venv
        . django-venv/bin/activate

    2.3) Change directory to metar_api:
        cd metar_api

    2.4) Install django, requests and redis:
         pip install django
         pip install requests
         pip install redis

3) Run:

    3.1) Start redis server in new terminal:
        redis-server

    3.2) Start django server:
        python3 manage.py runserver 8080

5) Go to http://localhost:8080/metar/ping/, if it returns {"data": "pong"} then server is running properly.
    Go to http://localhost:8080/metar/info?scode=<4 letter station code> for getting desired METAR json data.
	