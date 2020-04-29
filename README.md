# teesco-backend

## Setup and run

1. Create a virtual environment with Python3.7: `virtualenv env -p python3.7`
1. Activate the virutal environment: `source /env/bin/activate`
1. Install all the dependencies in `requirements.txt` file: `pip install -r requirements.txt`
1. Migrate the migrations: `python manage.py migrate`
1. Run the app: `python manage.py runserver`
1. Navigate to http://localhost:8000 in your browser
1. When you are done using the app, deactivate the virtual environment: `deactivate`

## Branches

The repository has the following permanent branches:

* **master** - This contains the code which has been released (production ready code).
* **develop** - This contains the latest code. All the contributing PRs must be sent to this branch.