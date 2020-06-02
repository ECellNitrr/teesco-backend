# teesco-backend

## Branches

The repository has the following primary branches:
* **master** - This contains the code which has been released (production ready code).
* **develop** - This contains the latest code. All the contributing PRs must be sent to this branch.


## Setup and run

1. Create a virtual environment with Python3.7: `virtualenv env -p python3.7`. If you dont have `python3.7` yet then you can install it with:
    1. linux(ubuntu/debian) - `sudo apt install python3.7`
    1. windows - Download installer from https://www.python.org/downloads/release/python-370/.
1. Activate the virutal environment: `source env/bin/activate`
1. Install all the dependencies in `requirements.txt` file: `pip install -r requirements.txt`
1. Make a copy of `.env.sample` to `.env` and change the values of variables with original values. [Click here ](#example-env-file) for sample .env file.
1. [See below for celery setup](#celery-setup).
1. [See below for email setup](#email-setup).
1. Migrate the migrations: `python manage.py migrate`
1. Run the app: `python manage.py runserver`
1. Navigate to http://localhost:8000 in your browser
1. When you are done using the app, deactivate the virtual environment: `deactivate`


## Example env file  

```
SECRET_KEY='iamthegodofsecretkeys'
ALLOWED_HOSTS='*'
DEBUG='True'
EMAIL_HOST_USER='naveen@gmail.com'
EMAIL_HOST_PASSWORD='wnejszjzrvacvkpn'
MOCK_EMAIL ='True'
EMAIL_BACKEND = 'your-backend-config'
AWS_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'
```

note:
1. MOCK_EMAIL defaults to True

## Email Setup

**For gmail:**

1. Set the `EMAIL_BACKEND` to 'django.core.mail.backends.smtp.EmailBackend'
1. If your are using gmail then normal password is not enough to send email through django email package. You have to enable two step verification in https://myaccount.google.com/security.
1. Then generate a new app password for teesco.
1. The app password will look like this.
1. This 16 letter code should be set to `EMAIL_HOST_PASSWORD` in `.env`.
1. We have added below images for help.

<img src='https://user-images.githubusercontent.com/33046846/81901877-d6f5d400-95dc-11ea-85de-d7809d85ccdb.png' width='200px' height='200px' /> <img src='https://user-images.githubusercontent.com/33046846/81902570-f3ded700-95dd-11ea-8a42-0eb44f1e195f.png' height='200px' width='200px'/> <img src='https://user-images.githubusercontent.com/33046846/81902642-183ab380-95de-11ea-9c95-86940d2f0b42.png' height='200px' width='200px'/>

**For Amazon SES**
1. Set the `EMAIL_BACKEND` to 'django_amazon_ses.EmailBackend' in `.env`
2. Also set the `AWS_SECRET_ACCESS_KEY` and `AWS_ACCESS_KEY_ID` in `.env`.

**Other than gmail:**
Other email providers like outlook, hotmail, rediffmail, yahoo mail etc., should work with normal email password. Else they will have a similar approach.


## Celery Setup

**For linux**
1. `sudo apt install redis-server`
1. In a separate terminal run `celery -A server worker -l info` when the celery command is needed.
1. If you see the below image celery is running successfully in your system.
![image](https://user-images.githubusercontent.com/33046846/81906947-add94180-95e4-11ea-9706-714317a15d42.png)


**For windows**
1. Even though redis can be installed in windows but the celery(a python package needed in this project) doesn't work on windows. 
1. Dont you worry we are exploring other alternatives for windows. 
1. Still you can contributions which dont require celery. 
Open two terminals and run  on second terminal



