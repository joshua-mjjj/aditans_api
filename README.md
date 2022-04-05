# ADi-tans API

# Environment Setup

    . Create a virtual environment on your local machine where your django dependencies will reside
        .python3 -m venv 'name of your virtual environment here but not in quatos'
        e.g python3 -m venv project1
    . Activate the virtural environment
        .source "virtual environment name here"/bin/activate
        e.g source project1/bin/activate

    . Install django in the virtual environment
        . pip install django

    . Install requirements from requirements.text
        . pip install -r reguirements.txt

    . Make migrations
        . python3 manage.py makemigrations
        . python3 manage.py migrate
